# main.py - Simulasi Penggunaan Aplikasi Loope

# from models import User, Category, Product, CartItem, Cart, Filter, Checkout, Payment

# --- Data Dummy ---
# Categories
CAT_T = Category(1, "Tops", "Pakaian atasan")
CAT_B = Category(2, "Bottoms", "Pakaian bawahan")

# Products
PRODUCT_DATA = [
    Product(101, 1, "Pink T-shirt", 17.00, "So fetch!", ["Pink", "White"], ["S", "M", "L"]), 
    Product(102, 2, "Plaid Mini Skirt", 12.00, "Trending Now", ["Pink Plaid", "Grey"], ["XS", "S", "M"]),
    Product(103, 1, "Black Tank Top", 18.00, "Sparkly tank top", ["Black", "Silver"], ["S", "M"]),
    Product(104, 2, "Blue Jeans", 30.00, "Classic denim", ["Blue", "Dark Blue"], ["S", "M", "L"]),
]

# User
agni = User(5056241024, "Agni Putri", "agni@example.com", "securepwd", "Jl. Contoh No. 123") 
# Keranjang belanja dibuat saat user login atau pertama kali mengakses
user_cart = Cart(cart_id=1, user_id=agni.user_id) 

# =========================================================
print("=========================================")
print("SIMULASI APLIKASI LOOPÉ (Katalog & Transaksi)")
print("=========================================\n")


# --- STEP 1: LOGIN dan EXPLORE ---
print("## STEP 1: LOGIN & KATEGORI ##")
if agni.login("securepwd"):
    print(f"1. Login berhasil untuk: {agni.name}")
    
    # User memilih kategori 'Tops'
    selected_category_name = agni.select_category(CAT_T.name)
    
    # Mendapatkan produk di kategori tersebut
    products_in_category = CAT_T.get_products(PRODUCT_DATA)
    print(f"2. Produk di kategori {selected_category_name}: {len(products_in_category)} item.")
    print(f"   Contoh Produk: {products_in_category[0].name}")
    
    # Melihat detail produk
    print("\n3. Detail Produk 104 (Blue Jeans):")
    details = PRODUCT_DATA[3].get_detail()
    for key, value in details.items():
        print(f"   - {key}: {value}")
else:
    print("Login Gagal.")
    exit()

print("\n" + "="*30 + "\n")


# --- STEP 2: FILTERING ---
print("## STEP 2: FILTERING ##")
# Membuat Filter: Harga Max $20.00, Warna Pink
my_filter = Filter(color="Pink", max_price=20.00)

# Menerapkan filter ke semua produk
filtered_items = my_filter.apply(PRODUCT_DATA)

print(f"1. Filter diterapkan (Warna: Pink, Harga Max: $20.00)")
print(f"2. Ditemukan {len(filtered_items)} Produk:")
for p in filtered_items:
    print(f"   - ID {p.product_id}: {p.name} (${p.price:.2f})")

print("\n" + "="*30 + "\n")


# --- STEP 3: ADD TO CART ---
print("## STEP 3: ADD TO CART ##")
# Product 101 (Pink T-shirt): Qty 1, Size M, Color Pink
item1 = CartItem(PRODUCT_DATA[0].product_id, "M", "Pink", 1, PRODUCT_DATA[0].price)

# Product 103 (Black Tank Top): Qty 2, Size S, Color Black
item2 = CartItem(PRODUCT_DATA[2].product_id, "S", "Black", 2, PRODUCT_DATA[2].price)

user_cart.add_item(item1)
agni.add_to_cart(PRODUCT_DATA[0].product_id, "M", "Pink", 1) # Simulasi method User
user_cart.add_item(item2)

print("\n1. Isi Keranjang Saat Ini:")
for item in user_cart.items():
    print(f"   -> {item}")
    
total_price = user_cart.calculate_total()
print(f"2. Total Harga Keranjang: ${total_price:.2f}")

print("\n" + "="*30 + "\n")


# --- STEP 4: CHECKOUT & PAYMENT ---
print("## STEP 4: CHECKOUT & PAYMENT ##")
agni.checkout() 

checkout_obj = Checkout(
    checkout_id=1001, 
    user_id=agni.user_id, 
    total_price=total_price, 
    shipping_address=agni.address
)

if checkout_obj.verify_order():
    payment_obj = checkout_obj.proceed_to_payment()
    
    # Proses Pembayaran
    if payment_obj.process_payment(total_price):
        # Konfirmasi oleh User (Simulasi)
        if agni.confirm_payment() and payment_obj.confirm_payment():
            print("\n✅ PEMBAYARAN SUKSES! Pesanan Anda sedang diproses.")
        else:
            print("❌ Konfirmasi Pembayaran Gagal.")
    else:
        print("❌ Pemrosesan Pembayaran Gagal.")
