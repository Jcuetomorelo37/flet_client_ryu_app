import flet as ft
from flet import *
from modules.graphs import *
import requests
import threading
import time
import queue
from modules.login import *

page: ft.Page

data_queue = queue.Queue()
update_event = threading.Event()


def generar_cards(ui_elements,page):
        if not ui_elements:
            return [
                ft.Text(
                   "No hay dispositivos conectados.",
                    text_align=ft.TextAlign.CENTER,
                    style=ft.TextStyle(size=16, color=ft.colors.ERROR),
                )
            ]
        
        return [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(f"Direccion IP: {d.get('ip', 'Desconocida')}", expand=True),
                                        ft.Text(f"Direccion MAC: {d.get('mac', 'Desconocida')}", expand=True),
                                        ft.Text(f"Switch conectado: {d.get('switch', 'No conectado')}", expand=True),
                                        ft.Text(f"Puerto de conexion: {d.get('port', 'No conectado')}", expand=True),
                                        ft.Text(f"Ancho de banda: {d.get('band', 'No medidio')} Mbps", expand=True),
                                        ft.Text(f"Prioridad asignada: {d.get('priority', 'No asignada')}", expand=True),
                                    ],
                                    spacing=5,
                                    alignment=ft.alignment.top_left,
                                    expand=True
                                ),
                                ft.Icon(ft.icons.DEVICES_OTHER,size=30),
                            ],
                            spacing=80,
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True
                            
                        ),
                    ],
                    spacing=10, alignment=ft.MainAxisAlignment.CENTER
                ),
                padding=padding.only(left=30,top=30,right=30,bottom=30),
                margin=margin.only(left=300,top=3,right=300,bottom=3),
                width=400,
                border_radius=5,
                bgcolor=ft.colors.SURFACE_VARIANT,
                on_click=lambda e, dispositivo=d: abrir_modal(dispositivo,page),
            )
            for d in ui_elements
        ]

def abrir_modal(dispositivo, page):
        ancho_banda_control = ft.TextField(
            label="Ancho de banda", value=dispositivo.get("band", "")
        )
        prioridad_control = ft.TextField(
            label="Prioridad", value=dispositivo.get("priority", "")
        )
    
        modal = ft.AlertDialog(
            title=ft.Text("Detalles del dispositivo"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Dispositivo: {dispositivo.get('ip', 'N/A')}"),
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
                            ft.TextButton("Cancelar", on_click=lambda e: cerrar_modal(page)),
                            ft.TextButton(
                                "Confirmar",
                                on_click=lambda e: confirmar_click(
                                dispositivo, ancho_banda_control, prioridad_control, page
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
        )

        page.dialog = modal  # Asignar el modal a la página
        modal.open = True
        page.update()  # Se actualiza solo cuando se asigna el modal

def cerrar_modal(page):
    page.dialog.open = False
    page.update()

def confirmar_click(dispositivo, ancho_banda_control, prioridad_control, page):
    dispositivo["band"] = ancho_banda_control.value
    dispositivo["priority"] = prioridad_control.value
    cerrar_modal(page)

def fetch_metrics():
    try:
        response = requests.get("http://127.0.0.1:5000/metrics")
        if response.status_code == 200:
            data = response.json()
            #print("Datos recibidos:", data)
            return data
    except requests.RequestException as e:
        print(f"Error al obtener métricas: {e}")
    return {}

def update_metrics(ui_elements, data_queue):
    while True:
        metrics = fetch_metrics()

        # Extrae la información de métricas
        topology_info = "\n".join([f"Switch ID: {switch_id}" for switch_id in metrics.get("switches", {})])
        events_info_consumed = f"CPU: {metrics.get('cpu', 0)}% | Memoria: {metrics.get('memory', 0)}%"
        traffic_info = "\n".join([
            f"Sw {switch_id} - Prt {port}: Recepcion {stats['rx_packets']} paquetes, Transmision {stats['tx_packets']} paquetes"
            for switch_id, ports in metrics.get("switches", {}).items()
            for port, stats in ports.items()
        ])
        events_list = metrics.get("events", [])
        events_info = "\n".join([f"[{event['timestamp']}] {event['event']}" for event in events_list])
        dispositivos = metrics.get("devices", [])
        notificaciones = metrics.get("notifications", [])

        # Crea un diccionario con los datos a actualizar
        data_to_send = {
            "topology": topology_info if topology_info else "No hay switches conectados.",
            "consumo": events_info_consumed,
            "traffic": traffic_info if traffic_info else "No hay datos de tráfico disponibles.",
            "events": events_info if events_info else "No hay eventos registrados.",
            "devices": dispositivos,
            "notifications": notificaciones
        }

        data_queue.put(data_to_send)
        
        time.sleep(1)

def process_data_and_update_ui(ui_elements, data_queue, page):
    while True:
        if not data_queue.empty():
            data = data_queue.get()

            ui_elements["topology"].value = data["topology"]
            ui_elements["consumo"].value = data["consumo"]
            ui_elements["traffic"].value = data["traffic"]
            ui_elements["events"].value = data["events"]
            
            if data["notifications"]:
                ui_elements["notifications"] = [
                    {
                        "timestamp": notif.get("timestamp", "N/A"),
                        "title": notif.get("title", "Sin título"),
                        "subtitle": notif.get("subtitle", ""),
                        "description": notif.get("description", ""),
                        "icon": ft.icons.NOTIFICATIONS,
                        "type": "success",
                    }
                    for notif in data["notifications"]
                ]
            else:
                print("No hay notificaciones... ----->")
                ui_elements["notifications"] = []

            if data["devices"]:
                ui_elements["cards"].controls = generar_cards(data["devices"],page)
            else:
                print("No hay dispositivos conectados... ----->")
                ui_elements["cards"].controls = generar_cards(data["devices"],page)

            ui_elements["update_needed"] = threading.Event()
            ui_elements["update_needed"].set()
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
                        ft.Text(f"{notification['description']}", size=14),
                    ]
                ),
                width=400,
                height=300,
                padding=ft.padding.all(20),
            ),
            actions=[
                ft.TextButton(
                    "Cerrar", on_click=close_modal_window
                )
            ],
        )
        page.dialog = modal
        modal.open = True
        page.update()
    
    ui_elements = {
      "cards": ft.Column([], scroll=ft.ScrollMode.AUTO),
      "topology": ft.Text("Cargando topología..."),
      "consumo": ft.Text("Cargando consumos..."),
      "traffic": ft.Text("Cargando tráfico..."),
      "events": ft.Text("Cargando eventos..."),
      "notifications": [],
    }
    
    
    page.update()

    def change_view(index):
        content.controls.clear()
        if index == 0:
            view = "monitoring"
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
                                        ],
                                        scroll=ft.ScrollMode.AUTO
                                    ),
                                    padding=ft.padding.only(top=30, bottom=20, left=20, right=20),
                                    margin=ft.margin.only(top=10, bottom=20, left=20, right=20),
                                    bgcolor=ft.colors.TRANSPARENT,
                                    border=ft.border.all(3, ft.colors.CYAN_900),
                                    width=450, height=610
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
                                        scroll=ft.ScrollMode.AUTO
                                    ),
                                    padding=ft.padding.only(top=20, bottom=20, left=20, right=20),
                                    margin=ft.margin.only(top=10, bottom=20, left=20, right=20),
                                    bgcolor=ft.colors.TRANSPARENT,
                                    border=ft.border.all(3, ft.colors.CYAN_900),
                                    width=650, height=610
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            scroll=ft.ScrollMode.HIDDEN
                        ),
                    ],
                    height=708, #scroll=ft.ScrollMode.AUTO
                )
            )
        elif index == 1:
            view = "statistics"
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
            section_devices_content = ft.Column(
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
                    ft.Container(
                        content=ui_elements["cards"],
                        # width=450,
                        width=1200,
                        height=610,
                        bgcolor=ft.colors.TRANSPARENT,
                        padding=ft.padding.all(10),
                        border_radius=ft.border_radius.all(10),
                    ),                    
                ],
                expand=True,
            )
            content.controls.clear()
            content.controls.append(section_devices_content)
        elif index == 3:
            content.controls.append(
                ft.Column(
                    [
                        # Encabezado de la sección
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
                            width=float("inf"),  # Tamaño fijo en lugar de float("inf")
                            border_radius=ft.border_radius.all(10),
                        ),
                        # Verificar si hay notificaciones
                        ft.Container(
                            content=(
                                ft.Text(
                                    "No hay notificaciones nuevas...",
                                    text_align=ft.TextAlign.CENTER,
                                    style=ft.TextStyle(size=16, color=ft.colors.ERROR),
                                )
                                if not ui_elements or not ui_elements.get("notifications")
                                else ft.ListView(
                                    controls=[
                                        ft.Container(
                                            content=ft.Card(
                                                content=ft.ListTile(
                                                    leading=ft.Icon(
                                                        notif["icon"],
                                                        color=ft.colors.WHITE,
                                                        size=20,
                                                    ),
                                                    title=ft.Text(
                                                        notif["title"],
                                                        color=ft.colors.WHITE,
                                                       size=20,
                                                    ),
                                                    subtitle=ft.Text(
                                                        notif["subtitle"],
                                                        color=ft.colors.WHITE,
                                                        size=14,
                                                    ),
                                                    on_click=lambda e, n=notif: show_notification_details(
                                                        n
                                                    ),
                                                ),
                                                color=ft.colors.GREEN,
                                            ),
                                            width=500,
                                            margin=ft.margin.only(left=70, right=70),
                                        )
                                        for notif in ui_elements["notifications"]
                                    ],
                                    expand=1,
                                )
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
        
    threading.Thread(target=update_metrics, args=(ui_elements, data_queue), daemon=True).start()

    threading.Thread(target=process_data_and_update_ui, args=(ui_elements, data_queue, page), daemon=True).start()



