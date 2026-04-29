-- SEARCH PROCEDURE

CREATE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name TEXT, email TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email, p.phone
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone LIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;

-- DELETE PROEDEURE

CREATE PROCEDURE delete_contact(p_val TEXT)
AS $$
DECLARE
    cid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_val;

    IF cid IS NOT NULL THEN
        DELETE FROM contacts WHERE id = cid;
        RETURN;
    END IF;

    DELETE FROM phones WHERE phone = p_val;
END;
$$ LANGUAGE plpgsql;

-- UPSERT PROC

CREATE PROCEDURE upsert_contact(
    p_name TEXT,
    p_phone TEXT,
    p_type TEXT
)
AS $$
DECLARE
    cid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_name;

    IF cid IS NULL THEN
        INSERT INTO contacts(name)
        VALUES (p_name)
        RETURNING id INTO cid;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM phones
        WHERE contact_id = cid AND phone = p_phone
    ) THEN
        INSERT INTO phones(contact_id, phone, type)
        VALUES (cid, p_phone, p_type);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- PAGINATION

CREATE FUNCTION pagination(lim INT, off INT)
RETURNS TABLE(name TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, p.phone
    FROM contacts c
    JOIN phones p ON c.id = p.contact_id
    ORDER BY c.id
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;

-- ADD PHONE

CREATE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
AS $$
DECLARE
    cid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_contact_name;

    IF cid IS NULL THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$ LANGUAGE plpgsql;

-- MOVE TO GROUP

CREATE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
AS $$
DECLARE
    cid INT;
    gid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_contact_name;

    IF cid IS NULL THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    SELECT id INTO gid FROM groups WHERE name = p_group_name;

    IF gid IS NULL THEN
        INSERT INTO groups(name)
        VALUES (p_group_name)
        RETURNING id INTO gid;
    END IF;

    UPDATE contacts
    SET group_id = gid
    WHERE id = cid;
END;
$$ LANGUAGE plpgsql;