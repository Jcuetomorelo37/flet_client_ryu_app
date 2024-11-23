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
        # Cambiar el texto del checkbox
        self.new_user_checkbox = Checkbox(value=False, label="Nuevo usuario? Regístrate")

    def read_credentials(self):
        try:
            with open("credentials.txt", "r") as f:
                credentials = {}
                for line in f.readlines():
                    user, password = line.strip().split(":")
                    credentials[user] = password
            return credentials
        except FileNotFoundError:
            return {}

    def save_register(self, username, password):
        with open("credentials.txt", "a") as f:  # Cambiar a modo 'append'
            f.write(f"{username}:{password}\n")

    def validate_credentials(self, e):
        username = self.username_field.textfield.value
        password = self.password_field.textfield.value

        if self.new_user_checkbox.value:
            # Registro de nuevo usuario
            if username and password:
                self.save_register(username, password)
                self.redirect_to_dashboard()
            else:
                self.show_error_modal("Por favor, ingresa usuario y contraseña para registrarte.")
        else:
            # Validación de credenciales existentes
            credentials = self.read_credentials()
            if credentials.get(username) == password:
                self.redirect_to_dashboard()
            else:
                if not username or not password:
                    self.show_error_modal("Por favor, ingresa tus credenciales.")
                else:
                    self.show_error_modal("Usuario o contraseña incorrectos.")

    def show_error_modal(self, message):
        modal = AlertDialog(
            title=Text("Error"),
            content=Text(message),
            actions=[
                ElevatedButton(
                    "Cerrar",
                    on_click=lambda e: self.close_modal(),
                )
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        self.page.dialog = modal
        self.page.dialog.open = True
        self.page.update()

    def close_modal(self):
        self.page.dialog.open = False
        self.page.update()

    def redirect_to_dashboard(self):
        self.page.clean()
        load_dashboard(self.page)

    def build(self):
        return Container(
            Stack(
                [
                    Container(
                        content=Image(
                            src="assets/sdn_core.jpeg",
                            fit=ft.ImageFit.COVER,
                        ),
                        bgcolor=ft.colors.GREY_900,
                        
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
                                            self.new_user_checkbox,
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
