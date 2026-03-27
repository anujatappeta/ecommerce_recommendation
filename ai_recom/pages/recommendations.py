import reflex as rx

from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer
from ai_recom.components.product_card import product_card
from ai_recom.state import State


def recommendations_page():

    return rx.box(

        # 🔹 NAVBAR
        navbar(),

        # 🔹 MAIN CONTENT
        rx.box(

            rx.vstack(

                # 🧠 TITLE
                rx.heading(
                    "Recommended For You",
                    size="7",
                    color="#0F1111"
                ),

                # 🧠 DYNAMIC MESSAGE
                rx.cond(
                    State.user_type == "new",
                    rx.text(
                        "Top rated products for you ⭐ (Cold Start)",
                        color="gray"
                    ),
                    rx.text(
                        "Personalized recommendations (Hybrid: Content + Collaborative) 🎯",
                        color="gray"
                    )
                ),

                # ✅ BUTTON (IMPORTANT)
                rx.button(
                    "Get Recommendations",
                    on_click=State.get_recommendations,
                    bg="blue",
                    color="white"
                ),

                # 🛍️ PRODUCT GRID
                rx.cond(
                    State.recommended_products,

                    rx.grid(
                        rx.foreach(State.recommended_products, product_card),
                        columns="repeat(5, 1fr)",
                        gap="20px",
                        width="100%"
                    ),

                    rx.center(
                        rx.text(
                            "Click 'Get Recommendations' to see results",
                            color="gray"
                        ),
                        padding="40px"
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