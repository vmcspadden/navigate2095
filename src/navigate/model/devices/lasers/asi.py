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
import time


# Local Imports
from navigate.model.devices.lasers.base import LaserBase
from navigate.model.devices.APIs.asi.asi_tiger_controller import TigerController
from navigate.tools.decorators import log_initialization

# Logger Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


def build_laser_connection(comport, baudrate=115200, timeout=0.25):
    """Build ASIFilterWheel Serial Port connection

    Parameters
    ----------
    comport : str
        Comport for communicating with the filter wheel, e.g., COM1.
    baudrate : int
        Baud rate for communicating with the filter wheel, default is 115200.
    timeout : float
        Timeout for communicating with the filter wheel, default is 0.25.

    Returns
    -------
    tiger_controller : TigerController
        ASI Tiger Controller object.
    """
    # wait until ASI device is ready
    tiger_controller = TigerController(comport, baudrate)
    tiger_controller.connect_to_serial()
    if not tiger_controller.is_open():
        logger.error("ASI stage connection failed.")
        raise Exception("ASI stage connection failed.")
    return tiger_controller


@log_initialization
class ASILaser(LaserBase):
    """ASILaser - Class for controlling ASI Lasers

    This class is used to control a laser connected to a ASI Tiger Controller with a TGDAC and PLC cards.
    The PLC card will handle the digital outputs and TGDAC card will the analog outputs 
    """

    def __init__(
        self,
        microscope_name: str,
        device_connection: Any,
        configuration: Dict[str, Any],
        laser_id: int,
        modulation_type="analog",
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

        #: TigerController: ASI Tiger Controller object.
        self.laser = device_connection

        #: str: The modulation type of the laser - Analog, Digital, or Mixed.
        self.modulation_type = modulation_type

        '''#: float: The minimum digital modulation voltage.
        self.laser_min_do = None

        #: float: The maximum digital modulation voltage.
        self.laser_max_do = None

        #: float: The minimum analog modulation voltage.
        self.laser_min_ao = None

        #: float: The maximum analog modulation voltage.
        self.laser_max_ao = None

        #: float: Current laser intensity.
        self._current_intensity = 0

        # Initialize the laser modulation type.
        if self.modulation_type == "mixed":
            self.initialize_digital_modulation()
            self.initialize_analog_modulation()
            logger.info(f"{str(self)} initialized with mixed modulation.")

        elif self.modulation_type == "analog":
            self.initialize_analog_modulation()
            logger.info(f"{str(self)} initialized with analog modulation.")

        elif self.modulation_type == "digital":
            self.initialize_digital_modulation()
            logger.info(f"{str(self)} initialized with digital modulation.")
    
    def __str__(self):
        """String representation of the class."""
        return "ASIFilterWheel"'''
    
    '''def initialize_analog_modulation(self) -> None:
        """Initialize the analog modulation of the laser."""

        #: str: axis the laser input is connected to
        self.axis = self.device_config["power"]["hardware"]["axis"]

        "Set the voltage to zero, may put this in the initialization"
        # Set voltage to zero, turns the laser off
        self.laser.move_axis(self.axis, 0)

        #: float: The minimum analog modulation voltage.
        self.laser_min_ao = self.device_config["power"]["hardware"]["min"]

        #: float: The maximum analog modulation voltage.
        self.laser_max_ao = self.device_config["power"]["hardware"]["max"]

        #: object: The laser analog modulation task.
        self.laser.laser_analog(self.axis, self.laser_min_ao, self.laser_max_ao)
        self.laser.sam(self.axis, 1)'''


    '''def initialize_digital_modulation(self) -> None:
        """Initialize the digital modulation of the laser."""
        laser_do_port = self.device_config["onoff"]["hardware"]["channel"]

        #: float: The minimum digital modulation voltage.
        self.laser_min_do = self.device_config["onoff"]["hardware"]["min"]

        #: float: The maximum digital modulation voltage.
        self.laser_max_do = self.device_config["onoff"]["hardware"]["max"]

        #: object: The laser analog or digital modulation task.
        self.laser_do_task = nidaqmx.Task()

        if "/ao" in laser_do_port:
            # Perform the digital modulation with an analog output port.
            self.laser_do_task.ao_channels.add_ao_voltage_chan(
                laser_do_port, min_val=self.laser_min_do, max_val=self.laser_max_do
            )
            self.digital_port_type = "analog"

        else:
            # Digital Modulation via a Digital Port
            self.laser_do_task.do_channels.add_do_chan(
                laser_do_port, line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
            )
            self.digital_port_type = "digital"
        """  

    def set_power(self, laser_intensity: float) -> None:
        """Sets the analog laser power.

        Parameters
        ----------
        laser_intensity : float
            The laser intensity.
        """
        
        laser_voltage = (int(laser_intensity) / 100) * self.laser_max_ao
        self._current_intensity = laser_intensity 

        if self.device_type == "analog":
            # TGDAC
            output_voltage = laser_voltage * 1000
            self.laser.move_axis(self.axis, laser_voltage)
        else:
            # Programmable Logic Card
            if laser_voltage > 2.5:
                output_voltage = 5
            else:
                output_voltage = 0
            self.laser.move_digital_axis(self.axis, output_voltage)



    "Fix these two"
    def turn_on(self) -> None:
        """Turns on the laser."""
        self.set_power(self._current_intensity)
        if self.digital_port_type == "digital":
            self.laser.move_digital_axis(self.axis, self.laser_max_do)
        elif self.digital_port_type == "analog":
            self.laser.move_axis(self.axis, self.laser_max_ao)

    def turn_off(self) -> None:
        """Turns off the laser."""
        tmp = self._current_intensity
        self.set_power(0)
        self._current_intensity = tmp

        if self.digital_port_type == "digital":
            self.laser.move_digital_axis(self.axis, self.laser_min_do)
        elif self.digital_port_type == "analog":
            self.laser.move_axis(self.axis, self.laser_min_ao)

    
    def close(self):
        """Close the ASI Laser serial port.

        Sets the laser to the home position and then closes the port.
        """
        if self.laser.is_open():
            self.laser.move_filter_wheel_to_home()
            self.laser.disconnect_from_serial()


    def __del__(self):
        """Destructor for the ASILaser class."""
        self.close()

'''
