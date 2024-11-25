import json
from datetime import datetime

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

def reminder_updater(reminders):
    time_now = datetime.now()
    for index, (text, date, status) in enumerate(reminders):
        status = "past" if date < time_now else "active"
        reminders[index] = (text, date, status)
