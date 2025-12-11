class User:

    def _init_(self, user_id, name, email, password, address):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password  
        self.address = address

    # Operasi (Methods)
    def login(self, entered_password):
        """Simulasi login."""
        return self.password == entered_password

    def update_profile(self, new_address):
        """Memperbarui alamat pengguna."""
        self.address = new_address
        print(f"Profile updated. New address: {self.address}")
        
    def select_category(self, category_name):
        """Simulasi memilih kategori."""
        print(f"User selected category: {category_name}")
        return category_name
        
    def apply_filter(self, filter_obj):
        """Simulasi menerapkan filter."""
        print("User applied a filter.")
        # Diimplementasikan lebih lanjut di Class Filter.

    def add_to_cart(self, product_id, size, color, qty):
        """Simulasi menambahkan produk ke keranjang."""
        print(f"Product {product_id} added to cart.")
        # Logika nyata memerlukan interaksi dengan objek Cart.

    def checkout(self):
        """Memulai proses checkout."""
        print("Initiating checkout process.")
        # Logika nyata akan membuat objek Checkout.

    def confirm_payment(self):
        """Konfirmasi pembayaran pesanan."""
        print("Payment confirmed.")
        # Logika nyata akan berinteraksi dengan objek Payment.


class Category:
    """
    Merepresentasikan kategori produk.
    Atribut: categoryId (int), name (string), description (string).
    """
    def _init_(self, category_id, name, description=""):
        self.category_id = category_id
        self.name = name
        self.description = description

    def get_products(self, all_products):
        """Mengambil produk dalam kategori ini dari daftar semua produk."""
        return [p for p in all_products if getattr(p, 'category_id', None) == self.category_id]


class Product:
    """
    Merepresentasikan item fashion dalam katalog.
    Atribut: productId (int), name (string), price (float), description (string), colors (list<string>), sizes (list<string>), images (list<string>).
    """
    def _init_(self, product_id, category_id, name, price, description="", colors=None, sizes=None, images=None):
        self.product_id = product_id
        self.category_id = category_id  
        self.name = name
        self.price = price
        self.description = description
        self.colors = colors if colors is not None else []
        self.sizes = sizes if sizes is not None else []
        self.images = images if images is not None else []

    def get_detail(self):
        """Mengembalikan detail lengkap produk."""
        return {
            "ID": self.product_id,
            "Nama": self.name,
            "Harga": f"${self.price:.2f}",
            "Deskripsi": self.description,
            "Warna Tersedia": ", ".join(self.colors),
            "Ukuran Tersedia": ", ".join(self.sizes)
        }

    def is_available(self, size, color):
        """Memeriksa ketersediaan produk dalam ukuran dan warna tertentu."""
        return size in self.sizes and color in self.colors


class CartItem:
    """
    Merepresentasikan satu produk dalam keranjang, termasuk variasi dan jumlahnya.
    Atribut: productId (int), size (string), color (string), qty (int), totalPrice (float).
    """
    def _init_(self, product_id, size, color, qty, product_price):
        self.product_id = product_id
        self.size = size
        self.color = color
        self.qty = qty
        self.total_price = qty * product_price 

    def _str_(self):
        return f"{self.qty}x Product ID {self.product_id} ({self.color}/{self.size}) - Subtotal: ${self.total_price:.2f}"


class Cart:
    """
    Menyimpan kumpulan item (CartItem) yang dipilih pengguna.
    Atribut: cartId (int), userId (int).
    """
    def _init_(self, cart_id, user_id):
        self.cart_id = cart_id
        self.user_id = user_id
        self._items = []  # list<CartItem>

    # Operasi (Methods)
    def items(self):
        """Mengembalikan daftar item dalam keranjang."""
        return self._items

    def add_item(self, cart_item):
        """Menambahkan item ke keranjang."""
        self._items.append(cart_item)

    def update_item(self, product_id, new_qty):
        """Memperbarui kuantitas item."""
        for item in self._items:
            if item.product_id == product_id:
                # Perlu logika untuk menghitung ulang totalPrice
                item.qty = new_qty
                # Logika update price di sini...
                return True
        return False

    def remove_item(self, product_id):
        """Menghapus item dari keranjang."""
        self._items = [item for item in self._items if item.product_id != product_id]

    def clear(self):
        """Mengosongkan keranjang."""
        self._items = []
        
    def calculate_total(self):
        """Menghitung total harga keranjang."""
        return sum(item.total_price for item in self._items)


class Filter:
    """
    Menyediakan filter untuk menyaring produk berdasarkan kriteria.
    Atribut: size (string), color (string), minPrice (float), maxPrice (float).
    """
    def _init_(self, size=None, color=None, min_price=None, max_price=None):
        self.size = size
        self.color = color
        self.min_price = min_price
        self.max_price = max_price

    def apply(self, products):
        """Menerapkan filter ke daftar produk."""
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
    """
    Mewakili proses pengecekan sebelum pembayaran.
    Atribut: checkoutId (int), userId (int), totalPrice (float), shippingAddress (string).
    """
    def _init_(self, checkout_id, user_id, total_price, shipping_address):
        self.checkout_id = checkout_id
        self.user_id = user_id
        self.total_price = total_price
        self.shipping_address = shipping_address

    def verify_order(self):
        """Verifikasi apakah pesanan sudah benar."""
        print(f"Verifying order for user {self.user_id}...")
        return True

    def proceed_to_payment(self):
        """Melanjutkan ke proses pembayaran."""
        print("Proceeding to payment gateway...")
        # Mengembalikan objek Payment baru
        return Payment(payment_id=1, method="Credit Card")


class Payment:
    """
    Menangani proses pembayaran.
    Atribut: paymentId (int), method (string), status (string).
    """
    def _init_(self, payment_id, method, status="pending"):
        self.payment_id = payment_id
        self.method = method
        self.status = status

    def process_payment(self, total_price):
        """Memproses transaksi pembayaran."""
        print(f"Processing payment of ${total_price:.2f} using {self.method}...")
        self.status = "paid"
        print(f"Payment status updated to: {self.status}")
        return self.status == "paid"

    def confirm_payment(self):
        """Konfirmasi status pembayaran."""
        print(f"Confirming payment status: {self.status}")
        return self.status == "paid"
