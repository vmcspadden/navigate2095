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

# Standard Library Imports
import logging
import tkinter as tk
from tkinter import ttk

# Third Party Imports

# Local Imports
from aslm.view.custom_widgets.popup import PopUp
from aslm.view.custom_widgets.LabelInputWidgetFactory import LabelInput
from aslm.view.custom_widgets.validation import ValidatedSpinbox, ValidatedEntry

# Logging Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


class TilingWizardPopup:
    """Popup for tiling parameters in View.

    Parameters
    ----------
    root : object
        GUI root
    *args : object
        Arguments
    **kwargs : object
        Keyword arguments

    Attributes
    ----------
    popup : object
        Popup window
    inputs : dict
        Dictionary of inputs
    buttons : dict
        Dictionary of buttons

    Methods
    -------
    get_variables()
        Returns the variables
    get_buttons()
        Returns the buttons
    get_widgets()
        Returns the widgets

    """

    def __init__(self, root, *args, **kwargs):
        self.popup = PopUp(
            root,
            "Multiposition Tiling Wizard",
            "625x530+330+330",
            top=False,
            transient=False,
        )

        # Storing the content frame of the popup, this will be the parent of
        # the widgets
        content_frame = self.popup.get_frame()
        content_frame.columnconfigure(0, pad=5)
        content_frame.columnconfigure(1, pad=5)
        content_frame.rowconfigure(0, pad=5)
        content_frame.rowconfigure(1, pad=5)
        content_frame.rowconfigure(2, pad=5)

        # Formatting
        tk.Grid.columnconfigure(content_frame, "all", weight=1)
        tk.Grid.rowconfigure(content_frame, "all", weight=1)

        # Sub Frames
        action_buttons = ttk.Frame(content_frame, padding=(0, 5, 0, 0))
        operation_mode = ttk.Frame(content_frame, padding=(0, 5, 0, 0))
        pos_grid = ttk.Frame(content_frame, padding=(0, 5, 0, 0))
        data = ttk.Frame(content_frame, padding=(0, 5, 0, 0))

        action_buttons.grid(row=0, sticky=tk.NSEW)
        operation_mode.grid(row=1, sticky=tk.NSEW)
        pos_grid.grid(row=2, sticky=tk.NSEW)
        data.grid(row=3, sticky=tk.NSEW)

        # Dictionary for all the variables
        self.inputs = {}
        self.buttons = {}

        names = [
            "set_table",
            "x_start",
            "x_end",
            "y_start",
            "y_end",
            "z_start",
            "z_end",
            "f_start",
            "f_end",
        ]

        entry_names = [
            "x_dist",
            "x_tiles",
            "y_dist",
            "y_tiles",
            "z_dist",
            "z_tiles",
            "f_dist",
            "f_tiles",
        ]

        dist_labels = [
            "X Distance",
            "Num. Tiles",
            "Y Distance",
            "Num. Tiles",
            "Z Distance",
            "Num. Tiles",
            "F Distance",
            "Num. Tiles",
        ]

        # Action buttons
        btn_labels = [
            "Populate Multi-Position Table",
            "Set X Start",
            "Set X End",
            "Set Y Start",
            "Set Y End",
            "Set Z Start",
            "Set Z End",
            "Set F Start",
            "Set F End",
        ]

        self.operating_modes = [
            "Tile in Z",
            "Tile in F",
        ]
        """
        save to disk    populate table
        set x start     x distance
        set x end       x tiles
        set y start     y distance
        set y end       y tiles
        set z start     z distance
        set z end       z tiles
        set f start     f distance
        set f end       f tiles
        """

        for i in range(1):
            self.buttons[names[i]] = ttk.Button(action_buttons, text=btn_labels[i])
            self.buttons[names[i]].grid(
                row=0, column=i, sticky=tk.NSEW, padx=(5, 0), pady=(5, 0)
            )

        self.mode = tk.StringVar()
        for i in range(len(self.operating_modes)):
            self.inputs[self.operating_modes[i]] = LabelInput(
                parent=operation_mode,
                label=self.operating_modes[i],
                input_class=ttk.Radiobutton,
                input_var=self.mode,
                input_args={"value": self.operating_modes[i]},
            )
            self.inputs[self.operating_modes[i]].grid(
                row=0, column=i, sticky=tk.NSEW, pady=3
            )

        # Add style to the buttons to signal to the user if they can be clicked.
        # Mainly important for f_start and f_end
        style = ttk.Style()

        # Configure the style for the Button widget
        style.configure(
            "Custom.TButton",
            foreground="black",
            background="white",
            highlightthickness="20",
        )

        style.map(
            "Custom.TButton",
            foreground=[("disabled", "red"), ("pressed", "black"), ("active", "black")],
        )

        # Position buttons
        for i in range(len(names)):
            if i == 0:
                self.buttons[names[i]] = ttk.Button(
                    action_buttons,
                    text=btn_labels[i],
                )
                self.buttons[names[i]].grid(
                    row=0, column=i, sticky=tk.NSEW, padx=(5, 0), pady=(5, 0)
                )
            if i > 0:
                self.buttons[names[i]] = ttk.Button(
                    pos_grid, text=btn_labels[i], style="Custom.TButton"
                )
                self.buttons[names[i]].grid(
                    row=i - 1, column=0, sticky=tk.NSEW, padx=(5, 0), pady=(5, 0)
                )

                # Validated Spinbox
                self.inputs[names[i]] = LabelInput(
                    parent=pos_grid,
                    input_class=ValidatedSpinbox,
                    input_var=tk.StringVar(),
                )
                self.inputs[names[i]].grid(
                    row=i - 1, column=1, sticky=tk.NSEW, pady=(20, 0), padx=5
                )
                self.inputs[names[i]].widget.state(["disabled"])

        # Dist and Tile entries
        for i in range(len(entry_names)):
            self.inputs[entry_names[i]] = LabelInput(
                parent=pos_grid,
                label=dist_labels[i],
                input_class=ValidatedEntry,
                input_var=tk.StringVar(),
            )
            self.inputs[entry_names[i]].grid(
                row=i, column=2, sticky=tk.NSEW, padx=(5, 0), pady=(17, 0)
            )
            self.inputs[entry_names[i]].widget.state(["disabled"])

        self.inputs["percent_overlay"] = LabelInput(
            parent=data,
            label="Percent Overlay",
            input_class=ValidatedSpinbox,
            input_var=tk.StringVar(),
            input_args={"width": 5, "increment": 5, "from_": 0, "to": 100},
        )
        self.inputs["percent_overlay"].grid(
            row=0, column=0, sticky=tk.NSEW, padx=(5, 0), pady=(5, 0)
        )

        self.inputs["total_tiles"] = LabelInput(
            parent=data,
            label="Total Tiles",
            input_class=ValidatedEntry,
            input_var=tk.StringVar(),
        )
        self.inputs["total_tiles"].widget.state(["disabled"])
        self.inputs["total_tiles"].grid(
            row=0, column=2, sticky=tk.NSEW, padx=5, pady=(5, 0)
        )

        # Formatting
        self.inputs["total_tiles"].grid(padx=(160, 0))

    # Getters
    def get_variables(self):
        """Get the variables tied to the widgets

        This function returns a dictionary of all the variables that are tied to each
        widget name. The key is the widget name, value is the variable associated.

        Parameters
        ----------
        None

        Returns
        -------
        variables : dict
            A dictionary of all the variables that are tied to each widget name.
        """
        variables = {}
        for key, widget in self.inputs.items():
            variables[key] = widget.get_variable()
        return variables

    def get_widgets(self):
        """Get the widgets

        This function returns the dictionary that holds the input widgets.
        The key is the widget name, value is the LabelInput class that has all the data.

        Parameters
        ----------
        None

        Returns
        -------
        self.inputs : dict
            A dictionary of all the widgets that are tied to each widget name.
        """
        return self.inputs

    def get_buttons(self):
        """Get the buttons

        This function returns the dictionary that holds the buttons.
        The key is the button name, value is the button.

        Parameters
        ----------
        None

        Returns
        -------
        self.buttons : dict
            A dictionary of all the buttons that are tied to each button name.
        """
        return self.buttons
