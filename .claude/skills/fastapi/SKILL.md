---
name: fastapi
description: Build high-performance REST APIs with FastAPI, a modern Python web framework. Use this skill when building Python web APIs, REST services, async endpoints, or backends requiring automatic validation, OpenAPI documentation, dependency injection, OAuth2/JWT authentication, or database integration with SQLModel/SQLAlchemy. Covers path/query/body parameters, Pydantic models, background tasks, middleware, and production deployment. (project)
---

# FastAPI

FastAPI is a modern, high-performance Python web framework for building APIs with automatic validation, serialization, and interactive documentation.

## Quick Start

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Run with: `fastapi dev main.py`

Access:
- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Path Operations

```python
@app.get("/items/{item_id}")      # Read
@app.post("/items/")               # Create
@app.put("/items/{item_id}")       # Update
@app.delete("/items/{item_id}")    # Delete
@app.patch("/items/{item_id}")     # Partial update
```

## Parameters

### Path Parameters

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):  # Automatic type conversion
    return {"item_id": item_id}
```

### Query Parameters

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10, q: str | None = None):
    return {"skip": skip, "limit": limit, "q": q}
```

### Request Body with Pydantic

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Combined Parameters

```python
from fastapi import Path, Query, Body
from typing import Annotated

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(ge=1, le=1000)],
    q: Annotated[str | None, Query(max_length=50)] = None,
    item: Item = None,
    importance: Annotated[int, Body(ge=1, le=5)] = None,
):
    return {"item_id": item_id, "q": q, "item": item}
```

## Response Models

```python
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email: EmailStr

@app.post("/users/", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    return user  # Password automatically excluded
```

## Error Handling

```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
            headers={"X-Error": "Item not found"}
        )
    return items_db[item_id]
```

## Dependency Injection

```python
from fastapi import Depends

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

### Class-based Dependencies

```python
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    return {"q": commons.q, "skip": commons.skip}
```

### Dependencies with Yield (Resource Cleanup)

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification scheduled"}
```

## Type Hints Reference

```python
# Simple types
item_a: str
item_b: int
item_c: float
item_d: bool

# Collections (Python 3.9+)
items: list[str]
prices: dict[str, float]
coords: tuple[int, int, str]
unique: set[bytes]

# Optional/Union (Python 3.10+)
name: str | None = None
value: int | str

# Annotated for metadata
from typing import Annotated
name: Annotated[str, "metadata here"]
```

## Project Structure (Recommended)

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app instance
│   ├── dependencies.py   # Shared dependencies
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   ├── models/           # Pydantic/SQLModel models
│   │   ├── __init__.py
│   │   └── item.py
│   └── crud/             # Database operations
│       └── item.py
├── tests/
├── requirements.txt
└── .env
```

### Router Organization

```python
# app/routers/items.py
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def read_items():
    return []

# app/main.py
from fastapi import FastAPI
from app.routers import items, users

app = FastAPI()
app.include_router(items.router)
app.include_router(users.router)
```

## Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Custom Middleware

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Static Files

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

## Advanced Topics

See `references/advanced.md` for:
- OAuth2/JWT authentication patterns
- SQLModel/SQLAlchemy database integration
- File uploads and streaming
- WebSockets
- Testing with pytest
- Production deployment
