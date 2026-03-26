import reflex as rx

config = rx.Config(
    app_name="ai_recom",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)