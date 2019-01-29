"""test_ulogconv."""
from context import mathpandas as mpd
import pandas as pd
import numpy as np
from numpy.testing import assert_almost_equal


def test_pythagoras():
    """test pythagoras series."""
    x = pd.Series([1, 2, 3, 4])
    y = pd.Series([2, 3, 4, 5])

    r = mpd.series_pythagoras(x, y, "result")

    assert_almost_equal(r.iloc[0], 2.23606797749979)
    assert_almost_equal(r.iloc[1], 3.605551275463989)
    assert_almost_equal(r.iloc[2], 5.0)
    assert_almost_equal(r.iloc[3], 6.4031242374328485)
    assert r.name == "result"
