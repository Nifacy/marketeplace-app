import pytest
from app.schemas import ProductInfo
from app.usecases import product, supplier
from pydantic import HttpUrl
from tests import utils


def test_product_creation(db_connection):
    _supplier = supplier.create_supplier(
        db_connection,
        utils.create_supplier_info_sample(),
    )
    product_info = utils.create_product_info_sample()
    _product = product.create_product(db_connection, _supplier, product_info)

    assert _product.info == product_info


def test_product_getable_after_creation(db_connection):
    _supplier = supplier.create_supplier(
        db_connection,
        utils.create_supplier_info_sample(),
    )
    product_info = utils.create_product_info_sample()
    created_product = product.create_product(db_connection, _supplier, product_info)
    found_product, = product.get_products(
        db_connection,
        product.SearchFilters(created_product.id),
    )

    assert created_product == found_product


def test_product_update(db_connection):
    _supplier = supplier.create_supplier(
        db_connection,
        utils.create_supplier_info_sample(),
    )

    product_info = utils.create_product_info_sample()
    _product = product.create_product(db_connection, _supplier, product_info)

    with pytest.raises(product.ProductNotFound):
        product.update_product(db_connection, -1, _product.info)

    _product.info = ProductInfo(
        images=[
            HttpUrl('http://changed-url-1.com'),
            HttpUrl('http://changed-url-2.com'),
        ],
        price=23.33,
        product_name='changed-product-name',
        description='changed-description',
    )
    
    product.update_product(db_connection, _product.id, _product.info)
    updated_product = product.get_products(
        db_connection,
        product.SearchFilters(product_id=_product.id),
    )[0]

    assert _product == updated_product


def test_remove_from_sale(db_connection):
    _supplier = supplier.create_supplier(
        db_connection,
        utils.create_supplier_info_sample(),
    )

    product_info = utils.create_product_info_sample()

    _product = product.create_product(db_connection, _supplier, product_info)
    assert _product.is_for_sale == True
    
    _updated_product = product.remove_product_from_sale(db_connection, _product.id)
    assert _updated_product.is_for_sale == False


def test_products_search_filters(db_connection):
    _first_supplier = supplier.create_supplier(
        db_connection,
        utils.create_supplier_info_sample(),
    )

    _second_supplier = supplier.create_supplier(
        db_connection,
        utils.create_supplier_info_sample(),
    )

    products_info = [
        (_first_supplier, utils.create_product_info_sample(product_name='a-1')),
        (_first_supplier, utils.create_product_info_sample(product_name='a-2')),
        (_second_supplier, utils.create_product_info_sample(product_name='b-1')),
        (_second_supplier, utils.create_product_info_sample(product_name='b-2')),
        (_second_supplier, utils.create_product_info_sample(product_name='b-3')),
    ]

    products = [
        product.create_product(db_connection, _supplier, product_info)
        for _supplier, product_info in products_info
    ]

    products[0] = product.remove_product_from_sale(db_connection, products[0].id)
    products[2] = product.remove_product_from_sale(db_connection, products[2].id)

    assert product.get_products(
        db_connection,
        product.SearchFilters(products[0].id),
    ) == [products[0]]

    assert product.get_products(
        db_connection,
        product.SearchFilters(owner_id=_first_supplier.id),
    ) == products[:2]
    
    assert product.get_products(
        db_connection,
        product.SearchFilters(
            product_id=products[0].id,
            owner_id=_second_supplier.id,
        ),
    ) == []
    
    assert product.get_products(
        db_connection,
        product.SearchFilters(name='a'),
    ) == products[:2]
    
    assert product.get_products(
        db_connection,
        product.SearchFilters(name='b'),
    ) == products[2:]
    
    assert product.get_products(
        db_connection,
        product.SearchFilters(name='-'),
    ) == products
    
    assert product.get_products(
        db_connection, 
        product.SearchFilters(),
    ) == products

    assert product.get_products(
        db_connection,
        product.SearchFilters(is_for_sale=False),
    ) == [products[0], products[2]]
