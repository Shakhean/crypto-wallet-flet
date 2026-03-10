import flet as ft

PRIMARY_BLUE = "#2872f9"
ACCENT_YELLOW = "#fed700"

def create_action_buttons(page):
    def make_3d_button(text, bg_color, text_color, url=None):
        def handle_click(e):
            if url:
                page.launch_url(url)  # Flet's built-in URL launcher
            else:
                print(f"{text} pressed")

        container = ft.Container(
            content=ft.Text(text, color=text_color, weight=ft.FontWeight.BOLD),
            padding=ft.padding.symmetric(horizontal=25, vertical=12),
            border_radius=12,
            bgcolor=bg_color,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                offset=ft.Offset(4, 4),
                color=ft.colors.with_opacity(0.4, "black"),
            ),
            on_click=handle_click,
            animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_IN_OUT)
        )

        # Hover effect
        def on_hover(e):
            if e.data == "true":
                container.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,
                    offset=ft.Offset(6, 6),
                    color=ft.colors.with_opacity(0.6, "black"),
                )
            else:
                container.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    offset=ft.Offset(4, 4),
                    color=ft.colors.with_opacity(0.4, "black"),
                )
            container.update()

        container.on_hover = on_hover
        return container

    button_row = ft.Row(
        controls=[
            make_3d_button("Buy", PRIMARY_BLUE, "white", "https://www.moonpay.com/buy"),
            make_3d_button("Earn", ACCENT_YELLOW, "black"),
            make_3d_button("Sell", PRIMARY_BLUE, "white"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    return button_row

def main(page: ft.Page):
    page.title = "My App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    page.add(
        ft.Column(
            controls=[
                ft.Text("Welcome to My App", size=30, weight=ft.FontWeight.BOLD),
                create_action_buttons(page),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30
        )
    )

ft.app(target=main)
