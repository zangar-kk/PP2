import psycopg2
import json
import csv

conn = psycopg2.connect(
    dbname="practice",
    user="postgres",
    password="zangar66",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def show_groups():
    cur.execute("SELECT * FROM groups")
    for row in cur.fetchall():
        print(row)

def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")

    print("Available groups:")
    show_groups()
    group_id = input("Choose group id: ")

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    n = int(input("How many phones: "))
    for _ in range(n):
        phone = input("Phone: ")
        ptype = input("Type (home/work/mobile): ")

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (contact_id, phone, ptype))

    conn.commit()
    print("Contact added!")

def search():
    pattern = input("Search: ")

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    if not rows:
        print("Nothing found")
    else:
        for r in rows:
            print(f"Name: {r[0]} | Email: {r[1]} | Phone: {r[2]}")

def upsert():
    name = input("Name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    cur.execute("CALL upsert_contact(%s, %s, %s)", (name, phone, ptype))
    conn.commit()

def show_all():
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.name
    """)

    for r in cur.fetchall():
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} ({r[5]})")

def delete_contact():
    val = input("Name or phone: ")

    cur.execute("CALL delete_contact(%s)", (val,))
    conn.commit()

    print("Deleted!")

def filter_by_group():
    cur.execute("SELECT * FROM groups")
    groups = cur.fetchall()

    for g in groups:
        print(g)

    gid = input("Choose group id: ")

    cur.execute("""
        SELECT c.name, p.phone
        FROM contacts c
        JOIN phones p ON c.id = p.contact_id
        WHERE c.group_id = %s
    """, (gid,))

    for r in cur.fetchall():
        print(r)

def search_by_email():
    pattern = input("Email search: ")

    cur.execute("""
        SELECT name, email
        FROM contacts
        WHERE email ILIKE %s
    """, (f"%{pattern}%",))

    rows = cur.fetchall()

    if not rows:
        print("Nothing found")
    else:
        for r in rows:
            print(r)

def sort_contacts():
    print("Sort by: name / birthday / id")
    field = input("Choose: ")

    if field not in ["name", "birthday", "id"]:
        print("Invalid field")
        return

    query = f"""
        SELECT c.name, c.birthday, p.phone
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.{field}
    """

    cur.execute(query)

    for r in cur.fetchall():
        print(r)

def pagination_loop():
    limit = 2
    offset = 0

    while True:
        cur.execute("SELECT * FROM pagination(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break
        else:
            print("Invalid")

def export_json():
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    rows = cur.fetchall()

    data = {}

    for name, email, birthday, group, phone, ptype in rows:
        if name not in data:
            data[name] = {
                "name": name,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group,
                "phones": []
            }

        if phone:
            data[name]["phones"].append({
                "number": phone,
                "type": ptype
            })

    with open("contacts.json", "w") as f:
        json.dump(list(data.values()), f, indent=4)

    print("Exported to contacts.json")

def import_json():
    import json

    with open("contacts.json", "r") as f:
        data = json.load(f)

    for contact in data:
        name = contact["name"]
        email = contact["email"]
        birthday = contact["birthday"]
        group = contact["group"]

        # проверка на дубликат
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} exists. skip / overwrite: ")

            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name = %s", (name,))

        # получаем group_id
        cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
        gid = cur.fetchone()
        gid = gid[0] if gid else None

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, gid))

        cid = cur.fetchone()[0]

        for ph in contact["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, ph["number"], ph["type"]))

    conn.commit()
    print("Imported!")

def import_csv():
    file = input("Enter CSV file: ")

    with open(file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row["name"].strip()
            email = (row["email"] or "").strip() or None
            birthday = (row["birthday"] or "").strip() or None
            group = (row["group"] or "").strip() or None
            phone = row["phone"].strip()
            ptype = (row["type"] or "mobile").strip()

            # 1) group_id (создать, если нет)
            gid = None
            if group:
                cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
                g = cur.fetchone()
                if not g:
                    cur.execute(
                        "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                        (group,)
                    )
                    gid = cur.fetchone()[0]
                else:
                    gid = g[0]

            # 2) контакт: найти или создать + обновить данные
            cur.execute("SELECT id, email, birthday, group_id FROM contacts WHERE name=%s", (name,))
            c = cur.fetchone()

            if not c:
                cur.execute("""
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (name, email, birthday, gid))
                cid = cur.fetchone()[0]
            else:
                cid, old_email, old_bday, old_gid = c
                cur.execute("""
                    UPDATE contacts
                    SET email    = COALESCE(%s, email),
                        birthday = COALESCE(%s, birthday),
                        group_id = COALESCE(%s, group_id)
                    WHERE id = %s
                """, (email, birthday, gid, cid))

            # 3) телефон: добавить, если нет
            cur.execute("""
                SELECT 1 FROM phones
                WHERE contact_id = %s AND phone = %s
            """, (cid, phone))

            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (cid, phone, ptype))

    conn.commit()
    print("CSV imported!")

def move_to_group():
    name = input("Contact name: ")
    group = input("New group: ")

    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()

def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()

while True:
    print("""
1. Add contact
2. Search
3. Upsert
4. Show all
5. Delete
6. Pagination
7. Filter by group
8. Search by email
9. Sort
10. Export to JSON
11. Import from JSON
12. Import from CSV
13. Add phone
14. Move to group
15. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        search()
    elif choice == "3":
        upsert()
    elif choice == "4":
        show_all()
    elif choice == "5":
        delete_contact()
    elif choice == "6":
        pagination_loop()
    elif choice == "7":
        filter_by_group()
    elif choice == "8":
        search_by_email()
    elif choice == "9":
        sort_contacts()
    elif choice == "10":
        export_json()
    elif choice == "11":
        import_json()
    elif choice == "12":
        import_csv()
    elif choice == "13":
        add_phone()
    elif choice == "14":
        move_to_group()
    elif choice == "15":
        break
    else:
        print("Invalid option")

cur.close()
conn.close()