# Copyright (c) 2021-2024  The University of Texas Southwestern Medical Center.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted for academic and research use only (subject to the
# limitations in the disclaimer below) provided that the following conditions are met:
#
#      * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#
#      * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#      * Neither the name of the copyright holders nor the names of its
#      contributors may be used to endorse or promote products derived from this
#      software without specific prior written permission.
#
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
# THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Standard Imports
import logging
import time
from typing import Any, Dict

# Third Party Imports

# Local Imports
from navigate.model.devices.stage.base import StageBase
from navigate.model.devices.APIs.asi.asi_MS2000_controller import (
    MS2000Controller,
    ASIException,
)
from navigate.model.devices.stage.asi import ASIStage
from navigate.tools.decorators import log_initialization

# Logger Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)

@log_initialization
class MS2000Stage(ASIStage):
    """Applied Scientific Instrumentation (ASI) Stage Class

    ASI Documentation: https://asiimaging.com/docs/products/serial_commands

    ASI Quick Start Guide: https://asiimaging.com/docs/command_quick_start

    Note
    ----
        ASI firmware requires all distances to be in a 10th of a micron.
    """

    def __init__(
        self,
        microscope_name: str,
        device_connection: Any,
        configuration: Dict[str, Any],
        device_id: int = 0,
    ):
        """Initialize the ASI Stage connection.

        Parameters
        ----------
        microscope_name : str
            Name of microscope in configuration
        device_connection : Any
            Hardware device to connect to
        configuration : Dict[str, Any]
            Global configuration of the microscope
        device_id : int
            Device ID for the stage, default to 0
        """
        super().__init__(microscope_name, device_connection, configuration, device_id)

        # Default axes mapping
        axes_mapping = {"x": "X", "y": "Y", "z": "Z"}
        if not self.axes_mapping:
            #: dict: Mapping of software axes to ASI hardware axes
            self.axes_mapping = {
                axis: axes_mapping[axis] for axis in self.axes if axis in axes_mapping
            }
        else:
            # Mapping of axes to ASI axes, force cast axes to uppercase
            self.axes_mapping = {k: v.upper() for k, v in self.axes_mapping.items()}

        #: dict: Dictionary of ASI axes to software axes
        self.asi_axes = dict(map(lambda v: (v[1], v[0]), self.axes_mapping.items()))

        # Set feedback alignment values - Default to 85 if not specified
        if self.stage_feedback is None:
            feedback_alignment = {axis: 85 for axis in self.asi_axes}
        else:
            feedback_alignment = {
                axis: self.stage_feedback
                for axis, self.stage_feedback in zip(self.asi_axes, self.stage_feedback)
            }

        #: object: ASI MS2000 Controller
        self.asi_controller = device_connection
        if device_connection is not None:
            # Set feedback alignment values
            for ax, aa in feedback_alignment.items():
                self.asi_controller.set_feedback_alignment(ax, aa)
            logger.debug("ASI Stage Feedback Alignment Settings:", feedback_alignment)

            # Set finishing accuracy to half of the minimum pixel size we will use
            # pixel size is in microns, finishing accuracy is in mm
            # TODO: check this over all microscopes sharing this stage,
            #       not just the current one
            finishing_accuracy = (
                0.001
                * min(
                    list(
                        configuration["configuration"]["microscopes"][microscope_name][
                            "zoom"
                        ]["pixel_size"].values()
                    )
                )
                / 2
            )
            # If this is changing, the stage must be power cycled for these changes to
            # take effect.
            for ax in self.asi_axes.keys():
                self.asi_controller.set_finishing_accuracy(ax, finishing_accuracy)
                self.asi_controller.set_error(ax, 1.2 * finishing_accuracy)

            # Set backlash to 0 (less accurate)
            for ax in self.asi_axes.keys():
                self.asi_controller.set_backlash(ax, 0.02)

            # Speed optimizations - Set speed to 90% of maximum on each axis
            self.set_speed(percent=0.9)

    @classmethod
    def connect(self, port, baudrate=115200, timeout=0.25):
        """Connect to the ASI Stage

        Parameters
        ----------
        port : str
            Communication port for ASI Tiger Controller - e.g., COM1
        baudrate : int
            Baud rate for ASI Tiger Controller - e.g., 9600
        timeout : float
            Timeout value.

        Returns
        -------
        asi_stage : object
            Successfully initialized stage object.
        """

        # wait until ASI device is ready
        asi_stage = MS2000Controller(port, baudrate)
        asi_stage.connect_to_serial()
        if not asi_stage.is_open():
            logger.error("ASI stage connection failed.")
            raise Exception("ASI stage connection failed.")

        return asi_stage


    def move_axis_relative(self, axis, distance, wait_until_done=False):
        """Move the stage relative to the current position along the specified axis.
        XYZ Values should remain in microns for the ASI API
        Theta Values are not accepted.

        Parameters
        ----------
        axis : str
            The axis along which to move the stage (e.g., 'x', 'y', 'z').
        distance : float
            The distance to move relative to the current position,
            in micrometers for XYZ axes.
        wait_until_done : bool
            Whether to wait until the stage has moved to its new position,
            by default False.

        Returns
        -------
        success : bool
            Indicates whether the move was successful.
        """
        if axis not in self.axes_mapping:
            return False

        abs_pos = self.get_axis_position(axis) + distance

        axis_abs = self.get_abs_position(axis, abs_pos)
        if axis_abs == -1e50:
            print("axis rel false")
            return False

        # Move stage
        try:
            # The 10 is to account for the ASI units, 1/10 of a micron
            self.asi_controller.moverel_axis(axis, distance * 10)

        except ASIException as e:
            print(
                f"ASI stage move axis absolute failed or is trying to move out of "
                f"range: {e}"
            )
            logger.exception("ASI Stage Exception", e)
            return False

        if wait_until_done:
            self.asi_controller.wait_for_device()
        return True

    def scan_axis_triggered_move(
        self, start_position, end_position, axis, ttl_triggered=False
    ):
        """Move the stage along the specified axis from start position to end position,
        with optional TTL triggering.

        Parameters
        ----------
        start_position : float
            The starting position of the stage along the specified axis.
        end_position : float
            The desired end position of the stage along the specified axis.
        axis : str
            The axis along which the stage will be moved (e.g., 'x', 'y', 'z').
        ttl_triggered : bool
            Whether to trigger the move using TTL signal, by default False.

        Returns
        -------
        success : bool
            Indicates whether the move was successful.
        """

        self.move_axis_absolute(axis, start_position, True)

        distance = end_position - start_position
        self.move_axis_relative(axis, distance, True)

        try:
            self.asi_controller.set_backlash(axis, 0.05)
            if ttl_triggered:
                self.asi_controller.set_triggered_move(axis)
        except ASIException as e:
            logger.exception(f"ASIException: {e}")
            return False
        except KeyError as e:
            logger.exception(f"ASI Stage - KeyError in scan_axis_triggered_move: {e}")
            return False

        return True

