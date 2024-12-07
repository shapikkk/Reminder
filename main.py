import os
import flet as ft
from storage import *
from ui import *

def main(page: ft.Page):
    page.title = "Reminder App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    task_manager = TaskManager()

    date_grid = DateGrid(Settings.get_year(), Settings.get_month(), task_manager)
    page.add(ft.Column(controls=[date_grid, ft.Divider(), task_manager]))

ft.app(target=main)
