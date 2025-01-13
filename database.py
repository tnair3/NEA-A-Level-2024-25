import sqlite3 as sql

from random import choice
from random import randint

# TESTING =========================================================================================
def displaydatabase(table):
    conn = sql.connect('pacmandata.db')
    cursor = conn.cursor()
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
    conn.close()

#CODE =============================================================================================
def initialisedatabase():
    conn = sql.connect('pacmandata.db')
    cursor = conn.cursor()
    logintable = """CREATE TABLE IF NOT EXISTS LOGIN (
                    UserID INT NOT NULL PRIMARY KEY,
                    Username VARCHAR(20) NOT NULL,
                    Password VARCHAR(99) NOT NULL,
                    Salt VARCHAR(99) NOT NULL
                ); """

    scorestable = """CREATE TABLE IF NOT EXISTS SCORES (
                    GameID INT NOT NULL PRIMARY KEY,
                    UserID INT NOT NULL,
                    Date CHAR(8) NOT NULL,
                    Time INT NOT NULL,
                    Score INT NOT NULL,
                    Cleared INT NOT NULL,
                    FOREIGN KEY (UserID) REFERENCES LOGIN(UserID)
                ); """
    
    cursor.execute(logintable)
    cursor.execute(scorestable)

    addnewlogindetails("Anonymous", "NOTREALLOGIN")
    
    conn.commit()
    conn.close()

#LOGIN
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
    conn = sql.connect('pacmandata.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT Username
                FROM LOGIN
                WHERE Username = ?""", (username,))

    numusernames = cursor.fetchall()
    if len(numusernames) == 0:
        if len(password) >= 8:
            password, salt = hashalgorithm(password, None)
            cursor.execute("""SELECT UserID
                        FROM LOGIN""")
            newID = len(cursor.fetchall())
            cursor.execute("""INSERT INTO LOGIN 
                           VALUES (?, ?, ?, ?)""", 
                        (newID, username, password, salt))
            conn.commit()
            conn.close()
            return True, False, False
        else:
            conn.commit()
            conn.close()
            return False, False, True
    else:
        conn.commit()
        conn.close()
        return False, True, False

def checklogindetails(username, inputpassword):
    conn = sql.connect('pacmandata.db')
    cursor = conn.cursor()
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
            conn.commit()
            conn.close()
            return True, True
        else:
            conn.commit()
            conn.close()
            return True, False
    else:
        conn.commit()
        conn.close()
        return False, False

def updatelogindetails(userID, newusername, password):
    conn = sql.connect('pacmandata.db')
    cursor = conn.cursor()
    if newusername != None:
        cursor.execute("""SELECT Username
                    FROM LOGIN
                    WHERE Username = ?""", (newusername,))
        if len(cursor.fetchall()) == 0:
            cursor.execute("""UPDATE LOGIN
                        SET Username = ?
                        WHERE UserID = ?""", (newusername, userID,))
            conn.commit()
            conn.close()
            return True, False, False
        else:
            conn.commit()
            conn.close()
            return False, True, False
    if password != None:
        if len(password) >= 8:
            password, salt = hashalgorithm(password, None)
            cursor.execute("""UPDATE LOGIN
                        SET Password = ?, Salt = ?
                        WHERE UserID = ?""", (password, salt, userID))
            conn.commit()
            conn.close()
            return True, False, False
        else:
            conn.commit()
            conn.close()
            return False, False, True

def getusername(userID):
    conn = sql.connect('pacmandata.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT Username
                FROM LOGIN
                WHERE UserID = ?""", (userID,))
    return cursor.fetchall()[0]

def getuserID(username):
    conn = sql.connect('pacmandata.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT UserID
                FROM LOGIN
                WHERE Username = ?""", (username,))
    data = cursor.fetchall()
    if len(data) != 0:
        return data[0][0]
    else:
        return None

#SCORES
def addnewscores(username, date, time, score, cleared):
    conn = sql.connect('pacmandata.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT GameID
                FROM SCORES""")
    newID = len(cursor.fetchall())
    userID = getuserID(username)
    cursor.execute("""INSERT INTO SCORES VALUES (?, ?, ?, ?, ?, ?)""",
                   (newID, userID, date, time, score, cleared))
    
    conn.commit()
    conn.close()
    
def selectfromscores(username):
    conn = sql.connect('pacmandata.db')
    cursor = conn.cursor()
    if username == None:
        cursor.execute("""SELECT * 
                    FROM SCORES""")
        data = cursor.fetchall()
        data = [list(row) for row in data]
        for i in range(0, len(data)):
            data[i][1] = getusername(data[i][1])
            changedata = data[i][1][0]
            data[i][1] = changedata
        data = map(list, data)
        return data
    else:
        UserID = getuserID(username)
        if UserID != None:
            UserID = int(UserID)
            cursor.execute("""SELECT *
                        FROM SCORES
                        WHERE UserID = ?""", (UserID,))
        
            data = cursor.fetchall()
            data = [list(row) for row in data]
            for i in range(0, len(data)):
                data[i][1] = getusername(data[i][1])
                changedata = data[i][1][0]
                data[i][1] = changedata
            data = map(list, data)
            return data
        else:
            return []