import flet as ft

PRIMARY_BLUE = "#2872f9"
ACCENT_YELLOW = "#fed700"

def create_action_buttons():
    def make_3d_button(text, bg_color, text_color, on_click):
        container = ft.Container(
            content=ft.Text(text, color=text_color, weight="bold"),
            padding=ft.padding.symmetric(horizontal=25, vertical=12),
            border_radius=12,
            bgcolor=bg_color,
            shadow=ft.BoxShadow(
                color="rgba(0,0,0,0.4)",
                offset=ft.Offset(4, 4),
                blur_radius=8
            ),
            on_click=on_click,
            animate=ft.animation.Animation(150, "easeInOut")
        )

        # Hover effect
        def on_hover(e):
            if e.data == "true":
                container.shadow = ft.BoxShadow(
                    color="rgba(0,0,0,0.6)",
                    offset=ft.Offset(6, 6),
                    blur_radius=12
                )
            else:
                container.shadow = ft.BoxShadow(
                    color="rgba(0,0,0,0.4)",
                    offset=ft.Offset(4, 4),
                    blur_radius=8
                )
            container.update()

        container.on_hover = on_hover
        return container

    button_row = ft.Row(
        controls=[
            make_3d_button("Buy", PRIMARY_BLUE, "white", lambda e: print("Buy pressed")),
            make_3d_button("Earn", ACCENT_YELLOW, "black", lambda e: print("Sell pressed")),
            make_3d_button("Sell", PRIMARY_BLUE, "white", lambda e: print("Earn pressed")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    return button_row