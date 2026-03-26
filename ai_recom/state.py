import reflex as rx
from typing import List, Dict, Any
import pandas as pd
import asyncio

from ai_recom.db import create_user, get_user, get_next_user_id, update_user_type
from ai_recom.backend.rating_based import get_top_rated
from ai_recom.backend.hybrid import get_hybrid_recommendations


class State(rx.State):

    user_id: int = 0
    email: str = ""
    password: str = ""
    name: str = ""
    message: str = ""
    user_type: str = ""

    show_password: bool = False
    search_query: str = ""

    products: List[Dict[str, Any]] = []
    recommended_products: List[Dict[str, Any]] = []

    cart: List[Dict[str, Any]] = []
    total_price: float = 0.0

    wishlist: List[Dict[str, Any]] = []
    orders: List[List[Dict[str, Any]]] = []

    payment_step: str = ""
    last_viewed_product_id: int = 0

    # -------------------------
    # INPUT
    # -------------------------
    def set_email(self, v: str): self.email = v
    def set_password(self, v: str): self.password = v
    def set_name(self, v: str): self.name = v
    def set_search(self, v: str): self.search_query = v

    def toggle_password(self): self.show_password = not self.show_password
    def reset_password_toggle(self): self.show_password = False

    def set_last_viewed(self, pid):
        try:
            self.last_viewed_product_id = int(pid)
        except:
            self.last_viewed_product_id = 0

    # -------------------------
    # AUTH
    # -------------------------
    def signup(self):
        if not self.name or not self.email or not self.password:
            self.message = "Fill all fields"
            return

        if get_user(self.email):
            self.message = "User already exists"
            return

        user_id = get_next_user_id()
        create_user(self.email, self.password, user_id, "new")

        self.user_id = user_id
        self.user_type = "new"
        self.message = ""

        return rx.redirect("/home")

    def login(self):
        if not self.email or not self.password:
            self.message = "Enter email & password"
            return

        user = get_user(self.email)

        if not user:
            self.message = "User not found"
            return

        email, password, user_id, user_type = user

        if password != self.password:
            self.message = "Wrong password"
            return

        self.user_id = user_id
        self.user_type = user_type
        self.message = ""

        return rx.redirect("/home")

    def logout(self):
        self.user_id = 0
        self.email = ""
        self.password = ""
        self.name = ""
        self.user_type = ""
        self.cart = []
        self.wishlist = []
        self.orders = []
        self.total_price = 0.0
        self.products = []
        self.recommended_products = []
        return rx.redirect("/")

    # -------------------------
    # LOAD PRODUCTS (MEMORY SAFE)
    # -------------------------
    def load_home_products(self):
        try:
            chunks = pd.read_csv(
                "final_clean_data.csv",
                usecols=["ProductID", "Name", "Price", "ImageURL","Description"],
                chunksize=200
            )
            df = next(chunks)
            self.products = df.head(70).to_dict("records")
        except Exception as e:
            print("Load Error:", e)
            self.products = []

    # -------------------------
    # SEARCH (MEMORY SAFE)
    # -------------------------
    def search_products(self):
        try:
            chunks = pd.read_csv(
                "final_clean_data.csv",
                usecols=["ProductID", "Name", "Price", "ImageURL","Description"],
                chunksize=500
            )
            df = next(chunks)

            if not self.search_query:
                self.products = df.head(20).to_dict("records")
                return

            filtered = df[
                df["Name"].str.contains(self.search_query, case=False, na=False)
            ]

            self.products = filtered.head(20).to_dict("records")

        except Exception as e:
            print("Search Error:", e)
            self.products = []

    def clear_search(self):
        self.search_query = ""
        self.load_home_products()

    # -------------------------
    # CART
    # -------------------------
    def add_to_cart(self, product: Dict[str, Any]):
        if product not in self.cart:
            self.cart.append(product)
            self.calculate_total()

    def calculate_total(self):
        self.total_price = sum(float(p.get("Price", 0)) for p in self.cart)

    def remove_from_cart(self, product_id: int):
        self.cart = [p for p in self.cart if p.get("ProductID") != product_id]
        self.calculate_total()

    def save_for_later(self, product: Dict[str, Any]):
        self.cart = [p for p in self.cart if p != product]
        if product not in self.wishlist:
            self.wishlist.append(product)
        self.calculate_total()

    # -------------------------
    # WISHLIST
    # -------------------------
    def add_to_wishlist(self, product: Dict[str, Any]):
        if product not in self.wishlist:
            self.wishlist.append(product)

    def remove_from_wishlist(self, product: Dict[str, Any]):
        self.wishlist = [p for p in self.wishlist if p != product]

    # -------------------------
    # RECOMMENDATIONS (MEMORY SAFE)
    # -------------------------
    def get_recommendations(self):
        try:
            user = get_user(self.email) if self.email else None

            if not user:
                result = get_top_rated()
            else:
                _, _, user_id, user_type = user

                if user_type == "new" or self.last_viewed_product_id == 0:
                    result = get_top_rated()
                else:
                    result = get_hybrid_recommendations(
                        user_id,
                        self.last_viewed_product_id
                    )

            chunks = pd.read_csv(
                "final_clean_data.csv",
                usecols=["ProductID", "Name", "Price", "ImageURL","Description"],
                chunksize=1000
            )
            df = next(chunks)

            if isinstance(result, list):
                df = df[df["ProductID"].isin(result)]

            self.recommended_products = df.head(20).to_dict("records")

        except Exception as e:
            print("Recommendation Error:", e)
            self.recommended_products = []

    # -------------------------
    # SAFE LOAD
    # -------------------------
    def on_load(self):
        if not self.products:
            self.load_home_products()

        if not self.recommended_products:
            self.get_recommendations()

    # -------------------------
    # PAYMENT (SIMULATION)
    # -------------------------
    async def start_payment(self):
        self.payment_step = "processing"
        await asyncio.sleep(2)
        self.payment_step = "success"

        self.place_order()
        update_user_type(self.email, "old")
        self.user_type = "old"

    def reset_payment(self):
        self.payment_step = ""

    def place_order(self):
        if self.cart:
            self.orders.append(self.cart.copy())
            self.cart = []
            self.total_price = 0.0