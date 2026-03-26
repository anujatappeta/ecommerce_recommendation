import reflex as rx
from ai_recom.state import State
from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer


def payment_page():

    return rx.box(

        # 🔝 NAVBAR
        navbar(),

        # 🔹 MAIN SECTION
        rx.box(

            rx.hstack(

                # 💳 LEFT SIDE - PAYMENT OPTIONS
                rx.box(

                    rx.vstack(

                        rx.heading(
                            "Select Payment Method",
                            size="6",
                            color="#111"
                        ),

                        rx.button("Google Pay", width="100%", variant="outline"),
                        rx.button("PhonePe", width="100%", variant="outline"),
                        rx.button("Paytm", width="100%", variant="outline"),

                        rx.divider(),

                        rx.button(
                            "Pay Now",
                            width="100%",
                            bg="#FFD814",
                            color="black",
                            _hover={"bg": "#F7CA00"},
                            on_click=State.start_payment
                        ),

                        spacing="4",
                        width="100%"
                    ),

                    background="white",
                    padding="25px",
                    border_radius="12px",
                    width="50%",
                    box_shadow="0 2px 8px rgba(0,0,0,0.1)"
                ),

                # 🧾 RIGHT SIDE - ORDER SUMMARY
                rx.box(

                    rx.vstack(

                        rx.heading(
                            "Order Summary",
                            size="6",
                            color="#111"
                        ),

                        rx.hstack(
                            rx.text("Items", color="#333"),
                            rx.spacer(),
                            rx.text(State.cart.length(), color="#333")
                        ),

                        rx.hstack(
                            rx.text("Total Amount", color="#333"),
                            rx.spacer(),
                            rx.text(
                                f"₹{State.total_price}",
                                font_weight="bold",
                                color="#B12704",
                                font_size="18px"
                            )
                        ),

                        rx.divider(),

                        rx.text(
                            "Secure payment powered by UPI",
                            font_size="12px",
                            color="gray"
                        ),

                        spacing="4",
                        width="100%"
                    ),

                    background="white",
                    padding="25px",
                    border_radius="12px",
                    width="40%",
                    box_shadow="0 2px 8px rgba(0,0,0,0.1)"
                ),

                spacing="8",
                width="100%"
            ),

            background="#f3f4f6",
            padding="40px",
            min_height="100vh"
        ),

        # 🔹 PAYMENT POPUP
        rx.cond(
            State.payment_step != "",

            rx.box(

                rx.vstack(

                    rx.heading(
                        "Payment Status",
                        size="5",
                        color="#111"
                    ),

                    # ⏳ PROCESSING
                    rx.cond(
                        State.payment_step == "processing",
                        rx.vstack(
                            rx.spinner(size="3"),
                            rx.text("Processing payment...", color="#333")
                        )
                    ),

                    # ✅ SUCCESS
                    rx.cond(
                        State.payment_step == "success",
                        rx.vstack(
                            rx.text(
                                "Payment Successful",
                                font_size="18px",
                                color="green",
                                font_weight="bold"
                            ),

                            rx.button(
                                "Go to Home",
                                on_click=lambda: [
                                    State.reset_payment(),
                                    rx.redirect("/home")
                                ],
                                bg="#2563eb",
                                color="white",
                                width="100%"
                            )
                        )
                    ),

                    spacing="5",
                    align="center"
                ),

                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                background="white",
                padding="35px",
                border_radius="14px",
                box_shadow="0 10px 40px rgba(0,0,0,0.25)",
                width="350px"
            )
        ),

        # 🔻 FOOTER
        footer()
    )