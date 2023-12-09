from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
import psycopg2.extensions

from . import database, schemas
from .usecases import customer, oauth2, supplier
from .dependencies import database, get_current_user


DependsDBConnection = Annotated[
    psycopg2.extensions.connection,
    Depends(database.get_connection),
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    database.open_connection()
    yield
    database.close_connection()


app = FastAPI(lifespan=lifespan)


@app.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier_endpoint(conn: DependsDBConnection, supplier_id: int):
    _supplier = supplier.get_supplier(conn, supplier_id)

    if not _supplier:
        raise HTTPException(status_code=404, detail=f"Supplier not found")

    return _supplier


@app.post("/supplier/register", response_model=schemas.Token)
async def register_supplier(conn: DependsDBConnection, register_form: schemas.SupplierRegisterForm):
    _supplier = supplier.register_supplier(conn, register_form)
    return schemas.Token(
        token=oauth2.generate_token(
            oauth2.TokenData(
                type="supplier",
                id=_supplier.id,
            ),
        ),
    )


@app.post("/supplier/login", response_model=schemas.Token)
async def login_supplier(conn: DependsDBConnection, credentials: schemas.SupplierCredentials):
    try:
        _supplier = supplier.login_supplier(conn, credentials)

        return schemas.Token(
            token=oauth2.generate_token(
                oauth2.TokenData(
                    type="supplier",
                    id=_supplier.id,
                ),
            ),
        )

    except supplier.InvalidCredentials:
        raise HTTPException(
            status_code=401,
            detail="Wrong login or password",
        )


@app.post("/customer/register", response_model=schemas.Token)
async def register_customer(conn: DependsDBConnection, register_form: schemas.CustomerRegisterForm):
    _customer = customer.register_customer(conn, register_form)
    return schemas.Token(
        token=oauth2.generate_token(
            oauth2.TokenData(
                type="customer",
                id=_customer.id,
            ),
        ),
    )


@app.post("/customer/login", response_model=schemas.Token)
async def login_customer(conn: DependsDBConnection, credentials: schemas.CustomerCredentials):
    try:
        _customer = customer.login_customer(conn, credentials)

        return schemas.Token(
            token=oauth2.generate_token(
                oauth2.TokenData(
                    type="customer",
                    id=_customer.id,
                )
            )
        )

    except supplier.InvalidCredentials:
        raise HTTPException(
            status_code=401,
            detail="Wrong login or password",
        )

# TODO: add
# user: Annotated[schemas.Supplier | schemas.Customer, Depends(get_current_user)]
# to the list of arguments
@app.get("/customer/{id}", response_model=schemas.Customer)
async def get_customer_endpoint(
    conn: DependsDBConnection, 
    id: int
    ):
    try:
        return customer.get_customer(conn, id)
    except customer.CustomerNotFound:
        raise HTTPException(status_code=404, detail="Customer not found")