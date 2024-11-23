import flet as ft
from flet import *
from modules.graphs import *
import requests
import threading
import time
from modules.login import *

global page

def cerrar_modal(e):
                modal.open = False
                page.update()
                
def abrir_modal(dispositivo):
                def confirmar_click(e):
                    dispositivo["ancho_banda"] = ancho_banda_control.value
                    dispositivo["prioridad"] = prioridad_control.value
                    modal.open = False
                    page.update()

                ancho_banda_control = ft.TextField(
                    label="Ancho de banda", value=dispositivo["ancho_banda"]
                )
                prioridad_control = ft.TextField(
                    label="Prioridad", value=dispositivo["prioridad"]
                )

                modal = ft.AlertDialog(
                    title=ft.Text("Modificar dispositivo"),
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"Dispositivo: {dispositivo['nombre']}"),
                                ancho_banda_control,
                                prioridad_control,
                            ],
                            spacing=10,
                        ),
                        height=200,
                    ),
                    actions=[
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.TextButton("Cancelar", on_click=cerrar_modal),
                                    ft.TextButton("Confirmar", on_click=confirmar_click),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                        ),
                    ],
                )

                page.dialog = modal
                modal.open = True
                page.update()

def content_builder(ui_elements, abrir_modal):
    # Validar si ui_elements["devices"] existe y es una lista
    dispositivos = ui_elements.get("devices", [])
    if not isinstance(dispositivos, list):
        dispositivos = []  # Si no es una lista, asigna una vacía

    return ft.Column(
        [
            ft.Container(
                content=ft.AnimatedSwitcher(
                    content=generar_cards(dispositivos, abrir_modal),
                    transition=ft.AnimatedSwitcherTransition.SCALE,
                    duration=300,
                    switch_in_curve=ft.AnimationCurve.EASE_IN,
                    switch_out_curve=ft.AnimationCurve.EASE_OUT,
                ),
                alignment=ft.alignment.center,
                width=float("inf"),
                height=610,
                margin=ft.margin.symmetric(horizontal=-20),
            ),
        ],
        expand=True,
    )

def generar_cards(ui_elements, abrir_modal):
    # Si ui_elements es una lista de dispositivos, accede a ellos directamente
    if not ui_elements:  # Si la lista está vacía
        return ft.Text("No hay dispositivos conectados.", text_align=ft.TextAlign.CENTER)
    return ft.Column(
        [
            ft.Container(
                content=ft.Text(f"IP: {d['ip']}"),
                padding=10,
                border_radius=5,
                bgcolor=ft.colors.SURFACE_VARIANT,
            )
            for d in ui_elements  # Aquí se asume que 'ui_elements' es una lista de dispositivos
        ],
        spacing=10,
    )

def fetch_metrics():
    try:
        response = requests.get("http://127.0.0.1:5000/metrics")
        if response.status_code == 200:
            data = response.json()
            print("Datos recibidos:", data)
            return data
    except requests.RequestException as e:
        print(f"Error al obtener métricas: {e}")
    return {}

def update_metrics(ui_elements):
    while True:
        metrics = fetch_metrics()

        topology_info = "\n".join([f"Switch ID: {switch_id}" for switch_id in metrics.get("switches", {})])
        ui_elements["topology"].value = topology_info if topology_info else "No hay switches conectados."

        events_info = f"CPU: {metrics.get('cpu', 0)}% | Memoria: {metrics.get('memory', 0)}%"
        ui_elements["consumo"].value = events_info

        traffic_info = "\n".join([
            f"Sw {switch_id} - Prt {port}: Recepcion {stats['rx_packets']} paquetes, Transmision {stats['tx_packets']} paquetes"
            for switch_id, ports in metrics.get("switches", {}).items()
            for port, stats in ports.items()
        ])
        ui_elements["traffic"].value = traffic_info if traffic_info else "No hay datos de tráfico disponibles."

        events_list = metrics.get("events", [])
        events_info = "\n".join([f"[{event['timestamp']}] {event['event']}" for event in events_list])
        ui_elements["events"].value = events_info if events_info else "No hay eventos registrados."

        dispositivos = metrics.get("devices", [])
        if not dispositivos:
            ui_elements["cards"].controls = [ft.Text("No hay dispositivos conectados.")]
        else:
            ui_elements["cards"].controls = generar_cards(dispositivos, abrir_modal)

        ui_elements["cards"].update()
        
        ui_elements["topology"].update()
        
        ui_elements["consumo"].update()
        ui_elements["traffic"].update()
        ui_elements["events"].update()

        time.sleep(1)


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

def on_hover(e):
    global is_hovered
    is_hovered = True if e.data == "true" else False

def build(self):
    return Container(
        Stack(
            [
                Image(src="assets/portada.png"),
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
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Checkbox(
                                                        value=False
                                                    ),  # Checkbox
                                                    ft.Text(
                                                        "Recordar ingreso",
                                                        color="white",
                                                        size=14,
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.START,  # Alineación del contenido
                                            ),
                                        ),
                                        ft.Container(
                                            content=ft.Text(
                                                "Contraseña olvidada",
                                                color=(
                                                    "white"
                                                    if not is_hovered
                                                    else "lightblue"
                                                ),  # Cambia el color en hover
                                                size=14,
                                                on_hover=on_hover,  # Asigna la función on_hover
                                            ),
                                            padding=ft.padding.only(
                                                top=10
                                            ),  # Espaciado adicional si es necesario
                                        ),
                                    ],
                                    alignment=MainAxisAlignment.SPACE_AROUND,
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

def logout(page, e):
    print("Cerrando sesión...")
    from modules.login import LoginApp
    page.clean()
    login_app = LoginApp()
    page.add(login_app)
    page.update()


def load_dashboard(page):
    page.bgcolor = ft.colors.BLACK26
    page.scroll = "adaptive"
    page.update()

    notification_colors = {
        "actualizacion": ft.colors.BLUE,
        "seguridad": ft.colors.GREY,
        "informe": ft.colors.YELLOW,
        "sincronizacion": ft.colors.ORANGE,
        "error_flujo": ft.colors.RED,
        "topologia": ft.colors.PURPLE,
        "rendimiento": ft.colors.AMBER,
        "flujo_correcto": ft.colors.GREEN,
    }

    notifications = [
        {
            "icon": ft.icons.NOTIFICATIONS,
            "title": "Nueva actualización disponible",
            "subtitle": "Hace 2 horas",
            "type": "actualizacion",
            "descripcion": "Se ha lanzado una nueva actualización del sistema. Por favor, revisa las notas de la versión para más detalles.",
        },
        {
            "icon": ft.icons.WARNING,
            "title": "Alerta de seguridad",
            "subtitle": "Hace 1 día",
            "type": "seguridad",
            "descripcion": "Se detectó un posible intento de acceso no autorizado. Se recomienda revisar los logs de seguridad.",
        },
        {
            "icon": ft.icons.INFO,
            "title": "Informe semanal listo",
            "subtitle": "Hace 3 días",
            "type": "informe",
            "descripcion": "El informe de rendimiento semanal está listo para su revisión. Incluye detalles sobre el tráfico de la red y rendimiento de los flujos.",
        },
        {
            "icon": ft.icons.ERROR,
            "title": "Fallo en la instalación de un flujo",
            "subtitle": "Hace 30 minutos",
            "type": "error_flujo",
            "descripcion": "Un error ocurrió al intentar instalar un flujo en el switch SW1. Verifique la configuración y vuelva a intentarlo.",
        },
    ]

    def close_modal_window(e):
        global modal
        modal.open = False
        page.dialog = None
        page.update()

    def show_notification_details(notification):
        global modal
        modal = ft.AlertDialog(
            title=ft.Text(notification["title"], size=20),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"{notification['subtitle']}", size=16),
                        ft.Text(f"{notification['descripcion']}", size=14),
                    ]
                ),
                width=400,  # Cambia el ancho del modal
                height=300,  # Cambia el alto del modal
                padding=ft.padding.all(20),  # Añade padding si es necesario
            ),
            actions=[
                ft.TextButton(
                    "Cerrar", on_click=close_modal_window
                )  # Vincula la función de cierre
            ],
        )
        page.dialog = modal
        modal.open = True
        page.update()
    
    ui_elements = {
    #   "cards": ft.Column([], scroll=ft.ScrollMode.ADAPTIVE),
      "cards": ft.Column([]),
      "topology": ft.Text("Cargando topología..."),
      "consumo": ft.Text("Cargando consumos..."),
      "traffic": ft.Text("Cargando tráfico..."),
      "events": ft.Text("Cargando eventos..."),
    }
    
    page.controls.append(ui_elements["cards"])
    page.update()

    def change_view(index):
        content.controls.clear()
        if index == 0:
            if "topology" not in ui_elements:
                ui_elements["topology"] = ft.Text("In progress...")
                
            if "consumo" not in ui_elements:
                ui_elements["consumo"] = ft.Text("In progress...")
                
            if "traffic" not in ui_elements:
                ui_elements["traffic"] = ft.Text("In progress...")
                
            if "events" not in ui_elements:
                ui_elements["events"] = ft.Text("In progress...")
            content.controls.append(
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "Monitorear Red",
                                theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=10, bottom=10),
                            margin=ft.margin.only(right=30, top=20, bottom=20),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            width=float("inf"),
                            border_radius=ft.border_radius.all(10),
                        ),
                        ft.Row(
                            controls=[
                                # Sección 1: Estado de la Red
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("Estado de la Red", weight=ft.FontWeight.BOLD, size=20, color=ft.colors.WHITE),
                                            ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text("Topología de la Red:"),
                                                        ui_elements["topology"],
                                                    ]
                                                ),
                                                padding=ft.padding.all(20),
                                                bgcolor=ft.colors.SURFACE_VARIANT,
                                                border_radius=ft.border_radius.all(10),
                                                width=530
                                            ),
                                            ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text("Uso de recursos:"),
                                                        ui_elements["consumo"],
                                                    ]
                                                ),
                                                padding=ft.padding.all(20),
                                                bgcolor=ft.colors.SURFACE_VARIANT,
                                                border_radius=ft.border_radius.all(10),
                                                width=530
                                            ),
                                            ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text("Eventos en la red:"),
                                                        ui_elements["events"],
                                                    ]
                                                ),
                                                padding=ft.padding.all(20),
                                                bgcolor=ft.colors.SURFACE_VARIANT,
                                                border_radius=ft.border_radius.all(10),
                                                width=530
                                            )
                                        ]
                                    ),
                                    padding=ft.padding.only(top=20, bottom=20, left=20, right=20),
                                    bgcolor=ft.colors.TRANSPARENT,
                                    border=ft.border.all(3, ft.colors.CYAN_900),
                                    width=450
                                ),
                                # Sección 2: Datos de Carga
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("Datos de Carga", weight=ft.FontWeight.BOLD, size=20, color=ft.colors.WHITE),
                                            ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text("Estadísticas de puertos:"),
                                                        ui_elements["traffic"],
                                                    ]
                                                ),
                                                padding=ft.padding.all(20),
                                                bgcolor=ft.colors.SURFACE_VARIANT,
                                                border_radius=ft.border_radius.all(10),
                                                width=600
                                            ),
                                        ],
                                    ),
                                    padding=ft.padding.only(top=20, bottom=20, left=20, right=20),
                                    bgcolor=ft.colors.TRANSPARENT,
                                    border=ft.border.all(3, ft.colors.CYAN_900),
                                    width=650
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    height=708,
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )
        elif index == 1:
            if "topology" not in ui_elements:
                ui_elements["topology"] = ft.Text("In progress...")
                
            if "consumo" not in ui_elements:
                ui_elements["consumo"] = ft.Text("In progress...")
                
            if "traffic" not in ui_elements:
                ui_elements["traffic"] = ft.Text("In progress...")
                
            if "events" not in ui_elements:
                ui_elements["events"] = ft.Text("In progress...")
            content.controls.append(
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "Estadisticas de Trafico",
                                theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=10, bottom=10),
                            margin=ft.margin.only(right=30, top=20, bottom=20),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            width=float("inf"),
                            border_radius=ft.border_radius.all(10),
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.Container(
                                            graph_one,
                                            height=300,
                                            margin=ft.margin.only(left=-15),
                                        ),
                                        ft.Container(
                                            graph_two,
                                            height=300,
                                            margin=ft.margin.only(left=-15),
                                        ),
                                    ],
                                ),
                                ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.Container(
                                            graph_three,
                                            height=300,
                                            margin=ft.margin.only(right=20),
                                        ),
                                        ft.Container(
                                            graph_four,
                                            height=300,
                                            margin=ft.margin.only(right=20),
                                        ),
                                    ],
                                ),
                            ]
                        ),
                    ]
                )
            )
        elif index == 2:
            if "topology" not in ui_elements:
                ui_elements["topology"] = ft.Text("In progress...")
                
            if "consumo" not in ui_elements:
                ui_elements["consumo"] = ft.Text("In progress...")
                
            if "traffic" not in ui_elements:
                ui_elements["traffic"] = ft.Text("In progress...")
                
            if "events" not in ui_elements:
                ui_elements["events"] = ft.Text("In progress...")
            content.controls.append(
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "Dispositivos Conectados",
                                theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=10, bottom=10),
                            margin=ft.margin.only(right=30, top=20, bottom=20),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            width=float("inf"),
                            border_radius=ft.border_radius.all(10),
                        ),
                        content_builder(ui_elements, abrir_modal)
                    ],
                    expand=True,
                )
            )
            print("nada de nada jajajaja")
        elif index == 3:
            if "topology" not in ui_elements:
                ui_elements["topology"] = ft.Text("In progress...")
                
            if "consumo" not in ui_elements:
                ui_elements["consumo"] = ft.Text("In progress...")
                
            if "traffic" not in ui_elements:
                ui_elements["traffic"] = ft.Text("In progress...")
                
            if "events" not in ui_elements:
                ui_elements["events"] = ft.Text("In progress...")
            content.controls.append(
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "Notificaciones",
                                theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=10, bottom=10),
                            margin=ft.margin.only(right=30, top=20, bottom=20),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            width=float("inf"),
                            border_radius=ft.border_radius.all(10),
                        ),
                        ft.Container(
                            content=ft.ListView(
                                controls=[
                                    ft.Container(
                                        content=ft.Card(
                                            content=ft.ListTile(
                                                leading=ft.Icon(
                                                    notification["icon"],
                                                    color=ft.colors.WHITE,
                                                    size=20,
                                                ),
                                                title=ft.Text(
                                                    notification["title"],
                                                    color=ft.colors.WHITE,
                                                    size=20,
                                                ),
                                                subtitle=ft.Text(
                                                    notification["subtitle"],
                                                    color=ft.colors.WHITE,
                                                    size=20,
                                                ),
                                                on_click=lambda e, n=notification: show_notification_details(
                                                    n
                                                ),
                                            ),
                                            color=notification_colors[
                                                notification["type"]
                                            ],
                                        ),
                                        width=500,
                                        margin=ft.margin.only(left=100, right=100),
                                    )
                                    for notification in notifications
                                ],
                                expand=1,
                            ),
                            height=610,
                        ),
                    ]
                )
            )
        page.update()

    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.NavigationRail(
                        selected_index=0,
                        on_change=lambda e: change_view(e.control.selected_index),
                        destinations=[
                            ft.NavigationRailDestination(
                                icon=ft.icons.INSIGHTS,
                                label="Monitoreo",
                                padding=ft.padding.only(top=75),
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.GRAPHIC_EQ_OUTLINED,
                                label="Estadísticas",
                                padding=ft.padding.symmetric(vertical=15),
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.DEVICES,
                                label="Dispositivos",
                                padding=ft.padding.symmetric(vertical=15),
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.NOTIFICATIONS,
                                label="Notificaciones",
                                padding=ft.padding.symmetric(vertical=15),
                            ),
                        ],
                        extended=False,
                        min_width=100,
                        min_extended_width=200,
                    ),
                    expand=True,
                    height=500,  # Ajustar este valor
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.LOGOUT_SHARP,
                        on_click=lambda e: logout(page, e),
                        icon_color=ft.colors.WHITE,
                        icon_size=24,
                    ),
                    margin=ft.margin.only(top=0, bottom=5),
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
        ),
        width=100,
        bgcolor=ft.colors.GREY_400,
        border_radius=10,
        margin=ft.margin.only(left=15, right=15, bottom=15, top=-15),
    )

    content = ft.Column(expand=True)

    change_view(0)

    page.add(
        ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1),
                ft.Container(content, expand=True),
            ],
            expand=True,
        )
    )
    
    threading.Thread(target=update_metrics, args=(ui_elements,), daemon=True).start()

