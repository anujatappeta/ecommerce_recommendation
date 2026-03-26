import reflex as rx
from ai_recom.state import State


def recommend_product_card(product):

    return rx.box(

        rx.vstack(

            # 🖼️ IMAGE
            rx.image(
                src=rx.cond(
                    product.get("ImageURL", "") != "",
                    product.get("ImageURL"),
                    "https://via.placeholder.com/150"
                ),
                height="140px",
                width="100%",
                object_fit="contain",
                border_radius="8px"
            ),

            # 📦 NAME
            rx.text(
                product.get("Name", "No Name"),
                font_weight="bold",
                font_size="14px",
                no_of_lines=2,
                color="#111"
            ),

            # 🏷️ BRAND
            rx.text(
                product.get("Brand", "Unknown"),
                font_size="12px",
                color="gray"
            ),

            # ⭐ RATING
            rx.hstack(
                rx.text("⭐"),
                rx.text(product.get("Rating", "4.0")),
                rx.text(f"({product.get('ReviewCount', 0)})"),
                font_size="12px",
                color="orange",
                spacing="1"
            ),

            # 💰 PRICE
            rx.text(
                f"₹ {product.get('Price', 'N/A')}",
                color="green",
                font_weight="bold",
                font_size="15px"
            ),

            # 🔘 BUTTONS
            rx.hstack(

                # 🛒 ADD TO CART
                rx.button(
                    "Add",
                    size="2",
                    color_scheme="blue",
                    on_click=lambda: State.add_to_cart(product)
                ),

                # 👁️ VIEW (FIXED HERE)
                rx.button(
                    "View",
                    size="2",
                    variant="outline",
                    on_click=lambda: State.set_last_viewed(
                        product.get("ProductID")   # ✅ FIX (NO int)
                    )
                ),

                spacing="2",
                width="100%"
            ),

            spacing="2",
            align="start",
            width="100%"
        ),

        # 🎨 CARD STYLE (IMPROVED)
        border="1px solid #e5e7eb",
        border_radius="12px",
        padding="12px",
        background="white",
        width="220px",
        box_shadow="0 6px 18px rgba(0,0,0,0.08)",

        _hover={
            "transform": "translateY(-4px)",
            "box_shadow": "0 12px 25px rgba(0,0,0,0.15)",
            "transition": "0.2s"
        }
    )