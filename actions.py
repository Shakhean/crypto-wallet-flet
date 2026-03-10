import flet as ft

def main(page: ft.Page):
    def handle_click(text, url=None):
        def _handle(e):
            if url:
                page.launch_url(url)
            else:
                print(f"{text} pressed")
        return _handle
    
    page.title = "My App"
    
    page.add(
        ft.Column([
            ft.Text("Welcome to My App"),
            ft.Row([
                ft.ElevatedButton("Buy", on_click=handle_click("Buy", "https://www.moonpay.com/buy")),
                ft.ElevatedButton("Earn", on_click=handle_click("Earn")),
                ft.ElevatedButton("Sell", on_click=handle_click("Sell")),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
