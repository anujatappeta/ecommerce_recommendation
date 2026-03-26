import reflex as rx
from ai_recom.state import State


def navbar():
    return rx.hstack(

        # 🛒 LOGO
        rx.text(
            "🛒 AI Shop",
            font_size="22px",
            font_weight="bold",
            color="white",
            cursor="pointer",
            on_click=rx.redirect("/home")
        ),

        # 🔍 SEARCH BAR
        rx.hstack(
            rx.input(
                placeholder="Search products...",
                value=State.search_query,
                on_change=State.set_search,

                width="350px",
                height="40px",
                bg="white",
                color="black",

                border="none",
                border_radius="4px 0 0 4px",
                padding="0 10px"
            ),

            rx.button(
                "Search",
                on_click=State.search_products,
                bg="#febd69",
                color="black",
                border_radius="0 4px 4px 0",
                height="40px"
            ),

            spacing="0"
        ),

        rx.spacer(),

        # 🔗 NAV LINKS
        rx.hstack(

            rx.text("Home", cursor="pointer", color="white", on_click=rx.redirect("/home")),
            rx.text("Products", cursor="pointer", color="white", on_click=rx.redirect("/products")),
            rx.text("Wishlist", cursor="pointer", color="white", on_click=rx.redirect("/wishlist")),
            rx.text("Orders", cursor="pointer", color="white", on_click=rx.redirect("/orders")),

            # 🛒 CART WITH COUNT (FIXED)
            rx.hstack(
                rx.text("Cart", cursor="pointer", color="white", on_click=rx.redirect("/cart")),
                rx.box(
                    rx.text(
                        State.cart.length(),
                        color="black",
                        font_size="12px"
                    ),
                    bg="#febd69",
                    border_radius="50%",
                    padding="2px 6px"
                ),
                spacing="1",
                align="center"
            ),

            spacing="5",
            align="center"
        ),

        # 👤 USER SECTION
        rx.cond(
            State.user_id != 0,

            # ✅ DROPDOWN
            rx.menu.root(

                rx.menu.trigger(
                    rx.hstack(
                        rx.avatar(name=State.email, size="2"),
                        rx.text(State.email, font_size="13px", color="white"),
                        cursor="pointer"
                    )
                ),

                rx.menu.content(

                    rx.menu.item("Profile", on_click=rx.redirect("/profile")),
                    rx.menu.item("Wishlist", on_click=rx.redirect("/wishlist")),
                    rx.menu.item("Orders", on_click=rx.redirect("/orders")),

                    rx.menu.separator(),

                    rx.menu.item(
                        "Logout",
                        color="red",
                        on_click=State.logout
                    ),
                )
            ),

            # ❌ NOT LOGGED IN
            rx.hstack(
                rx.button("Login", on_click=rx.redirect("/")),
                rx.button("Signup", on_click=rx.redirect("/signup")),
                spacing="2"
            )
        ),

        # 🎨 STYLE
        justify="between",
        align="center",
        padding="12px 24px",
        bg="#131921",
        width="100%",
        position="sticky",
        top="0",
        z_index="1000"
    )