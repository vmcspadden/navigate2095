import pytest


@pytest.mark.hardware
def test_remote_focus_ni_functions():
    from navigate.model.devices.daq.ni import NIDAQ
    from navigate.model.devices.remote_focus.ni import NIRemoteFocus
    from test.model.dummy import DummyModel

    model = DummyModel()
    daq = NIDAQ(model.configuration)
    microscope_name = model.configuration["experiment"]["MicroscopeState"][
        "microscope_name"
    ]
    rf = NIRemoteFocus(microscope_name, daq, model.configuration)

    funcs = ["adjust"]
    args = [
        [
            {"channel_1": 0.2, "channel_2": 0.1, "channel_3": 0.15},
            {"channel_1": 0.3, "channel_2": 0.2, "channel_3": 0.25},
        ]
    ]

    for f, a in zip(funcs, args):
        if a is not None:
            getattr(rf, f)(*a)
        else:
            getattr(rf, f)()
