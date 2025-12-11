# katalog_crud_upgrade.py - Upgrade Kasir CRUD menjadi Katalog Loopé Themed

import streamlit as st

# --- KELAS & REPOSITORI (DIKOREKSI DAN DIUPGRADE) ---

class Product:
    """Merepresentasikan item dengan validasi properti."""
    def __init__(self, name: str, price: float, image_url: str = "https://via.placeholder.com/150x150?text=LOOPÉ"):
        # FIX: Mengganti _init_ menjadi __init__
        self._name = None
        self._price = None
        self.name = name
        self.price = price
        self.image_url = image_url # Tambahan URL Gambar

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Nama produk harus berupa string tidak kosong.")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not (isinstance(value, (int, float)) and value >= 0):
            raise ValueError("Harga harus angka >= 0.")
        self._price = float(value)

    def subtotal(self, qty: int):
        return self.price * qty

    def display_price(self):
        return f"Rp {self.price:,.0f}"


class Cart:
    """Mengelola kumpulan item keranjang."""
    def __init__(self):
        # FIX: Mengganti _init_ menjadi __init__
        # items: list of dict {'product': Product, 'qty': int}
        self.items = []

    def add_item(self, product: Product, qty: int):
        for it in self.items:
            if it["product"].name == product.name:
                it["qty"] += qty
                return
        self.items.append({"product": product, "qty": qty})

    def update_item(self, product_name: str, qty: int):
        for it in self.items:
            if it["product"].name == product_name:
                if qty <= 0:
                    self.items.remove(it)
                else:
                    it["qty"] = qty
                return

    def remove_item(self, product_name: str):
        self.items = [it for it in self.items if it["product"].name != product_name]

    def clear(self):
        self.items = []

    def total(self):
        return sum(it["product"].subtotal(it["qty"]) for it in self.items)

    def receipt_text(self):
        lines = []
        for it in self.items:
            p = it["product"]
            q = it["qty"]
            lines.append(f"{p.name} x{q} = Rp {p.subtotal(q):,.0f}")
        lines.append("-" * 30)
        lines.append(f"TOTAL = Rp {self.total():,.0f}")
        return "\n".join(lines)


class ProductRepository:
    """Mengelola CRUD untuk Product."""
    def __init__(self, initial=None):
        # FIX: Mengganti _init_ menjadi __init__
        self._products = initial[:] if initial else []

    def create_product(self, name: str, price: float, image_url: str = None):
        if self.get_by_name(name) is not None:
            raise ValueError("Produk dengan nama sama sudah ada.")
        p = Product(name, price, image_url)
        self._products.append(p)
        return p

    def get_all(self):
        return list(self._products)

    def get_by_name(self, name: str):
        for p in self._products:
            if p.name == name:
                return p
        return None

    def update_product(self, old_name: str, new_name: str = None, new_price: float = None):
        p = self.get_by_name(old_name)
        if p is None:
            raise ValueError("Produk tidak ditemukan.")
        if new_name and new_name != old_name and self.get_by_name(new_name):
            raise ValueError("Nama baru sudah digunakan produk lain.")
        if new_name:
            p.name = new_name
        if new_price is not None:
            p.price = new_price
        return p

    def delete_product(self, name: str):
        p = self.get_by_name(name)
        if p is None:
            raise ValueError("Produk tidak ditemukan.")
        self._products.remove(p)


# --- DATA AWAL (Upgrade untuk Tema Loopé) ---
# Menggunakan harga yang lebih kecil dan gambar yang relevan

default_catalog = [
    Product("Pink T-shirt", 17.00, "https://i.imgur.com/W2zU98S.png"), 
    Product("Rok Mini Plaid", 12.00, "https://i.imgur.com/g0t6XkM.png"), 
    Product("Black Tank Top", 18.00, "https://i.imgur.com/vHqP4Yn.png"),
    Product("Jogger Pants", 35.00, "https://i.imgur.com/7b58UoJ.png"),
]


# --- THEME DAN STYLE (CSS Injection untuk Warna Loopé) ---

def apply_custom_css():
    """Mengatur tema warna (Pink/Magenta Loopé) pada tombol utama."""
    st.markdown(f"""
        <style>
            /* Mengubah warna tombol utama menjadi pink/magenta */
            .stButton>button {{
                background-color: #F04D9D;
                color: white;
                border-radius: 8px;
                border: 1px solid #F04D9D;
            }}
            .stButton>button:hover {{
                background-color: #FF66A3;
                color: white;
            }}
            /* Mengubah warna form submit */
            .st-emotion-cache-1jicfl2 {{ 
                background-color: #F04D9D !important;
                color: white !important;
            }}
            h1, h2, h3, h4 {{
                color: #B53F77; /* Warna judul mendekati pink */
            }}
        </style>
    """, unsafe_allow_html=True)


# --- STREAMLIT UI (Full Bahasa Indonesia) ---

# Terapkan CSS custom
apply_custom_css()

st.markdown(f'<div style="background-color: #F04D9D; padding: 10px; border-radius: 5px;"><h1 style="color: white; text-align: center;">KATALOG & KASIR LOOPÉ</h1></div>', unsafe_allow_html=True)
st.subheader("Sistem Pengelolaan Produk dan Keranjang")

# Initialize repo and cart di session state
if "repo" not in st.session_state:
    st.session_state.repo = ProductRepository(initial=default_catalog)
if "cart" not in st.session_state:
    st.session_state.cart = Cart()
if 'unique_key_counter' not in st.session_state:
    st.session_state.unique_key_counter = 0

def get_unique_key():
    """Menghasilkan kunci unik untuk tombol/widget agar Streamlit tidak crash."""
    st.session_state.unique_key_counter += 1
    return f"key_{st.session_state.unique_key_counter}"


# --- TAB UTAMA: KATALOG & KERANJANG ---
tab_katalog, tab_cart, tab_crud = st.tabs(["🛍️ Katalog Produk", "🛒 Keranjang Belanja", "⚙️ Kelola CRUD"])


# --- 1. TAB KATALOG PRODUK ---
with tab_katalog:
    st.header("Katalog Produk")
    st.markdown("Pilih produk di bawah ini dan masukkan ke keranjang.")
    
    products = st.session_state.repo.get_all()
    
    # Tampilkan Produk dalam grid 3 kolom
    cols = st.columns(3)
    
    if not products:
        st.info("Belum ada produk di katalog.")
    
    for i, p in enumerate(products):
        with cols[i % 3]:
            with st.container(border=True):
                st.image(p.image_url, caption=p.name, width=150)
                st.markdown(f"**{p.name}**")
                st.markdown(f"Harga: **{p.display_price()}**")

                col_sel, col_btn = st.columns([1, 1])
                
                with col_sel:
                    qty = st.number_input("Jumlah", min_value=1, value=1, step=1, key=f"qty_sel_{p.name}")
                
                with col_btn:
                    # Tombol Tambah ke Keranjang
                    if st.button("Tambah", key=f"add_{p.name}", use_container_width=True):
                        st.session_state.cart.add_item(p, qty)
                        st.success(f"'{p.name}' x{qty} ditambahkan ke keranjang.")

# --- 2. TAB KERANJANG BELANJA ---
with tab_cart:
    st.header("Keranjang Belanja")
    
    if not st.session_state.cart.items:
        st.info("Keranjang masih kosong.")
    else:
        st.subheader("Isi Keranjang Saat Ini")
        
        # Tampilkan dalam format tabel/dataframe
        cart_data = []
        for it in st.session_state.cart.items:
            p = it["product"]
            q = it["qty"]
            cart_data.append({
                "Nama Produk": p.name,
                "Harga Satuan": p.display_price(),
                "Jumlah (Qty)": q,
                "Subtotal": f"Rp {p.subtotal(q):,.0f}"
            })
        
        df_cart = pd.DataFrame(cart_data)
        st.dataframe(df_cart, hide_index=True, use_container_width=True)

        st.metric("TOTAL PEMBAYARAN", f"Rp {st.session_state.cart.total():,.0f}")
        
        # Form untuk Mengelola Keranjang (Update/Hapus)
        st.divider()
        st.subheader("Kelola Item")
        
        item_names = [it["product"].name for it in st.session_state.cart.items]
        
        if item_names:
            sel_item_name = st.selectbox("Pilih Produk", item_names, key="cart_sel_edit")
            current_qty = next(it["qty"] for it in st.session_state.cart.items if it["product"].name == sel_item_name)
            
            col_uq, col_ub = st.columns(2)
            with col_uq:
                upd_qty = st.number_input("Jumlah Baru (0 untuk Hapus)", min_value=0, value=current_qty, step=1, key="cart_upd_qty")
            
            with col_ub:
                st.markdown("<br>", unsafe_allow_html=True) # Jarak agar tombol sejajar
                if st.button("Perbarui Item", key="cart_update_btn", use_container_width=True):
                    st.session_state.cart.update_item(sel_item_name, int(upd_qty))
                    st.success(f"Jumlah '{sel_item_name}' diperbarui.")
                    st.experimental_rerun()
        
        st.divider()
        
        col_reset, col_nota = st.columns(2)
        with col_reset:
            if st.button("Reset Keranjang", type="secondary"):
                st.session_state.cart.clear()
                st.warning("Keranjang direset!")
                st.experimental_rerun()
        with col_nota:
            if st.button("Tampilkan Nota Pembelian", type="primary"):
                st.text("NOTA PEMBELIAN:")
                st.code(st.session_state.cart.receipt_text())

# --- 3. TAB PENGELOLAAN CRUD PRODUK ---
with tab_crud:
    st.header("⚙️ Pengelolaan Produk (CRUD)")
    
    st.subheader("Daftar Produk Saat Ini")
    products_list = st.session_state.repo.get_all()
    
    if products_list:
        data_table = [{
            "Nama": p.name, 
            "Harga": p.display_price(), 
            "URL Gambar": p.image_url
        } for p in products_list]
        st.dataframe(pd.DataFrame(data_table), hide_index=True, use_container_width=True)
    else:
        st.info("Tidak ada produk di repositori.")

    st.divider()

    # Form Tambah Produk (Create)
    with st.form("form_add_crud"):
        st.subheader("Tambah Produk Baru")
        new_name = st.text_input("Nama produk", key="crud_add_name")
        new_price = st.number_input(
            "Harga (Rp)", min_value=0, value=10000, step=5000, key="crud_add_price"
        )
        new_image = st.text_input("URL Gambar (Opsional)", key="crud_add_image")
        submitted = st.form_submit_button("Tambah Produk Baru", type="primary")
        
        if submitted:
            try:
                st.session_state.repo.create_product(new_name, new_price, new_image)
                st.success(f"Produk '{new_name}' berhasil ditambahkan.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Gagal menambahkan produk: {str(e)}")

    st.divider()

    # Form Update / Delete Produk
    st.subheader("Edit / Hapus Produk")
    product_names = [p.name for p in products_list]
    
    if product_names:
        sel = st.selectbox("Pilih produk yang ingin diedit/dihapus", product_names, key="crud_sel_edit")
        p_edit = st.session_state.repo.get_by_name(sel)
        
        col1, col2 = st.columns(2)
        with col1:
            upd_name = st.text_input("Nama baru", value=p_edit.name, key="crud_upd_name")
        with col2:
            upd_price = st.number_input(
                "Harga baru", min_value=0, value=int(p_edit.price), step=5000, key="crud_upd_price"
            )
        upd_image = st.text_input("URL Gambar baru", value=p_edit.image_url, key="crud_upd_image")

        if st.button("Simpan Perubahan", key="crud_save_btn", type="primary"):
            try:
                st.session_state.repo.update_product(
                    p_edit.name, new_name=upd_name, new_price=upd_price
                )
                # Update URL gambar secara manual (karena setter/getter tidak mencakup ini di kode Anda)
                p_edit.image_url = upd_image
                st.success("Produk berhasil diperbarui.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Gagal menyimpan perubahan: {str(e)}")
        
        if st.button("Hapus Produk Ini", key="crud_delete_btn"):
            try:
                st.session_state.repo.delete_product(p_edit.name)
                # Hapus dari keranjang juga
                st.session_state.cart.remove_item(p_edit.name)
                st.warning(f"Produk '{p_edit.name}' telah dihapus.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Gagal menghapus produk: {str(e)}")
    else:
        st.info("Tidak ada produk untuk diedit/dihapus.")
