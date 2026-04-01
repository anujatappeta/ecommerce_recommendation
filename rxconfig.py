import os
import reflex as rx

config = rx.Config(
    app_name="ai_recom",
    api_url=os.environ.get("REFLEX_API_URL") or "http://127.0.0.1:8000",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)