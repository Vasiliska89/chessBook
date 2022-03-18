import sqlite3 as sq
def getComment(fen):
    with sq.connect("chessNote.db") as con:  # this will be created if not exist
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS notes (fen TEXT, comment TEXT NOT NULL DEFAULT 'No comment yet')""")
        cur.execute("""SELECT comment FROM notes WHERE fen=?""", (fen,))
        com = cur.fetchall()
        return com[0][0] if len(com) > 0 else "This position is not explored by you!"
def makeComment(text, fen):
    print(text)
    with sq.connect("chessNote.db") as con:  # this will be created if not exist
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS notes (fen TEXT, comment TEXT NOT NULL DEFAULT 'No comment yet')""")
        cur.execute("""SELECT comment FROM notes WHERE fen=?""", (fen,))
        if len(cur.fetchall())==0:
            cur.execute("""INSERT INTO notes VALUES(?, ?)""", (fen, text))
        else:
            cur.execute("""UPDATE notes SET comment = ? WHERE fen = ?""", (text, fen))