import reflex as rx
from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer
from ai_recom.state import State


@rx.page(route="/product-details")
def product_detail_page():

    return rx.box(

        navbar(),

        rx.box(

            rx.cond(
                State.selected_product,   # ✅ FIXED

                rx.hstack(

                    # IMAGE
                    rx.image(
                        src=State.selected_product.get(
                            "ImageURL",
                            "https://via.placeholder.com/200"
                        ),
                        width="300px",
                        height="300px",
                        object_fit="contain",
                        background="white",
                        border_radius="10px"
                    ),

                    # DETAILS
                    rx.vstack(

                        rx.text(
                            State.selected_product.get("Name", "No Name"),
                            font_size="22px",
                            font_weight="bold"
                        ),

                        rx.text(
                            f"₹{State.selected_product.get('Price', 'N/A')}",
                            font_size="20px",
                            color="green"
                        ),

                        rx.text(
                            State.selected_product.get(
                                "Description",
                                "No description available"
                            ),
                            color="gray"
                        ),

                        rx.button(
                            "Add to Cart",
                            on_click=lambda: State.add_to_cart(State.selected_product),
                            width="200px"
                        ),

                        spacing="4",
                        align="start"
                    ),

                    spacing="8"
                ),

                rx.text("No product selected")
            ),

            padding="40px",
            max_width="1000px",
            margin="0 auto"
        ),

        footer()
    )