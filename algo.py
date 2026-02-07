import array
from google_funct import get_tasks, get_events_next_week, calendar_service, task_service
from my_calendar import MyCalendar
tasks = get_tasks(task_service=task_service)

events = get_events_next_week(calendar_service=calendar_service)

# 1 day is 96 15min intervals
#7 days a week

cal = MyCalendar(7)
cal.set_range(0, "09:00", "11:30", 1)
cal.set_range(0, "13:00", "14:00", 2)

print(cal.get_range(0, "09:00", "10:00"))
cal.print_calendar()

