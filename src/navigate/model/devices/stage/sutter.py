# Copyright (c) 2021-2024  The University of Texas Southwestern Medical Center.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted for academic and research use only (subject to the
# limitations in the disclaimer below) provided that the following conditions are met:

#      * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#      * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.

#      * Neither the name of the copyright holders nor the names of its
#      contributors may be used to endorse or promote products derived from this
#      software without specific prior written permission.

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

# from idlelib.debugger_r import DictProxy
from typing import Any, Dict

# Third-Party Imports
from serial import SerialException

# Local Imports
from navigate.model.devices.stage.base import StageBase
from navigate.model.devices.APIs.sutter.MP285 import MP285
from navigate.model.devices.serial_devices import SerialDevice
from navigate.tools.decorators import log_initialization

# Logger Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


@log_initialization
class MP285Stage(StageBase, SerialDevice):
    """MP285Stage Class for MP-285."""

    def __init__(
        self,
        microscope_name: str,
        axes: list,
        stage_limits: dict,
        axes_mapping=None: list,
        feedback_alignment=None: list,
        device_connection=None: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the MP285Stage.

        Parameters
        ----------
        microscope_name : str
            Name of the microscope.
        device_connection : Any
            MP285 stage connection.
        configuration : Dict[str, Any]
            Configuration dictionary for the MP285Stage.
        device_id : int
            Device ID for the MP285Stage.

        Raises
        ------
        UserWarning
            Error while connecting to the MP285Stage.
        UserWarning
            Error while setting resolution and velocity.
        UserWarning
            Error while setting absolute operation mode.
        """
        super().__init__(microscope_name, device_connection, configuration, device_id)

        # Device Connection
        if device_connection is None:
            logger.error("The MP285 stage is unavailable.")
            raise UserWarning("The MP285 stage is unavailable.")

        #: object: MP285 stage.
        self.stage = device_connection

        #: bool: Wait until stage has finished moving before returning.
        self.stage.wait_until_done = True

        # Default mapping from self.axes to corresponding MP285 axis labelling
        axes_mapping = {"x": "x", "y": "y", "z": "z"}
        if not self.axes_mapping:
            #: dict: Dictionary of stage axes and their corresponding hardware axes.
            self.axes_mapping = {
                axis: axes_mapping[axis] for axis in self.axes if axis in axes_mapping
            }

        #: dict: Dictionary of hardware axes and their corresponding stage axes.
        self.device_axes = dict(map(lambda v: (v[1], v[0]), self.axes_mapping.items()))

        # Default Operating Parameters
        #: str: Resolution of the stage.
        self.resolution = "low"  # "high"

        #: int: Speed of the stage in units microns/s.
        self.speed = 3000

        #: float: Position of the stage along the x-axis.
        self.stage_x_pos = 0

        #: float: Position of the stage along the y-axis.
        self.stage_y_pos = 0

        #: float: Position of the stage along the z-axis.
        self.stage_z_pos = 0

        # Set the resolution and velocity of the stage
        try:
            self.stage.set_resolution_and_velocity(
                resolution=self.resolution, speed=self.speed
            )
        except Exception as e:
            logger.error(f"Communication Error: {e}")
            raise UserWarning("Sutter MP-285 - Error setting resolution and velocity")

        # Set the operating mode of the stage.
        try:
            self.stage.set_absolute_mode()
        except Exception as e:
            logger.error(f"Communication Error: {e}")
            raise UserWarning("Sutter MP-285 - Error setting absolute operation mode")

        self.report_position()

    def __del__(self) -> None:
        """Delete MP285Stage Serial Port.

        Raises
        ------
        UserWarning
            Error while closing the MP285Stage Serial Port.
        """
        self.close()

    @classmethod
    def connect(cls, port: str, baud_rate=115200: int, timeout=0.25: float) -> None:
        """Connect to the MP285Stage."""
        try:
            mp285_stage = MP285(port, baud_rate, timeout)
            mp285_stage.connect_to_serial()
            self.stage = mp285_stage
            return mp285_stage
        except SerialException as e:
            logger.error(f"Communication Error: {e}")
            raise UserWarning(
                "Could not communicate with Sutter MP-285 via COMPORT", com_port
            )
        

    def report_position(self) -> dict:
        """Reports the position for all axes, and creates a position dictionary.

        Positions from the MP-285 are converted to microns.

        Returns
        -------
        position : dict
            Dictionary containing the position of all axes
        """
        position = {}
        try:
            (
                stage_x_pos,
                stage_y_pos,
                stage_z_pos,
            ) = self.stage.get_current_position()
            if stage_x_pos is not None:
                self.stage_x_pos = stage_x_pos
                self.stage_y_pos = stage_y_pos
                self.stage_z_pos = stage_z_pos
                for axis, hardware_axis in self.axes_mapping.items():
                    hardware_position = getattr(self, f"stage_{hardware_axis}_pos")
                    self.__setattr__(f"{axis}_pos", hardware_position)
            else:
                logger.debug(
                    "MP-285 didn't return current position, using previous position!"
                )

            position = self.get_position_dict()
            logger.debug(f"MP-285 - Position: {position}")
        except SerialException as e:
            print("Communication Error: {e}")
            logger.error(f"Communication Error: {e}")
            time.sleep(0.01)

        return position

    def move_axis_absolute(
        self, axis: str, abs_pos: float, wait_until_done=False
    ) -> bool:
        """Implement movement logic along a single axis.

        Parameters
        ----------
        axis : str
            An axis. For example, 'x', 'y', 'z', 'f', 'theta'.
        abs_pos : float
            Absolute position value
        wait_until_done : bool
            Block until stage has moved to its new spot.

        Returns
        -------
        bool
            Was the move successful?
        """
        move_dictionary = {f"{axis}_abs": abs_pos}
        return self.move_absolute(move_dictionary, wait_until_done)

    def move_absolute(self, move_dictionary: dict, wait_until_done=True) -> bool:
        """Move stage along a single axis.

        Parameters
        ----------
        move_dictionary : dict
            A dictionary of values required for movement. Includes 'x_abs', 'x_min',
            etc. for one or more axes. Expects values in micrometers, except for theta,
            which is in degrees.
        wait_until_done : bool
            Wait until the stage has finished moving before returning.

        Returns
        -------
        bool
            Was the move successful?
        """
        pos_dict = self.verify_abs_position(move_dictionary)
        if not pos_dict:
            return False

        # rely on cached positions
        # if len(pos_dict.keys()) < 3:
        #     self.report_position()
        self.stage.wait_until_done = wait_until_done
        move_stage = {}
        for axis in pos_dict:
            if (
                abs(
                    getattr(self, f"stage_{self.axes_mapping[axis]}_pos")
                    - pos_dict[axis]
                )
                < 0.02
            ):
                move_stage[axis] = False
            else:
                move_stage[axis] = True
                setattr(self, f"stage_{self.axes_mapping[axis]}_pos", pos_dict[axis])

        move_stage = any(move_stage.values())
        if move_stage is True:
            try:
                self.stage.move_to_specified_position(
                    x_pos=self.stage_x_pos,
                    y_pos=self.stage_y_pos,
                    z_pos=self.stage_z_pos,
                )
            except SerialException as e:
                logger.debug(f"MP285: move_axis_absolute failed - {e}")
                # make sure the cached positions are the "same" as device
                self.report_position()
                return False

        return True

    def stop(self) -> None:
        """Stop all stage movement abruptly."""
        try:
            self.stage.interrupt_move()
        except SerialException as error:
            logger.exception(f"MP-285 - Stage stop failed: {error}")

    def close(self) -> None:
        """Close the stage."""

        try:
            self.stop()
            self.stage.close()
            logger.debug("MP-285 stage connection closed")
        except (AttributeError, BaseException) as e:
            print("Error while closing the MP-285 stage connection", e)
            logger.debug("Error while disconnecting the MP-285 stage", e)
