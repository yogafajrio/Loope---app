# katalog_loope.py - Aplikasi Katalog Loopé (Full Bahasa Indonesia & Themed)

import streamlit as st
import random 
import pandas as pd
import base64

# --- A. DEFINISI KELAS (Logika Bisnis) ---

class User:
    def __init__(self, user_id, name, email, password, address):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.address = address

class Category:
    def __init__(self, category_id, name, description=""):
        self.category_id = category_id
        self.name = name
        self.description = description

class Product:
    def __init__(self, product_id, category_id, name, price, description="", colors=None, sizes=None, image_url=None):
        self.product_id = product_id
        self.category_id = category_id
        self.name = name
        self.price = price
        self.description = description
        self.colors = colors if colors is not None else []
        self.sizes = sizes if sizes is not None else []
        self.image_url = image_url if image_url else "https://via.placeholder.com/200x200?text=LOOPÉ+Product" # URL gambar placeholder

class CartItem:
    def __init__(self, product_id, size, color, qty, product_price):
        self.product_id = product_id
        self.size = size
        self.color = color
        self.qty = qty
        self.product_price = product_price 
        self.total_price = qty * product_price 

class Cart:
    def __init__(self, cart_id, user_id):
        self.cart_id = cart_id
        self.user_id = user_id

    def items(self):
        return st.session_state.cart_items

    def add_item(self, cart_item):
        """Menambahkan atau mengupdate item."""
        found = False
        for item in st.session_state.cart_items:
            if (item.product_id == cart_item.product_id and 
                item.size == cart_item.size and 
                item.color == cart_item.color):
                item.qty += cart_item.qty
                item.total_price = item.qty * item.product_price
                found = True
                break
        if not found:
            st.session_state.cart_items.append(cart_item)

    def clear(self):
        st.session_state.cart_items = []
        
    def calculate_total(self):
        return sum(item.total_price for item in st.session_state.cart_items)

    def update_item_qty(self, product_id, size, color, new_qty):
        """Memperbarui kuantitas item dalam keranjang."""
        
        # Hapus item lama (ID, Size, Color yang sama)
        st.session_state.cart_items = [
            item for item in st.session_state.cart_items 
            if not (item.product_id == product_id and item.size == size and item.color == color)
        ]
        
        if new_qty > 0:
            product = next(p for p in DATA_PRODUCTS if p.product_id == product_id)
            new_item = CartItem(product_id, size, color, new_qty, product.price)
            st.session_state.cart_items.append(new_item)


class Filter:
    def __init__(self, size=None, color=None, min_price=None, max_price=None):
        self.size = size
        self.color = color
        self.min_price = min_price
        self.max_price = max_price

    def apply(self, products):
        filtered_products = products
        
        if self.size:
            filtered_products = [p for p in filtered_products if self.size in p.sizes]
        if self.color:
            filtered_products = [p for p in filtered_products if self.color in p.colors]
        if self.min_price is not None:
            filtered_products = [p for p in filtered_products if p.price >= self.min_price]
        if self.max_price is not None:
            filtered_products = [p for p in filtered_products if p.price]
