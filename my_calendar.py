from datetime import datetime

class MyCalendar:
    SLOTS_PER_DAY = 96
    MINUTES_PER_SLOT = 15

    def __init__(self, days_ahead: int):
        if days_ahead <= 0:
            raise ValueError("days_ahead must be positive")

        self.days_ahead = days_ahead
        self._cal = [[0] * self.SLOTS_PER_DAY for _ in range(days_ahead)]

    # ---------- Internal helpers ----------

    def _time_to_slot(self, time_str: str) -> int:
        try:
            hour, minute = map(int, time_str.split(":"))
        except ValueError:
            raise ValueError("Time must be in HH:MM format")

        if not (0 <= hour < 24):
            raise ValueError("Hour must be between 0 and 23")

        if minute % self.MINUTES_PER_SLOT != 0:
            raise ValueError("Time must be in 15-minute increments")

        return hour * 4 + minute // self.MINUTES_PER_SLOT

    def _check_day(self, day: int):
        if not (0 <= day < self.days_ahead):
            raise IndexError("Invalid day index")

    # ---------- Public API ----------

    def set_range(self, day: int, start_time: str, end_time: str, value):
        self._check_day(day)

        start = self._time_to_slot(start_time)
        end = self._time_to_slot(end_time)

        if start >= end:
            raise ValueError("start_time must be before end_time")

        self._cal[day][start:end] = [value] * (end - start)

    def get_range(self, day: int, start_time: str, end_time: str):
        self._check_day(day)

        start = self._time_to_slot(start_time)
        end = self._time_to_slot(end_time)

        if start >= end:
            raise ValueError("start_time must be before end_time")

        return self._cal[day][start:end]

    def clear_day(self, day: int):
        self._check_day(day)
        self._cal[day] = [0] * self.SLOTS_PER_DAY

    def print_calendar(self):
        for day, slots in enumerate(self._cal):
            print(f"Day {day}: {slots}")
