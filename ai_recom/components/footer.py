import reflex as rx

def footer():
    return rx.box(
        rx.vstack(
            rx.text("© 2026 AI Shop"),
            rx.text("Built with AI Recommendations"),
            rx.text("Powered by Reflex + ML"),
            spacing="1"
        ),
        background="black",
        color="white",
        padding="20px",
        text_align="center",
        width="100%"
    )