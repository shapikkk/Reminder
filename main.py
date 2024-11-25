import os
import flet as ft
from storage import *
from ui import *

def main(page: ft.Page):
    page.title = "Reminder App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    reminders = load_reminders()

    page.theme_mode = ft.ThemeMode.DARK
    task_manager = TaskManager()
    date_grid = DateGrid(Settings.get_year(), Settings.get_month(), task_manager)
    page.add(ft.Column(controls=[date_grid, ft.Divider(), task_manager]))

if __name__ == "__main__":
    if os.getenv("CI") != "true":
        ft.app(target=main)
    else:
        print("Running in CI/CD mode. GUI is disabled.")
