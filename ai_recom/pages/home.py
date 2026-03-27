import reflex as rx
from ai_recom.state import State
from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer
from ai_recom.components.chatbot import chatbot
from ai_recom.components.product_card import product_card


def home():
    return rx.box(

        navbar(),

        rx.box(
            rx.vstack(

                rx.heading(
                    "Discover Smart Shopping",
                    font_size="40px",
                    font_weight="bold",
                    color="white"
                ),

                rx.text(
                    "AI-powered recommendations tailored for you",
                    font_size="18px",
                    color="#cbd5f5"
                ),

                rx.button(
                    "Explore Products",
                    on_click=rx.redirect("/products"),
                    bg="#2563eb",
                    color="white",
                    border_radius="10px"
                ),

                spacing="4",
                align="center"
            ),

            height="60vh",
            display="flex",
            justify_content="center",
            align_items="center",
            background="linear-gradient(to right, #0f172a, #1e293b)",
            text_align="center"
        ),

        # RECOMMENDATIONS SECTION
        rx.box(
            rx.vstack(

                rx.heading(
                    "Recommended for You",
                    font_size="28px",
                    font_weight="bold",
                    color="#111"
                ),

                # IMPORTANT BUTTON
                rx.button(
                    "Load Recommendations",
                    on_click=State.get_recommendations,
                    bg="blue",
                    color="white"
                ),

                rx.cond(
                    State.recommended_products,

                    rx.grid(
                        rx.foreach(State.recommended_products, product_card),
                        columns="repeat(5, 1fr)",
                        gap="20px",
                        width="100%"
                    ),

                    rx.text("No recommendations available", color="gray")
                ),

                spacing="6",
                width="100%"
            ),

            padding="30px",
            background="#eaeded",
            min_height="100vh"
        ),

        chatbot(),
        footer()
    )