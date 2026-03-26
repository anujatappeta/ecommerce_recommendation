import reflex as rx

@rx.page(route="/test")
def test():
    return rx.text("TEST OK")