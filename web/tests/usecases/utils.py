import itertools

from app.schemas import Address, Contacts, SupplierInfo


_counter = itertools.count(start=1)

def create_supplier_info_sample() -> SupplierInfo:
    count = next(_counter)

    return SupplierInfo(
        name=f'test-supplier-{count}',
        contacts=Contacts(
            phone='+1 (123) 456-7890',
            email='test.email@mail.com',
            telegram='@testsupplier',
        ),
        address=Address(
            street='Street',
            city='Moscow',
            country='Russia',
            postal_code='12345',
            house=1,
            entrance=1,
            appartment=1,
        )
    )


