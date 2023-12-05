from enum import Enum
import psycopg2.extensions
from ._exceptions import UnableToAddToFavorite, ProductNotFound, CustomerNotFound


class _StatusCode(Enum):
    OK = 0
    CUSTOMER_NOT_EXISTS = 1
    PRODUCT_NOT_EXISTS = 2


def add_to_favorite(conn: psycopg2.extensions.connection, customer_id: int, product_id: int) -> None:
    cur = conn.cursor()
    cur.callproc('add_to_favorite', (customer_id, product_id))
    response = cur.fetchone()
    cur.close()

    if response is None:
        raise UnableToAddToFavorite()
    
    status_code = _StatusCode(response[0])

    if status_code == _StatusCode.CUSTOMER_NOT_EXISTS:
        raise CustomerNotFound()

    if status_code == _StatusCode.PRODUCT_NOT_EXISTS:
        raise ProductNotFound()