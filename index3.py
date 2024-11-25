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
                            width=800,  # Tamaño fijo en lugar de float("inf")
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
                                            margin=ft.margin.only(left=100, right=100),
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
