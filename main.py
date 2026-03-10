import flet as ft
import asyncio
import httpx

# Map currency codes to symbols
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "ZAR": "R",
    "NGN": "₦",
    "KES": "KSh",
    "GHS": "₵",
    "EGP": "E£",
    "MAD": "DH"
}

# Crypto colors (used for card accent)
CRYPTO_COLORS = {
    "bitcoin": "#F7931A",
    "dogecoin": "#C3A634",
    "litecoin": "#345D9D"
}

# Local images for each coin
COIN_IMAGES = {
    "bitcoin": "bitcoin.png",
    "dogecoin": "dogecoin.png",
    "litecoin": "litecoin.png"
}

# Default currency
DEFAULT_CURRENCY = "USD"

# CoinMarketCap API key
CMC_API_KEY = "46d91bb1-c3e0-48c6-930a-d83c8d41f791"  # replace with your API key

# Coins to track (CMC IDs)
COINS = {
    "bitcoin": 1,
    "dogecoin": 74,
    "litecoin": 2
}

# App colors
PRIMARY_BLUE = "#2872f9"
ACCENT_YELLOW = "#fed700"

def main(page: ft.Page):
    page.title = "Crypto Prices"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"

    coins_column = ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Initially add empty column so UI renders immediately
    page.add(
        ft.Row([ft.Text("Crypto Prices", size=28, weight="bold", color="#FFFFFF")]),
        coins_column
    )

    # Theme toggle
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = "#FFFFFF"
            theme_icon.icon = ft.icons.DARK_MODE
            theme_icon.icon_color = PRIMARY_BLUE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = "#0F172A"
            theme_icon.icon = ft.icons.LIGHT_MODE
            theme_icon.icon_color = ACCENT_YELLOW
        page.update()
        asyncio.create_task(fetch_coins(currency_dropdown.value))

    # Async fetch prices
    async def fetch_coins(currency_code_upper):
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
        currency_code = currency_code_upper.upper()
        try:
            ids = ",".join(str(v) for v in COINS.values())
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
            params = {"id": ids, "convert": currency_code}

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url, headers=headers, params=params)
                data = response.json().get("data", {})

            coins_column.controls.clear()

            for coin_name, coin_id in COINS.items():
                coin_data = data.get(str(coin_id), {})
                quote = coin_data.get("quote", {}).get(currency_code, {})
                price = quote.get("price", 0)
                change_24h = quote.get("percent_change_24h", 0)
                symbol = coin_data.get("symbol", "").upper()

                change_color = "#4CAF50" if change_24h >= 0 else "#F44336"
                change_icon = "▲" if change_24h >= 0 else "▼"
                crypto_color = CRYPTO_COLORS.get(coin_name, "#6366F1")

                card_bg = "#1E293B" if page.theme_mode == ft.ThemeMode.DARK else "#F8FAFC"
                text_primary = "#FFFFFF" if page.theme_mode == ft.ThemeMode.DARK else "#0F172A"
                text_secondary = "#94A3B8" if page.theme_mode == ft.ThemeMode.DARK else "#475569"
                hover_bg = "#2D3A4F" if page.theme_mode == ft.ThemeMode.DARK else "#E2E8F0"

                card = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Image(src=COIN_IMAGES[coin_name], width=40, height=40),
                            ft.Column(
                                controls=[
                                    ft.Text(coin_name.capitalize(), size=18, weight="bold", color=text_primary),
                                    ft.Text(symbol, size=12, color=text_secondary)
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(f"{CURRENCY_SYMBOLS[currency_code_upper]}{price:,.2f}", size=18, weight="bold", color=text_primary),
                                    ft.Row(
                                        controls=[
                                            ft.Text(change_icon, color=change_color, size=12),
                                            ft.Text(f"{abs(change_24h):.2f}%", color=change_color, size=12)
                                        ],
                                        spacing=2
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                spacing=2
                            )
                        ],
                        alignment="spaceBetween",
                        vertical_alignment="center"
                    ),
                    padding=15,
                    border_radius=15,
                    bgcolor=card_bg,
                    border=ft.border.all(2, PRIMARY_BLUE),
                    animate=ft.animation.Animation(200, "easeInOut")
                )

                def on_hover(e, card=card, hover_bg=hover_bg, card_bg=card_bg):
                    card.bgcolor = hover_bg if e.data == "true" else card_bg
                    card.update()

                card.on_hover = on_hover
                coins_column.controls.append(card)

            page.update()

        except Exception as e:
            coins_column.controls.clear()
            coins_column.controls.append(ft.Text(f"Error fetching prices: {e}", color="#F44336"))
            page.update()

    # Theme toggle button
    theme_icon = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        icon_color=ACCENT_YELLOW,
        on_click=toggle_theme,
        tooltip="Switch Theme"
    )

    # Currency dropdown
    currency_dropdown = ft.Dropdown(
        width=150,
        options=[ft.dropdown.Option(code) for code in CURRENCY_SYMBOLS.keys()],
        value=DEFAULT_CURRENCY,
        on_change=lambda e: asyncio.create_task(fetch_coins(e.control.value)),
        bgcolor="#1E293B",
        border_color=PRIMARY_BLUE,
        color="#FFFFFF",
        focused_border_color=ACCENT_YELLOW
    )

    # Header row with theme and currency
    header_row = ft.Row(
        controls=[ft.Text("Crypto Prices", size=28, weight="bold", color="#FFFFFF"), ft.Row([theme_icon], spacing=5)],
        alignment="spaceBetween"
    )

    currency_row = ft.Row(
        controls=[ft.Text("Select Currency:", color="#94A3B8"), currency_dropdown],
        spacing=10
    )

    page.controls.clear()
    page.add(header_row, currency_row, ft.Divider(height=20, color="#334155"), coins_column)

    # Initial fetch
    asyncio.create_task(fetch_coins(DEFAULT_CURRENCY))

ft.app(target=main)
