from uuid import UUID
from typing import Dict, List
from datetime import datetime
from .models import Customer

_db: Dict[UUID, Customer] = {}


def list_customers() -> List[Customer]:
    return list(_db.values())


def get_customer(customer_id: UUID) -> Customer:
    return _db.get(customer_id)


def create_customer(customer: Customer) -> Customer:
    _db[customer.id] = customer
    return customer


def update_customer(customer_id: UUID, data: dict) -> Customer:
    cust = _db[customer_id]
    updated = cust.copy(update={**data, "updatedAt": datetime.utcnow()})
    _db[customer_id] = updated
    return updated


def delete_customer(customer_id: UUID) -> None:
    _db.pop(customer_id, None)
