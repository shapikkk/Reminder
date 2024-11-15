import flet as ft
import json
from datetime import datetime, timedelta

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
        json.dumps(reminders, output_file)

def main(page: ft.Page):
    page.title = "Reminder App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    #list of reminders
    reminders = load_reminders()
    selected_date = None

    def add_reminder(e):
        if reminder_text.value and selected_date:
            if selected_date > datetime.now():
                reminders.append((reminder_text.value, selected_date))
                reminders_list.controls.append(ft.Text(f"Reminder {reminder_text.value} at {selected_date.strftime('%Y-%m-%d %H:%M')}"))
                save_reminders(reminders)
                reminder_text.value = ""
                reminders_list.update()
            else:
                errorMessage = ft.SnackBar(ft.Text("Date must be in the future"))
                page.overlay.append(errorMessage)
                errorMessage.open = True
        else:
            errorMessage = ft.SnackBar(ft.Text("Fill all fields"))
            page.overlay.append(errorMessage)
            errorMessage.open = True

    #UI tools
    reminder_text = ft.TextField(label="Reminder text", width=300)
    reminders_list = ft.Column()
    selected_date_text = ft.Text("No date selected", size=16)
    add_button = ft.ElevatedButton("Add Reminder", on_click=add_reminder)

    # Cupertino date picker. Online docs: https://flet.dev/docs/controls/cupertinodatepicker/
    def handle_date_change(e: ft.ControlEvent):
        nonlocal selected_date
        selected_date = e.control.value
        selected_date_text.value = f"Selected date: {selected_date.strftime('%Y-%m-%d %H:%M')}"
        selected_date_text.update()

    for text, date in reminders:
        reminders_list.controls.append(
            ft.Text(f"Reminder: {text} at {date.strftime('%Y-%m-%d %H:%M')}")
        )

    cupertino_date_picker = ft.CupertinoDatePicker(
        date_picker_mode=ft.CupertinoDatePickerMode.DATE,
        on_change=handle_date_change,
    )

    open_dataPickerButton = ft.ElevatedButton(
            "DatePicker",
            on_click=lambda e: page.open(
                ft.CupertinoBottomSheet(
                    cupertino_date_picker,
                    height=216,
                    padding=ft.padding.only(top=6),
            )
        ),
    )

    page.add(
        ft.Column(
            [
                ft.Text("Reminder App", size=20, weight=ft.FontWeight.BOLD),
                reminder_text,
                selected_date_text,
                open_dataPickerButton,
                add_button,
                ft.Divider(),
                ft.Text("Your reminders:", size=20),
                reminders_list
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
    )

ft.app(target=main)