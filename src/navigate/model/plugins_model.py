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

# Standard library imports
import os
from pathlib import Path
from typing import Union

# Third-party imports

# Local application imports
from navigate.tools.file_functions import save_yaml_file
from navigate.tools.decorators import FeatureList, AcquisitionMode
from navigate.config.config import get_navigate_path
from navigate.plugins.plugin_manager import PluginFileManager, PluginPackageManager


class PluginsModel:
    """Plugins manager in the model side"""

    def __init__(self) -> None:
        """Initialize plugins manager class"""
        #: dict: devices dictionary
        self.devices_dict = {}

        #: dict: plugin acquisition modes dictionary
        self.plugin_acquisition_modes = {}

        #: str: feature lists path
        self.feature_lists_path = os.path.join(get_navigate_path(), "feature_lists")

    def load_plugins(self) -> tuple:
        """Load plugins"""
        if not os.path.exists(self.feature_lists_path):
            os.makedirs(self.feature_lists_path)

        plugins_path = os.path.join(Path(__file__).resolve().parent.parent, "plugins")
        plugins_config_path = os.path.join(
            get_navigate_path(), "config", "plugins_config.yml"
        )
        plugin_file_manager = PluginFileManager(plugins_path, plugins_config_path)
        self.load_plugins_through_manager(plugin_file_manager)
        self.load_plugins_through_manager(PluginPackageManager)
        return self.devices_dict, self.plugin_acquisition_modes

    def load_plugins_through_manager(
        self, plugin_manager: Union[PluginFileManager, PluginPackageManager]
    ) -> None:
        """Load plugins through plugin manager

        Parameters
        -------
        plugin_manager : PluginFileManager or PluginPackageManager
            - PluginFileManager
            - PluginPackageManager

        """
        plugins = plugin_manager.get_plugins()

        for _, plugin_ref in plugins.items():
            # read "plugin_config.yml"
            plugin_config = plugin_manager.load_config(plugin_ref)
            if plugin_config is None:
                continue

            # feature
            plugin_manager.load_features(plugin_ref)

            # feature lists
            plugin_manager.load_feature_lists(plugin_ref, self.register_feature_list)

            # acquisition mode
            acquisition_modes = plugin_config.get("acquisition_modes", [])
            plugin_manager.load_acquisition_modes(
                plugin_ref,
                acquisition_modes,
                self.register_acquisition_mode,
            )

            # load devices
            plugin_manager.load_devices(plugin_ref, self.register_device)

    def register_device(self, device, module):
        """Register device

        Parameters
        ----------
        device : str
            device type name
        module : module
            device_startup_functions module
        """
        if module:
            try:
                device_type_name = module.DEVICE_TYPE_NAME
            except AttributeError:
                print(
                    f"Plugin device: {device} is not set correctly!"
                    "Please make sure the DEVICE_TYPE_NAME is given right!"
                )
                return
            # core devices
            core_devices = [
                "camera",
                "remote_focus",
                "galvo",
                "filter_wheel",
                "stage",
                "zoom",
                "shutter",
                "laser",
            ]
            if device_type_name in core_devices:
                if device_type_name not in self.devices_dict:
                    self.devices_dict[device_type_name] = {}
                    self.devices_dict[device_type_name]["load_device"] = []
                    self.devices_dict[device_type_name]["start_device"] = []
                self.devices_dict[device_type_name]["load_device"].append(
                    module.load_device
                )
                self.devices_dict[device_type_name]["start_device"].append(
                    module.start_device
                )
            elif device_type_name == "multiple_devices":
                for device_name in core_devices:
                    if device_name not in self.devices_dict:
                        self.devices_dict[device_name] = {}
                        self.devices_dict[device_name]["load_device"] = []
                        self.devices_dict[device_name]["start_device"] = []
                    self.devices_dict[device_name]["load_device"].append(
                        module.load_device
                    )
                    self.devices_dict[device_name]["start_device"].append(
                        module.start_device
                    )
            else:
                self.devices_dict[device_type_name] = {}
                self.devices_dict[device_type_name]["ref_list"] = module.DEVICE_REF_LIST
                self.devices_dict[device_type_name]["load_device"] = module.load_device
                self.devices_dict[device_type_name][
                    "start_device"
                ] = module.start_device

    def register_acquisition_mode(self, acquisition_mode_name, module):
        """Register acquisition mode

        Parameters
        ----------
        acquisition_mode_name : str
            The name of an acquisition mode
        module : module
            acquisition_mode module
        """
        if not module:
            return
        acquisition_mode = [
            m for m in dir(module) if isinstance(getattr(module, m), AcquisitionMode)
        ]
        if acquisition_mode:
            self.plugin_acquisition_modes[acquisition_mode_name] = getattr(
                module, acquisition_mode[0]
            )(acquisition_mode_name)

    def register_feature_list(self, plugin_feature_list, module):
        """Register feature list

        Parameters
        ----------
        plugin_feature_list : str
            plugin_feature_list path string
        module : module
            feature list module
        """
        features = [
            f for f in dir(module) if isinstance(getattr(module, f), FeatureList)
        ]
        for feature_name in features:
            feature = getattr(module, feature_name)
            feature_list_name = feature.feature_list_name
            feature_list_file_name = "_".join(feature_list_name.split())
            feature_list_content = {
                "module_name": feature_name,
                "feature_list_name": feature_list_name,
                "filename": plugin_feature_list,
            }
            save_yaml_file(
                self.feature_lists_path,
                feature_list_content,
                f"{feature_list_file_name}.yml",
            )
