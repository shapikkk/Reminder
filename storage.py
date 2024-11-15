import json
from datetime import datetime

REMINDERS_FILE = "./reminders.json"

def load_reminders():
    try:
        with open("./reminders.json", 'r') as reminders:
            data = json.load(reminders)
            return [(item["text"], datetime.fromisoformat(item["date"])) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_reminders(reminders):
    with open("./reminders.json", 'w') as output_file:
        data = [{"text": text, "date": date.isoformat()} for text, date in reminders]
        json.dump(data, output_file)
