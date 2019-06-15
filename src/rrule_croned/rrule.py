from typing import List, Optional
from enum import IntEnum
from datetime import datetime
from functools import partial

from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY

from rrule_croned.cron import CronExpression


class FrequencyEnum(IntEnum):
    YEARLY = YEARLY
    MONTHLY = MONTHLY
    WEEKLY = WEEKLY
    DAILY = DAILY
    HOURLY = HOURLY
    MINUTELY = MINUTELY
    QUARTERLY = 90
    SEMIANNUALLY = 180


def croned(
    freq: FrequencyEnum, dtstart: Optional[datetime] = None, byweekday: Optional[List[int]] = None
) -> List[CronExpression]:
    minute = dtstart.minute if dtstart else None
    hour = dtstart.hour if dtstart else None
    day = dtstart.day if dtstart else None
    month = dtstart.month if dtstart else None

    cron_expression = partial(CronExpression, minutes=[minute], hours=[hour], weekdays=byweekday)

    if freq == FrequencyEnum.DAILY:
        return cron_expression()

    elif freq == FrequencyEnum.MONTHLY:
        return cron_expression(days=[day])

    elif freq == FrequencyEnum.QUARTERLY:
        recurrence = rrule(MONTHLY, interval=3, dtstart=dtstart, count=4)
        months = [d.month for d in recurrence]

        return cron_expression(days=[day], months=months)

    elif freq == FrequencyEnum.SEMIANNUALLY:
        recurrence = rrule(MONTHLY, interval=6, dtstart=dtstart, count=2)
        months = [d.month for d in recurrence]

        return cron_expression(days=[day], months=months)

    elif freq == FrequencyEnum.YEARLY:
        return cron_expression(days=[day], months=[month])

    raise NotImplementedError({"freq": freq, "dtstart": dtstart, "byweekday": byweekday})
