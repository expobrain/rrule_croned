import pytest

from dateutil.rrule import MO, TU, WE, TH, FR, SU

from rrule_croned import CronExpression


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        # minute
        [{"minutes": [-1]}, "Minute range is between 0-59, got -1"],
        [{"minutes": [60]}, "Minute range is between 0-59, got 60"],
        # hour
        [{"hours": [-1]}, "Hour range is between 0-23, got -1"],
        [{"hours": [24]}, "Hour range is between 0-23, got 24"],
        # day
        [{"days": [0]}, "Day range is between 1-31, got 0"],
        [{"days": [32]}, "Day range is between 1-31, got 32"],
        # Month
        [{"months": [0]}, "Month range is between 1-12, got 0"],
        [{"months": [13]}, "Month range is between 1-12, got 13"],
        # Weekday
        [{"weekdays": [-1]}, "Weekday range is between 0-6, got -1"],
        [{"weekdays": [7]}, "Weekday range is between 0-6, got 7"],
    ],
)
def test_cron_raise_value_error(kwargs, expected):
    with pytest.raises(ValueError, match=expected):
        CronExpression(**kwargs)


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        # single value
        [{"minutes": [0]}, "0 * * * *"],
        [{"hours": [0]}, "* 0 * * *"],
        [{"days": [1]}, "* * 1 * *"],
        [{"weekdays": [0]}, "* * * * 0"],
        [{"weekdays": [MO]}, "* * * * 0"],
        # multiple values
        [{"minutes": [0, 15, 30]}, "0,15,30 * * * *"],
        [{"hours": [6, 12]}, "* 6,12 * * *"],
        [{"days": [1, 15, 20]}, "* * 1,15,20 * *"],
        [{"months": [1, 12]}, "* * * 1,12 *"],
        [{"weekdays": [0, 2, 6]}, "* * * * 0,2,6"],
        [{"weekdays": [MO, WE, SU]}, "* * * * 0,2,6"],
        # multiple values shuffled
        [{"minutes": [15, 0, 30]}, "0,15,30 * * * *"],
        [{"hours": [12, 6]}, "* 6,12 * * *"],
        [{"days": [15, 1, 20]}, "* * 1,15,20 * *"],
        [{"months": [12, 1]}, "* * * 1,12 *"],
        [{"weekdays": [6, 0, 2]}, "* * * * 0,2,6"],
        [{"weekdays": [SU, MO, WE]}, "* * * * 0,2,6"],
        # duplicate values
        [{"minutes": [15, 15, 30]}, "15,30 * * * *"],
        [{"hours": [12, 6, 6]}, "* 6,12 * * *"],
        [{"days": [15, 1, 1, 20]}, "* * 1,15,20 * *"],
        [{"months": [12, 1, 1]}, "* * * 1,12 *"],
        [{"weekdays": [6, 0, 0, 2]}, "* * * * 0,2,6"],
        [{"weekdays": [SU, MO, MO, WE]}, "* * * * 0,2,6"],
        # ranged values
        [{"minutes": [0, 1, 2, 3, 4]}, "0-4 * * * *"],
        [{"minutes": [0, 2, 3, 4]}, "0,2-4 * * * *"],
        [{"minutes": [0, 1, 2, 4]}, "0-2,4 * * * *"],
        [{"hours": [0, 1, 2, 3, 4]}, "* 0-4 * * *"],
        [{"hours": [0, 2, 3, 4]}, "* 0,2-4 * * *"],
        [{"hours": [0, 1, 2, 4]}, "* 0-2,4 * * *"],
        [{"days": [1, 2, 3, 4, 5]}, "* * 1-5 * *"],
        [{"days": [1, 3, 4, 5]}, "* * 1,3-5 * *"],
        [{"days": [1, 2, 3, 5]}, "* * 1-3,5 * *"],
        [{"months": [1, 2, 3, 4, 5]}, "* * * 1-5 *"],
        [{"months": [1, 3, 4, 5]}, "* * * 1,3-5 *"],
        [{"months": [1, 2, 3, 5]}, "* * * 1-3,5 *"],
        [{"weekdays": [MO, TU, WE, TH, FR]}, "* * * * 0-4"],
        [{"weekdays": [0, 1, 2, 3, 4]}, "* * * * 0-4"],
        [{"weekdays": [0, 2, 3, 4]}, "* * * * 0,2-4"],
        [{"weekdays": [0, 1, 2, 4]}, "* * * * 0-2,4"],
    ],
)
def test_cron_str(kwargs, expected):
    result = CronExpression(**kwargs).as_cron_expression()

    assert result == expected
