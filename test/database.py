import pymysql
conn = pymysql.connect(
    host='127.0.0.1',
    user='newuser1',
    password='111111',
    database='poems',
    port=3306,
    charset='utf8'
)
curson = conn.cursor()


def poemadd(poemcontent, poemtheme):
    curson = conn.cursor()
    sql = 'insert into poemhistory values(%s)'%("'"+poemcontent+"'"+","+"'"+poemtheme+"'")
    curson.execute(sql)
    conn.commit()
    # curson.callproc("poemAdd", [[poemcontent], [poemtheme]])
    # curson.fetchall()


def poemshow():
    curson.callproc("poemShow")
    result = curson.fetchall()
    for row in result:
        print(row)
    return result
#
# //poemadd("123","456")
poemshow()
# curson.close()
# conn.close()
