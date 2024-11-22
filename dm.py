import flet as ft
import requests
import threading
import time

# Función para obtener métricas desde el servidor Ryu
def fetch_metrics():
    try:
        response = requests.get("http://127.0.0.1:5000/metrics")
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener métricas: {e}")
    return {}

# Función para actualizar las métricas en la aplicación Flet
def update_metrics(ui_elements):
    while True:
        metrics = fetch_metrics()
        # Actualizar datos de topología
        topology_info = "\n".join([f"Switch ID: {switch_id}" for switch_id in metrics.get("switches", {})])
        ui_elements["topology"].value = topology_info if topology_info else "No hay switches conectados."

        # Actualizar eventos de la red
        events_info = f"CPU: {metrics.get('cpu', 0)}% | Memoria: {metrics.get('memory', 0)}%"
        ui_elements["events"].value = events_info

        # Actualizar estadísticas de tráfico por puertos
        traffic_info = "\n".join([
            f"Switch {switch_id} - Puerto {port}: RX {stats['rx_packets']} paquetes, TX {stats['tx_packets']} paquetes"
            for switch_id, ports in metrics.get("switches", {}).items()
            for port, stats in ports.items()
        ])
        ui_elements["traffic"].value = traffic_info if traffic_info else "No hay datos de tráfico disponibles."

        time.sleep(5)  # Actualizar cada 5 segundos

# Aplicación Flet
def main(page: ft.Page):
    page.title = "Monitor de Red"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK

    # Elementos de la interfaz
    ui_elements = {
        "topology": ft.Text("Cargando topología..."),
        "events": ft.Text("Cargando eventos..."),
        "traffic": ft.Text("Cargando tráfico..."),
    }

    # Diseño
    page.add(
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
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Eventos de la Red:"),
                                ui_elements["events"],
                            ]
                        ),
                        padding=ft.padding.all(20),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=ft.border_radius.all(10),
                    ),
                ]
            ),
            padding=ft.padding.all(20),
            bgcolor=ft.colors.TRANSPARENT,
            border=ft.border.all(3, ft.colors.CYAN_900),
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
                    ),
                ]
            ),
            padding=ft.padding.all(20),
            bgcolor=ft.colors.TRANSPARENT,
            border=ft.border.all(3, ft.colors.CYAN_900),
        ),
    )

    # Hilo para actualizar métricas periódicamente
    threading.Thread(target=update_metrics, args=(ui_elements,), daemon=True).start()

# Ejecutar aplicación
ft.app(target=main)
