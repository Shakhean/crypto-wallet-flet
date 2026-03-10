import flet as ft

# ==================== CONSTANTS ====================

# Map currency codes to symbols
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
}

# Default currency
DEFAULT_CURRENCY = "USD"

# ==================== ACTION BUTTONS ====================
def create_action_buttons():
    """Create the Deposit, Earn, Withdraw buttons"""
    
    def make_button(text):
        return ft.ElevatedButton(
            text=text,
            on_click=lambda e: print(f"{text} pressed")
        )

    return ft.Row(
        controls=[
            make_button("Deposit"),
            make_button("Earn"),
            make_button("Withdraw"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

# ==================== CRYPTO PRICES ====================
def create_crypto_prices(page):
    """Create the crypto prices section with images"""
    
    # Sample data (no API calls)
    coins_data = [
        {"name": "Bitcoin", "symbol": "BTC", "price": 50000, "change": 2.5, "image": "bitcoin.png"},
        {"name": "Dogecoin", "symbol": "DOGE", "price": 0.12, "change": -1.2, "image": "dogecoin.png"},
        {"name": "Litecoin", "symbol": "LTC", "price": 80, "change": 0.8, "image": "litecoin.png"},
    ]
    
    # Title
    title = ft.Text("Crypto Prices", size=20)
    
    # Currency dropdown
    currency_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(code) for code in CURRENCY_SYMBOLS.keys()],
        value=DEFAULT_CURRENCY,
        width=150
    )
    
    # Container for coin list
    coins_container = ft.Column(spacing=10)
    
    # Function to update prices based on currency
    def update_prices(currency):
        coins_container.controls.clear()
        
        # Conversion rates (simple example)
        rates = {"USD": 1, "EUR": 0.92, "GBP": 0.78}
        rate = rates.get(currency, 1)
        symbol = CURRENCY_SYMBOLS.get(currency, "$")
        
        for coin in coins_data:
            converted_price = coin["price"] * rate
            
            # Create a row for each coin
            coin_row = ft.Row(
                controls=[
                    # Coin image (placeholder text if image not found)
                    ft.Container(
                        content=ft.Text(coin["symbol"][0], size=20),
                        width=40,
                        height=40,
                        bgcolor=ft.colors.GREY_300,
                        border_radius=20,
                        alignment=ft.alignment.center
                    ),
                    # Coin name and symbol
                    ft.Text(
                        f"{coin['name']} ({coin['symbol']})",
                        weight=ft.FontWeight.BOLD,
                        expand=True
                    ),
                    # Price
                    ft.Text(
                        f"{symbol}{converted_price:.2f}",
                        weight=ft.FontWeight.BOLD
                    ),
                    # 24h change
                    ft.Text(
                        f"{coin['change']:+.2f}%",
                        color=ft.colors.GREEN if coin['change'] >= 0 else ft.colors.RED,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
            
            coins_container.controls.append(coin_row)
            coins_container.controls.append(ft.Divider(height=1))
        
        # Remove last divider
        if coins_container.controls and isinstance(coins_container.controls[-1], ft.Divider):
            coins_container.controls.pop()
        
        page.update()
    
    # Dropdown change handler
    def on_currency_change(e):
        update_prices(currency_dropdown.value)
    
    currency_dropdown.on_change = on_currency_change
    
    # Initial update
    update_prices(DEFAULT_CURRENCY)
    
    # Return the complete crypto section
    return ft.Column(
        controls=[
            title,
            ft.Row([ft.Text("Select Currency:"), currency_dropdown]),
            ft.Divider(),
            coins_container,
        ],
        spacing=15,
    )

# ==================== MAIN APP ====================
def main(page: ft.Page):
    # Page setup
    page.title = "Crypto Wallet"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20
    
    # App title
    app_title = ft.Text("Crypto Wallet", size=30)
    
    # Create buttons (above)
    action_buttons = create_action_buttons()
    
    # Create crypto prices with images (below)
    crypto_prices = create_crypto_prices(page)
    
    # Arrange everything in a column (buttons on top, coins below)
    content = ft.Column(
        controls=[
            app_title,
            ft.Divider(),
            action_buttons,
            ft.Divider(),
            crypto_prices,
        ],
        spacing=20,
    )
    
    # Add to page
    page.add(content)
    page.update()

# ==================== RUN APP ====================
if __name__ == "__main__":
    ft.app(target=main)
