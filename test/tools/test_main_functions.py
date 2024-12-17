import unittest
from unittest.mock import patch, MagicMock
from argparse import Namespace
from pathlib import Path
from src.navigate.tools.main_functions import evaluate_parser_input_arguments

class TestEvaluateParserInputArguments(unittest.TestCase):

    @patch('src.navigate.tools.main_functions.get_configuration_paths')
    def test_default_arguments(self, mock_get_configuration_paths):
        # Mock the return value of get_configuration_paths
        mock_get_configuration_paths.return_value = (
            'default_config_path',
            'default_experiment_path',
            'default_waveform_constants_path',
            'default_rest_api_path',
            'default_waveform_templates_path',
            'default_gui_configuration_path',
            'default_multi_positions_path'
        )

        args = Namespace(
            configurator=False,
            config_file=None,
            experiment_file=None,
            waveform_constants_path=None,
            rest_api_file=None,
            waveform_templates_file=None,
            gui_config_file=None,
            multi_positions_file=None,
            logging_config=None
        )

        result = evaluate_parser_input_arguments(args)
        expected = (
            'default_config_path',
            'default_experiment_path',
            'default_waveform_constants_path',
            'default_rest_api_path',
            'default_waveform_templates_path',
            None,
            False,
            'default_gui_configuration_path',
            'default_multi_positions_path'
        )

        self.assertEqual(result, expected)

    @patch('src.navigate.tools.main_functions.get_configuration_paths')
    @patch('pathlib.Path.exists', MagicMock(return_value=True))
    def test_non_default_arguments(self, mock_get_configuration_paths):
        # Mock the return value of get_configuration_paths
        mock_get_configuration_paths.return_value = (
            'default_config_path',
            'default_experiment_path',
            'default_waveform_constants_path',
            'default_rest_api_path',
            'default_waveform_templates_path',
            'default_gui_configuration_path',
            'default_multi_positions_path'
        )

        args = Namespace(
            configurator=True,
            config_file=Path('/path/to/config.yml'),
            experiment_file=Path('/path/to/experiment.yml'),
            waveform_constants_path=Path('/path/to/waveform_constants.yml'),
            waveform_constants_file=Path('/path/to/waveform_constants.yml'),
            rest_api_file=Path('/path/to/rest_api.yml'),
            waveform_templates_file=Path('/path/to/waveform_templates.yml'),
            gui_config_file=Path('/path/to/gui_config.yml'),
            multi_positions_file=Path('/path/to/multi_positions.yml'),
            logging_config=Path('/path/to/logging.yml')
        )

        result = evaluate_parser_input_arguments(args)
        expected = (
            Path('/path/to/config.yml'),
            Path('/path/to/experiment.yml'),
            Path('/path/to/waveform_constants.yml'),
            Path('/path/to/rest_api.yml'),
            Path('/path/to/waveform_templates.yml'),
            Path('/path/to/logging.yml'),
            True,
            Path('/path/to/gui_config.yml'),
            Path('/path/to/multi_positions.yml')
        )

        self.assertEqual(result, expected)

    @patch('src.navigate.tools.main_functions.get_configuration_paths')
    @patch('pathlib.Path.exists', MagicMock(return_value=False))
    def test_invalid_path(self, mock_get_configuration_paths):
        # Mock the return value of get_configuration_paths
        mock_get_configuration_paths.return_value = (
            'default_config_path',
            'default_experiment_path',
            'default_waveform_constants_path',
            'default_rest_api_path',
            'default_waveform_templates_path',
            'default_gui_configuration_path',
            'default_multi_positions_path'
        )

        args = Namespace(
            configurator=True,
            config_file=Path('/invalid/path/to/config.yml'),
            experiment_file=None,
            waveform_constants_file=None,
            rest_api_file=None,
            waveform_templates_file=None,
            gui_config_file=None,
            multi_positions_file=None,
            logging_config=None
        )

        with self.assertRaises(AssertionError):
            evaluate_parser_input_arguments(args)

if __name__ == '__main__':
    unittest.main()