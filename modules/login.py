
import flet as ft
from flet import *
from modules.inputs import *
from shared.dashboard import *

style_frame: dict = {
    "expand": True,
    "bgcolor": "#1F2127",
    "border_radius": 18,
    "padding": 20,
    "border": border.all(1, "#44f4f4f4"),
    "alignment": alignment.center,
}

class LoginApp(UserControl):
    def __init__(self):
        super().__init__()
        self.username_field = InputField(
            width=320, height=60, hint_text="Usuario", icon=icons.PERSON_ROUNDED
        )
        self.password_field = InputField(
            width=320,
            height=60,
            hint_text="Contraseña",
            icon=icons.LOCK_ROUNDED,
            password=True,
        )
        self.remember_me = Checkbox(value=False, label="Recordar ingreso")

    def read_credentials(self):
        with open("credentials.txt", "r") as f:
            credentials = {}
            for line in f.readlines():
                user, password = line.strip().split(":")
                credentials[user] = password
        return credentials

    def save_remember_me(self, username, password):
        if self.remember_me.value:
            with open("remember_me.txt", "w") as f:
                f.write(f"{username}:{password}")

    def check_remember_me(self):
        try:
            with open("remember_me.txt", "r") as f:
                username, password = f.read().strip().split(":")
                return username, password
        except FileNotFoundError:
            return None, None

    def validate_credentials(self, e):
        credentials = self.read_credentials()
        username = self.username_field.textfield.value
        password = self.password_field.textfield.value

        if credentials.get(username) == password:
            self.save_remember_me(username, password)
            self.redirect_to_dashboard()
        else:
            self.show_error("Usuario o contraseña incorrectos.")

    def redirect_to_dashboard(self):
        self.page.clean()
        load_dashboard(self.page)

    def show_error(self, message):
        error_message = Text(message, color="red", size=16)
        self.page.add(error_message)

    def build(self):
        remembered_user, remembered_pass = self.check_remember_me()
        if remembered_user and remembered_pass:
            self.username_field.textfield.value = remembered_user
            self.password_field.textfield.value = remembered_pass
            self.redirect_to_dashboard()

    def build(self):
        return Container(
            Stack(
                [
                    Container(
                        content=Image(
                            src="assets/portada.png",
                            fit=ft.ImageFit.COVER,
                        ),
                        bgcolor=ft.colors.GREY_900,
                        expand=True 
                    ),

                    Container(
                        alignment=alignment.center,
                        margin=margin.only(top=150),
                        content=Container(
                            Column(
                                [
                                    Row(
                                        [
                                            Text(
                                                "Iniciar sesión",
                                                color="white",
                                                weight="w700",
                                                size=26,
                                                text_align="center",
                                            ),
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        [self.username_field],
                                        alignment=MainAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        [self.password_field],
                                        alignment=MainAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        [
                                            Checkbox(value=False),
                                            Text(
                                                "Recordar ingreso",
                                                color="white",
                                                size=14,
                                            ),
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        [
                                            ElevatedButton(
                                                "Ingresar",
                                                color="black",
                                                bgcolor="gray",
                                                width=300,
                                                height=60,
                                                on_click=self.validate_credentials,
                                            )
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                            ),
                            width=400,
                            height=400,
                            border_radius=18,
                            blur=Blur(10, 12, BlurTileMode.MIRROR),
                            border=border.all(1, "#44f4f4f4"),
                            bgcolor="#10f4f4f4",
                            alignment=alignment.center,
                        ),
                    ),
                ]
            )
        )
