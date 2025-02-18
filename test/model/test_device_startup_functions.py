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

# Standard library imports
import unittest
from unittest.mock import MagicMock

# Third party imports

# Local application imports
from navigate.model.device_startup_functions import auto_redial, start_device


class TestAutoRedial(unittest.TestCase):
    """Test the auto_redial function."""

    def test_successful_connection_first_try(self):
        """Test successful connection on the first try."""
        mock_func = MagicMock(return_value="success")
        result = auto_redial(mock_func, ())
        self.assertEqual(result, "success")

    def test_successful_connection_after_failures(self):
        """Test successful connection after a few failures."""
        mock_func = MagicMock(
            side_effect=[
                Exception("fail"),
                Exception("fail"),
                "success",
                Exception("fail"),
                "success",
            ]
        )
        result = auto_redial(mock_func, (), n_tries=5)
        self.assertEqual(result, "success")
        assert mock_func.call_count == 3

    def test_failure_after_all_retries(self):
        """Test failure after all retries."""
        mock_func = MagicMock(side_effect=Exception("fail"))
        with self.assertRaises(Exception):
            auto_redial(mock_func, (), n_tries=3)
        assert mock_func.call_count == 3

    def test_exception_type_handling(self):
        """Test that only the specified exception type is caught."""
        mock_func = MagicMock(side_effect=[ValueError("wrong exception"), "success"])
        with self.assertRaises(ValueError):
            auto_redial(mock_func, (), n_tries=3, exception=TypeError)
        assert mock_func.call_count == 1

    def test_arguments_passing(self):
        """Test that arguments and keyword arguments are correctly passed."""
        mock_func = MagicMock()
        auto_redial(mock_func, (1, 2), n_tries=1, kwarg1="test")
        mock_func.assert_called_with(1, 2, kwarg1="test")

