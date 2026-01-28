from payment.domain.entities import Payment

def payment_to_dict(payment: Payment) -> dict:
    return {
        "id": payment.id,
        "id_checkout": payment.id_checkout,
        "id_user": payment.id_user,
        "metode": payment.metode,
        "total_harga": payment.total_harga,
        "status": payment.status,
        "created_at": payment.created_at,
        "paid_at": payment.paid_at,
    }

def payment_from_dict(row: dict) -> Payment:
    return Payment(
        id=row["id"],
        id_checkout=row["id_checkout"],
        id_user=row["id_user"],
        metode=row["metode"],
        total_harga=row["total_harga"],
        status=row["status"],
        created_at=row["created_at"],
        paid_at=row["paid_at"],
    )
