import psycopg2

conect = psycopg2.connect(
    dbname="practice",
    user="postgres",
    password="zangar66",
    host="localhost",
    port="5432"
)

cur = conect.cursor()

while True:
    print("""
1. Search
2. Upsert (insert/update)
3. Insert many
4. Pagination
5. Delete
6. Show all
7. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        pattern = input("Search: ")
        cur.execute("SELECT * FROM search_contact(%s)", (pattern,))
        for row in cur.fetchall():
            print(row)

    elif choice == "2":
        name = input("Name: ")
        phone = input("Phone: ")
        cur.execute("CALL insert_contact(%s, %s)", (name, phone))
        conect.commit()

    elif choice == "3":
        n = int(input("How many contacts: "))
        
        names = []
        phones = []

        for i in range(n):
            name = input("Name: ")
            phone = input("Phone: ")
            names.append(name)
            phones.append(phone)

        cur.execute("CALL insert_many(%s::text[], %s::text[])", (names, phones))
        conect.commit()

    elif choice == "4":
        lim = int(input("Limit: "))
        off = int(input("Offset: "))
        cur.execute("SELECT * FROM pagination(%s, %s)", (lim, off))
        for row in cur.fetchall():
            print(row)

    elif choice == "5":
        val = input("Name or phone: ")
        cur.execute("CALL delete_contact(%s)", (val,))
        conect.commit()

    
    elif choice == "6":
        cur.execute("SELECT * FROM practice")
        for row in cur.fetchall():
            print(row)

    elif choice == "7":
        break

    else:
        print("Invalid option")

cur.close()
conect.close()