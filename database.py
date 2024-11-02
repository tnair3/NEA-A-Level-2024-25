import sqlite3 as sql
from random import choice
from random import randint

conn = sql.connect('pacmandata.db')
cursor = conn.cursor()

# TESTING =================================================================================
def displaydatabase(table): #FOR TESTING PURPOSES
    match table:
        case "LOGIN":
            print("LOGIN TABLE")
            print("USERNAME | HASHED PASSWORD | SALT")
            data = cursor.execute('''SELECT * FROM LOGIN''')
            for row in data:
                print(row)
            print()
        case "SCORES":
            print("SCORES TABLE")
            print("USERNAME | DATE | TIME | SCORE")
            data = cursor.execute('''SELECT * FROM SCORES''')
            for row in data:
                print(row)
            print()
#TESTING ==================================================================================

def initialisedatabase():
    logintable = """CREATE TABLE IF NOT EXISTS LOGIN (
                    Username VARCHAR(20) NOT NULL,
                    Password VARCHAR(99) NOT NULL,
                    Salt VARCHAR(99) NOT NULL
                ); """
    
    scorestable = """CREATE TABLE IF NOT EXISTS SCORES (
                    Username VARCHAR(20) NOT NULL,
                    Date CHAR(8) NOT NULL,
                    Time INT NOT NULL,
                    Score INT NOT NULL
                ); """
    
    cursor.execute(logintable)
    cursor.execute(scorestable)
    conn.commit()

def hashalgorithm(password, salt):
    def generatesalt():
        salt = ""
        characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                    "!", "£", "$", "%", "&", "*", "-", "_", "=", "+", "#", "@", ",", ".", "?", "/"]
        lengthofsalt = randint(9, 15)
        for i in range(0, lengthofsalt):
            salt = salt + choice(characters)
        return salt
    
    if salt == None:
        salt = generatesalt()
    password = str(password) + str(salt)
    hashedpassword = ""
    for i in range(len(password)):
        hashedpassword += str(ord(password[i]))
    hashedpassword = hex(int(hashedpassword) % 5923479346)[2:]
    hashedpassword = str(hashedpassword)
    return hashedpassword, salt

def addnewlogindetails(username, password):
    cursor.execute("""SELECT Username
                FROM LOGIN
                WHERE Username = ?""", (username,))

    numusernames = cursor.fetchall()
    if len(numusernames) == 0:
        password, salt = hashalgorithm(password, None)
        cursor.execute("""INSERT INTO LOGIN VALUES (?, ?, ?)""", 
                    (username, password, salt))
        return True
    else:
        return False

def updatelogindetails(username, newusername, password):
    if newusername != None:
        cursor.execute("""UPDATE LOGIN
                       SET Username = ?
                       WHERE Username = ?""", (newusername, username,))
    if password != None:
        password, salt = hashalgorithm(password, None)
        cursor.execute("""UPDATE LOGIN
                       SET Password = ?, Salt = ?
                       WHERE Username = ?""", (password, salt, username))

def addnewscores(username, date, time, score):
    cursor.execute("""INSERT INTO SCORES VALUES (?, ?, ?, ?)""",
                   (username, date, time, score))
    
def selectfromscores(username, date):
    if username == None and date == None:
        cursor.execute("""SELECT * 
                    FROM SCORES""")
    if username == None and date != None:
        cursor.execute("""SELECT *
                    FROM SCORES
                    WHERE Date = ?""", (date,))
    if username != None and date == None:
        cursor.execute("""SELECT *
                    FROM SCORES
                    WHERE Username = ?""", (username,))
    if username != None and date != None:
        cursor.execute("""SELECT *
                    FROM SCORES
                    WHERE Date = ? AND Username = ?""", (username, date,))
        
   
    data = cursor.fetchall()
    for row in data:
        print(row)

def checklogindetails(username, inputpassword):
    cursor.execute("""SELECT "Password", "Salt"
                   FROM LOGIN
                   WHERE Username = ?""", (username,))
    data = cursor.fetchall()
    if len(data) > 0:
        data = data[0]
        validpassword = data[0]
        salt = data[1]
        hashedpass = hashalgorithm(inputpassword, salt)[0]
        if hashedpass == validpassword:
            return True, True
        else:
            return True, False
    else:
        return False, False

initialisedatabase()

conn.commit()
conn.close()