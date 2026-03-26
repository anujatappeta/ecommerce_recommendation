import reflex as rx
from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer
from ai_recom.state import State


# 🔥 CHECKOUT STATE WITH VALIDATION
class CheckoutState(rx.State):
    name: str = ""
    address: str = ""
    phone: str = ""
    error: str = ""

    def set_name(self, v):
        self.name = v

    def set_address(self, v):
        self.address = v

    def set_phone(self, v):
        self.phone = v

    # ✅ VALIDATION FUNCTION
    def validate_and_proceed(self):
        # ❌ Empty fields
        if self.name.strip() == "" or self.address.strip() == "":
            self.error = "❌ Please fill all details"
            return

        # ❌ Invalid phone
        if not self.phone.isdigit() or len(self.phone) != 10:
            self.error = "❌ Enter valid 10-digit phone number"
            return

        # ✅ Success
        self.error = ""
        return rx.redirect("/payment")


# 🔥 INPUT STYLE
def input_style():
    return {
        "background_color": "#f9fafb",
        "color": "#111",
        "border": "1px solid #d1d5db",
        "border_radius": "10px",
        "padding": "0 14px",
        "height": "50px",
        "font_size": "16px",
        "box_sizing": "border-box",
        "width": "100%",
    }


# 🔥 MAIN PAGE
def checkout_page():
    return rx.box(

        navbar(),

        rx.flex(
            rx.box(

                rx.vstack(

                    # 🔹 TITLE
                    rx.heading("Checkout", size="7", color="#111"),

                    rx.text(
                        "Enter your delivery details",
                        color="gray",
                        font_size="14px"
                    ),

                    # 🔹 NAME
                    rx.vstack(
                        rx.text("Full Name", font_weight="medium", color="#111"),
                        rx.input(
                            placeholder="Enter your full name",
                            value=CheckoutState.name,
                            on_change=CheckoutState.set_name,
                            **input_style()
                        ),
                        width="100%"
                    ),

                    # 🔹 ADDRESS
                    rx.vstack(
                        rx.text("Address", font_weight="medium", color="#111"),
                        rx.text_area(
                            placeholder="Enter your address",
                            value=CheckoutState.address,
                            on_change=CheckoutState.set_address,
                            width="100%",
                            style={
                                "background_color": "#f9fafb",
                                "color": "#111",
                                "border": "1px solid #d1d5db",
                                "border_radius": "10px",
                                "padding": "12px",
                                "min_height": "110px",
                                "font_size": "16px",
                                "box_sizing": "border-box",
                            }
                        ),
                        width="100%"
                    ),

                    # 🔹 PHONE
                    rx.vstack(
                        rx.text("Phone Number", font_weight="medium", color="#111"),
                        rx.input(
                            placeholder="Enter phone number",
                            value=CheckoutState.phone,
                            on_change=CheckoutState.set_phone,
                            type_="tel",   # 🔥 mobile keypad
                            **input_style()
                        ),
                        width="100%"
                    ),

                    rx.divider(),

                    # 🔹 TOTAL
                    rx.hstack(
                        rx.text("Total", font_size="16px", color="gray"),
                        rx.spacer(),
                        rx.text(
                            f"₹{State.total_price}",
                            font_weight="bold",
                            font_size="18px",
                            color="#111"
                        ),
                        width="100%"
                    ),

                    # 🔴 ERROR MESSAGE
                    rx.cond(
                        CheckoutState.error != "",
                        rx.text(
                            CheckoutState.error,
                            color="red",
                            font_size="14px"
                        )
                    ),

                    # 🔹 BUTTON
                    rx.button(
                        "Proceed to Payment",
                        on_click=CheckoutState.validate_and_proceed,
                        width="100%",
                        size="3",
                        border_radius="10px",
                        box_shadow="0 4px 12px rgba(0,0,0,0.2)",
                        color_scheme="blue"
                    ),

                    spacing="5",
                    width="100%"
                ),

                width="420px",
                padding="30px",
                background="white",
                border_radius="16px",
                box_shadow="0 12px 30px rgba(0,0,0,0.15)"
            ),

            justify="center",
            align="center",
            height="85vh",
            background="#f3f4f6"
        ),

        footer()
    )