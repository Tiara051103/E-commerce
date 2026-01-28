from payment.domain.entities import Payment
from checkout.domain.repositories import CheckoutRepository
from payment.domain.repositories import PaymentRepository
from katalog.infrastructure.uuid.id_services import UuidGeneratorService
from .result import Result


class BuatPembayaranUseCase:
    def __init__(
        self,
        checkout_repo: CheckoutRepository,
        payment_repo: PaymentRepository,
        id_service: UuidGeneratorService
    ):
        self.checkout_repo = checkout_repo
        self.payment_repo = payment_repo
        self.id_service = id_service

    def execute(self, id_checkout: str, id_user: int, metode: str):
        # Ambil checkout
        checkout = self.checkout_repo.get_by_id(id_checkout)

        if checkout is None:
            return Result(False, message="Checkout tidak ditemukan")

        if checkout.status != "pending":
            return Result(False, message="Checkout tidak valid untuk dibayar")

        # Cek apakah sudah pernah ada payment
        existing_payment = self.payment_repo.get_by_checkout(id_checkout)
        if existing_payment:
            return Result(False, message="Checkout sudah memiliki pembayaran")

        # Buat payment
        payment = Payment(
            id=self.id_service.generate(),
            id_checkout=id_checkout,
            id_user=id_user,
            metode=metode,
            total_harga=checkout.total_harga,
            status="PENDING"
        )

        self.payment_repo.create(payment)

        return Result(True, data=payment, message="Pembayaran berhasil dibuat")

class KonfirmasiPembayaranUseCase:
    def __init__(
        self,
        payment_repo: PaymentRepository,
        checkout_repo: CheckoutRepository
    ):
        self.payment_repo = payment_repo
        self.checkout_repo = checkout_repo

    def execute(self, payment_id: str, status: str):
        # Validasi status input
        valid_status = ["SUKSES", "GAGAL"]
        if status not in valid_status:
            return Result(False, message="Status pembayaran tidak valid")

        payment = self.payment_repo.get_by_id(payment_id)

        if payment is None:
            return Result(False, message="Payment tidak ditemukan")

        if payment.status == "SUKSES":
            return Result(False, message="Pembayaran sudah dikonfirmasi")

        # Update status payment
        self.payment_repo.update_status(payment_id, status)

        # Jika sukses → update checkout
        if status == "SUKSES":
            self.checkout_repo.update_status(
                payment.id_checkout,
                "sukses"  # status checkout ikut sama istilah sukses
            )

        return Result(True, message="Pembayaran berhasil dikonfirmasi")
