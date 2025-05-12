#!/usr/bin/env bash
#
# setup.sh
#
# Usage: ./setup.sh [project_name]
# Defaults to "customer-api" if no name is provided.
#
set -euo pipefail

PROJECT_NAME="${1:-customer-api}"
PACKAGE_NAME="${PROJECT_NAME//-/_}"

echo "📦 Creating project '${PROJECT_NAME}'..."

# 0. Prevent overwriting an existing non-empty directory
if [ -d "${PROJECT_NAME}" ] && [ "$(ls -A "${PROJECT_NAME}")" ]; then
  echo "Error: Directory '${PROJECT_NAME}' already exists and is not empty."
  exit 1
fi

# 1. Scaffold new Poetry project
poetry new "${PROJECT_NAME}" --src
cd "${PROJECT_NAME}"

# 2. Add runtime dependencies
poetry add requests pydantic python-dotenv openai fastapi uvicorn

# 3. Define groups and add group-specific dependencies
poetry add --group docs mkdocs
poetry add --group dev pre-commit black flake8
poetry add --group test pytest pytest-cov tox selenium

# 4. Install all dependencies including groups
poetry install --with=docs --with=dev --with=test

# 5. Create .gitignore
cat > .gitignore <<'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual env
.venv/

# Env files
.env

# Poetry lock
poetry.lock

# pytest
.pytest_cache/

# tox
.tox/

# Coverage
htmlcov/
.coverage

# Docs build
/site/
EOF

# 6. Create README.md
cat > README.md <<EOF
# ${PROJECT_NAME}

FastAPI-based Customer Domain API, implemented with Pydantic and tested via pytest.

## Prerequisites

- Python 3.10+
- Poetry

## Setup

\`\`\`bash
git clone <repo-url> ${PROJECT_NAME}
cd ${PROJECT_NAME}
./setup.sh   # idempotent: installs runtime + docs + dev + test deps
\`\`\`

## Running

\`\`\`bash
uvicorn ${PACKAGE_NAME}.main:app --reload
\`\`\`

## Testing

\`\`\`bash
make test
\`\`\`

## Documentation

\`\`\`bash
make docs
\`\`\`
EOF

# 7. Create Makefile
cat > Makefile <<'EOF'
.PHONY: install run test lint format coverage docs

install:
\tpoetry install --with=docs --with=dev --with=test

run:
\tuvicorn ${PACKAGE_NAME}.main:app --reload

test:
\tpytest

lint:
\tblack --check src tests
\tflake8 src tests

format:
\tblack src tests

coverage:
\tpytest --cov=src/${PACKAGE_NAME}

docs:
\tmkdocs serve
EOF

# 8. Create tox.ini
cat > tox.ini <<'EOF'
[tox]
envlist = py310, lint

[testenv]
deps =
    pytest
    pytest-cov
commands =
    pytest --cov=src/${PACKAGE_NAME}

[testenv:lint]
deps =
    black==24.1
    flake8==6.0
commands =
    black --check src tests
    flake8 src tests
EOF

# 9. Create .env
cat > .env <<'EOF'
APP_ENV=development
HOST=0.0.0.0
PORT=8000
EOF

# 10. MkDocs config & docs folder
cat > mkdocs.yml <<'EOF'
site_name: Customer Domain API
nav:
  - Home: index.md
EOF
mkdir -p docs
cat > docs/index.md <<'EOF'
# Customer Domain API Documentation

Welcome to the Customer Domain API docs.
EOF

# 11. Scaffold source package
mkdir -p src/${PACKAGE_NAME}

# config.py
cat > src/${PACKAGE_NAME}/config.py <<'EOF'
from pydantic import BaseSettings

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
EOF

# models.py
cat > src/${PACKAGE_NAME}/models.py <<'EOF'
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class Address(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    street1: str
    street2: Optional[str]
    city: str
    state: str
    postalCode: str
    country: str

class Phone(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    countryCode: str
    number: str
    extension: Optional[str]

class NotificationPreferences(BaseModel):
    email: bool
    sms: bool
    push: bool
    mail: bool

class Customer(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    firstName: str
    middleName: Optional[str]
    lastName: str
    email: EmailStr
    addresses: List[Address]
    phoneNumbers: List[Phone]
    notificationPreferences: NotificationPreferences
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
EOF

# crud.py
cat > src/${PACKAGE_NAME}/crud.py <<'EOF'
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
EOF

# main.py
cat > src/${PACKAGE_NAME}/main.py <<'EOF'
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
from .models import Customer
from .crud import list_customers, get_customer, create_customer, update_customer, delete_customer
from .config import settings

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
EOF

# 12. Create tests
mkdir -p tests

cat > tests/conftest.py <<'EOF'
import pytest
from fastapi.testclient import TestClient
from src.${PACKAGE_NAME}.main import app

@pytest.fixture
def client():
    return TestClient(app)
EOF

cat > tests/test_customers.py <<'EOF'
def test_crud_flow(client):
    payload = {
        "firstName": "Test",
        "middleName": None,
        "lastName": "User",
        "email": "test.user@example.com",
        "addresses": [{
            "type": "home",
            "street1": "1 Main St",
            "city": "City",
            "state": "ST",
            "postalCode": "12345",
            "country": "US"
        }],
        "phoneNumbers": [{
            "type": "mobile",
            "countryCode": "+1",
            "number": "5551234"
        }],
        "notificationPreferences": {
            "email": True,
            "sms": False,
            "push": False,
            "mail": False
        }
    }
    # Create
    resp = client.post("/customers", json=payload)
    assert resp.status_code == 201
    cust_id = resp.json()["id"]

    # Read
    assert client.get(f"/customers/{cust_id}").status_code == 200

    # List
    assert client.get("/customers").status_code == 200

    # Patch
    updated = client.patch(f"/customers/{cust_id}", json={"email": "updated@example.com"})
    assert updated.status_code == 200
    assert updated.json()["email"] == "updated@example.com"

    # Delete
    assert client.delete(f"/customers/{cust_id}").status_code == 204

    # Confirm deletion
    assert client.get(f"/customers/{cust_id}").status_code == 404
EOF

echo "✅ Project '${PROJECT_NAME}' created successfully."
