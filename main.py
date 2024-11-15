import flet as ft
from storage import *
from ui import *

def main(page: ft.Page):
    page.title = "Reminder App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    reminders = load_reminders()
    ui = ui_build(page, reminders, save_reminders)

    page.add(ui)

ft.app(target=main)