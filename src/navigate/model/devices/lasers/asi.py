# Copyright (c) 2021-2024  The University of Texas Southwestern Medical Center.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted for academic and research use only
# (subject to the limitations in the disclaimer below)
# provided that the following conditions are met:

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

# Standard Library Imports
import logging
from typing import Any, Dict

# Third Party Imports
import nidaqmx
from nidaqmx.errors import DaqError
from nidaqmx.constants import LineGrouping

# Local Imports
from navigate.model.devices.lasers.base import LaserBase
from navigate.tools.decorators import log_initialization

# Logger Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


@log_initialization
class LaserASI(LaserBase):
    """LaserNI Class

    This class is used to control a laser connected to a National Instruments DAQ.
    """

    def __init__(
        self,
        microscope_name: str,
        device_connection: Any,
        configuration: Dict[str, Any],
        laser_id: int,
        modulation_type="digital",
    ) -> None:
        """Initialize the LaserNI class.

        Parameters
        ----------
        microscope_name : str
            The microscope name.
        device_connection : Any
            The device connection object.
        configuration : Dict[str, Any]
            The device configuration.
        laser_id : int
            The laser id.
        modulation_type : str
            The modulation type of the laser - Analog, Digital, or Mixed.
        """
        super().__init__(microscope_name, device_connection, configuration, laser_id)

        #: str: The modulation type of the laser - Analog, Digital, or Mixed.
        self.modulation_type = modulation_type

        #: float: Current laser intensity.
        self._current_intensity = 0

    def set_power(self, laser_intensity: float) -> None:
        """Sets the analog laser power.

        Parameters
        ----------
        laser_intensity : float
            The laser intensity.
        """
        if self.laser_ao_task is None:
            return
        try:
            scaled_laser_voltage = (int(laser_intensity) / 100) * self.laser_max_ao
            self.laser_ao_task.write(scaled_laser_voltage, auto_start=True)
            self._current_intensity = laser_intensity
        except DaqError as e:
            logger.exception(e)

    def print_laser_info(self) -> None:
        print("Laser Information: ")
        print("Microscope Name:", self.microscope_name)
        print("Device Connection:", self.device_connection)
        print("Configuration:", self.configuration)
        print("Modulation Type:", self.modulation_type)
        print("Power Level:", self._current_intensity)

    


