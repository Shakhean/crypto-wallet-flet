import flet as ft
import httpx

# ==================== CONSTANTS ====================

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

# Default currency
DEFAULT_CURRENCY = "USD"

# CoinMarketCap API key
CMC_API_KEY = "46d91bb1-c3e0-48c6-930a-d83c8d41f791"

# Coins to track (CMC IDs) with their image filenames
COINS = {
    "bitcoin": {"id": 1, "image": "bitcoin.png"},
    "dogecoin": {"id": 74, "image": "dogecoin.png"},
    "litecoin": {"id": 2, "image": "litecoin.png"}
}

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
    
    # Store USD prices globally
    usd_prices = {}
    exchange_rates = {}
    
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
    
    # Loading message
    coins_container.controls.append(ft.Text("Loading prices..."))
    
    # Function to fetch USD prices from CoinMarketCap
    def fetch_usd_prices():
        nonlocal usd_prices
        try:
            headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
            ids = ",".join(str(coin["id"]) for coin in COINS.values())
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
            
            response = httpx.get(
                url,
                headers=headers,
                params={"id": ids, "convert": "USD"},
                timeout=10
            )
            data = response.json().get("data", {})
            
            # Process USD prices
            for coin_name, coin_info in COINS.items():
                coin_data = data.get(str(coin_info["id"]), {})
                quote = coin_data.get("quote", {}).get("USD", {})
                usd_prices[coin_name] = {
                    "price": quote.get("price", 0),
                    "change_24h": quote.get("percent_change_24h", 0),
                    "symbol": coin_data.get("symbol", "").upper(),
                    "image": coin_info["image"]
                }
            return True
        except Exception as e:
            print(f"Error fetching USD prices: {e}")
            return False
    
    # Function to fetch exchange rates
    def fetch_exchange_rates():
        nonlocal exchange_rates
        try:
            url = "https://open.er-api.com/v6/latest/USD"
            response = httpx.get(url, timeout=10)
            data = response.json()
            exchange_rates = data.get("rates", {})
            return True
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return False
    
    # Function to display prices in selected currency
    def display_prices(target_currency):
        if not usd_prices:
            coins_container.controls.clear()
            coins_container.controls.append(ft.Text("No price data available"))
            page.update()
            return
        
        # Update display
        coins_container.controls.clear()
        
        for coin_name, data in usd_prices.items():
            # Convert price if currency is not USD
            if target_currency != "USD" and target_currency in exchange_rates:
                rate = exchange_rates[target_currency]
                converted_price = data["price"] * rate
                price_symbol = CURRENCY_SYMBOLS.get(target_currency, '$')
                price_text = f"{price_symbol}{converted_price:.2f}"
            else:
                price_text = f"${data['price']:.2f}"
            
            # Create a row for each coin with image and text
            coin_row = ft.Row(
                controls=[
                    # Coin image
                    ft.Image(
                        src=data["image"],
                        width=40,
                        height=40,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    # Coin name and symbol
                    ft.Text(
                        f"{coin_name.capitalize()} ({data['symbol']})",
                        weight=ft.FontWeight.BOLD,
                        expand=True
                    ),
                    # Price
                    ft.Text(
                        price_text,
                        weight=ft.FontWeight.BOLD
                    ),
                    # 24h change
                    ft.Text(
                        f"{data['change_24h']:+.2f}%",
                        color=ft.colors.GREEN if data['change_24h'] >= 0 else ft.colors.RED,
                        weight=ft.FontWeight.BOLD
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
            
            # Add the coin row
            coins_container.controls.append(coin_row)
            coins_container.controls.append(ft.Divider(height=1))
        
        # Remove the last divider
        if coins_container.controls and isinstance(coins_container.controls[-1], ft.Divider):
            coins_container.controls.pop()
        
        page.update()
    
    # Initial load function
    def load_initial_data():
        # Show loading
        coins_container.controls.clear()
        coins_container.controls.append(ft.Text("Loading prices..."))
        page.update()
        
        # Fetch USD prices
        if fetch_usd_prices():
            # Fetch exchange rates
            fetch_exchange_rates()
            # Display in default currency
            display_prices(DEFAULT_CURRENCY)
        else:
            coins_container.controls.clear()
            coins_container.controls.append(ft.Text("Failed to load prices"))
            page.update()
    
    # Dropdown change handler
    def on_currency_change(e):
        display_prices(currency_dropdown.value)
    
    currency_dropdown.on_change = on_currency_change
    
    # Load initial data
    load_initial_data()
    
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
