import flet as ft
import calendar
from database import *
from storage import *
from datetime import datetime

cal = calendar.Calendar()

date_class = {0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"}
month_class = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

# Calendar settings
class Settings:
    year = datetime.now().year
    month = datetime.now().month

    @staticmethod
    def get_year():
        return Settings.year

    @staticmethod
    def get_month():
        return Settings.month

    @staticmethod
    def get_date(delta: int):
        if delta == 1:
            if Settings.month + delta > 12:
                Settings.month = 1
                Settings.year += 1
            else:
                Settings.month += 1
        if delta == -1:
            if Settings.month + delta < 1:
                Settings.month = 12
                Settings.year -= 1
            else:
                Settings.month -= 1

# Container to show the day
class DateBox(ft.Container):
    def __init__(self, day, date=None, date_instance=None, task_instance=None, opacity_=1.0):
        super().__init__(
            width=30,
            height=30,
            alignment=ft.alignment.center,
            shape=ft.BoxShape.RECTANGLE,
            border_radius=5,
            opacity=opacity_,
            data=date,
            on_click=self.selected
        )
        self.day = day
        self.date_instance = date_instance
        self.task_instance = task_instance
        self.content = ft.Text(self.day, text_align="center")

    def selected(self, e: ft.TapEvent):
        if self.date_instance:
            for row in self.date_instance.controls[1:]:
                for date in row.controls:
                    date.bgcolor = "#20303e" if date == e.control else None
                    date.border = (
                        ft.border.all(0.5, "#4fadf9") if date == e.control else None
                    )
                    if date == e.control:
                        self.task_instance.set_selected_date(e.control.data)
            self.date_instance.update()
            self.task_instance.update()

class DateGrid(ft.Column):
    def __init__(self, year, month, task_instance):
        super().__init__()
        self.year = year
        self.month = month
        self.task_manager = task_instance
        self.date = ft.Text(f"{month_class[self.month]} {self.year}")
        self.controls.insert(
            1,
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.IconButton("chevron_left", on_click=lambda e: self.update_date_grid(e, -1)),
                        ft.Container(width=150, content=self.date, alignment=ft.alignment.center),
                        ft.IconButton("chevron_right", on_click=lambda e: self.update_date_grid(e, 1)),
                    ],
                    alignment="center",
                )
            ),
        )
        self.populate_date_grid(self.year, self.month)

    def populate_date_grid(self, year, month):
        del self.controls[1:]
        for week in cal.monthdayscalendar(year, month):
            row = ft.Row(controls=[], alignment="spaceEvenly")
            for day in week:
                if day != 0:
                    row.controls.append(
                        DateBox(day, self.format_date(day), self, self.task_manager)
                    )
                else:
                    row.controls.append(DateBox(" "))
            self.controls.append(row)

    def update_date_grid(self, e, delta):
        Settings.get_date(delta)
        self.update_year_and_month(Settings.get_year(), Settings.get_month())
        self.populate_date_grid(Settings.get_year(), Settings.get_month())
        self.update()

    def update_year_and_month(self, year, month):
        self.year = year
        self.month = month
        self.date.value = f"{month_class[self.month]} {self.year}"

    def format_date(self, day):
        return f"{month_class[self.month]} {day}, {self.year}"

class TaskManager(ft.Column):

    newDB = Database()

    def __init__(self):
        super().__init__()
        self.selected_date = None
        self.date_text = ft.Text("No date selected", size=16)
        self.reminder_text = ft.TextField(label="Reminder text", width=300)
        self.reminders_list = ft.Column()
        self.reminders = load_reminders()
        self.remindersGetTasks = self.newDB.get_all_tasks()
        self.controls.append(self.date_text)
        self.controls.append(self.reminder_text)
        self.controls.append(self.reminders_list)
        self.controls.append(
            ft.ElevatedButton("Add Reminder", on_click=self.add_reminder)
        )
        self.load_existing_reminders()

    def set_selected_date(self, date):
        self.selected_date = date
        self.date_text.value = f"Selected date: {self.selected_date}"
        self.update()

    def add_reminder(self, e):
        if self.selected_date and self.reminder_text.value:
            try:
                reminder = (self.reminder_text.value, self.selected_date, "0")
                self.newDB.save_task(reminder)
                self.reminders_list.controls.append(
                    ft.Text(f"Reminder: {self.reminder_text.value} at {self.selected_date}")
                )
                self.reminder_text.value = ""
                self.update()
            except ValueError as ex:
                print(f"Error parsing date: {ex}")

    def load_existing_reminders(self):
        for id, description, date, status in self.remindersGetTasks:
            reminder_status = f"({status})" if status else ""
            self.reminders_list.controls.append(
                ft.Text(f"Reminder: {description} at {date.isoformat()} {reminder_status}")
            )