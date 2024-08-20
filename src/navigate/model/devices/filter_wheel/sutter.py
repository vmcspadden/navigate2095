# Copyright (c) 2021-2022  The University of Texas Southwestern Medical Center.
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
#

#  Standard Library Imports
import logging
import time

# Third Party Imports
import serial

# Local Imports
from navigate.model.devices.filter_wheel.base import FilterWheelBase

# Logger Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


def build_filter_wheel_connection(comport, baudrate, timeout=0.25):
    """Build SutterFilterWheel Serial Port connection

    Attributes
    ----------
    comport : str
        Comport for communicating with the filter wheel, e.g., COM1.
    baudrate : int
        Baud rate for communicating with the filter wheel, e.g., 9600.
    timeout : float
        Timeout for communicating with the filter wheel, e.g., 0.25.

    Returns
    -------
    serial.Serial
        Serial port connection to the filter wheel.

    Raises
    ------
    UserWarning
        Could not communicate with Sutter Lambda 10-B via COMPORT.
    """
    logging.debug(f"SutterFilterWheel - Opening Serial Port {comport}")
    try:
        return serial.Serial(comport, baudrate, timeout=timeout)
    except serial.SerialException:
        logger.warning("SutterFilterWheel - Could not establish Serial Port Connection")
        raise UserWarning(
            "Could not communicate with Sutter Lambda 10-B via COMPORT", comport
        )


class SutterFilterWheel(FilterWheelBase):
    """SutterFilterWheel - Class for controlling Sutter Lambda Filter Wheels

    Note
    ----
        Additional information on the Sutter Lambda 10-B can be found at:
        https://www.sutter.com/manuals/LB10-3_OpMan.pdf
    """

    def __init__(self, device_connection, device_config):
        """Initialize the SutterFilterWheel class.

        Parameters
        ----------
        device_connection : dict
            Dictionary of device connections.
        device_config : dict
            Dictionary of device configuration parameters.
        """
        super().__init__(device_connection, device_config)

        #: obj: Serial port connection to the filter wheel.
        self.serial = device_connection

        #: bool: Wait until filter wheel has completed movement.
        self.wait_until_done = True

        #: float: Delay in s for the wait until done function.
        self.wait_until_done_delay = None

        #: bool: Read on initialization.
        self.read_on_init = True

        #: bool: Software initialization complete flag.
        self.init_finished = False

        #: int: Filter wheel speed.
        self.speed = 2

        logger.debug("SutterFilterWheel - Placing device In Online Mode")
        self.serial.write(bytes.fromhex("ee"))

        if self.read_on_init:
            self.read(2)  # class 'bytes'
            self.init_finished = True
            logger.debug("SutterFilterWheel - Initialized.")

        # Set filter to the 0th position by default upon initialization.
        self.set_filter(list(self.filter_dictionary.keys())[0])

        logger.debug("SutterFilterWheel -  Placed in Default Filter Position.")

    def __enter__(self):
        """Enter the SutterFilterWheel context manager."""
        return self

    def __exit__(self, *args, **kwargs):
        """Exit the SutterFilterWheel context manager."""
        logger.debug("SutterFilterWheel - Closing Device.")
        self.close()

    def __del__(self):
        """Close the SutterFilterWheel serial port.

        Sets the filter wheel to the Empty-Alignment position and then closes the port.
        """
        logger.debug("SutterFilterWheel - Closing the Filter Wheel Serial Port")
        self.set_filter(list(self.filter_dictionary.keys())[0])
        self.serial.close()

    def filter_change_delay(self, filter_name):
        """Calculate duration of time necessary to change filter wheel positions.

        Calculate duration of time necessary to change filter wheel positions.
        Identifies the number of positions that must be switched, and then retrieves
        the duration of time necessary to perform the switch from self.delay_matrix.

        Parameters
        ----------
        filter_name : str
            Name of filter that we want to move to.

        Note
        ----
            Detailed information on timing located on page 38:
            https://www.sutter.com/manuals/LB10-3_OpMan.pdf

        Warn
        ----
            Delay matrix should be model specific.
        """
        old_position = self.wheel_position
        self.wheel_position = self.filter_dictionary[filter_name]
        delta_position = int(abs(old_position - self.wheel_position))
        self.wait_until_done_delay = 0.025 * delta_position

    def set_filter(self, filter_name, wait_until_done=True):
        """Change the filter wheel to the filter designated by the filter
        position argument.

        Parameters
        ----------
        filter_name : str
            Name of filter to move to.
        wait_until_done : bool
            Waits duration of time necessary for filter wheel to change positions.
        """
        if self.check_if_filter_in_filter_dictionary(filter_name) is True:

            # Calculate the Delay Needed to Change the Positions
            self.filter_change_delay(filter_name)

            # Make sure you are moving it to a reasonable filter position at a
            # reasonable speed.
            assert self.wheel_position in range(10)
            assert self.speed in range(8)

            if not self.init_finished:
                self.read(2)
                self.init_finished = True
                logger.debug("SutterFilterWheel - Initialized.")

            output_command = (
                (self.filter_wheel_number - 1) * 128
                + self.wheel_position
                + 16 * self.speed
            )
            output_command = output_command.to_bytes(1, "little")
            self.serial.write(output_command)
            self.read(1)

            #  Wheel Position Change Delay
            if wait_until_done:
                time.sleep(self.wait_until_done_delay)
                # read 0D back.
                self.read(1)

    def read(self, num_bytes):
        """Reads the specified number of bytes from the serial port.

        Parameters
        ----------
        num_bytes : int
            Number of bytes to read from the serial port.

        Returns
        -------
        bytes
            Bytes read from the serial port.

        Raises
        ------
        UserWarning
            The serial port to the Sutter Lambda 10-B is on, but it isn't responding as
            expected.
        """
        for i in range(100):
            num_waiting = self.serial.inWaiting()
            # if there are unread returns from previous commands
            if num_waiting >= num_bytes:
                break
            time.sleep(0.02)
        else:
            logger.error(
                "The serial port to the Sutter Lambda 10-B is on, but it isn't "
                "responding as expected."
            )
            raise UserWarning(
                "The serial port to the Sutter Lambda 10-B is on, but it isn't "
                "responding as expected."
            )
        return self.serial.read(num_bytes)
