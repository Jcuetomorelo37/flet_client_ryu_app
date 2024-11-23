import flet as ft
from flet import *
from modules.graphs import *
from modules.inputs import *
from modules.login import *


style_frame: dict = {
    "expand": True,
    "bgcolor": "#1F2127",
    "border_radius": 18,
    "padding": 20,
    "border": border.all(1, "#44f4f4f4"),
    "alignment": alignment.center,
}


graph_one: ft.Container = GraphOne()
graph_two: ft.Container = GraphTwo()
graph_three: ft.Container = GraphThree()
graph_four: ft.Container = GraphFour()

is_hovered = False


def main(page: ft.Page):

    page.padding = 0
    page.window.resizable = True
    page.window.maximized = True
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.GREY_300
    page.scroll = "adaptive"
    # login_app = LoginApp()
    # page.add(login_app)
    page.update()

    load_dashboard(page)


ft.app(target=main)
