import psycopg2
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="snake_game",  #
        user="madikbaizakov",  
        password="Madik1722"  
    )

try:
    conf=connect_db()
    conf = connect_db()
    cur = conf.cursor()
    cur.execute("DELETE FROM user_scores WHERE username = 'madik'")
    conf.commit()
    cur.close()
    conf.close()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)