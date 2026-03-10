import flet as ft
from actions import create_action_buttons

def main(page: ft.Page):
    page.title = "Crypto Wallet App"
    page.padding = 20
    page.bgcolor = "#0F172A"

    # Add the action buttons at the top
    action_buttons = create_action_buttons()
    
    # You can add more content below later
    page.add(action_buttons)

ft.app(target=main)
