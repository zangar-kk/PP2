CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, name TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM practice
    WHERE name ILIKE '%' || pattern || '%'
       OR phone LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION pagination(lim INT, off INT)
RETURNS TABLE(id INT, name TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM practice
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;