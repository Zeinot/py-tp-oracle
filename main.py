import oracledb
user = "directeur"
pwd = "admin"
connection = oracledb.connect(
    user=user,
    password=pwd,
    host="localhost", 
    port=1521, 
    service_name="scolarite")
cursor = connection.cursor()
print("version : ", connection.version)

cursor.execute("""
               INSERT INTO Etudiant (NomEt, PrenomEt, DateNais) 
    VALUES ('NEW', 'Jean', TO_DATE('1995-04-15', 'YYYY-MM-DD'))
    """)
connection.commit()


for row in cursor.execute("SELECT * FROM Etudiant"):
    print(row)
    
    
cursor.execute("SELECT * FROM Etudiant")
while True:
    row = cursor.fetchone()
    if row is None:
        break
    print(row)
    
    
cursor.execute("SELECT IDET from Etudiant")
rows = cursor.fetchall()
print(rows)
print(f"Number of rows: {len(rows)}")
if rows:
    for row in rows:
        print(row)
else:
    print("No data found.")
    
    
# Execute a simple query to test the connection 
cursor.execute("SELECT SYSDATE FROM dual") 
result = cursor.fetchone() 
# Print the result 
print("Current database date and time:", result[0])

cursor.close() 
connection.close()