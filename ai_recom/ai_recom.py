import reflex as rx

from ai_recom.pages.home import home
from ai_recom.pages.products import products_page
from ai_recom.pages.recommendations import recommendations_page
from ai_recom.pages.login import login_page
from ai_recom.pages.signup import signup_page
from ai_recom.pages.cart import cart_page
from ai_recom.pages.product_details import product_detail_page
from ai_recom.pages.checkout import checkout_page
from ai_recom.pages.payment import payment_page
from ai_recom.pages.profile import profile_page
from ai_recom.pages.wishlist import wishlist_page
from ai_recom.pages.orders import orders_page

app = rx.App()

# Signup
app.add_page(signup_page, route="/signup")

# Home 
app.add_page(
    home,
    route="/home"
)

# Login
app.add_page(
    login_page,
    route="/"
)

# Products 
app.add_page(
    products_page,
    route="/products"
)

# Recommendations 
app.add_page(
    recommendations_page,
    route="/recommendations"
)

# Other pages
app.add_page(cart_page, route="/cart")
app.add_page(wishlist_page, route="/wishlist")
app.add_page(orders_page, route="/orders")
app.add_page(profile_page, route="/profile")
app.add_page(checkout_page, route="/checkout")
app.add_page(payment_page, route="/payment")
app.add_page(product_detail_page, route="/product")