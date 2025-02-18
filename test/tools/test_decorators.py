import unittest
from time import sleep
from src.navigate.tools.decorators import function_timer, FeatureList, AcquisitionMode, log_initialization

class TestFunctionTimer(unittest.TestCase):

    @function_timer
    def sample_function(self, duration):
        sleep(duration)
        return "Completed"

    def test_function_timer(self):
        duration = 1
        result = self.sample_function(duration)
        self.assertEqual(result, "Completed")

    def test_function_timer_zero_duration(self):
        duration = 0
        result = self.sample_function(duration)
        self.assertEqual(result, "Completed")


def sample_feature():
    return "Feature Executed"

class TestFeatureList(unittest.TestCase):

    def setUp(self):
        self.feature_list = FeatureList(sample_feature)

    def test_feature_list_name(self):
        self.assertEqual(self.feature_list.feature_list_name, "Sample Feature")

    def test_feature_list_execution(self):
        result = self.feature_list()
        self.assertEqual(result, "Feature Executed")

class SampleClass:
    def __init__(self, value):
        self.value = value

class TestAcquisitionMode(unittest.TestCase):

    def setUp(self):
        self.acquisition_mode = AcquisitionMode(SampleClass)

    def test_acquisition_mode_initialization(self):
        instance = self.acquisition_mode(10)
        self.assertIsInstance(instance, SampleClass)
        self.assertEqual(instance.value, 10)

    def test_acquisition_mode_flag(self):
        self.acquisition_mode.__is_acquisition_mode = True
        self.assertTrue(self.acquisition_mode.__is_acquisition_mode)

if __name__ == '__main__':
    unittest.main()