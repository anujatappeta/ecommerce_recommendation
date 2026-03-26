import reflex as rx
from ai_recom.state import State
from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer


# 🧾 SINGLE ORDER CARD
def order_card(order):

    return rx.box(

        rx.vstack(

            # 🔹 TITLE
            rx.text(
                "Order",
                font_weight="bold",
                color="#0F1111"
            ),

            rx.divider(),

            # 🛍️ PRODUCTS
            rx.foreach(
                order,
                lambda product: rx.text(
                    product["Name"],
                    font_size="14px",
                    color="black"   # ✅ FIXED (important)
                )
            ),

            rx.divider(),

            # 📦 ITEM COUNT (SAFE WAY)
            rx.text(
                "Items: " + order.length().to_string(),  # ✅ BEST FIX
                color="black",
                font_size="12px"
            ),

            spacing="3",
            width="100%"
        ),

        background="white",
        padding="15px",
        border_radius="10px",
        box_shadow="0 4px 10px rgba(0,0,0,0.1)",
        width="100%"
    )


# 📦 ORDERS PAGE
# @rx.page(route="/orders")
def orders_page():

    return rx.box(

        # 🔹 NAVBAR
        navbar(),

        # 🔹 MAIN CONTENT
        rx.box(

            rx.vstack(

                # 🧾 HEADING
                rx.heading(
                    "Your Orders 📦",
                    size="7",
                    color="black"   # ✅ ensure visibility
                ),

                # 🔍 CONDITIONAL RENDER
                rx.cond(
                    State.orders.length() > 0,

                    # ✅ SHOW ORDERS
                    rx.vstack(
                        rx.foreach(State.orders, order_card),
                        spacing="4",
                        width="100%"
                    ),

                    # ❌ EMPTY STATE
                    rx.center(
                        rx.text(
                            "No orders yet",
                            color="black"
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