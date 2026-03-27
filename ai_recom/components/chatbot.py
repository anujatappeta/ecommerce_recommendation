import reflex as rx
from typing import List, Dict
from ai_recom.backend.chatbot import get_chatbot_response

class ChatState(rx.State):
    user_input: str = ""
    messages: List[Dict] = []
    is_open: bool = False

    def set_input(self, value: str):
        self.user_input = value

    def toggle_chat(self):
        self.is_open = not self.is_open

    def send_message(self):
        if self.user_input.strip() == "":
            return

        #  User message
        self.messages.append({
            "type": "user",
            "text": self.user_input
        })

        # Get bot response
        bot_reply = get_chatbot_response(self.user_input)

        # FIX: ensure string
        if isinstance(bot_reply, dict):
            bot_reply = bot_reply.get("data", str(bot_reply))

        # Bot message
        self.messages.append({
            "type": "bot",
            "text": str(bot_reply)
        })

        self.user_input = ""


def chatbot():
    return rx.box(

        #  CHAT WINDOW
        rx.cond(
            ChatState.is_open,

            rx.box(
                rx.vstack(

                    # 🔹 Header
                    rx.hstack(
                        rx.text(
                            "🤖 AI Assistant",
                            font_weight="bold",
                            font_size="18px",
                            color="black"
                        ),
                        rx.spacer(),
                        rx.button("✖", on_click=ChatState.toggle_chat, size="2"),
                        width="100%"
                    ),

                    # 🔹 Messages 
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                ChatState.messages,
                                lambda msg: rx.box(

                                    rx.text(
                                        msg["text"],  
                                        font_size="16px"
                                    ),

                                    align_self=rx.cond(
                                        msg["type"] == "user",
                                        "flex-end",
                                        "flex-start"
                                    ),

                                    background=rx.cond(
                                        msg["type"] == "user",
                                        "#2563eb",
                                        "#f1f5f9"
                                    ),

                                    color=rx.cond(
                                        msg["type"] == "user",
                                        "white",
                                        "black"
                                    ),

                                    padding="12px",
                                    border_radius="12px",
                                    max_width="85%"
                                )
                            ),
                            spacing="3",
                            width="100%"
                        ),
                        height="350px",
                        overflow_y="auto",
                        width="100%",
                        padding="5px"
                    ),

                    # 🔹 Input
                    rx.hstack(
                        rx.input(
                            placeholder="Ask about products...",
                            value=ChatState.user_input,
                            on_change=lambda v: ChatState.set_input(v),
                            width="100%",
                            size="3",
                            background_color="#f5f5f5",
                            color="black",
                            border="1px solid #ccc"
                        ),

                        rx.button(
                            "Send",
                            on_click=ChatState.send_message,
                            size="3"
                        ),
                        width="100%"
                    ),

                    spacing="4",
                    width="100%"
                ),

                width="400px",
                padding="16px",
                background="white",
                border_radius="16px",
                box_shadow="0 15px 35px rgba(0,0,0,0.3)"
            ),
        ),

        #  Floating Button
        rx.button(
            "💬",
            on_click=ChatState.toggle_chat,
            border_radius="50%",
            width="65px",
            height="65px",
            font_size="22px",
            color_scheme="blue",
            box_shadow="0 6px 16px rgba(0,0,0,0.3)"
        ),

        position="fixed",
        bottom="20px",
        right="20px",
        z_index="999"
    )