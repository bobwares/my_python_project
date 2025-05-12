from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
from .models import Customer
from .crud import list_customers, get_customer, create_customer, update_customer, delete_customer

app = FastAPI(title="Customer Domain API", version="1.0.0", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/customers", response_model=list[Customer])
def read_customers():
    return list_customers()


@app.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
def add_customer(customer: Customer):
    return create_customer(customer)


@app.get("/customers/{customer_id}", response_model=Customer)
def read_customer(customer_id: UUID):
    cust = get_customer(customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return cust


@app.patch("/customers/{customer_id}", response_model=Customer)
def edit_customer(customer_id: UUID, data: dict):
    if not get_customer(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return update_customer(customer_id, data)


@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_customer(customer_id: UUID):
    if not get_customer(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    delete_customer(customer_id)
