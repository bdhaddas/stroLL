import sqlite3

# create an SQL connection to the SQLite database
con = sqlite3.connect("site.db")

cur = con.cursor()

# # printing everything from user
# for row in cur.execute('SELECT * FROM user;'):
#     print(row)

# # storing an email in a variable
# cur.execute('SELECT email FROM user WHERE id="1"')
# email1 = cur.fetchall()
# print(email1)

# # returning all attractions where water = true
# cur.execute('SELECT attr_lat, attr_long FROM attractions WHERE water="true"')
# water_attractions = cur.fetchall()
# print(water_attractions)

# put data into database


def create_attraction(con, attr_lat, attr_long, attractionName, attractionDescriptor, water, green_spaces, traffic, buildings):
    sql = """
        INSERT INTO customers (attr_lat, attr_long, attractionName, attractionDescriptor, water, green_spaces, traffic, buildings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    cur = con.cursor()
    cur.execute(sql, (attr_lat, attr_long, attractionName,
                attractionDescriptor, water, green_spaces, traffic, buildings))
    return cur.lastrowid

# get data from database


def get_users(con, id):
    cur.execute("""
    SELECT email, username FROM user WHERE id = ?
    """, (id))
    return(cur.fetchall())


# user1 = get_users(con, '1')
# print(user1)

def get_journeys(con, id):
    cur.execute("""
    SELECT email, username FROM journey WHERE id = ?
    """, (id))
    return(cur.fetchall())

def get_attractions(con, water, green_space, traffic, buildings):
    cur.execute("""
        SELECT attr_lat, attr_long FROM attractions WHERE water = ? AND green_space = ? AND traffic = ? AND buildings = ?
        """, (water, green_space, traffic, buildings))
    return(cur.fetchall())



# close connection
con.close()
