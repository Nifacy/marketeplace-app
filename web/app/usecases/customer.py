import psycopg2.extras
import psycopg2
from app.schemas import Customer, CustomerInfo
from ._exceptions import *
from ._address import get_address, create_address
from ._contacts import get_contacts, create_contacts


def get_customer(conn: psycopg2.extensions.connection, customer_id: int) -> Customer:
    cur = conn.cursor()

    cur.callproc('get_customer', (customer_id,))

    # 0 - id; 1 - first_name; 2 - last_name; 3 - contacts; 4 - address
    customer_data = cur.fetchone()

    if customer_data is None:
        raise CustomerNotFound()

    contacts = get_contacts(conn, customer_data[3])
    address = get_address(conn, customer_data[4])
    
    customer_info = CustomerInfo(
        first_name=customer_data[1],
        last_name=customer_data[2],
        contacts=contacts,
        address=address
    )
    customer = Customer(
        id=customer_data[0],
        info=customer_info
    )

    cur.close()

    return customer


def create_customer(conn: psycopg2.extensions.connection, customer_info: CustomerInfo) -> int:
    cur = conn.cursor()

    address_id = create_address(conn, customer_info.address)
    contacts_id = create_contacts(conn, customer_info.contacts)

    cur.callproc(
        'create_customer', 
        (
            customer_info.first_name, 
            customer_info.last_name, 
            contacts_id, 
            address_id
        )
    )

    response = cur.fetchone()
    cur.close()

    if response is None:
        raise UnableToCreateCustomer()
    
    return response[0]
