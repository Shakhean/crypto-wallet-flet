import flet as ft
import httpx

# --------------------------
# Config
# --------------------------
CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "ZAR": "R", "NGN": "₦",
    "KES": "KSh", "GHS": "₵", "EGP": "E£", "MAD": "DH"
}

COIN_IMAGES = {
    "bitcoin": "bitcoin.png",
    "dogecoin": "dogecoin.png",
    "litecoin": "litecoin.png"
}

COINS = {
    "bitcoin": 1,
    "dogecoin": 74,
    "litecoin": 2
}

CMC_API_KEY = "46d91bb1-c3e0-48c6-930a-d83c8d41f791"
DEFAULT_CURRENCY = "USD"

# --------------------------
# Buttons component
# --------------------------
def create_buttons():
    def handle_click(text):
        def _handle(e):
            print(f"{text} pressed")
        return _handle

    return ft.Row(
        [
            ft.ElevatedButton("Deposite", on_click=handle_click("Deposite")),
            ft.ElevatedButton("Earn", on_click=handle_click("Earn")),
            ft.ElevatedButton("Withdraw", on_click=handle_click("Withdraw")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

# --------------------------
# Coinlist component
# --------------------------
def create_coinlist(page: ft.Page, currency_code: str):
    coins_column = ft.Column(spacing=15)

    async def fetch_coins(currency_code_upper):
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
        currency_code = currency_code_upper.upper()

        try:
            # 1️⃣ Get USD prices from CoinMarketCap
            ids = ",".join(str(v) for v in COINS.values())
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
            params = {"id": ids, "convert": "USD"}

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url, headers=headers, params=params)
                data = response.json().get("data", {})

                # 2️⃣ Get conversion rate if currency is not USD
                if currency_code != "USD":
                    conv_response = await client.get("https://open.er-api.com/v6/latest/USD")
                    conv_data = conv_response.json().get("rates", {})
                    rate = conv_data.get(currency_code, 1)
                else:
                    rate = 1

            coins_column.controls.clear()

            for coin_name, coin_id in COINS.items():
                coin_data = data.get(str(coin_id), {})
                quote = coin_data.get("quote", {}).get("USD", {})
                price_usd = quote.get("price", 0)
                change_24h = quote.get("percent_change_24h", 0)
                price = price_usd * rate
                symbol = coin_data.get("symbol", "").upper()

                change_color = "#4CAF50" if change_24h >= 0 else "#F44336"
                change_icon = "▲" if change_24h >= 0 else "▼"

                card = ft.Container(
                    padding=15,
                    border_radius=15,
                    content=ft.Row(
                        [
                            ft.Image(src=COIN_IMAGES[coin_name], width=40, height=40),
                            ft.Column(
                                [
                                    ft.Text(coin_name.capitalize(), size=18, weight="bold"),
                                    ft.Text(symbol, size=12)
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.Column(
                                [
                                    ft.Text(f"{CURRENCY_SYMBOLS.get(currency_code,'')}{price:,.2f}", size=18, weight="bold"),
                                    ft.Row(
                                        [
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
                    )
                )

                coins_column.controls.append(card)

            page.update()

        except Exception as e:
            coins_column.controls.clear()
            coins_column.controls.append(ft.Text(f"Error fetching prices: {e}", color="#F44336"))
            page.update()

    # Schedule first fetch
    page.run_task(fetch_coins, currency_code)

    return coins_column, fetch_coins

# --------------------------
# Main app
# --------------------------
def main(page: ft.Page):
    page.title = "Crypto Wallet App"

    # Buttons
    buttons = create_buttons()

    # Dropdown for currency selection
    currency_dropdown = ft.Dropdown(
        width=150,
        options=[ft.dropdown.Option(code) for code in CURRENCY_SYMBOLS.keys()],
        value=DEFAULT_CURRENCY
    )

    # Coinlist
    coins_column, fetch_coins = create_coinlist(page, DEFAULT_CURRENCY)

    # Update coinlist when dropdown changes
    def on_currency_change(e):
        page.run_task(fetch_coins, e.control.value)

    currency_dropdown.on_change = on_currency_change

    # Layout
    page.add(
        ft.Column(
            [
                buttons,
                ft.Row([ft.Text("Select Currency:"), currency_dropdown], spacing=10),
                ft.Divider(height=20),
                coins_column
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        )
    )

ft.app(target=main)
