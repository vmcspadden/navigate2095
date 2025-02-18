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
#

# Standard Library Imports
import logging
import traceback
from typing import Any, Dict



# Third Party Imports


# Local Imports
from navigate.model.devices.shutter.base import ShutterBase
from navigate.tools.decorators import log_initialization
from navigate.model.devices.APIs.asi.asi_tiger_controller import TigerController

# Logger Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


@log_initialization
class ASIShutterTTL(ShutterBase):
    """ShutterTTL Class

    Triggering for shutters delivered from the TigerController.
    Each output keeps their last digital state for as long the device is not
    powered down.
    """

    def __init__(
        self,
        microscope_name: str,
        device_connection: Any,
        configuration: Dict[str, Any],
        address=None,
    ) -> None:
        """Initialize the ASIShutterTTL.

        Parameters
        ----------
        microscope_name : str
            Name of microscope in configuration
        device_connection : Any
            Hardware device to connect to
        configuration : Dict[str, Any]
            Global configuration of the microscope
        """

        super().__init__(microscope_name, device_connection, configuration)
        
        shutter_channel = configuration["configuration"]["microscopes"][
            microscope_name
        ]["shutter"]["hardware"]["channel"]

        self.address = address

    def __del__(self):
        if self.sutter_task:
            try:
                self.shutter_task.stop()
                self.shutter_task.close()
            except Exception:
                logger.exception(f"Error stopping task: {traceback.format_exc()}")



    def open_shutter(self):
        self."joel_output" = 1
        try:
            response = self.send_command("joel_output")
            logger.debug("ShutterTTL - Shutter opened")
        except Exception as e:
            print(
                "Shutter not open"
            )
            logger.debug(e)

    def close_shutter(self):
        self."joel_output" = 0
        try:
            response = self.send_command("joel_output")
            logger.debug("ShutterTTL - Shutter closed")
        except Exception as e:
            print(
                "Shutter did not close"
            )
            logger.debug(e)
        

    @property
    def state(self):
        return self."joel_output"
        

