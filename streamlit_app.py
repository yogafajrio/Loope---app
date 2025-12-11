# katalog_loope_final.py - Aplikasi Katalog Loopé (Baby Pink Theme & Fix Cart)

import streamlit as st
import random 
import pandas as pd
import time # Untuk simulasi loading

# --- A. DEFINISI KELAS (Mengacu pada Diagram Class PPT) ---

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
        self.image_url = image_url if image_url else "https://via.placeholder.com/200x200?text=LOOPÉ"
        
    def display_price(self):
        # Menggunakan format USD karena data dummy dalam USD
        return f"${self.price:.2f}"

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
        found = False
        for item in st.session_state.cart_items:
            # FIX PENTING: Pengecekan harus berdasarkan ID, Size, dan Color
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
        
        # Hapus item lama yang sesuai
        st.session_state.cart_items = [
            item for item in st.session_state.cart_items 
            if not (item.product_id == product_id and item.size == size and item.color == color)
        ]
        
        if new_qty > 0:
            product = next(p for p in DATA_PRODUCTS if p.product_id == product_id)
            new_item = CartItem(product_id, size, color, new_qty, product.price)
            st.session_state.cart_items.append(new_item)

class Filter:
    # Filter class
    pass

class Checkout:
    # Checkout class
    def __init__(self, checkout_id, user_id, total_price, shipping_address):
        self.checkout_id = checkout_id
        self.user_id = user_id
        self.total_price = total_price
        self.shipping_address = shipping_address
    def verify_order(self): return True
    def proceed_to_payment(self, method): return Payment(payment_id=random.randint(2000, 9999), method=method)

class Payment:
    # Payment class
    def __init__(self, payment_id, method, status="pending"):
        self.payment_id = payment_id
        self.method = method
        self.status = status
    def process_payment(self, total_price):
        self.status = "paid"
        return self.status == "paid"

# --- B. DATA DUMMY (Sesuai Gambar PPT) ---
# Menggunakan link gambar agar sesuai dengan tema Loopé

DATA_PRODUCTS = [
    # Data 1: Pink T-shirt
    Product(101, 1, "Pink T-shirt", 17.00, "Kaos warna pink yang lucu.", ["Pink", "Putih"], ["S", "M", "L"], 
            "https://cdn-img.prettylittlething.com/1/f/6/e/1f6ef32b4f56aef20f9f1d174fe42839ff392211_cmb4452_1.jpg"), 
    # Data 2: Plaid Mini Skirt
    Product(102, 2, "Rok Mini Plaid", 12.00, "Rok mini motif plaid trendi.", ["Plaid Pink", "Abu-abu"], ["XS", "S", "M"],
            "https://i.imgur.com/g0t6XkM.png"), 
    # Data 3: Black Tank Top (diganti ke Jogger Pants Pink untuk variasi)
    Product(103, 2, "Jogger Pants Pink", 35.00, "Celana jogger super nyaman.", ["Pink", "Hitam"], ["L", "XL"],
            "https://i.imgur.com/7b58UoJ.png"), 
    # Data 4: Cropped Cardi
    Product(104, 1, "Cardigan Crop", 20.00, "Cardigan rajut crop untuk OOTD.", ["Pink", "Putih"], ["S", "M"],
            "https://i.imgur.com/T0yD7E1.png"), 
    # Data 5: Grey Skirt (dibuat mirip dengan produk di gambar)
     Product(105, 2, "Rok Mini Abu", 12.00, "Rok mini kasual warna abu.", ["Abu-abu"], ["XS", "S", "M"],
            "https://i.imgur.com/7d5b8yY.png"), 
]

DATA_CATEGORIES = [
    Category(1, "Atasan", "Pakaian bagian atas"),
    Category(2, "Bawahan", "Pakaian bagian bawah"),
]

# --- C. THEME DAN STYLE (Baby Pink) ---

def apply_custom_css():
    """Mengatur tema warna ke Baby Pink/Soft Magenta."""
    st.markdown(f"""
        <style>
            /* Warna Dasar: Baby Pink/Soft Magenta */
            :root {{
                --loop-pink: #FF99CC; 
                --loop-pink-dark: #F04D9D;
                --loop-purple: #E0B0FF;
            }}
            /* Sidebar background */
            [data-testid="stSidebar"] {{
                background-color: var(--loop-pink);
            }}
            /* Mengubah warna tombol utama (primary) */
            .stButton > button {{
                background-color: var(--loop-pink-dark);
                color: white;
                border-radius: 8px;
                border: 1px solid var(--loop-pink-dark);
            }}
            .stButton > button:hover {{
                background-color: var(--loop-pink);
                border: 1px solid var(--loop-pink-dark);
                color: white;
            }}
            /* Mengubah warna form submit button */
            .st-emotion-cache-1jicfl2 {{
                background-color: var(--loop-pink-dark) !important;
                color: white !important;
            }}
            /* Custom Header/Brand Area */
            .loop-header {{
                background-color: var(--loop-pink-dark);
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            .loop-header h1 {{
                color: white;
                text-align: center;
                margin: 0;
            }}
            /* Custom text color for headings */
            h1, h2, h3, h4 {{
                color: #A03370; /* Deep Pink/Maroon for contrast */
            }}
            /* Cart button in header */
            .header-cart-btn button {{
                background-color: var(--loop-purple) !important;
                border-color: var(--loop-purple) !important;
                font-weight: bold;
                color: black !important;
            }}
        </style>
    """, unsafe_allow_html=True)


# --- D. FUNGSI LOGIKA & SESI STREAMLIT ---

# Inisialisasi Session State
if 'user' not in st.session_state:
    st.session_state.user = User(5056241024, "Agni Putri", "agni@example.com", "securepwd", "Jl. Contoh No. 123")
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = [] # List CartItem
if 'cart_obj' not in st.session_state:
    st.session_state.cart_obj = Cart(cart_id=1, user_id=st.session_state.user.user_id)
if 'page' not in st.session_state:
    st.session_state.page = 'katalog' 

def set_page(page_name):
    st.session_state.page = page_name

def add_to_cart_callback(product_id, size, color, qty=1):
    product = next(p for p in DATA_PRODUCTS if p.product_id == product_id)
    cart_item = CartItem(
        product_id=product.product_id,
        size=size,
        color=color,
        qty=qty,
        product_price=product.price
    )
    st.session_state.cart_obj.add_item(cart_item)
    st.toast(f"✅ Item ditambahkan: {product.name} ({color}, {size})")
    # Tidak perlu rerun, toast sudah cukup.

# --- E. FUNGSI TAMPILAN Halaman ---

def display_header():
    """Menampilkan Header (Judul 'Loope') dan Tombol Cart/Checkout."""
    st.markdown('<div class="loop-header"><h1>LOOPÉ</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col2:
        cart_total = st.session_state.cart_obj.calculate_total()
        st.markdown('<div class="header-cart-btn">', unsafe_allow_html=True)
        st.button(
            f"🛒 Checkout (${cart_total:.2f})",
            on_click=set_page,
            args=('checkout',),
            key="header_cart_button"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

def display_product_card(product):
    """Menampilkan satu produk dalam format card (mirip gambar)."""
    with st.container(border=True):
        st.image(product.image_url, caption=f"ID: {product.product_id}", width=150)
        
        # Nama dan Harga di kolom terpisah
        col_name, col_price = st.columns([2, 1])
        with col_name:
            st.markdown(f"**{product.name}**")
        with col_price:
            st.markdown(f"**{product.display_price()}**")

        st.markdown(f"_{product.description[:20]}..._")
        
        # Pilihan Variasi
        key_base = f"prod_{product.product_id}"
        col_s, col_c = st.columns(2)
        with col_s:
            selected_size = st.selectbox("Ukuran", product.sizes, key=f"size_{key_base}")
        with col_c:
            selected_color = st.selectbox("Warna", product.colors, key=f"color_{key_base}")

        # Tombol Add to Cart
        st.button(
            "Tambah ke Keranjang",
            key=f"add_{key_base}",
            on_click=add_to_cart_callback,
            args=(product.product_id, selected_size, selected_color, 1),
            use_container_width=True
        )

def page_katalog():
    """Halaman utama katalog dengan Filter dan Grid Produk."""
    display_header()
    
    # Sidebar untuk Filter
    with st.sidebar:
        st.header("Saring")
        st.info(f"Halo, {st.session_state.user.name}!")
        
        # Filter (hanya untuk tampilan, karena kode di PPT tidak detail)
        category_map = {c.name: c.category_id for c in DATA_CATEGORIES}
        selected_category_name = st.selectbox("Kategori", list(category_map.keys()))
        
        # Jika Anda ingin menambahkan filter, masukkan logikanya di sini

    st.subheader("TRENDING NOW") 
    st.info(f"Menampilkan item di kategori: **{selected_category_name}**")
    
    products_in_category = [p for p in DATA_PRODUCTS if p.category_id == category_map[selected_category_name]]
    # Filter diterapkan di sini (saat ini hanya filter kategori)

    cols = st.columns(3) # Tampilkan 3 kolom produk
    for i, product in enumerate(products_in_category):
        with cols[i % 3]:
            display_product_card(product)

def page_checkout():
    """Halaman Checkout dan Pembayaran."""
    st.title("💸 Keranjang & Pembayaran")
    
    cart_items = st.session_state.cart_obj.items()
    total_price = st.session_state.cart_obj.calculate_total()

    if not cart_items:
        st.warning("Keranjang belanja Anda kosong. Tambahkan item di halaman katalog.")
        st.button("⬅️ Kembali ke Katalog", on_click=set_page, args=('katalog',), key="back_from_empty")
        return

    col_cart, col_summary = st.columns([2, 1])

    with col_cart:
        st.subheader("Item di Keranjang")
        
        cart_data = []
        for item in cart_items:
            product = next((p for p in DATA_PRODUCTS if p.product_id == item.product_id), None)
            key = f"{item.product_id}-{item.size}-{item.color}" 
            cart_data.append({
                "Nama Produk": product.name if product else "N/A",
                "Variasi": f"{item.color} ({item.size})",
                "Harga Satuan": item.product_price,
                "Qty": item.qty,
                "Subtotal": item.total_price,
                "Key": key
            })
        
        df_cart = pd.DataFrame(cart_data)
        df_cart['Harga Satuan'] = df_cart['Harga Satuan'].apply(lambda x: f"${x:.2f}")
        df_cart['Subtotal'] = df_cart['Subtotal'].apply(lambda x: f"${x:.2f}")

        st.dataframe(df_cart[['Nama Produk', 'Variasi', 'Harga Satuan', 'Qty', 'Subtotal']], hide_index=True, use_container_width=True)

        st.divider()
        st.subheader("Kelola Jumlah Item")
        
        item_keys = [item['Key'] for item in cart_data]
        if item_keys:
            # Menggunakan format_func untuk menampilkan nama produk + variasi
            selected_key = st.selectbox("Pilih Item", item_keys, 
                                        format_func=lambda k: next(d['Nama Produk'] + " " + d['Variasi'] for d in cart_data if d['Key'] == k), 
                                        key="checkout_sel_item")
            
            selected_data = next(d for d in cart_data if d['Key'] == selected_key)
            
            p_id, size, color = selected_key.split('-')
            p_id = int(p_id)
            
            col_u1, col_u2 = st.columns(2)
            with col_u1:
                new_qty = st.number_input("Jumlah Baru (0 untuk Hapus)", min_value=0, value=selected_data['Qty'], step=1, key="checkout_qty")
            
            with col_u2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Perbarui Item", key="checkout_update_btn", use_container_width=True):
                    st.session_state.cart_obj.update_item_qty(p_id, size, color, new_qty)
                    st.toast("Keranjang diperbarui!")
                    st.experimental_rerun()
            
    with col_summary:
        st.subheader("Ringkasan Pesanan")
        shipping_address = st.session_state.user.address
        
        st.metric("Total Pembayaran", f"${total_price:.2f}")
        st.info(f"Dikirim ke: {shipping_address}")

        st.divider()
        st.subheader("Pembayaran")
        payment_method = st.selectbox("Pilih Metode", ["Transfer Bank", "E-Wallet", "Kartu Kredit"])
        
        if st.button("Konfirmasi Pesanan & Bayar", use_container_width=True, type="primary"):
            # Simulasi Proses Pembayaran
            with st.spinner('Memproses pembayaran...'):
                time.sleep(1) 
            
            checkout_obj = Checkout(random.randint(1000, 9999), st.session_state.user.user_id, total_price, shipping_address)
            if checkout_obj.verify_order():
                payment_obj = checkout_obj.proceed_to_payment(payment_method)
                
                if payment_obj.process_payment(total_price):
                    st.session_state.cart_obj.clear() 
                    set_page('success')
                else:
                    st.error("Gagal memproses pembayaran. Coba lagi.")
            st.rerun()

    if st.button("⬅️ Kembali ke Katalog"):
        set_page('katalog')
        st.rerun()

def page_success():
    """Halaman Konfirmasi Sukses."""
    st.title("✅ PESANAN BERHASIL!")
    st.balloons()
    st.success(f"Terima kasih, {st.session_state.user.name}. Pembayaran Anda sudah dikonfirmasi.")
    st.info("Anda akan diarahkan kembali ke katalog.")
    if st.button("Mulai Belanja Lagi", type="primary"):
        set_page('katalog')
        st.experimental_rerun()

# --- F. LOGIKA NAVIGASI UTAMA ---
def main():
    apply_custom_css()
    if st.session_state.page == 'katalog':
        page_katalog()
    elif st.session_state.page == 'checkout':
        page_checkout()
    elif st.session_state.page == 'success':
        page_success()

if __name__ == "__main__":
    main()
