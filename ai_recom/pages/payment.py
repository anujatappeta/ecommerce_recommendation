import reflex as rx
from ai_recom.components.navbar import navbar
from ai_recom.state import State   # ✅ only this

@rx.page(route="/payment", title="Payment")
def payment_page() -> rx.Component:
    return rx.box(
        # Razorpay script
        rx.script(src="https://checkout.razorpay.com/v1/checkout.js"),

        navbar(),

        rx.container(
            rx.vstack(
                rx.heading("Order Summary", size="8", margin_top="2rem"),

                # -------- PRICE SUMMARY --------
                rx.card(
                    rx.vstack(
                        rx.heading("Price Details", size="4"),

                        rx.hstack(
                            rx.text("Total Items Price"),
                            rx.spacer(),
                            rx.text(f"₹ {State.total_price}"),
                            width="100%",
                        ),

                        rx.hstack(
                            rx.text("Delivery"),
                            rx.spacer(),
                            rx.text("FREE", color="green"),
                            width="100%",
                        ),

                        rx.divider(),

                        rx.hstack(
                            rx.text("Total Amount", weight="bold"),
                            rx.spacer(),
                            rx.text(f"₹ {State.total_price}", weight="bold"),
                            width="100%",
                        ),

                        # -------- PAYMENT BUTTON --------
                        rx.button(
                            "Pay Now",
                            color_scheme="blue",
                            width="100%",
                            margin_top="1rem",
                            on_click=State.start_payment,  # ✅ use State
                        ),

                        # -------- PAYMENT STATUS --------
                        rx.cond(
                            State.payment_step == "processing",
                            rx.text("Processing payment...", color="orange"),
                        ),

                        rx.cond(
                            State.payment_step == "success",
                            rx.text("✅ Payment Successful!", color="green"),
                        ),

                        width="100%",
                    ),
                    padding="2rem",
                    max_width="400px",
                    width="100%",
                ),

                align_items="center",
                width="100%",
            ),
            size="3",
        ),

        background_color="#f5f5f5",
        min_height="100vh",
    )