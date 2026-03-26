import reflex as rx
from ai_recom.state import State
from ai_recom.components.product_card import product_card
from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer


# @rx.page(route="/products", on_load=State.load_home_products)
def products_page():

    return rx.box(

        # 🔹 NAVBAR
        navbar(),

        # 🔹 MAIN CONTENT (AMAZON STYLE)
        rx.box(

            rx.vstack(

                # 🔍 SEARCH BAR (BETTER UI)
                rx.hstack(
                    rx.input(
                        placeholder="Search for products...",
                        value=State.search_query,
                        on_change=State.set_search,
                        width="400px",
                        bg="white",
                        color="black",
                        border_radius="4px"
                    ),

                    rx.button(
                        "Search",
                        on_click=State.search_products,
                        bg="#febd69",
                        color="black"
                    ),

                    spacing="2"
                ),

                # 🛍️ PRODUCT GRID (IMPROVED)
                rx.grid(
                    rx.foreach(State.products, product_card),
                    columns="repeat(5, 1fr)",   # ✅ AMAZON STYLE GRID
                    gap="20px",
                    width="100%"
                ),

                spacing="6",
                width="100%"
            ),

            background="#eaeded",   # ✅ AMAZON BACKGROUND
            padding="20px",
            min_height="100vh"
        ),

        # 🔹 FOOTER
        footer()
    )