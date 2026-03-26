import reflex as rx
from ai_recom.state import State
from ai_recom.pages.product_details import ProductState


def product_card(product):

    return rx.box(

        rx.vstack(

            # ❤️ WISHLIST BUTTON (TOP RIGHT)
            rx.hstack(
                rx.spacer(),

                rx.cond(
                    State.wishlist.contains(product),

                    # 💔 REMOVE
                    rx.button(
                        "❤️",
                        size="1",
                        bg="white",
                        on_click=lambda: State.remove_from_wishlist(product)
                    ),

                    # 🤍 ADD
                    rx.button(
                        "🤍",
                        size="1",
                        bg="white",
                        on_click=lambda: State.add_to_wishlist(product)
                    )
                ),

                width="100%"
            ),

            # 🖼️ IMAGE
            rx.image(
                src=rx.cond(
                    product.get("ImageURL", "") != "",
                    product.get("ImageURL"),
                    "/no_image.png"
                ),
                height="200px",
                width="100%",
                object_fit="contain"
            ),

            # 📦 NAME
            rx.text(
                product.get("Name", "No Name"),
                font_size="14px",
                no_of_lines=2,
                color="#0F1111"
            ),

            # ⭐ RATING
            rx.hstack(
                rx.text("⭐", color="#FFA41C"),
                rx.text(
                    product.get("Rating", "4.0"),
                    font_size="13px",
                    color="#0F1111"
                ),
                spacing="1"
            ),

            # 💰 PRICE
            rx.text(
                f"₹{product.get('Price', 'N/A')}",
                color="#B12704",
                font_weight="bold",
                font_size="16px"
            ),

            # 🔘 BUTTONS
            rx.vstack(

                # 🛒 ADD TO CART
                rx.button(
                    "Add to Cart",
                    width="100%",
                    bg="#FFD814",
                    color="black",
                    _hover={"bg": "#F7CA00"},
                    on_click=lambda: State.add_to_cart(product)
                ),

                # 👁️ VIEW DETAILS
                rx.button(
                    "View Details",
                    width="100%",
                    variant="outline",
                    on_click=lambda: [
                        ProductState.set_product(product),
                        State.set_last_viewed(product.get("ProductID")),
                        rx.redirect("/product")
                    ]
                ),

                spacing="2",
                width="100%"
            ),

            spacing="3",
            align="start",
            width="100%"
        ),

        # 🎨 CARD STYLE
        background="white",
        padding="12px",
        border_radius="8px",
        width="100%",
        box_shadow="0 2px 6px rgba(0,0,0,0.1)",

        _hover={
            "transform": "scale(1.02)",
            "transition": "0.2s"
        }
    )