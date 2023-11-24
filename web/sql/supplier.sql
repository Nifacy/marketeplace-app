CREATE OR REPLACE FUNCTION get_supplier(supplier_id INT)
RETURNS TABLE (
    id INT,
    name VARCHAR(50),
    contacts INT,
    address INT
) AS $$
BEGIN
    RETURN QUERY SELECT suppliers.* FROM suppliers WHERE suppliers.id = supplier_id;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_supplier(
    p_name VARCHAR(50),
    p_contacts INT,
    p_address INT
) RETURNS INT AS $$ -- Не уверен нужно будет ретурнить id. Оставлю здесь комментарий.
DECLARE
    v_supplier_id INT;
BEGIN
    INSERT INTO suppliers(
        name, 
        contacts, 
        address
    )
    VALUES (
        p_name, 
        p_contacts, 
        p_address
    )
    RETURNING id INTO v_supplier_id;

    RETURN v_supplier_id;
END; $$
LANGUAGE plpgsql;
