
import flet as ft
from flet import *

style_frame: dict = {
    "expand": True,
    "bgcolor": "#1F2127",
    "border_radius": 18,
    "padding": 20,
    "border": border.all(1, "#44f4f4f4"),
    "alignment": alignment.center,
}

class InputField(UserControl):
    def __init__(self, width, height, hint_text, icon, password=False):
        super().__init__()
        self.password_visible = password
        self.textfield = TextField(
            hint_text=hint_text,
            border=InputBorder.NONE,
            color="white",
            hint_style=TextStyle(
                color="white",
            ),
            width=width / 5 * 4,
            height=height,
            bgcolor="transparent",
            text_style=TextStyle(size=18, weight="w400"),
            password=self.password_visible,
        )
        self.icon_button = Icon(
            icon,
            color="white",
        )

        self.body = Container(
            Row(
                [
                    self.textfield,
                    GestureDetector(
                        on_tap=self.toggle_password_visibility,
                        content=self.icon_button,
                    ),
                ]
            ),
            width=width,
            height=height,
            border=border.all(1, "#44f4f4f4"),
            border_radius=18,
            bgcolor="transparent",
            alignment=alignment.center,
        )

    def toggle_password_visibility(self, e):
        self.password_visible = not self.password_visible
        self.textfield.password = self.password_visible
        self.icon_button.icon = (
            icons.LOCK_OPEN_ROUNDED if not self.password_visible else icons.LOCK_ROUNDED
        )
        self.update()

    def build(self):
        return self.body
