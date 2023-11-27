from dataclasses import dataclass
import itertools

import psycopg2
import psycopg2.extensions

from app.schemas import Product, ProductInfo, Supplier
from ._exceptions import UnableToCreateProduct, ProductNotFound, UnableToUpdateProduct
from . import supplier


@dataclass(frozen=True)
class SearchFilters:
    product_id: int | None = None
    name: str | None = None
    owner_id: int | None = None


def _deserialize_build(record, owner) -> Product:
    return Product(
        id=record[0],
        in_favorites=False,
        info=ProductInfo(
            images=record[1],
            price=record[2],
            product_name=record[3],
            description=record[4],
        ),
        supplier=owner,
    )


def _is_error_message(message: str) -> bool:
    return message.startswith('error:')


def _get_error_message(message: str) -> str:
    return message.replace('error:', '').strip().lower()


def _match_error_to_usecase_exception(error_message: str):
    if 'product not exists' in error_message:
        raise ProductNotFound()
    
    raise ValueError(f"Can't match usecase exception for {error_message!r}")


def get_products(conn: psycopg2.extensions.connection, filters: SearchFilters) -> list[Product]:
    cur = conn.cursor()
    cur.callproc('get_products', (
        filters.product_id,
        filters.name,
        filters.owner_id,
    ))

    found_records = cur.fetchall()
    cur.close()

    products = []
    grouped_records = itertools.groupby(found_records, key=lambda record: record[5])

    for owner_id, group in grouped_records:
        owner = supplier.get_supplier(conn, owner_id)
        products.extend(_deserialize_build(record, owner) for record in group)

    return products


def create_product(conn: psycopg2.extensions.connection, supplier: Supplier, product_info: ProductInfo) -> Product:
    cur = conn.cursor()

    cur.callproc(
        'create_product', 
        (
            list(map(str, product_info.images)),
            product_info.product_name,
            product_info.price,
            product_info.description,
            supplier.id,
        )
    )

    product_id = cur.fetchone()
    cur.close()

    if product_id is None:
        raise UnableToCreateProduct()

    return get_products(conn, SearchFilters(product_id=product_id))[0]


def update_product(
    conn: psycopg2.extensions.connection,
    product_id: int,
    product_info: ProductInfo,
) -> Product:
    with conn.cursor() as cur:
        cur.callproc(
            'update_product',
            (
                product_id,
                product_info.price,
                product_info.product_name,
                product_info.description,
                list(map(str, product_info.images)),
            )
        )

        response = cur.fetchone()

        if response is None:
            raise UnableToUpdateProduct()
        
        if _is_error_message(response[0]):
            _match_error_to_usecase_exception(_get_error_message(response[0]))

    return get_products(conn, SearchFilters(product_id=product_id))[0]
