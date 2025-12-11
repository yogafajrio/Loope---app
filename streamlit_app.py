# loope_catalog_app.py - Aplikasi Katalog Loopé yang Lengkap dan Dapat Dijalankan

import streamlit as st
import random 
import pandas as pd

# --- A. DEFINISI KELAS (DARI models.py) ---
# Dipertahankan sesuai Diagram Class Anda: User, Product, Cart, Filter, Checkout, Payment

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
    def __init__(self, product_id, category_id, name, price, description="", colors=None, sizes=None, images=None):
        self.product_id = product_id
        self.category_id = category_id
        self.name = name
        self.price = price
        self.description = description
        self.colors = colors if colors is not None else []
        self.sizes = sizes if sizes is not None else []
        self.images = images if images is not None else []
        
    def get_info(self):
        """Mengembalikan data produk dalam format dict untuk DataFrame."""
        return {
            "ID": self.product_id,
            "Nama": self.name,
            "Harga": self.price,
            "Deskripsi": self.description,
            "Warna": ", ".join(self.colors),
            "Ukuran": ", ".join(self.sizes)
        }

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
        # items disimpan di session_state untuk persistensi

    def items(self):
        """Mengambil item dari session state."""
        return st.session_state.cart_items

    def add_item(self, cart_item):
        """Menambahkan atau mengupdate item."""
        found = False
        for item in st.session_state.cart_items:
            # Cari item yang sama persis (ID, Size, Color)
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
        st.session_state.cart_items = [
            item for item in st.session_state.cart_items 
            if not (item.product_id == product_id and item.size == size and item.color == color)
        ]
        if new_qty > 0:
             # Cari produk untuk harga
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
            filtered_products = [p for p in filtered_products if p.price <= self.max_price]
            
        return filtered_products


class Checkout:
    def __init__(self, checkout_id, user_id, total_price, shipping_address):
        self.checkout_id = checkout_id
        self.user_id = user_id
        self.total_price = total_price
        self.shipping_address = shipping_address

    def verify_order(self):
        return True

    def proceed_to_payment(self, method):
        return Payment(payment_id=random.randint(2000, 9999), method=method)


class Payment:
    def __init__(self, payment_id, method, status="pending"):
        self.payment_id = payment_id
        self.method = method
        self.status = status

    def process_payment(self, total_price):
        self.status = "paid"
        return self.status == "paid"

# --- B. DATA DUMMY ---
DATA_PRODUCTS = [
    Product(101, 1, "Pink T-shirt", 17.00, "So fetch!", ["Pink", "White"], ["S", "M", "L"]), 
    Product(102, 2, "Plaid Mini Skirt", 12.00, "Trending Now", ["Pink Plaid", "Grey"], ["XS", "S", "M"]), 
    Product(103, 1, "Black Tank Top", 18.00, "Sparkly tank top", ["Black", "Silver"], ["S", "M"]),
    Product(104, 2, "Jogger Pants", 35.00, "Comfy outfit", ["Pink"], ["L", "XL"]),
    Product(105, 1, "Cropped Cardi", 20.00, "Pre-Spring Pick", ["Pink", "White"], ["S", "M"]),
]

DATA_CATEGORIES = [
    Category(1, "Tops", "Atasan"),
    Category(2, "Bottoms", "Bawahan"),
]

# --- C. FUNGSI LOGIKA & SESI STREAMLIT ---

# Inisialisasi Session State (Wajib Streamlit)
if 'user' not in st.session_state:
    st.session_state.user = User(5056241024, "Agni Putri", "agni@example.com", "securepwd", "Jl. Contoh No. 123")
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = [] # Simpan list CartItem di sini
if 'cart_obj' not in st.session_state:
    # Objek Cart hanya untuk memanggil method, data di cart_items
    st.session_state.cart_obj = Cart(cart_id=1, user_id=st.session_state.user.user_id)
if 'page' not in st.session_state:
    st.session_state.page = 'katalog' 

def set_page(page_name):
    """Fungsi pembantu untuk navigasi halaman."""
    st.session_state.page = page_name

def add_to_cart_callback(product_id, size, color, qty=1):
    """Menambahkan item ke keranjang (Callback untuk tombol)."""
    product = next(p for p in DATA_PRODUCTS if p.product_id == product_id)
    cart_item = CartItem(
        product_id=product.product_id,
        size=size,
        color=color,
        qty=qty,
        product_price=product.price
    )
    st.session_state.cart_obj.add_item(cart_item)
    st.toast(f"✅ Added {qty}x {product.name} ({color}, {size}) to cart!")
    st.experimental_rerun() # Refresh tampilan keranjang

# --- D. FUNGSI TAMPILAN Halaman ---

def display_header():
    """Menampilkan Header dan Tombol Cart/Checkout."""
    st.title("🛍️ LOOPÉ Online Catalog")
    
    col1, col2 = st.columns([5, 1])
    with col2:
        cart_total = st.session_state.cart_obj.calculate_total()
        st.button(
            f"🛒 ({len(st.session_state.cart_items)}) | ${cart_total:.2f}",
            on_click=set_page,
            args=('checkout',),
            key="header_cart_button"
        )
    st.divider()

def display_product_card(product):
    """Menampilkan satu produk dalam format card."""
    with st.container(border=True):
        st.image("https://via.placeholder.com/150", caption=product.name)
        st.markdown(f"**{product.name}**")
        st.markdown(f"**$ {product.price:.2f}**")
        
        # FIX: Menggunakan key unik yang stabil untuk setiap widget (wajib di Streamlit)
        col_s, col_c = st.columns(2)
        with col_s:
            selected_size = st.selectbox("Size", product.sizes, key=f"size_{product.product_id}")
        with col_c:
            selected_color = st.selectbox("Color", product.colors, key=f"color_{product.product_id}")

        st.button(
            "Add to Cart",
            key=f"add_{product.product_id}",
            on_click=add_to_cart_callback,
            args=(product.product_id, selected_size, selected_color, 1),
            use_container_width=True
        )

def page_katalog():
    """Halaman utama katalog dengan Filter."""
    display_header()
    
    with st.sidebar:
        st.header("🔍 Filter Produk")
        
        category_map = {c.name: c.category_id for c in DATA_CATEGORIES}
        selected_category_name = st.selectbox("Category", list(category_map.keys()))
        selected_category_id = category_map[selected_category_name]
        
        selected_size = st.selectbox("Size", ["All"] + sorted(list(set(s for p in DATA_PRODUCTS for s in p.sizes))))
        selected_color = st.selectbox("Color", ["All"] + sorted(list(set(c for p in DATA_PRODUCTS for c in p.colors))))
        min_p = st.slider("Min Price", min_value=0.0, max_value=50.0, value=0.0, step=1.0)
        max_p = st.slider("Max Price", min_value=0.0, max_value=50.0, value=50.0, step=1.0)
        
        current_filter = Filter(
            size=selected_size if selected_size != "All" else None,
            color=selected_color if selected_color != "All" else None,
            min_price=min_p,
            max_price=max_p
        )

    st.header("TRENDING NOW") 
    
    products_in_category = [p for p in DATA_PRODUCTS if p.category_id == selected_category_id]
    filtered_products = current_filter.apply(products_in_category)

    st.subheader(f"Displaying {len(filtered_products)} items in {selected_category_name}")
    
    cols = st.columns(3)
    for i, product in enumerate(filtered_products):
        with cols[i % 3]:
            display_product_card(product)

def page_checkout():
    """Halaman Checkout dan Pembayaran."""
    st.title("💸 Checkout & Payment")
    
    cart_items = st.session_state.cart_obj.items()
    total_price = st.session_state.cart_obj.calculate_total()

    if not cart_items:
        st.warning("Keranjang belanja Anda kosong. Silakan kembali ke katalog.")
        st.button("Kembali ke Katalog", on_click=set_page, args=('katalog',), key="back_from_empty")
        return

    col_cart, col_summary = st.columns([2, 1])

    with col_cart:
        st.subheader("Item di Keranjang")
        
        # Display menggunakan DataFrame agar mirip dengan tabel
        cart_data = []
        for i, item in enumerate(cart_items):
            product = next((p for p in DATA_PRODUCTS if p.product_id == item.product_id), None)
            cart_data.append({
                "Nama Produk": product.name if product else "N/A",
                "Variasi": f"{item.color}/{item.size}",
                "Harga Satuan": item.product_price,
                "Qty": item.qty,
                "Subtotal": item.total_price,
                "Key": f"{item.product_id}-{item.size}-{item.color}" # Key unik untuk update
            })
        
        df_cart = pd.DataFrame(cart_data)
        
        st.dataframe(df_cart[['Nama Produk', 'Variasi', 'Harga Satuan', 'Qty', 'Subtotal']], hide_index=True)

        # Bagian Update/Remove (Mirip dengan contoh yang Anda berikan)
        st.divider()
        st.subheader("Kelola Keranjang")
        
        # FIX: Menggunakan format key unik untuk selectbox
        item_keys = [item['Key'] for item in cart_data]
        if item_keys:
            selected_key = st.selectbox("Pilih Item", item_keys, format_func=lambda k: next(d['Nama Produk'] + " " + d['Variasi'] for d in cart_data if d['Key'] == k), key="checkout_sel_item")
            
            selected_data = next(d for d in cart_data if d['Key'] == selected_key)
            
            p_id, size, color = selected_key.split('-')
            p_id = int(p_id)
            
            col_u1, col_u2 = st.columns(2)
            with col_u1:
                new_qty = st.number_input("Jumlah Baru", min_value=0, value=selected_data['Qty'], step=1, key="checkout_qty")
            
            with col_u2:
                if st.button("Perbarui / Hapus", key="checkout_update_btn"):
                    st.session_state.cart_obj.update_item_qty(p_id, size, color, new_qty)
                    st.toast("Keranjang diperbarui!")
                    st.experimental_rerun()
            
    with col_summary:
        st.subheader("Order Summary")
        shipping_address = st.session_state.user.address
        
        st.markdown(f"*Total Harga:* **${total_price:.2f}**")
        st.markdown(f"*Alamat Pengiriman:* {shipping_address}")

        st.divider()
        st.subheader("Payment")
        payment_method = st.selectbox("Pilih Metode Pembayaran", ["Transfer Bank", "E-Wallet", "Credit Card"])
        
        if st.button("Confirm Order & Pay", use_container_width=True, type="primary"):
            checkout_obj = Checkout(
                checkout_id=random.randint(1000, 9999), 
                user_id=st.session_state.user.user_id, 
                total_price=total_price, 
                shipping_address=shipping_address
            )
            
            if checkout_obj.verify_order():
                payment_obj = checkout_obj.proceed_to_payment(payment_method)
                
                if payment_obj.process_payment(total_price):
                    st.session_state.cart_obj.clear() 
                    set_page('success')
                else:
                    st.error("Gagal memproses pembayaran. Coba lagi.")
            st.rerun()

    if st.button("⬅️ Back to Catalog", on_click=set_page, args=('katalog',)):
        pass

def page_success():
    """Halaman Konfirmasi Sukses."""
    st.title("✅ Pesanan Berhasil Dibuat!")
    st.balloons()
    st.info(f"Terima kasih, {st.session_state.user.name}. Pesanan Anda akan segera dikirim.")
    if st.button("Mulai Belanja Lagi", on_click=set_page, args=('katalog',)):
        pass

# --- E. LOGIKA NAVIGASI UTAMA ---
def main():
    if st.session_state.page == 'katalog':
        page_katalog()
    elif st.session_state.page == 'checkout':
        page_checkout()
    elif st.session_state.page == 'success':
        page_success()

if __name__ == "__main__":
    main()
