import reflex as rx
from ai_recom.state import State
from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer
from ai_recom.components.product_card import product_card


# @rx.page(route="/wishlist")
def wishlist_page():

    return rx.box(

        # 🔹 NAVBAR
        navbar(),

        # 🔹 MAIN CONTENT
        rx.box(

            rx.vstack(

                rx.heading(
                    "Your Wishlist ❤️",
                    size="7",
                    color="#0F1111"
                ),

                rx.cond(
                    State.wishlist,

                    # 🛍️ GRID
                    rx.grid(
                        rx.foreach(State.wishlist, product_card),
                        columns="repeat(5, 1fr)",
                        gap="20px",
                        width="100%"
                    ),

                    # EMPTY STATE
                    rx.center(
                        rx.text(
                            "Your wishlist is empty",
                            color="gray"
                        ),
                        padding="50px"
                    )
                ),

                spacing="6",
                width="100%"
            ),

            background="#eaeded",
            padding="20px",
            min_height="100vh"
        ),

        # 🔹 FOOTER
        footer()
    )