import reflex as rx

from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer
from ai_recom.components.product_card import product_card
from ai_recom.state import State


#@rx.page(route="/recommendations", on_load=State.get_recommendations)
def recommendations_page():

    return rx.box(

        # 🔹 NAVBAR
        navbar(),

        # 🔹 MAIN CONTENT
        rx.box(

            rx.vstack(

                # 🧠 TITLE + SUBTEXT
                rx.vstack(

                    rx.heading(
                        "Recommended For You",
                        size="7",
                        color="#0F1111"
                    ),

                    rx.cond(
                        State.user_type == "new",
                        rx.text(
                            "Top rated products ⭐",
                            color="gray"
                        ),
                        rx.text(
                            "Personalized recommendations based on your activity 🎯",
                            color="gray"
                        )
                    ),

                    align="start",
                    spacing="1",
                    width="100%"
                ),

                # 🛍️ PRODUCT GRID
                rx.cond(
                    State.recommended_products,

                    rx.grid(
                        rx.foreach(State.recommended_products, product_card),
                        columns="repeat(5, 1fr)",   # ✅ AMAZON GRID
                        gap="20px",
                        width="100%"
                    ),

                    rx.center(
                        rx.text(
                            "No recommendations available",
                            color="gray"
                        ),
                        padding="40px"
                    )
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