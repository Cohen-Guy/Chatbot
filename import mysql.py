import mysql.connector
from mysql.connector import Error

# Establish the database connection
def create_db_connection():
    try:
        cnx = mysql.connector.connect(user='guyc', password='Zxcv0987!',
                                      host='localhost', database='mydatabase')
        if cnx.is_connected():
            return cnx
    except Error as e:
        print(f"Error: {e}")
        return None

# Create table for customers
def create_table(cursor):
    try:
        query = '''CREATE TABLE IF NOT EXISTS Customers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    contact_details VARCHAR(255),
                    room_description TEXT,
                    room_dimensions TEXT,
                    preferred_style TEXT,
                    color_preferences TEXT,
                    elements_to_keep TEXT
                ); '''
        cursor.execute(query)
        print('The table Customers was created successfully')
    except mysql.connector.Error as e:
        print(f"Error: {e}")

# Get the connection
db = create_db_connection()

if db is not None:
    cursor = db.cursor()
    create_table(cursor)
    cursor.execute("SELECT * FROM Customers")
    results = cursor.fetchall()
    for row in results:
        print(row)

    db.close()
