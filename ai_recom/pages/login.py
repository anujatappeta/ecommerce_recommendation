import reflex as rx
from ai_recom.state import State


def login_page():
    return rx.center(

        rx.box(

            rx.vstack(

                # TITLE
                rx.text(
                    "🛒 AI Shop",
                    font_size="32px",
                    font_weight="bold",
                    color="#111"
                ),

                rx.text(
                    "Welcome back 👋",
                    color="#555",
                    font_size="14px"
                ),

                rx.divider(),

                # EMAIL
                rx.vstack(
                    rx.text("Email", font_weight="bold", color="#111"),

                    rx.input(
                        placeholder="Enter your email",
                        value=State.email,
                        on_change=State.set_email,
                        width="100%",
                        height="50px",
                        font_size="15px",
                        color="black",
                        bg="white",
                        border="1px solid #ccc",
                        border_radius="12px",
                        padding="0 14px"
                    ),

                    spacing="2",
                    width="100%"
                ),

                # PASSWORD (FINAL FIXED)
                rx.vstack(
                    rx.text("Password", font_weight="bold", color="#111"),

                    rx.hstack(

                        rx.input(
                            placeholder="Enter your password",
                            type=rx.cond(State.show_password, "text", "password"),
                            value=State.password,
                            on_change=State.set_password,

                            width="100%",
                            height="50px",
                            font_size="15px",

                            color="black",
                            bg="white",

                            border="1px solid #ccc",
                            border_radius="12px",
                            padding="0 14px"
                        ),

                        rx.button(
                            rx.icon(
                                tag=rx.cond(
                                    State.show_password,
                                    "eye-off",
                                    "eye"
                                )
                            ),
                            on_click=State.toggle_password,
                            variant="ghost",
                            size="3",
                            color="#2563eb"
                        ),

                        width="100%",
                        align="center"
                    ),

                    spacing="2",
                    width="100%"
                ),

                # LOGIN BUTTON
                rx.button(
                    "Sign In",
                    width="100%",
                    height="52px",
                    bg="#2563eb",
                    color="white",
                    border_radius="14px",
                    font_weight="bold",
                    font_size="16px",

                    _hover={
                        "bg": "#1d4ed8",
                        "transform": "translateY(-1px)"
                    },

                    on_click=State.login
                ),

                # MESSAGE
                rx.cond(
                    State.message != "",
                    rx.text(
                        State.message,
                        color="red",
                        font_size="14px",
                        text_align="center"
                    )
                ),

                # SIGNUP LINK
                rx.hstack(
                    rx.text("New user?", color="#555"),
                    rx.text(
                        "Create account",
                        color="#2563eb",
                        font_weight="bold",
                        cursor="pointer",
                        _hover={"text_decoration": "underline"},
                        on_click=rx.redirect("/signup")
                    ),
                    spacing="2"
                ),

                spacing="6",
                width="100%"
            ),

            padding="45px",
            bg="white",
            border_radius="22px",
            box_shadow="0 30px 60px rgba(0,0,0,0.25)",
            width="420px"
        ),

        bg="linear-gradient(135deg, #0f172a, #1e293b)",
        height="100vh"
    )