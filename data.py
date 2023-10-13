import sqlite3


con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()



def add_event(title, date, time, public):
    da = [(title, date, time, public)]
    cur.executemany("insert into concerts values (?,?,?,?)", da)
    con.commit()

def update_event(title, date, new_title, new_date, new_time, public):

    cur.execute("update concerts set title==:t where title==:tt and date==:d",
                {"t": f"{new_title}", "tt": f"{title}", "d": f"{date}"})
    cur.execute("update concerts set date==:t where title==:tt and date==:d",
                {"t": f"{new_date}", "tt": f"{title}", "d": f"{date}"})
    cur.execute("update concerts set date==:t where title==:tt and date==:d",
                {"t": f"{new_date}", "tt": f"{title}", "d": f"{date}"})
    cur.execute("update concerts set time==:t where title==:tt and date==:d",
                {"t": f"{new_time}", "tt": f"{title}", "d": f"{date}"})
    cur.execute("update concerts set public==:p where title==:tt and date==:d",
                {"p": f"{public}", "tt": f"{title}", "d": f"{date}"})

    con.commit()
def update_class(id, teacher, new_id, new_teacher, new_leader, room, login, pwd):
    cur.execute("update classes set id==:i where id==:c and teacher==:t",
                {"i": f"{new_id}", "c": f"{id}", "t": f"{teacher}"})
    cur.execute("update classes set teacher==:t where id==:c and teacher==:q",
                {"t": f"{new_teacher}", "c": f"{id}", "q": f"{teacher}"})
    cur.execute("update classes set leader==:l where id==:c and teacher==:t",
                {"l": f"{new_leader}", "c": f"{id}", "t": f"{teacher}"})
    cur.execute("update classes set room==:r where id==:c and teacher==:t",
                {"c": f"{id}", "t": f"{teacher}", "r": f"{room}"})
    cur.execute("update classes set login==:l where id==:c and teacher==:t",
                {"l": f"{login}", "c": f"{id}", "t": f"{teacher}"})
    cur.execute("update classes set pwd==:p where id==:c and teacher==:t",
                {"p": f"{pwd}", "c": f"{id}", "t": f"{teacher}"})

    con.commit()

def add_class(id, teacher, leader, room, login, pwd):
    da = [(id, teacher, leader, room, login, pwd)]
    cur.executemany("insert into classes values (?,?,?,?,?,?)", da)
    con.commit()

# cur.execute("create table classes (id text, teacher text, leader text)")

# ur.executemany("insert into concerts values (?,?,?)", data)

con.commit()
