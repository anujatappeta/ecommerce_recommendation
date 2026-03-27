import reflex as rx
from ai_recom.state import State


def product_card(product):

    return rx.box(

        rx.vstack(

            # ❤️ Wishlist
            rx.hstack(
                rx.spacer(),

                rx.cond(
                    State.wishlist.contains(product),

                    rx.button(
                        "❤️",
                        size="1",
                        bg="white",
                        on_click=lambda: State.remove_from_wishlist(product)
                    ),

                    rx.button(
                        "🤍",
                        size="1",
                        bg="white",
                        on_click=lambda: State.add_to_wishlist(product)
                    )
                ),

                width="100%"
            ),

            # 🖼️ Image
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

            # 📦 Name
            rx.text(
                product.get("Name", "No Name"),
                font_size="14px",
                no_of_lines=2
            ),

            # ⭐ Rating
            rx.hstack(
                rx.text("⭐"),
                rx.text(product.get("Rating", "4.0")),
            ),

            # 💰 Price
            rx.text(
                f"₹{product.get('Price', 'N/A')}",
                font_weight="bold"
            ),

            # 🔘 Buttons
            rx.vstack(

                # 🛒 Add to Cart
                rx.button(
                    "Add to Cart",
                    width="100%",
                    on_click=lambda: State.add_to_cart(product)
                ),

                # ✅ FIXED VIEW DETAILS
                rx.button(
                    "View Details",
                    width="100%",
                    variant="outline",
                    on_click=lambda: State.view_product(product)
                ),

                spacing="2",
                width="100%"
            ),

            spacing="3",
            width="100%"
        ),

        padding="12px",
        border="1px solid #ddd",
        border_radius="8px"
    )