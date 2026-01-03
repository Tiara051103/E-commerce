from cart.domain.entities import Cart, CartItem
from cart.domain.repositories import CartRepository, CartItemRepository
from katalog.domain.repositories import ProdukRepository
from cart.application.result import Result
from cart.domain.services import IdGeneratorService


# =====================================================
# AMBIL / LIHAT CART USER
# =====================================================
class AmbilCartUseCase:
    def __init__(self, cart_repo: CartRepository, item_repo: CartItemRepository):
        self.cart_repo = cart_repo
        self.item_repo = item_repo

    def execute(self, id_user: str) -> Result:
        cart = self.cart_repo.get_by_user(id_user)
        if cart is None:
            return Result.ok(None)

        cart.items = self.item_repo.get_by_cart(cart.id)
        return Result.ok(cart)


# =====================================================
# TAMBAH ITEM KE CART
# =====================================================
class TambahItemCartUseCase:
    def __init__(
        self,
        cart_repo: CartRepository,
        item_repo: CartItemRepository,
        produk_repo: ProdukRepository,
        id_gen: IdGeneratorService
    ):
        self.cart_repo = cart_repo
        self.item_repo = item_repo
        self.produk_repo = produk_repo
        self.id_gen = id_gen

    def execute(self, id_user: str, id_produk: str, jumlah: int) -> Result:
        if jumlah <= 0:
            return Result.error("Jumlah harus lebih dari 0")

        # 1️⃣ Ambil cart
        cart = self.cart_repo.get_by_user(id_user)

        # 2️⃣ Jika belum ada, buat cart
        if cart is None:
            cart = Cart(
                id=self.id_gen.generate_id(),
                id_user=id_user
            )
            self.cart_repo.add(cart)

        # 🔐 VALIDASI KERAS
        if not cart.id:
            return Result.error("ID cart tidak valid")

        # 3️⃣ Ambil produk
        produk = self.produk_repo.get_by_id(id_produk)
        if produk is None:
            return Result.error("Produk tidak ditemukan")

        # 4️⃣ Cek item cart
        item = self.item_repo.get_by_cart_and_produk(cart.id, id_produk)

        if item:
            item.jumlah += jumlah
            self.item_repo.update(item)
        else:
            self.item_repo.add(
                CartItem(
                    id=self.id_gen.generate_id(),
                    id_cart=cart.id,   # ✅ DIJAMIN ADA
                    id_produk=produk.id,
                    nama_produk=produk.nama,
                    harga_satuan=produk.harga,
                    jumlah=jumlah
                )
            )

        return Result.ok()

# =====================================================
# UBAH JUMLAH ITEM
# =====================================================
class UbahJumlahItemCartUseCase:
    def __init__(self, item_repo: CartItemRepository):
        self.item_repo = item_repo

    def execute(self, id_item: str, jumlah: int) -> Result:
        if jumlah <= 0:
            return Result.error("Jumlah harus lebih dari 0")

        item = self.item_repo.get_by_id(id_item)
        if item is None:
            return Result.error("Item tidak ditemukan")

        item.jumlah = jumlah
        self.item_repo.update(item)
        return Result.ok()


# =====================================================
# HAPUS ITEM
# =====================================================
class HapusItemCartUseCase:
    def __init__(self, item_repo: CartItemRepository):
        self.item_repo = item_repo

    def execute(self, id_item: str) -> Result:
        item = self.item_repo.get_by_id(id_item)
        if item is None:
            return Result.error("Item tidak ditemukan")

        self.item_repo.delete_by_id(id_item)
        return Result.ok()


# =====================================================
# KOSONGKAN CART
# =====================================================
class KosongkanCartUseCase:
    def __init__(self, cart_repo: CartRepository, item_repo: CartItemRepository):
        self.cart_repo = cart_repo
        self.item_repo = item_repo

    def execute(self, id_user: str) -> Result:
        cart = self.cart_repo.get_by_user(id_user)
        if cart is None:
            return Result.error("Cart tidak ditemukan")

        for item in self.item_repo.get_by_cart(cart.id):
            self.item_repo.delete_by_id(item.id)

        return Result.ok()
