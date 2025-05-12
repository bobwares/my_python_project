# customer-api

FastAPI-based Customer Domain API, implemented with Pydantic and tested via pytest.

## Prerequisites

- Python 3.10+
- Poetry

## Setup

```bash
git clone <repo-url> customer-api
cd customer-api
./setup.sh   # idempotent: installs runtime + docs + dev + test deps
```

## Running

```bash
uvicorn customer_api.main:app --reload
```

## Testing

```bash
make test
```

## Documentation

```bash
make docs
```
