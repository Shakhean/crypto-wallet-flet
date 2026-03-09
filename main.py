import flet as ft
import requests

# Map currency codes to symbols
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "ZAR": "R",
    "NGN": "₦"

}

# Crypto colors for subtle styling
CRYPTO_COLORS = {
    "bitcoin": "#F7931A",
    "dogecoin": "#C3A634",
    "litecoin": "#345D9D"
}

# App color scheme
PRIMARY_BLUE = "#2872f9"
ACCENT_YELLOW = "#fed700"

# Default currency
DEFAULT_CURRENCY = "GBP"

def main(page: ft.Page):
    page.title = "Crypto Prices"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"

    # Column for coins
    coins_column = ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = "#FFFFFF"
            theme_icon.icon = ft.icons.DARK_MODE
            theme_icon.icon_color = PRIMARY_BLUE
            theme_icon.tooltip = "Switch to Dark Mode"
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = "#0F172A"
            theme_icon.icon = ft.icons.LIGHT_MODE
            theme_icon.icon_color = ACCENT_YELLOW
            theme_icon.tooltip = "Switch to Light Mode"
        
        # Update UI colors based on theme
        update_theme_colors()
        fetch_coins(currency_dropdown.value)
        page.update()

    def update_theme_colors():
        # Update header text color
        header.controls[0].color = "#FFFFFF" if page.theme_mode == ft.ThemeMode.DARK else "#0F172A"
        
        # Update currency dropdown colors
        currency_dropdown.bgcolor = "#1E293B" if page.theme_mode == ft.ThemeMode.DARK else "#F8FAFC"
        currency_dropdown.border_color = "#334155" if page.theme_mode == ft.ThemeMode.DARK else "#E2E8F0"
        currency_dropdown.color = "#FFFFFF" if page.theme_mode == ft.ThemeMode.DARK else "#0F172A"
        
        # Update currency label color
        currency_label.color = "#94A3B8" if page.theme_mode == ft.ThemeMode.DARK else "#475569"
        
        # Update refresh button color
        refresh_btn.icon_color = ACCENT_YELLOW if page.theme_mode == ft.ThemeMode.DARK else PRIMARY_BLUE
        
        # Update divider color
        divider.color = "#334155" if page.theme_mode == ft.ThemeMode.DARK else "#E2E8F0"

    def fetch_coins(currency_code_upper):
        currency_code = currency_code_upper.lower()
        
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": currency_code,
                "ids": "bitcoin,dogecoin,litecoin",
                "price_change_percentage": "24h"
            }
            
            response = requests.get(url, params=params, timeout=10)
            coins = response.json()
            
            # Update display
            coins_column.controls.clear()
            
            for coin in coins:
                # Get price change data
                price_change = coin.get("price_change_percentage_24h", 0)
                change_color = "#4CAF50" if price_change >= 0 else "#F44336"
                change_icon = "▲" if price_change >= 0 else "▼"
                
                # Get crypto color
                crypto_color = CRYPTO_COLORS.get(coin["id"], "#6366F1")
                
                # Theme-based colors
                if page.theme_mode == ft.ThemeMode.DARK:
                    card_bg = "#1E293B"
                    card_border = "#334155"
                    text_primary = "#FFFFFF"
                    text_secondary = "#94A3B8"
                    hover_bg = "#2D3A4F"
                else:
                    card_bg = "#F8FAFC"
                    card_border = "#E2E8F0"
                    text_primary = "#0F172A"
                    text_secondary = "#475569"
                    hover_bg = "#E2E8F0"
                
                # Create card with blue accent border
                card = ft.Container(
                    content=ft.Row(
                        controls=[
                            # Icon with colored background
                            ft.Container(
                                content=ft.Image(src=coin["image"], width=40, height=40),
                                padding=8,
                                border_radius=12,
                                bgcolor=ft.colors.with_opacity(0.2, crypto_color)
                            ),
                            
                            # Name and symbol
                            ft.Column(
                                controls=[
                                    ft.Text(coin["name"], size=18, weight="bold", color=text_primary),
                                    ft.Text(coin["symbol"].upper(), size=12, color=text_secondary),
                                ],
                                spacing=2,
                                expand=True
                            ),
                            
                            # Price and change
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"{CURRENCY_SYMBOLS[currency_code_upper]}{coin['current_price']:,}",
                                        size=18,
                                        weight="bold",
                                        color=text_primary
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Text(change_icon, color=change_color, size=12),
                                            ft.Text(f"{abs(price_change):.1f}%", color=change_color, size=12),
                                        ],
                                        spacing=2
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                spacing=2
                            )
                        ],
                        alignment="spaceBetween",
                        vertical_alignment="center",
                    ),
                    padding=15,
                    border_radius=15,
                    bgcolor=card_bg,
                    border=ft.border.all(2, PRIMARY_BLUE),  # Blue border on cards
                    animate=ft.animation.Animation(200, "easeInOut")
                )
                
                # Simple hover effect with yellow accent
                def on_hover(e, card=card, hover_bg=hover_bg, card_bg=card_bg):
                    if e.data == "true":
                        card.bgcolor = hover_bg
                        card.border = ft.border.all(2, ACCENT_YELLOW)  # Yellow border on hover
                    else:
                        card.bgcolor = card_bg
                        card.border = ft.border.all(2, PRIMARY_BLUE)  # Back to blue
                    card.update()
                
                card.on_hover = on_hover
                coins_column.controls.append(card)
            
            page.update()
            
        except Exception as e:
            print(f"Error: {e}")

    # Theme toggle button
    theme_icon = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        icon_color=ACCENT_YELLOW,
        on_click=toggle_theme,
        tooltip="Switch to Light Mode"
    )

    # Refresh button
    refresh_btn = ft.IconButton(
        icon=ft.icons.REFRESH,
        icon_color=ACCENT_YELLOW,
        on_click=lambda _: fetch_coins(currency_dropdown.value),
        tooltip="Refresh"
    )

    # Currency dropdown
    currency_dropdown = ft.Dropdown(
        width=150,
        options=[ft.dropdown.Option(code) for code in CURRENCY_SYMBOLS.keys()],
        value=DEFAULT_CURRENCY,
        on_change=lambda e: fetch_coins(e.control.value),
        bgcolor="#1E293B",
        border_color=PRIMARY_BLUE,  # Blue border
        color="#FFFFFF",
        focused_border_color=ACCENT_YELLOW,  # Yellow when focused
    )

    # Currency label
    currency_label = ft.Text("Currency:", color="#94A3B8")

    # Header with title and controls
    header = ft.Row(
        controls=[
            ft.Text(
                "Crypto Prices", 
                size=28, 
                weight="bold", 
                color="#FFFFFF",
                spans=[
                    ft.TextSpan(
                        " ₿",
                        style=ft.TextStyle(color=ACCENT_YELLOW, size=32)
                    )
                ]
            ),
            ft.Row(
                controls=[theme_icon, refresh_btn],
                spacing=5
            )
        ],
        alignment="spaceBetween"
    )

    # Currency selector row
    currency_row = ft.Row(
        controls=[currency_label, currency_dropdown],
        spacing=10
    )

    # Divider
    divider = ft.Divider(height=20, color="#334155")

    # Initial fetch
    fetch_coins(DEFAULT_CURRENCY)

    # Add everything to page
    page.add(
        header,
        currency_row,
        divider,
        coins_column
    )

ft.app(target=main)