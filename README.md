# rrule_croned

[![Build Status](https://travis-ci.org/expobrain/rrule_croned.svg?branch=master)](https://travis-ci.org/expobrain/rrule_croned)

This library allows to generate a standard UNIX [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression) from a [RFC-5545 recurrence rule](https://tools.ietf.org/html/rfc5545) using the same Python's `dateutil` [rrule()](https://dateutil.readthedocs.io/en/stable/rrule.html) function signature.

## Usage

```python
from datetime import datetime
from rrule_croned import croned, FrequencyEnum

cron_expression = croned(FrequencyEnum.DAILY, dtstart=datetime(2019, 6, 1))
```

The `cron_expression` is a instance of `CronExpression` which can be further manipulated and returns the UNIX cron expression as string by calling the `as_cron_expression()` method:

```python
print(cron_expression.as_cron_expression())
# 0 0 * * *
```

Weekdays are supported as well:

```python
from rrule_croned import croned, FrequencyEnum, MO, TU, WE, TH, FR

cron_expression = croned(FrequencyEnum.DAILY, byweekday=[MO, TU, WE, TH, FR])
print(cron_expression.as_cron_expression())
# * * * * 0-4
```
