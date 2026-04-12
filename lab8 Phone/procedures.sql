
CREATE OR REPLACE PROCEDURE upsert_contact(n TEXT, p TEXT)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM practice WHERE name = n) THEN
        UPDATE practice SET phone = p WHERE name = n;
    ELSE
        INSERT INTO practice(name, phone) VALUES (n, p);
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_many(names TEXT[], phones TEXT[])
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF length(phones[i]) >= 5 THEN
            INSERT INTO practice(name, phone)
            VALUES (names[i], phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: %', phones[i];
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_contact(val TEXT)
AS $$
BEGIN
    DELETE FROM practice
    WHERE name = val OR phone = val;
END;
$$ LANGUAGE plpgsql;