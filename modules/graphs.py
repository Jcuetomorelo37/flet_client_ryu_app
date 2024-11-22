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

class GraphOne(ft.Container):
    def __init__(self):
        super().__init__(**style_frame)
        data_1 = [
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(0, 3),
                    ft.LineChartDataPoint(2, 2),
                    ft.LineChartDataPoint(4, 5),
                    ft.LineChartDataPoint(6, 3.1),
                    ft.LineChartDataPoint(8, 4),
                    ft.LineChartDataPoint(10, 3),
                    ft.LineChartDataPoint(11, 4),
                    ft.LineChartDataPoint(14, 4.2),
                    ft.LineChartDataPoint(14.8, 5),
                ],
                stroke_width=5,
                color=ft.colors.CYAN,
                curved=True,
                stroke_cap_round=True,
                gradient=ft.LinearGradient(colors=[ft.colors.CYAN, ft.colors.WHITE]),
            )
        ]

        self.content = ft.LineChart(
            data_series=data_1,
            border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.BLACK)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                width=1,
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                width=1,
            ),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=1, label=ft.Text("10", size=14, color=ft.colors.WHITE)
                    ),
                    ft.ChartAxisLabel(
                        value=2, label=ft.Text("20", size=14, color=ft.colors.WHITE)
                    ),
                    ft.ChartAxisLabel(
                        value=3, label=ft.Text("30", size=14, color=ft.colors.WHITE)
                    ),
                    ft.ChartAxisLabel(
                        value=4, label=ft.Text("40", size=14, color=ft.colors.WHITE)
                    ),
                    ft.ChartAxisLabel(
                        value=5, label=ft.Text("50", size=14, color=ft.colors.WHITE)
                    ),
                    ft.ChartAxisLabel(
                        value=6, label=ft.Text("60", size=14, color=ft.colors.WHITE)
                    ),
                ],
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=2,
                        label=ft.Text(
                            "2",
                            size=16,
                            color=ft.colors.with_opacity(0.8, ft.colors.WHITE),
                        ),
                    ),
                    ft.ChartAxisLabel(
                        value=6,
                        label=ft.Text(
                            "6",
                            size=16,
                            color=ft.colors.with_opacity(0.8, ft.colors.WHITE),
                        ),
                    ),
                    ft.ChartAxisLabel(
                        value=10,
                        label=ft.Text(
                            "10",
                            size=16,
                            color=ft.colors.with_opacity(0.8, ft.colors.WHITE),
                        ),
                    ),
                    ft.ChartAxisLabel(
                        value=14,
                        label=ft.Text(
                            "14",
                            size=16,
                            color=ft.colors.with_opacity(0.8, ft.colors.WHITE),
                        ),
                    ),
                ],
                labels_size=32,
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),
            min_y=0,
            max_y=6,
            min_x=0,
            max_x=15,
            expand=True,
        )
        
class GraphTwo(ft.Container):
    def __init__(self):
        super().__init__(**style_frame)
        self.content = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=40,
                            gradient=ft.LinearGradient(
                                [ft.colors.CYAN, ft.colors.BLUE], rotation=90
                            ),
                            tooltip="40.00",
                            border_radius=15,
                            width=20,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=1,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=48,
                            gradient=ft.LinearGradient(
                                [ft.colors.CYAN, ft.colors.BLUE], rotation=90
                            ),
                            tooltip="48.00",
                            border_radius=15,
                            width=20,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=2,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=34,
                            gradient=ft.LinearGradient(
                                [ft.colors.CYAN, ft.colors.BLUE], rotation=90
                            ),
                            tooltip="34.00",
                            border_radius=15,
                            width=20,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=3,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=68,
                            gradient=ft.LinearGradient(
                                [ft.colors.CYAN, ft.colors.BLUE], rotation=90
                            ),
                            tooltip="68.00",
                            border_radius=15,
                            width=20,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=4,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=80,
                            gradient=ft.LinearGradient(
                                [ft.colors.CYAN, ft.colors.BLUE], rotation=90
                            ),
                            tooltip="80.00",
                            border_radius=15,
                            width=20,
                        ),
                    ],
                ),
            ],
            border=ft.border.all(1, ft.colors.BLACK38),
            left_axis=ft.ChartAxis(
                labels_size=40,
                title=ft.Text(
                    "Traffic", color=ft.colors.WHITE
                ),  # Color blanco para el título del eje izquierdo
                title_size=40,
                labels=[
                    ft.ChartAxisLabel(
                        value=i, label=ft.Text(str(i), color=ft.colors.WHITE)
                    )
                    for i in range(0, 101, 20)
                ],  # Color blanco para las etiquetas del eje
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0,
                        label=ft.Container(
                            ft.Text("A", color=ft.colors.WHITE), padding=10
                        ),  # Color blanco
                    ),
                    ft.ChartAxisLabel(
                        value=1,
                        label=ft.Container(
                            ft.Text("B", color=ft.colors.WHITE), padding=10
                        ),  # Color blanco
                    ),
                    ft.ChartAxisLabel(
                        value=2,
                        label=ft.Container(
                            ft.Text("C", color=ft.colors.WHITE), padding=10
                        ),  # Color blanco
                    ),
                    ft.ChartAxisLabel(
                        value=3,
                        label=ft.Container(
                            ft.Text("D", color=ft.colors.WHITE), padding=10
                        ),  # Color blanco
                    ),
                    ft.ChartAxisLabel(
                        value=4,
                        label=ft.Container(
                            ft.Text("E", color=ft.colors.WHITE), padding=10
                        ),  # Color blanco
                    ),
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.BLACK38, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
            max_y=100,
            interactive=True,
            expand=True,
        )

class GraphThree(ft.Container):
    def __init__(self):
        super().__init__(**style_frame)
        self.normal_radius = 100  # Aumentado de 80 a 100
        self.hover_radius = 110  # Aumentado de 90 a 110
        self.normal_title_style = ft.TextStyle(
            size=18,  # Aumentado de 16 a 18
            color=ft.colors.BLACK54,
            weight=ft.FontWeight.BOLD,
        )
        self.hover_title_style = ft.TextStyle(
            size=18,  # Aumentado de 16 a 18
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK38),
        )
        self.normal_badge_size = 30  # Aumentado de 30 a 35

        self.content = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    60,
                    title="60%",
                    title_style=self.normal_title_style,
                    color=ft.colors.GREEN,
                    radius=self.normal_radius,
                    badge=self.badge(ft.icons.VIDEO_CALL, self.normal_badge_size),
                    badge_position=1.1,
                ),
                ft.PieChartSection(
                    15,
                    title="15%",
                    title_style=self.normal_title_style,
                    color=ft.colors.ORANGE,
                    radius=self.normal_radius,
                    badge=self.badge(ft.icons.FACEBOOK, self.normal_badge_size),
                    badge_position=1.1,
                ),
                ft.PieChartSection(
                    12,
                    title="12%",
                    title_style=self.normal_title_style,
                    color=ft.colors.CYAN,
                    radius=self.normal_radius,
                    badge=self.badge(ft.icons.WEB, self.normal_badge_size),
                    badge_position=1.1,
                ),
                ft.PieChartSection(
                    8,
                    title="8%",
                    title_style=self.normal_title_style,
                    color=ft.colors.BLUE,
                    radius=self.normal_radius,
                    badge=self.badge(ft.icons.GAMES, self.normal_badge_size),
                    badge_position=1.1,
                ),
                ft.PieChartSection(
                    5,
                    title="5%",
                    title_style=self.normal_title_style,
                    color=ft.colors.PURPLE,
                    radius=self.normal_radius,
                    badge=self.badge(ft.icons.MY_LIBRARY_MUSIC, self.normal_badge_size),
                    badge_position=1.1,
                ),
            ],
            sections_space=0.5,
            center_space_radius=0,
            on_chart_event=self.on_chart_event,
            expand=True,
        )

    def badge(self, icon, size):
        return ft.Container(
            ft.Icon(
                icon, color=ft.colors.BLACK, size=20
            ),  # Aumentado el tamaño del icono
            width=size,
            height=size,
            border=ft.border.all(1, ft.colors.BLACK38),
            border_radius=size / 2,
            bgcolor=ft.colors.WHITE,
        )

    def on_chart_event(self, event):
        for idx, section in enumerate(self.content.sections):
            if idx == event.section_index:
                section.radius = self.hover_radius
                section.title_style = self.hover_title_style
            else:
                section.radius = self.normal_radius
                section.title_style = self.normal_title_style
        self.content.update()

class GraphFour(ft.Container):
    def __init__(self):
        super().__init__(**style_frame)
        self.normal_border = ft.BorderSide(
            3,  # Aumentado el grosor del borde normal
            ft.colors.with_opacity(0.6, ft.colors.WHITE38),  # Aumentado la opacidad
        )
        self.hovered_border = ft.BorderSide(
            5, ft.colors.WHITE
        )  # Aumentado el grosor del borde al pasar el mouse
        self.normal_title_style = ft.TextStyle(
            size=18,  # Aumentado el tamaño del texto
            color=ft.colors.BLACK38,
            weight=ft.FontWeight.BOLD,
        )
        self.normal_radius = 60  # Aumentado el radio normal
        self.content = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    26,
                    title="26%",
                    title_style=self.normal_title_style,
                    color=ft.colors.YELLOW,
                    radius=self.normal_radius,
                    border_side=self.normal_border,
                ),
                ft.PieChartSection(
                    13,
                    title="13%",
                    title_style=self.normal_title_style,
                    color=ft.colors.GREEN,
                    radius=self.normal_radius,
                    border_side=self.normal_border,
                ),
                ft.PieChartSection(
                    6,
                    title="6%",
                    title_style=self.normal_title_style,
                    color=ft.colors.RED,
                    radius=self.normal_radius,
                    border_side=self.normal_border,
                ),
                ft.PieChartSection(
                    7,
                    title="7%",
                    title_style=self.normal_title_style,
                    color=ft.colors.BLUE,
                    radius=self.normal_radius,
                    border_side=self.normal_border,
                ),
                ft.PieChartSection(
                    48,
                    title="48%",
                    title_style=self.normal_title_style,
                    color=ft.colors.CYAN,
                    radius=self.normal_radius,
                    border_side=self.normal_border,
                ),
            ],
            sections_space=3,  # Aumentado el espacio entre secciones
            center_space_radius=50,  # Aumentado el radio del espacio central
            on_chart_event=self.on_chart_event,
            expand=True,
        )

    def on_chart_event(self, event: ft.PieChartEvent):
        for idx, section in enumerate(self.content.sections):
            if idx == event.section_index:
                section.radius = (
                    self.normal_radius + 10
                )  # Aumentado el radio al pasar el mouse
                section.border_side = self.hovered_border
            else:
                section.radius = self.normal_radius
                section.border_side = self.normal_border
        self.content.update()
