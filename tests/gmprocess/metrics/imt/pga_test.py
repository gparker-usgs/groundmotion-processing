#!/usr/bin/env python
# -*- coding: utf-8 -*-

# stdlib imports
import warnings

# third party imports
import numpy as np

# local imports
from gmprocess.io.geonet.core import read_geonet
from gmprocess.metrics.station_summary import StationSummary
from gmprocess.utils.test_utils import read_data_dir


def test_pga():
    datafiles, _ = read_data_dir("geonet", "us1000778i", "20161113_110259_WTMC_20.V2A")
    datafile_v2 = datafiles[0]
    stream_v2 = read_geonet(datafile_v2)[0]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        station_summary = StationSummary.from_stream(
            stream_v2,
            [
                "channels",
                "greater_of_two_horizontals",
                "gmrotd0",
                "gmrotd50",
                "gmrotd100",
                "rotd50",
                "geometric_mean",
                "arithmetic_mean",
            ],
            ["pga", "sa1.0", "saincorrect"],
        )
    pga_df = station_summary.pgms.loc["PGA"]
    AM = pga_df.loc["ARITHMETIC_MEAN"].Result
    GM = pga_df.loc["GEOMETRIC_MEAN"].Result
    HN1 = pga_df.loc["H1"].Result
    HN2 = pga_df.loc["H2"].Result
    HNZ = pga_df.loc["Z"].Result
    gmrotd0 = pga_df.loc["GMROTD(0.0)"].Result
    gmrotd50 = pga_df.loc["GMROTD(50.0)"].Result
    gmrotd100 = pga_df.loc["GMROTD(100.0)"].Result
    rotd50 = pga_df.loc["ROTD(50.0)"].Result
    greater = pga_df.loc["GREATER_OF_TWO_HORIZONTALS"].Result
    np.testing.assert_allclose(AM, 90.242335558014219)
    np.testing.assert_allclose(GM, 89.791654017670112)
    np.testing.assert_allclose(HN2, 81.234672390673683)
    np.testing.assert_allclose(HN1, 99.249998725354743)
    np.testing.assert_almost_equal(HNZ, 183.77223618666929)
    np.testing.assert_allclose(greater, 99.249998725354743)

    np.testing.assert_allclose(gmrotd0, 83.487703753812113)
    np.testing.assert_allclose(gmrotd50, 86.758642638162982)
    np.testing.assert_allclose(gmrotd100, 89.791654017670112)
    np.testing.assert_allclose(rotd50, 91.401785419354567)


if __name__ == "__main__":
    test_pga()
