import reflex as rx
from ai_recom.state import State
from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer


# SINGLE CART ITEM
def cart_item(product):
    return rx.box(

        rx.hstack(

            # IMAGE
            rx.image(
                src=product.get("ImageURL", "/no_image.png"),
                height="80px",
                width="80px",
                object_fit="contain",
                border_radius="8px",
            ),

            # DETAILS
            rx.vstack(

                rx.text(
                    product.get("Name", "No Name"),
                    font_weight="bold",
                    no_of_lines=2,
                    color="#111",
                ),

                rx.text(
                    f"₹{product.get('Price', 'N/A')}",
                    color="#B12704",
                    font_weight="bold",
                ),

                # QUANTITY CONTROLS
                rx.hstack(

                    rx.button(
                        "-",
                        on_click=lambda: State.remove_from_cart(
                            product.get("ProductID")
                        ),
                        size="2"
                    ),

                    rx.text(
                        f"{product.get('quantity', 1)}",
                        font_weight="bold",
                        font_size="16px"
                    ),

                    rx.button(
                        "+",
                        on_click=lambda: State.add_to_cart(product),
                        size="2"
                    ),

                    spacing="3",
                    align="center"
                ),

                # ACTIONS
                rx.hstack(
                    rx.text(
                        "Delete",
                        color="#007185",
                        cursor="pointer",
                        font_size="14px",
                        _hover={"text_decoration": "underline"},
                        on_click=lambda: State.remove_from_cart(
                            product.get("ProductID")
                        ),
                    ),

                    rx.text("|", color="gray"),

                    rx.text(
                        "Save for later",
                        color="#007185",
                        cursor="pointer",
                        font_size="14px",
                        _hover={"text_decoration": "underline"},
                        on_click=lambda: State.save_for_later(product),
                    ),

                    spacing="2",
                ),

                align="start",
                spacing="2",
                width="100%",
            ),

            spacing="4",
            width="100%",
        ),

        padding="12px",
        border_bottom="1px solid #E7E7E7",
        width="100%",
    )


# CART PAGE
def cart_page():

    return rx.box(

        # NAVBAR
        navbar(),

        rx.box(

            rx.hstack(

                # LEFT SIDE (CART ITEMS)
                rx.box(
                    rx.vstack(

                        rx.heading("Your Cart", size="7", color="#111"),

                        rx.cond(
                            State.cart,

                            rx.vstack(
                                rx.foreach(State.cart, cart_item),
                                spacing="4",
                            ),

                            rx.text("Your cart is empty", color="gray"),
                        ),

                        spacing="5",
                    ),
                    width="65%",
                    padding="20px",
                ),

                # RIGHT SIDE (SUMMARY)
                rx.box(
                    rx.vstack(

                        rx.heading("Order Summary", size="6", color="#111"),

                        rx.hstack(
                            rx.text("Total", color="#333"),
                            rx.spacer(),
                            rx.text(
                                f"₹{State.total_price}",
                                font_weight="bold",
                                color="#111",
                            ),
                        ),

                        rx.button(
                            "Proceed to Checkout",
                            width="100%",
                            background="#FFD814",
                            color="black",
                            _hover={"background": "#F7CA00"},
                            on_click=rx.redirect("/checkout"),
                        ),

                        spacing="4",
                    ),

                    width="30%",
                    padding="20px",
                    background="white",
                    border_radius="12px",
                ),

                spacing="6",
                padding="30px",
                align="start",
            ),

            flex="1",
        ),

        footer(),

        display="flex",
        flex_direction="column",
        height="100vh",
        background="#F3F3F3",
    )