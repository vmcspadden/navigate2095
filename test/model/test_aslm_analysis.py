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
import unittest

# Third Party Imports
import numpy as np
import pytest

# Local Imports
# sys.path.append('../../../')


def box(size):
    x = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, x)
    l = (1 - size) / 2  # noqa
    u = l + size
    image = (X > l) & (X < u) & (Y > l) & (Y < u)
    return image.astype(float)


def power_tent(r, off, scale, sigma, alpha):
    return off + scale * (1 - np.abs(sigma * r) ** alpha)


def power_tent_res(x, r, val):
    return power_tent(r, *x) - val


def rsq(res_func, x, r, val):
    ss_err = (res_func(x, r, val) ** 2).sum()
    ss_tot = ((val - val.mean()) ** 2).sum()
    rsq = 1 - (ss_err / ss_tot)
    return rsq


def test_fast_normalized_dct_shannon_entropy_tent():
    from scipy.ndimage import gaussian_filter
    from scipy.optimize import least_squares

    from navigate.model.analysis.image_contrast import (
        fast_normalized_dct_shannon_entropy,
    )

    im = box(0.5)

    r = range(0, 60)
    points = np.zeros((len(r),))
    for i in r:
        points[i] = fast_normalized_dct_shannon_entropy(gaussian_filter(im, i), 1)[0]

    res = least_squares(
        power_tent_res, [np.min(points), np.max(points), 1, 0.5], args=(r, points)
    )

    assert rsq(power_tent_res, res.x, r, points) > 0.9


def test_fast_normalized_dct_shannon_entropy():
    from navigate.model.analysis.image_contrast import (
        fast_normalized_dct_shannon_entropy,
    )

    # image_array = np.ones((np.random.randint(1,4),128,128)).squeeze()
    image_array = np.ones((128, 128)).squeeze()
    psf_support_diameter_xy = np.random.randint(3, 10)

    entropy = fast_normalized_dct_shannon_entropy(image_array, psf_support_diameter_xy)

    assert np.all(entropy == 0)


"""
Delete the below assert once the calculate entropy function is found
"""


def test_entropy():
    assert True


try:
    # from navigate.model.navigate_analysis import Analysis as navigate_analysis
    from navigate.model.navigate_debug_model import calculate_entropy

    class TestNavigateAnalysis(unittest.TestCase):
        """
        Unit Tests for the Navigate Analysis Module
        """

        @pytest.mark.skip(reason="file path not found")
        def test_calculate_entropy_on(self):
            """
            Test the calculation of the Shannon Entropy
            """
            dct_array = np.ones((128, 128))
            otf_support_x = 3
            otf_support_y = 3
            # This trys to call from the navigate_analysis module however its only
            # located in the navigate_debug_model
            # entropy = navigate_analysis.calculate_entropy()
            entropy = calculate_entropy(
                self,
                dct_array=dct_array,
                otf_support_x=otf_support_x,
                otf_support_y=otf_support_y,
            )
            self.assertEqual(entropy, 0)

except ImportError as e:
    print(e)

if __name__ == "__main__":
    unittest.main()
