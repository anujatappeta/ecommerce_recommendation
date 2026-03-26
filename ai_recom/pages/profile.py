import reflex as rx
from ai_recom.state import State
from ai_recom.components.navbar import navbar
from ai_recom.components.footer import footer


#@rx.page(route="/profile")
def profile_page():

    return rx.box(

        # ✅ CHILDREN FIRST
        navbar(),

        rx.center(

            rx.box(

                rx.vstack(

                    # 🔥 TITLE
                    rx.heading("My Profile", size="7", color="#111"),

                    rx.divider(),

                    # 🔹 USER DETAILS
                    rx.vstack(

                        rx.hstack(
                            rx.text("Email", font_weight="bold", color="#111"),
                            rx.spacer(),
                            rx.text(State.email, color="#111"),
                            width="100%"
                        ),

                        rx.hstack(
                            rx.text("User ID", font_weight="bold", color="#111"),
                            rx.spacer(),
                            rx.text(State.user_id, color="#111"),
                            width="100%"
                        ),

                        rx.hstack(
                            rx.text("User Type", font_weight="bold", color="#111"),
                            rx.spacer(),
                            rx.text(State.user_type, color="#111"),
                            width="100%"
                        ),

                        spacing="3",
                        width="100%"
                    ),

                    rx.divider(),

                    # 🔹 LOGOUT BUTTON
                    rx.button(
                        "Logout",
                        width="100%",
                        color_scheme="red",
                        on_click=State.logout
                    ),

                    spacing="5",
                    width="100%"
                ),

                width="400px",
                padding="30px",
                background="white",
                color="#111",
                border_radius="16px",
                box_shadow="0 10px 30px rgba(0,0,0,0.2)"
            ),

            flex="1"
        ),

        footer(),

        # ✅ PROPS LAST
        display="flex",
        flex_direction="column",
        height="100vh",
    )