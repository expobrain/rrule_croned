from datetime import datetime

from dateutil.rrule import MO, TU, WE, TH, FR
import pytest

from rrule_croned import croned, CronExpression, FrequencyEnum


@pytest.mark.parametrize(
    "freq, kwargs, expected",
    [
        # daily
        [
            FrequencyEnum.DAILY,
            {"dtstart": datetime(2019, 6, 15)},
            CronExpression(minutes=[0], hours=[0]),
        ],
        [
            FrequencyEnum.DAILY,
            {"dtstart": datetime(2019, 6, 15, 10, 45)},
            CronExpression(minutes=[45], hours=[10]),
        ],
        [
            FrequencyEnum.DAILY,
            {"dtstart": datetime(2019, 6, 15, 10, 45), "byweekday": [MO, TU, WE, TH, FR]},
            CronExpression(minutes=[45], hours=[10], weekdays=[0, 1, 2, 3, 4]),
        ],
        # monthly
        [
            FrequencyEnum.MONTHLY,
            {"dtstart": datetime(2019, 6, 15)},
            CronExpression(minutes=[0], hours=[0], days=[15]),
        ],
        [
            FrequencyEnum.MONTHLY,
            {"dtstart": datetime(2019, 6, 15, 10, 45)},
            CronExpression(minutes=[45], hours=[10], days=[15]),
        ],
        # quarterly
        [
            FrequencyEnum.QUARTERLY,
            {"dtstart": datetime(2019, 1, 1)},
            CronExpression(minutes=[0], hours=[0], days=[1], months=[1, 4, 7, 10]),
        ],
        [
            FrequencyEnum.QUARTERLY,
            {"dtstart": datetime(2019, 1, 1, 10, 45)},
            CronExpression(minutes=[45], hours=[10], days=[1], months=[1, 4, 7, 10]),
        ],
        # semiannually
        [
            FrequencyEnum.SEMIANNUALLY,
            {"dtstart": datetime(2019, 1, 1)},
            CronExpression(minutes=[0], hours=[0], days=[1], months=[1, 7]),
        ],
        [
            FrequencyEnum.SEMIANNUALLY,
            {"dtstart": datetime(2019, 1, 1, 10, 45)},
            CronExpression(minutes=[45], hours=[10], days=[1], months=[1, 7]),
        ],
        # yearly
        [
            FrequencyEnum.YEARLY,
            {"dtstart": datetime(2019, 6, 15)},
            CronExpression(minutes=[0], hours=[0], days=[15], months=[6]),
        ],
        [
            FrequencyEnum.YEARLY,
            {"dtstart": datetime(2019, 6, 15, 10, 45)},
            CronExpression(minutes=[45], hours=[10], days=[15], months=[6]),
        ],
    ],
)
def test_rrule_croned(freq, kwargs, expected):
    result = croned(freq, **kwargs)

    assert result == expected
