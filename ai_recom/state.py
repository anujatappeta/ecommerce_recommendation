import reflex as rx
from typing import List, Dict, Any
import pandas as pd
import asyncio

from ai_recom.db import create_user, get_user, get_next_user_id, update_user_type
from ai_recom.backend.rating_based import get_top_rated
from ai_recom.backend.hybrid import get_hybrid_recommendations


class State(rx.State):

    # ---------- USER ----------
    user_id: int = 0
    email: str = ""
    password: str = ""
    name: str = ""
    message: str = ""
    user_type: str = ""

    show_password: bool = False
    search_query: str = ""

    # ---------- DATA ----------
    products: List[Dict[str, Any]] = []
    recommended_products: List[Dict[str, Any]] = []

    cart: List[Dict[str, Any]] = []
    total_price: float = 0.0

    wishlist: List[Dict[str, Any]] = []
    orders: List[List[Dict[str, Any]]] = []

    payment_step: str = ""
    last_viewed_product_id: int = 0
    selected_product: Dict[str, Any] = {}

    # ---------- BASIC ----------
    def set_email(self, v: str):
        self.email = v

    def set_password(self, v: str):
        self.password = v

    def set_name(self, v: str):
        self.name = v

    def set_search(self, v: str):
        self.search_query = v

    def toggle_password(self):
        self.show_password = not self.show_password

    def set_last_viewed(self, pid):
        try:
            self.last_viewed_product_id = int(pid)
        except:
            self.last_viewed_product_id = 0

    # ---------- AUTH ----------
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
        return rx.redirect("/home")

    def login(self):
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
        return rx.redirect("/home")

    def logout(self):
        self.user_id = 0
        self.email = ""
        self.password = ""
        self.name = ""
        self.message = ""
        self.user_type = ""
        return rx.redirect("/")

    # ---------- PRODUCTS ----------
    def load_home_products(self):
        df = pd.read_csv("final_clean_data.csv").head(50)
        self.products = df.to_dict("records")

    def search_products(self):
        df = pd.read_csv("final_clean_data.csv")

        if not self.search_query:
            self.products = df.head(20).to_dict("records")
            return

        filtered = df[df["Name"].str.contains(self.search_query, case=False, na=False)]
        self.products = filtered.head(20).to_dict("records")

    # ---------- VIEW DETAILS ----------
    def view_product(self, product: Dict[str, Any]):
        if not product:
            return

        self.selected_product = product
        self.last_viewed_product_id = product.get("ProductID", 0)
        return rx.redirect("/product-details")

    # ---------- CART ----------
    def add_to_cart(self, product: Dict[str, Any]):
        found = False
        updated = []

        for item in self.cart:
            if item["ProductID"] == product.get("ProductID"):
                updated.append({**item, "quantity": item.get("quantity", 1) + 1})
                found = True
            else:
                updated.append(item)

        if not found:
            updated.append({
                "ProductID": product.get("ProductID"),
                "Name": product.get("Name"),
                "Price": product.get("Price"),
                "ImageURL": product.get("ImageURL"),
                "quantity": 1
            })

        self.cart = updated
        self.calculate_total()

    def remove_from_cart(self, product_id: int):
        updated = []

        for item in self.cart:
            if item["ProductID"] == product_id:
                if item.get("quantity", 1) > 1:
                    updated.append({
                        **item,
                        "quantity": item["quantity"] - 1
                    })
            else:
                updated.append(item)

        self.cart = updated
        self.calculate_total()

    def calculate_total(self):
        self.total_price = sum(
            float(p.get("Price", 0)) * p.get("quantity", 1)
            for p in self.cart
        )

    # ---------- SAVE FOR LATER (FIXED) ----------
    def save_for_later(self, product: Dict[str, Any]):

        self.cart = [
            p for p in self.cart
            if p.get("ProductID") != product.get("ProductID")
        ]

        if not any(p["ProductID"] == product.get("ProductID") for p in self.wishlist):
            self.wishlist.append(product)

        self.calculate_total()

    # ---------- WISHLIST ----------
    def add_to_wishlist(self, product: Dict[str, Any]):
        if not any(p["ProductID"] == product.get("ProductID") for p in self.wishlist):
            self.wishlist.append(product)

    def remove_from_wishlist(self, product: Dict[str, Any]):
        self.wishlist = [
            p for p in self.wishlist
            if p.get("ProductID") != product.get("ProductID")
        ]

    # ---------- RECOMMENDATIONS ----------
    def get_recommendations(self):
        df = pd.read_csv("final_clean_data.csv")

        if self.user_type == "new":
            ids = get_top_rated()
        else:
            ids = get_hybrid_recommendations(
                self.user_id,
                self.last_viewed_product_id
            )

        df = df[df["ProductID"].isin(ids)]
        self.recommended_products = df.head(20).to_dict("records")

    # ---------- PAYMENT ----------
    async def start_payment(self):
        self.payment_step = "processing"
        await asyncio.sleep(2)
        self.payment_step = "success"

        self.orders.append(self.cart.copy())
        self.cart = []
        self.total_price = 0.0

        update_user_type(self.email, "old")
        self.user_type = "old"

    def reset_payment(self):
        self.payment_step = ""