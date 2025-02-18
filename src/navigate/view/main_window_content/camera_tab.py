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
import tkinter as tk
from tkinter import ttk

# Third Party Imports

# Local Imports
import navigate
from navigate.view.custom_widgets.LabelInputWidgetFactory import LabelInput
from navigate.view.custom_widgets.validation import ValidatedSpinbox, ValidatedEntry
from navigate.view.custom_widgets.common import uniform_grid

# Logger Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


class CameraSettingsTab(tk.Frame):
    """
    This class holds and controls the layout of the major label frames for the
    camera  settings tab in the settings notebook. Any imported classes are children
    that makeup the content of the major frames. If you need to adjust anything in
    the frames follow the children.
    """

    def __init__(
            self,
            setntbk: "navigate.view.main_window_content.settings_notebook",
            *args: tuple,
            **kwargs: dict
    ) -> None:
        """Initialize the Camera Settings Tab

        Parameters
        ----------
        setntbk : ttk.Notebook
            The settings notebook that the tab will be placed in.
        *args : tuple
            Positional arguments for ttk.Frame
        **kwargs : dict
            Keyword arguments for ttk.Frame
        """
        # Init Frame
        super().__init__(setntbk, *args, **kwargs)

        #: The index of the tab in the notebook
        self.index = 1

        #: tk.Frame: The camera mode frame
        self.camera_mode = CameraMode(self)
        self.camera_mode.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)

        # Framerate Label Frame
        #: tk.Frame: The framerate label frame
        self.framerate_info = FramerateInfo(self)
        self.framerate_info.grid(row=0, column=1, sticky=tk.NSEW, padx=10, pady=10)

        # Region of Interest Settings
        #: tk.Frame: The region of interest settings frame
        self.camera_roi = ROI(self)
        self.camera_roi.grid(
            row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )

        # Uniform Grid
        uniform_grid(self)


class CameraMode(ttk.Labelframe):
    """This class generates the camera mode label frame.

    Widgets can be adjusted below. Dropdown values need to be set in the controller.
    The function widget.set_values(values) allows this. It can be found in the
    LabelInput class.

    The widgets can be found in the dictionary by using the first word in the label,
    after using get_widgets. The variables tied to each widget can be accessed via
    the widget directly or with the dictionary generated by get_variables.
    """

    def __init__(
            self,
            settings_tab: "CameraSettingsTab",
            *args,
            **kwargs
    ) -> None:
        """Initialize the Camera Mode Frame

        Parameters
        ----------
        settings_tab : CameraSettingsTab
            The settings tab that the frame will be placed in.
        *args : tuple
            Positional arguments for ttk.LabelFrame
        **kwargs : dict
            Keyword arguments for ttk.LabelFrame
        """
        # Init Frame
        text_label = "Camera Mode"
        ttk.Labelframe.__init__(self, settings_tab, text=text_label, *args, **kwargs)

        #: dict: Dictionary of all the widgets in the frame.
        self.inputs = {}

        #: list: List of all the labels for the widgets.
        self.labels = ["Sensor Mode", "Readout Direction", "Number of Pixels"]

        #: list: List of all the names for the widgets.
        self.names = ["Sensor", "Readout", "Pixels"]

        for i in range(len(self.labels)):
            self.rowconfigure(i, weight=1, uniform="1")
        for i in range(2):
            self.columnconfigure(i, weight=1, uniform="1")

        # Dropdown loop
        for i in range(len(self.labels)):
            label = ttk.Label(self, text=self.labels[i])
            label.grid(row=i, column=0, pady=3, padx=5, sticky=tk.W)

            if i < len(self.labels) - 1:
                self.inputs[self.names[i]] = LabelInput(
                    parent=self,
                    input_class=ttk.Combobox,
                    input_var=tk.StringVar(),
                    input_args={"width": 12},
                )
            else:
                self.inputs[self.names[i]] = LabelInput(
                    parent=self,
                    input_class=ValidatedSpinbox,
                    input_var=tk.StringVar(),
                    input_args={"from_": 0, "to": 10000, "increment": 1, "width": 5},
                )
            self.inputs[self.names[i]].grid(
                row=i, column=1, pady=3, padx=5, sticky=tk.W)

    def get_variables(self) -> dict:
        """Get Variables.

        This function returns a dictionary of all the variables that are tied to each
        widget name.

        The key is the widget name, value is the variable associated with the widget.

        Returns
        -------
        variables : dict
            Dictionary of all the variables tied to each widget.
        """
        variables = {}
        for key, widget in self.inputs.items():
            variables[key] = widget.get()
        return variables

    def get_widgets(self) -> dict:
        """Get Widgets.

        This function returns the dictionary that holds the widgets.

        The key is the widget name, value is the LabelInput class that has all the data.

        Parameters
        ----------
        self.inputs : dict
            Dictionary of all the widgets in the frame.
        """
        return self.inputs


class FramerateInfo(ttk.LabelFrame):
    """Framerate Info Frame.

    This class generates the framerate label frame. Widgets can be adjusted below.
    Entry values need to be set in the controller. The widgets can be found in the
    dictionary by using the first word in the label, after using get_widgets

    The variables tied to each widget can be accessed via the widget directly or with
    the dictionary generated by get_variables.
    """

    def __init__(
            self,
            settings_tab: CameraSettingsTab,
            *args: tuple,
            **kwargs: dict
    ) -> None:
        """Initialize the Framerate Info Frame

        Parameters
        ----------
        settings_tab : CameraSettingsTab
            The settings tab that the frame will be placed in.
        *args : tuple
            Positional arguments for ttk.LabelFrame
        **kwargs : dict
            Keyword arguments for ttk.LabelFrame
        """
        # Init Frame
        text_label = "Framerate Info"
        ttk.LabelFrame.__init__(self, settings_tab, text=text_label, *args, **kwargs)

        #: dict: Dictionary of all the widgets in the frame.
        self.inputs = {}

        #: list: List of all the labels for the widgets.
        self.labels = [
            "Exposure Time (ms)",
            "Readout Time (ms)",
            "Framerate (Hz)",
            "Images to Average",
        ]

        #: list: List of all the names for the widget values.
        self.names = [
            "exposure_time",
            "readout_time",
            "max_framerate",
            "frames_to_average",
        ]

        for i in range(len(self.labels)):
            self.rowconfigure(i, weight=1, uniform="1")
        for i in range(2):
            self.columnconfigure(i, weight=1, uniform="1")

        #: list: List of all the read only values for the widgets.
        self.read_only = [True, True, True, False]

        #  Dropdown loop
        for i in range(len(self.labels)):
            label = ttk.Label(self, text=self.labels[i])
            label.grid(row=i, column=0, pady=1, padx=5, sticky=tk.W)

            if self.read_only[i]:
                self.inputs[self.names[i]] = LabelInput(
                    parent=self,
                    input_class=ValidatedEntry,
                    input_var=tk.DoubleVar(),
                    input_args={"width": 6},
                )
                self.inputs[self.names[i]].widget["state"] = "readonly"
            else:
                self.inputs[self.names[i]] = LabelInput(
                    parent=self,
                    input_class=ValidatedSpinbox,
                    input_var=tk.DoubleVar(),
                    input_args={"from_": 1, "to": 1000, "increment": 1.0, "width": 6},
                )
            self.inputs[self.names[i]].grid(row=i, column=1, pady=1, padx=5, sticky=tk.W)


    def get_variables(self) -> dict:
        """Get Variables

        This function returns a dictionary of all variables tied to each widget.

        The key is the widget name, value is the variable associated.

        Returns
        -------
        variables : dict
            Dictionary of all the variables tied to each widget.

        """
        variables = {}
        for key, widget in self.inputs.items():
            variables[key] = widget.get()
        return variables

    def get_widgets(self) -> dict:
        """Get Widgets

        This function returns the dictionary that holds the widgets.
        The key is the widget name, value is the LabelInput class that has all the data.

        Returns
        -------
        self.inputs : dict
            Dictionary of all the widgets in the frame.

        """
        return self.inputs


class ROI(ttk.Labelframe):
    """ROI Frame.

    Widgets can be adjusted below. Dropdown values need to be set in the controller.
    The function widget.set_values(values) allows this. It can be found in the
    LabelInput class. The widgets can be found in the dictionary by using the first
    word in the label, after using get_widgets. The variables tied to each widget can
    be accessed via the widget directly or with the dictionary generated by
    get_variables.
    """

    def __init__(
            self,
            settings_tab: CameraSettingsTab,
            *args: tuple,
            **kwargs: dict) -> None:
        """Initialize the ROI Frame

        Parameters
        ----------
        settings_tab : CameraSettingsTab
            The settings tab that the frame will be placed in.
        *args : tuple
            Positional arguments for ttk.LabelFrame
        **kwargs : dict
            Keyword arguments for ttk.LabelFrame
        """
        # Init Frame
        text_label = "Region of Interest Settings"
        ttk.Labelframe.__init__(self, settings_tab, text=text_label, *args, **kwargs)

        # Formatting
        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # Parent Label Frames for widgets
        #: ttk.LabelFrame: The parent frame for any the camera size.
        self.roi_frame = ttk.LabelFrame(self, text="Number of Pixels")
        self.roi_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)

        # Button Frame
        #: ttk.LabelFrame: The parent frame for default FOV options.
        self.btn_frame = ttk.LabelFrame(self, text="Default FOVs")
        self.btn_frame.grid(row=0, column=1, sticky=tk.NSEW, padx=(40, 10), pady=10)

        # FOV
        #: ttk.LabelFrame: The parent frame for the FOV size.
        self.fov_frame = ttk.LabelFrame(self, text="FOV Dimensions (microns)")
        self.fov_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=10)

        # ROI boundary
        #: ttk.LabelFrame: The parent frame for the boundary of the FOV.
        self.roi_boundary_frame = ttk.LabelFrame(self, text="ROI Boundary")
        self.roi_boundary_frame.grid(
            row=1, column=1, sticky=tk.NSEW, padx=(40, 10), pady=10
        )

        # Formatting
        tk.Grid.columnconfigure(self.roi_frame, "all", weight=1)
        tk.Grid.rowconfigure(self.roi_frame, "all", weight=1)
        tk.Grid.columnconfigure(self.btn_frame, "all", weight=1)
        tk.Grid.rowconfigure(self.btn_frame, "all", weight=1)
        tk.Grid.columnconfigure(self.fov_frame, "all", weight=1)
        tk.Grid.rowconfigure(self.fov_frame, "all", weight=1)
        tk.Grid.columnconfigure(self.roi_boundary_frame, "all", weight=1)
        tk.Grid.rowconfigure(self.roi_boundary_frame, "all", weight=1)

        #: dict: Dictionary of all the widgets in the frame.
        self.inputs = {}

        #: dict: Dictionary of all the buttons in the frame.
        self.buttons = {}

        # Labels and names
        #: list: List of all the labels for the widgets.
        roi_labels = ["Width", "Height"]  # names are the same, can be reused
        xy_labels = ["X", "Y"]
        fov_names = ["FOV_X", "FOV_Y"]

        roi_boundary_names = ["Top_X", "Top_Y", "Bottom_X", "Bottom_Y"]
        roi_boundary_labels = ["X", "Y", "X", "Y"]

        #: str: The binning label.
        self.binning = "Binning"

        # Buttons
        btn_labels = ["Use All Pixels", "1600x1600", "1024x1024", "512x512"]
        btn_names = ["All", "1600", "1024", "512"]

        # Loop for each frame
        # Button Frame
        for i in range(len(btn_names)):
            self.buttons[btn_names[i]] = ttk.Button(
                self.btn_frame, text=btn_labels[i], width=9
            )
            self.buttons[btn_names[i]].grid(row=i, column=0, pady=5, padx=35)

        for i in range(2):
            # Num Pix frame
            self.inputs[roi_labels[i]] = LabelInput(
                parent=self.roi_frame,
                label=roi_labels[i],
                input_class=ValidatedSpinbox,
                input_var=tk.IntVar(),
                input_args={"from_": 0, "increment": 2.0, "width": 5},
            )
            self.inputs[roi_labels[i]].grid(row=i, column=0, pady=5, padx=5)

            # FOV Frame
            self.inputs[fov_names[i]] = LabelInput(
                parent=self.fov_frame,
                label=xy_labels[i],
                input_class=ValidatedSpinbox,
                input_var=tk.IntVar(),
                input_args={"width": 7, "required": True},
            )
            self.inputs[fov_names[i]].grid(row=i, column=0, pady=1, padx=5)

        # ROI boundary
        self.inputs["is_centered"] = LabelInput(
            parent=self.roi_boundary_frame,
            label="Center ROI",
            input_class=ttk.Checkbutton,
            input_var=tk.BooleanVar(),
        )
        self.inputs["is_centered"].grid(
            row=0, columnspan=3, padx=(10, 0), pady=(10, 5), sticky=tk.NW
        )
        top_label = ttk.Label(self.roi_boundary_frame, text="Top-Left:")
        bottom_label = ttk.Label(self.roi_boundary_frame, text="Bottom-Right:")
        top_label.grid(row=1, column=0, padx=10, pady=1, sticky=tk.NW)
        bottom_label.grid(row=2, column=0, padx=10, pady=1, sticky=tk.NW)
        for i in range(len(roi_boundary_names)):
            self.inputs[roi_boundary_names[i]] = LabelInput(
                parent=self.roi_boundary_frame,
                label=roi_boundary_labels[i],
                # input_class=ttk.Spinbox,
                input_class=ValidatedSpinbox,
                input_var=tk.IntVar(),
                input_args={"from_": 0, "to": 2048, "increment": 1.0, "width": 6},
            )
            self.inputs[roi_boundary_names[i]].grid(
                row=i // 2 + 1, column=i % 2 + 1, pady=1, padx=5, sticky=tk.NW
            )
            self.inputs[roi_boundary_names[i]].label.grid(padx=(0, 10), sticky=tk.NW)

        # binning
        self.inputs[self.binning] = LabelInput(
            parent=self.roi_frame,
            label=self.binning,
            input_class=ttk.Combobox,
            input_var=tk.StringVar(),
            input_args={"width": 5},
        )
        self.inputs[self.binning].grid(row=3, column=0, pady=5, padx=5)

        # Number of Pixels
        self.inputs["Width"].grid(pady=(10, 5))
        self.inputs["Width"].label.grid(padx=(0, 13))
        self.inputs["Height"].label.grid(padx=(0, 10))
        self.inputs["Binning"].label.grid(padx=(0, 6))

        # FOV
        self.inputs["FOV_X"].grid(pady=(10, 5))
        self.inputs["FOV_X"].label.grid(padx=(0, 10))
        self.inputs["FOV_Y"].label.grid(padx=(0, 10))

    def get_variables(self) -> dict:
        """Get Variables.

        This function returns a dictionary of all the variables that are tied to each
        widget name.

        The key is the widget name, value is the variable associated.

        Returns
        -------
        variables : dict
            Dictionary of all the variables tied to each widget.
        """
        variables = {}
        for key, widget in self.inputs.items():
            variables[key] = widget.get()
        return variables

    def get_widgets(self) -> dict:
        """Get Widgets.

        This function returns the dictionary that holds the widgets.
        The key is the widget name, value is the LabelInput class that has all the data.

        Returns
        -------
        self.inputs : dict
            Dictionary of all the widgets in the frame.
        """
        return self.inputs

    def get_buttons(self) -> dict:
        """Get Buttons.

        This function returns the dictionary that holds the buttons.
        The key is the widget name, value is the LabelInput class that has all the data.

        Returns
        -------
        self.buttons : dict
            Dictionary of all the buttons in the frame.
        """
        return self.buttons
