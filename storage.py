import json
from datetime import datetime
from plyer import notification
from database import *

REMINDERS_FILE = "./reminders.json"

def load_reminders():
    try:
        with open(REMINDERS_FILE, 'r') as reminders:
            data = json.load(reminders)
            reminders_data = [(item["text"], datetime.fromisoformat(item["date"]), item["status"]) for item in data]
            reminder_updater(reminders_data)
            return reminders_data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_reminders(reminders):
    with open(REMINDERS_FILE, 'w') as output_file:
        data = [{"text": text, "date": date.isoformat(), "status": status} for text, date, status in reminders]
        json.dump(data, output_file, indent=4)

def show_notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='Reminder',
        app_icon='',
        timeout=5
    )

def reminder_updater():
    db = Database()

    reminders = db.get_all_tasks()

    time_now = datetime.now()

    for reminder_id, description, date, status in reminders:
        new_status = 1 if date < time_now.date() else 0
        if int(status) != new_status:
            db.update_task_status(reminder_id, int(new_status))

        time_difference = (date - time_now.date()).days * 24 * 3600
        if new_status == 0 and 0 <= time_difference <= 86400:
            show_notify("Reminder for tomorrow!", f"Don't forget: {description}")