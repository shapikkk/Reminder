import flet as ft
from datetime import datetime

def ui_build(page, reminders, save_reminders):
    selected_date = None

    #UI tools
    reminder_text = ft.TextField(label="Reminder text", width=300)
    reminders_list = ft.Column()
    selected_date_text = ft.Text("No date selected", size=16)

    def add_reminder(e):
        if reminder_text.value and selected_date:
            if selected_date > datetime.now():
                reminders.append((reminder_text.value, selected_date))
                reminders_list.controls.append(ft.Text(f"Reminder: {reminder_text.value} at {selected_date.strftime('%Y-%m-%d %H:%M')}"))
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
        #date_picker_mode=ft.CupertinoDatePickerMode.DATE,
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

    return ft.Column(
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