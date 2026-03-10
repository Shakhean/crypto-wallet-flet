import flet as ft

def main(page: ft.Page):
    # Function to handle button clicks
    def handle_click(text):
        def _handle(e):
            print(f"{text} pressed")
        return _handle
    
    page.title = "My App"
    
    # Add a simple column with text and buttons
    page.add(
        ft.Column(
            [
                ft.Text("Welcome to My App"),
                ft.Row(
                    [
                        ft.ElevatedButton("Deposite", on_click=handle_click("Deposite")),
                        ft.ElevatedButton("Earn", on_click=handle_click("Earn")),
                        ft.ElevatedButton("Withdraw", on_click=handle_click("Withdraw")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)
