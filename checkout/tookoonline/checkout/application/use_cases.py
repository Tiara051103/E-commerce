from checkout.domain.entities import Checkout, CheckoutItem
from katalog.infrastructure.uuid.id_services import UuidGeneratorService
from cart.domain.entities import CartItem
from checkout.infrastructure.sqlite_db.checkout_repository_sqlite import CheckoutRepositorySqlite, CheckoutItemRepositorySqlite
from cart.infrastructure.sqlite_db.cart_repository_sqlite import CartRepositorySqlite, CartItemRepositorySqlite
from .result import Result

class BuatCheckoutUseCase:
    def __init__(
        self,
        checkout_repo,
        checkout_item_repo,
        cart_repo,
        cart_item_repo,
        id_service: UuidGeneratorService
    ):
        self.checkout_repo = checkout_repo
        self.checkout_item_repo = checkout_item_repo
        self.cart_repo = cart_repo
        self.cart_item_repo = cart_item_repo
        self.id_service = id_service

    def execute(
        self,
        id_user: int,
        items: list[CartItem],
        metode_pembayaran: str,
        bank: str | None = None
    ):
        if not items:
            return Result(False, message="Tidak ada item untuk checkout")

        total_harga = sum(
            item.harga_satuan * item.jumlah for item in items
        )

        checkout_id = self.id_service.generate()

        checkout = Checkout(
            id=checkout_id,
            id_user=id_user,
            total_harga=total_harga,
            status="pending",
            metode_pembayaran=metode_pembayaran,
            bank=bank,
            items=[
                CheckoutItem(
                    id=self.id_service.generate(),
                    id_checkout=checkout_id,
                    id_produk=item.id_produk,
                    nama_produk=item.nama_produk,
                    harga_satuan=item.harga_satuan,
                    jumlah=item.jumlah,
                    subtotal=item.harga_satuan * item.jumlah
                )
                for item in items
            ]
        )

        self.checkout_repo.create(checkout)
        self.checkout_item_repo.add_many(checkout.items)

        # 🔴 OPSIONAL (REKOMENDASI)
        # Jangan hapus cart dulu → hapus setelah payment sukses
        # for item in items:
        #     self.cart_item_repo.delete(item.id)

        return Result(True, data=checkout)