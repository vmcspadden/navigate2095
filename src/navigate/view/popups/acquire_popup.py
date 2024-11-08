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


# Standard Library Imports
import logging
from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import platform

from navigate.view.custom_widgets.hover import HoverCheckButton
# Third Party Imports

# Local Imports
from navigate.view.custom_widgets.popup import PopUp
from navigate.view.custom_widgets.LabelInputWidgetFactory import LabelInput
from navigate.view.custom_widgets.validation import ValidatedCombobox, \
    ValidatedSpinbox
from navigate.model.data_sources import FILE_TYPES
from navigate.view.custom_widgets.common import CommonMethods

# Logger Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


SOLVENTS = ("BABB", "Water", "CUBIC", "CLARITY", "uDISCO", "eFLASH")


class AcquirePopUp(CommonMethods):
    """Class creates the popup that is generated when the Acquire button is pressed and
    Save File checkbox is selected."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the AcquirePopUp class

        Parameters
        ----------
        root : tk.Tk
            The root window
        """
        #: tk.Tk: The root window
        self.tk = root

        #: int: Width of the first column
        self.column1_width = 20

        #: int: Width of the second column
        self.column2_width = 40

        #: PopUp: The popup window
        if platform.system() == "Windows":
            self.popup = PopUp(
                root, "File Saving Dialog", "450x500+320+180", transient=True
            )
        else:
            self.popup = PopUp(
                root, "File Saving Dialog", "600x500+320+180", transient=True
            )

        #: dict: Button dictionary.
        self.buttons = {}

        #: dict: Input dictionary.
        self.inputs = {}

        content_frame = self.popup.get_frame()

        path_entries = ttk.Frame(content_frame, padding=(5, 5, 5, 5))
        tab_frame = ttk.Frame(content_frame, padding=(5, 5, 5, 5))
        button_frame = ttk.Frame(content_frame, padding=(5, 5, 5, 5))
        separator1 = ttk.Separator(content_frame, orient="horizontal")
        separator2 = ttk.Separator(content_frame, orient="horizontal")

        path_entries.grid(row=0, column=0, sticky=tk.NSEW, padx=0, pady=3)
        separator1.grid(row=1, column=0, sticky=tk.NSEW, padx=0, pady=3)
        tab_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=0, pady=3)
        separator2.grid(row=3, column=0, sticky=tk.NSEW, padx=0, pady=3)
        button_frame.grid(row=4, column=0, sticky=tk.NSEW, padx=0, pady=3)

        #: ButtonFrame: ButtonFrame object
        self.button_frame = ButtonFrame(parent=self, frame=button_frame)

        #: EntryFrame: EntryFrame object
        self.path_frame = EntryFrame(parent=self, frame=path_entries)

        #: TabFrame: TabFrame object
        self.tab_frame = TabFrame(parent=self, frame=tab_frame)


class ButtonFrame:
    def __init__(self, parent: AcquirePopUp, frame: ttk.Frame) -> None:
        """Initialize the ButtonFrame

        Parameters
        ----------
        parent : AcquirePopUp
            The AcquirePopup window.
        frame : ttk.Frame
            The AcquirePopup Window.
        """

        width = int((parent.column1_width + parent.column2_width - 10) / 2)
        parent.buttons["Cancel"] = ttk.Button(
            frame, text="Cancel Acquisition", width=width
        )
        parent.buttons["Done"] = ttk.Button(frame, text="Acquire Data", width=width)
        parent.buttons["Cancel"].grid(row=0, column=0, padx=5, sticky=tk.NSEW)
        parent.buttons["Done"].grid(row=0, column=1, padx=5, sticky=tk.NSEW)


class EntryFrame:
    def __init__(self, parent: AcquirePopUp, frame: ttk.Frame) -> None:
        """Initialize the EntryFrame

        Parameters
        ----------
        parent : AcquirePopUp
            The AcquirePopup window.
        frame : ttk.Frame
            The EntryFrame Window.
        """
        text = "Please Fill Out the Fields Below"

        #: ttk.Label: Label for the entries
        label = ttk.Label(frame, text=text)
        label.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, pady=5, padx=5)

        # Creating Entry Widgets
        entry_names = [
            "root_directory",
            "user",
            "tissue",
            "celltype",
            "label",
            "prefix",
            "solvent",
            "file_type",
        ]

        entry_labels = [
            "Root Directory",
            "User",
            "Tissue Type",
            "Cell Type",
            "Label",
            "Prefix",
            "Solvent",
            "File Type",
        ]

        # Loop for each entry and label
        for i in range(len(entry_names)):
            if entry_names[i] == "file_type":
                parent.inputs[entry_names[i]] = LabelInput(
                    parent=frame,
                    label=entry_labels[i],
                    input_class=ValidatedCombobox,
                    input_var=tk.StringVar(),
                )
                parent.inputs[entry_names[i]].widget.state(["!disabled", "readonly"])
                parent.inputs[entry_names[i]].set_values(tuple(FILE_TYPES))
                parent.inputs[entry_names[i]].set("TIFF")

            elif entry_names[i] == "solvent":
                parent.inputs[entry_names[i]] = LabelInput(
                    parent=frame,
                    label=entry_labels[i],
                    input_class=ValidatedCombobox,
                    input_var=tk.StringVar(),
                )
                parent.inputs[entry_names[i]].widget.state(["!disabled", "readonly"])
                parent.inputs[entry_names[i]].set_values(SOLVENTS)
                parent.inputs[entry_names[i]].set("BABB")

            else:
                parent.inputs[entry_names[i]] = LabelInput(
                    parent=frame,
                    label=entry_labels[i],
                    input_class=ttk.Entry,
                    input_var=tk.StringVar(),
                    input_args={"width": parent.column2_width},
                )

            # Widgets
            parent.inputs[entry_names[i]].grid(
                row=i + 1, column=0, columnspan=1,
                sticky=tk.NSEW, padx=(0, 0), pady=(1, 1)
            )

            # Labels
            parent.inputs[entry_names[i]].label.grid(padx=(5, 5))
            parent.inputs[entry_names[i]].label.config(width=parent.column1_width)

        # Formatting
        parent.inputs["user"].widget.grid(padx=(0, 0), pady=(1, 1))
        parent.inputs["tissue"].widget.grid(padx=(0, 0), pady=(1, 1))
        parent.inputs["celltype"].widget.grid(padx=(0, 0), pady=(1, 1))
        parent.inputs["prefix"].widget.grid(padx=(0, 0), pady=(1, 1))
        parent.inputs["label"].widget.grid(padx=(0, 0), pady=(1, 1))


class TabFrame:
    def __init__(self, parent: AcquirePopUp, frame: ttk.Frame) -> None:
        """Initialize the TabFrame

        Parameters
        ----------
        parent : AcquirePopUp
            The AcquirePopup window.
        frame : ttk.Frame
            The TabFrame Window.
        """
        notebook = ttk.Notebook(frame, padding=(5, 2, 5, 2))
        notebook.grid(row=0, column=0, sticky=tk.NSEW)

        tab1 = tk.Frame(notebook)
        # tab1.columnconfigure(index=0, weight=1)

        tab2 = tk.Frame(notebook)
        tab2.columnconfigure(index=0, weight=1)
        tab2.columnconfigure(index=1, weight=1)
        tab2.columnconfigure(index=2, weight=1)

        notebook.add(tab1, text="Misc. Notes")
        notebook.add(tab2, text="BDV Settings")

        # Tab 1 Widgets
        self.inputs = {"misc": ScrolledText(
            tab1,
            wrap=tk.WORD,
            height=10,
            width=parent.column2_width + parent.column2_width - 35,
        )
        }

        self.inputs["misc"].grid(row=0, column=0, columnspan=1, sticky=tk.W)

        # Tab 2 Widgets
        total_width = tab2.winfo_width()
        column_width = int(total_width // 3)

        row_index = 0
        text = ("HDF5/N5/Zarr files are saved with BDV metadata, "
                "enabling immediate visualization with BigDataViewer.")
        tk.Label(tab2, text=text, wraplength=400, justify=tk.LEFT).grid(
            row=row_index, column=0, columnspan=2, pady=(5, 5)
        )

        row_index += 1
        self.inputs["shear_data"] = LabelInput(
            parent=tab2,
            label_pos="top",
            label="Shear Data",
            input_class=ttk.Checkbutton,
            input_var=tk.BooleanVar(),
            input_args={"width": column_width - 10,
                        "onvalue": True,
                        "offvalue": False}
        )
        self.inputs["shear_data"].grid(row=row_index,
                                       column=0,
                                       columnspan=1,
                                       sticky=tk.W,
                                       padx=(5, 0),
                                       pady=(1, 1))

        values = ["XZ", "YZ", "XY"]
        self.inputs["shear_dimension"] = LabelInput(
            parent=tab2,
            label_pos="top",
            label="Dimension",
            input_class=ttk.Combobox,
            input_var=tk.StringVar(),
            input_args={"width": column_width - 10,
                        "values": values,
                        "state": "readonly"}
        )

        self.inputs["shear_dimension"].grid(row=row_index,
                                            column=1,
                                            columnspan=1,
                                            sticky=tk.W,
                                            padx=(0, 0),
                                            pady=(1, 1)
                                            )

        self.inputs["shear_angle"] = LabelInput(
            parent=tab2,
            label_pos="top",
            label="Angle (\u00B0)",
            input_class=ValidatedSpinbox,
            input_var=tk.StringVar(),
            input_args={"width": column_width - 10,
                        "from_": 0,
                        "to": 360,
                        "increment": 1,
                        }
        )
        self.inputs["shear_angle"].grid(row=row_index,
                                        column=2,
                                        columnspan=1,
                                        sticky=tk.W,
                                        padx=(0, 0),
                                        pady=(1, 1)
                                        )

        row_index += 1
        separator1 = ttk.Separator(tab2, orient="horizontal")
        separator1.grid(row=row_index, column=0, columnspan=3,
                        sticky=tk.NSEW, padx=0, pady=3)

        row_index += 1
        self.inputs["rotate_data"] = LabelInput(
            parent=tab2,
            label_pos="left",
            label="Rotate Data",
            input_class=ttk.Checkbutton,
            input_var=tk.BooleanVar(),
            input_args={"width": column_width - 10,
                        "onvalue": True,
                        "offvalue": False}
        )

        self.inputs["rotate_data"].grid(
            row=row_index, column=0, columnspan=1, sticky=tk.W,
            padx=(5, 0), pady=(1, 1))

        values = ["X", "Y", "Z"]
        self.inputs["rotate_axis"] = LabelInput(
            parent=tab2,
            label_pos="top",
            label="Dimension",
            input_class=ttk.Combobox,
            input_var=tk.StringVar(),
            input_args={"width": column_width - 10,
                        "values": values,
                        "state": "readonly"}
        )

        self.inputs["rotate_axis"].grid(
            row=row_index,
            column=1,
            columnspan=1,
            sticky=tk.W,
            padx=(0, 0),
            pady=(1, 1)
        )

        self.inputs["rotate_angle"] = LabelInput(
            parent=tab2,
            label_pos="top",
            label="Angle (\u00B0)",
            input_class=ValidatedSpinbox,
            input_var=tk.StringVar(),
            input_args={"width": column_width - 10,
                        "from_": 0,
                        "to": 360,
                        "increment": 1,
                        }
        )
        self.inputs["rotate_angle"].grid(row=row_index,
                                        column=2,
                                        columnspan=1,
                                        sticky=tk.W,
                                        padx=(0, 0),
                                        pady=(1, 1)
                                        )

        row_index += 1
        separator1 = ttk.Separator(tab2, orient="horizontal")
        separator1.grid(row=row_index, column=0, columnspan=3,
                        sticky=tk.NSEW, padx=0, pady=3)

        row_index += 1
        separator2 = ttk.Separator(tab2, orient="horizontal")
        separator2.grid(row=row_index, column=0, columnspan=3,
                        sticky=tk.NSEW, padx=0, pady=3)

        row_index += 1
        self.inputs["down_sample_data"] = LabelInput(
            parent=tab2,
            label_pos="top",
            label="Downsample Data",
            input_class=ttk.Checkbutton,
            input_var=tk.BooleanVar(),
            input_args={"width": column_width - 10,
                        "onvalue": True,
                        "offvalue": False}
        )

        self.inputs["down_sample_data"].grid(
            row=row_index, column=0, columnspan=1, sticky=tk.NSEW,
            padx=(5, 0), pady=(1, 1))

        #   "Down-sampling is accompanied with additional computational "
        #   "overhead and slows data write operations.")
