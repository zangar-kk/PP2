import psycopg2
import csv

def INSERT():
    cur = conect.cursor()
    
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO practice (name, phone) VALUES (%s, %s)", (name, phone))

    conect.commit()
    cur.close()

def DELETE():
    cur = conect.cursor()
    ch = input("Delete (id/phone): ")
    if ch == "id":
        id = input("Enter id: ")
        cur.execute("DELETE FROM practice WHERE id=%s", (id,))
    elif ch == "phone":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM practice WHERE phone=%s", (phone,))
    conect.commit()
    cur.close()

def UPDATE():
    id = input("Enter id of contact to update: ")
    new_name = input("Enter new name (leave blank to skip): ")
    new_phone = input("Enter new phone (leave blank to skip): ")

    cur = conect.cursor()

    if new_name:
        cur.execute("UPDATE practice SET name=%s WHERE id=%s", (new_name, id))
    if new_phone:
        cur.execute("UPDATE practice SET phone=%s WHERE id=%s", (new_phone, id))

    conect.commit()
    cur.close()
    
def QUERY():
    filter_type = input("Filter by (name/phone/id/all): ")

    cur = conect.cursor()

    if filter_type == "name":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM practice WHERE name ILIKE %s", (name,))
    elif filter_type == "phone":
        phone = input("Enter phone: ")
        cur.execute("SELECT * FROM practice WHERE phone LIKE %s", (phone,))
    elif filter_type == "id":
        id = input("Enter id: ")
        cur.execute("SELECT * FROM practice WHERE id LIKE %s", (id,))
    else:
        cur.execute("SELECT * FROM practice")

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()

def INSERT_CSV(file):
    cur = conect.cursor()

    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO practice (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )
            

    conect.commit()
    cur.close()
conect = psycopg2.connect(
    dbname="practice",
    user="postgres",
    password="zangar66",
    host="localhost",
    port="5432"
)


while True:
    print("\n1. Insert \n2. Insert CSV \n3. Update \n4. Query contacts \n5. Delete \n6. Exit \n\nChose your option: ", end= "")
    choise = int(input())
    if choise == 1:
        INSERT()
    elif choise == 2:
        fname = input("File Name: ")
        INSERT_CSV(fname)
    elif choise == 4:
        QUERY()
    elif choise == 5:
        DELETE()
    elif choise == 3:
        UPDATE()
    elif choise == 6:
        break