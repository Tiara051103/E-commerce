from cart.domain.entities import Cart, CartItem
from cart.domain.repositories import CartRepository, CartItemRepository
from katalog.domain.repositories import ProdukRepository
from cart.application.result import Result
from cart.domain.services import IdGeneratorService


class AmbilCartUseCase:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    def execute(self, id_user=None, guest_id=None):
        if id_user:
            cart = self.cart_repo.get_or_create_by_user(id_user)
        elif guest_id:
            cart = self.cart_repo.get_by_guest(guest_id)
        else:
            return Result.error("User tidak valid")

        return Result.ok(cart)

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

    def execute(self, *, id_user, guest_id, id_produk, jumlah) -> Result:
        if jumlah <= 0:
            return Result.error("Jumlah harus lebih dari 0")

        # ambil cart
        if id_user:
            cart = self.cart_repo.get_or_create_by_user(id_user)
        else:
            cart = self.cart_repo.get_by_guest(guest_id)
            if cart is None:
                return Result.error("Cart guest tidak ditemukan")

        produk = self.produk_repo.get_by_id(id_produk)
        if not produk:
            return Result.error("Produk tidak ditemukan")

        item = self.item_repo.get_by_cart_and_produk(cart.id, id_produk)

        if item:
            item.jumlah += jumlah
            self.item_repo.update(item)
        else:
            self.item_repo.add(
                CartItem(
                    id=self.id_gen.generate_id(),
                    id_cart=cart.id,
                    id_produk=produk.id,
                    nama_produk=produk.nama,
                    harga_satuan=produk.harga,
                    jumlah=jumlah
                )
            )

        return Result.ok("Produk ditambahkan ke keranjang")

class UbahJumlahItemCartUseCase:
    def __init__(self, item_repo: CartItemRepository):
        self.item_repo = item_repo

    def execute(self, *, id_cart, id_produk, jumlah) -> Result:
        if jumlah <= 0:
            return Result.error("Jumlah harus lebih dari 0")

        item = self.item_repo.get_by_cart_and_produk(id_cart, id_produk)
        if not item:
            return Result.error("Item tidak ditemukan")

        item.jumlah = jumlah
        self.item_repo.update(item)
        return Result.ok("Jumlah diperbarui")

class HapusItemCartUseCase:
    def __init__(self, item_repo: CartItemRepository):
        self.item_repo = item_repo

    def execute(self, *, id_cart, id_produk) -> Result:
        item = self.item_repo.get_by_cart_and_produk(id_cart, id_produk)
        if not item:
            return Result.error("Item tidak ditemukan")

        self.item_repo.delete_by_id(item.id)
        return Result.ok("Item dihapus")

class KosongkanCartUseCase:
    def __init__(self, cart_repo: CartRepository, item_repo: CartItemRepository):
        self.cart_repo = cart_repo
        self.item_repo = item_repo

    def execute(self, *, id_user=None, guest_id=None) -> Result:
        if id_user:
            cart = self.cart_repo.get_or_create_by_user(id_user)
        elif guest_id:
            cart = self.cart_repo.get_by_guest(guest_id)
        else:
            return Result.error("User tidak valid")

        if not cart:
            return Result.error("Cart tidak ditemukan")

        for item in self.item_repo.get_by_cart(cart.id):
            self.item_repo.delete_by_id(item.id)

        return Result.ok("Cart dikosongkan")
