from typing import Optional, List

from dateutil import rrule
import dataclasses


@dataclasses.dataclass(frozen=True)
class CronExpression:
    minutes: Optional[List[int]] = None
    hours: Optional[List[int]] = None
    days: Optional[List[int]] = None
    months: Optional[List[int]] = None
    weekdays: Optional[List[int]] = None

    def __post_init__(self):
        for minute in self.minutes or []:
            if not (0 <= minute <= 59):
                raise ValueError(f"Minute range is between 0-59, got {minute})")

        for hour in self.hours or []:
            if not (0 <= hour <= 23):
                raise ValueError(f"Hour range is between 0-23, got {hour})")

        for day in self.days or []:
            if not (1 <= day <= 31):
                raise ValueError(f"Day range is between 1-31, got {day})")

        for month in self.months or []:
            if not (1 <= month <= 12):
                raise ValueError(f"Month range is between 1-12, got {month})")

        for i, weekday in enumerate(self.weekdays or []):
            if isinstance(weekday, rrule.weekday):
                self.weekdays[i] = weekday.weekday
            elif isinstance(weekday, int) and not (0 <= weekday <= 6):
                raise ValueError(f"Weekday range is between 0-6, got {weekday})")

    def __format_values(self, values: Optional[List[int]]) -> str:
        if not values:
            return "*"

        values = sorted(set(values))
        values_length = len(values)
        output_value = None
        output = []
        in_range = False

        for i, value in enumerate(values):
            is_before_last = i + 2 == values_length
            two_more_items = i + 2 < values_length

            is_value_plus_1 = (two_more_items or is_before_last) and values[i + 1] == value + 1
            is_value_plus_2 = two_more_items and values[i + 2] == value + 2

            if is_value_plus_1 and is_value_plus_2 or is_value_plus_1:
                if not in_range:
                    output_value = f"{value}-"
                    in_range = True
            elif in_range:
                output_value += str(value)
                output.append(output_value)
                in_range = False
            else:
                output.append(str(value))

        return ",".join(output)

    def as_cron_expression(self):
        return " ".join(
            [
                self.__format_values(self.minutes),
                self.__format_values(self.hours),
                self.__format_values(self.days),
                self.__format_values(self.months),
                self.__format_values(self.weekdays),
            ]
        )
