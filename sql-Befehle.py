import sqlite3

def sNamesuch(vorname, nachname):
    connection = sqlite3.connect('schuelerliste.db')
    cursor = connection.cursor()
    sql = "SELECT sID, sName, sVName, sJahrg, sKla, sErst, sZweit, sDritt, sZu FROM schueler WHERE sVName LIKE '"+vorname+"' AND sVName LIKE '"+nachname+"' ORDER BY sKla ASC"
    cursor.execute(sql)
    print(sql) #überflüssig
    connection.close()
    
def sKlasuch(klasse):
    connection = sqlite3.connect('schuelerliste.db')
    cursor = connection.cursor()
    sql = "SELECT sID, sName, sVName, sErst, sZweit, sDritt, sZu FROM schueler WHERE sKla LIKE '"+klasse+"' ORDER BY sVName ASC"
    cursor.execute(sql)
    print(sql) #überflüssig
    connection.close()
    
def sJahrgsuch(jahrgang):
    connection = sqlite3.connect('schuelerliste.db')
    cursor = connection.cursor()
    sql = "SELECT sID, sName, sVName, sKla, sErst, sZweit, sDritt, sZu FROM schueler WHERE sJahrg LIKE '"+jahrgang+"' ORDER BY sVName ASC"
    cursor.execute(sql)
    print(sql) #überflüssig
    connection.close()
    
def sKurssuch(jahrgang):
    connection = sqlite3.connect('schuelerliste.db')
    cursor = connection.cursor()
    sql = "SELECT sID, sName, sVName, sKla, sErst, sZweit, sDritt, sZu FROM schueler WHERE sJahrg LIKE '"+jahrgang+"' ORDER BY sVName ASC"
    cursor.execute(sql)
    print(sql) #überflüssig
    connection.close()
    
'''# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()'''