from dotenv import load_dotenv
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta, timezone

load_dotenv()

#load env variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
WANTED_LISTS = os.getenv("WANTED_LISTS")


#SCOPES = [
#    "https://www.googleapis.com/auth/tasks",
#    "https://www.googleapis.com/auth/calendar",
#]
SCOPES = ["https://www.googleapis.com/auth/tasks","https://www.googleapis.com/auth/calendar"]

creds = Credentials(
    token=None,  # access token will be fetched automatically
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=SCOPES,
)

task_service = build("tasks", "v1", credentials=creds)
calendar_service = build("calendar", "v3", credentials=creds)

#gets refresh token for client
def get_refresh_token():
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:3000/oauth2callback"],
            }
        },
        SCOPES,
    )

    creds = flow.run_local_server(port=3000,prompt="consent",
        access_type="offline",)

    print("NEW REFRESH TOKEN:")
    print(creds.refresh_token)

#pulls task lists
def get_tasks_list_ids(task_service):
    task_lists = task_service.tasklists().list().execute()
    task_ids = []
    for task_list in task_lists['items']:
        task_ids.append({'id': task_list['id'], 'title': task_list['title'], 'selfLink': task_list['selfLink']})
    return task_ids

#filters the lists based on WANTED_LISTS in .env
def filter_lists(task_service):
    list_ids = []
    for list in get_tasks_list_ids(task_service=task_service):
        if list['title'] in WANTED_LISTS:
            list_ids.append(list)
    return list_ids

#pull all the different tasks
def get_tasks(task_service):
    tasks = []
    for tasklist in filter_lists(task_service=task_service):
        raw_data = task_service.tasks().list(tasklist = tasklist['id']).execute()
        tasks.append({'list_id': tasklist['id'], 'list_title': tasklist['title'], 'tasks': raw_data['items']})
    return tasks

def get_events_next_week(calendar_service):
    now = datetime.now(timezone.utc)
    one_week = now + timedelta(days=7)

    events_result = calendar_service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=one_week.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return events_result.get("items", [])

