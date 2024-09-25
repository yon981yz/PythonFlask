# -*- coding: utf-8 -*-
"""
author       : Changbin
Description  : MySQL의 Python Databas와 CRUD on Web
Usage1       : http://127.0.0.1:5000/select
Usage        : http://127.0.0.1:5000/insert?code=a001&name=james&dept=math&phone=001&address=seoul
Usage2       : http://127.0.0.1:5000/update?code=a001&name=Ben&dept=econ&phone=002&address=kyeonggi
Usage4       : http://127.0.0.1:5000/update2?code=a001&name=Ben
Usage3       : http://127.0.0.1:5000/remove?code=a001
"""

from flask import Flask, jsonify, request 
import pymysql
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # for utf8

def connection():
    # MySQL Connection
    conn = pymysql.connect(
        host="127.0.0.1",  ## 데이타베이스 ip
        user="root",
        password="qwer1234",
        db="education",
        charset="utf8"
    )
    return conn

@app.route("/select")
def select():
    conn = connection()
    curs = conn.cursor()

    # sql 문장
    sql = "select * from student"
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    print(rows)


    # JSON 만들기
    result = json.dumps(rows, ensure_ascii=False).encode('utf8')
    # return result
    return result

@app.route("/insert")
def insert():
    code = request.args.get("code")
    name = request.args.get("name")
    dept = request.args.get("dept")
    phone = request.args.get("phone")
    address = request.args.get("address")

    conn = connection()
    curs = conn.cursor()

    sql = "insert into student(scode, sname, sdept, sphone, saddress) values (%s,%s,%s,%s,%s)"
    curs.execute(sql, (code, name, dept, phone, address))
    conn.commit()
    return jsonify([{'result': 'OK'}])

@app.route("/remove")
def remove():
    code = request.args.get("code") 

    conn = connection()
    curs = conn.cursor()

    sql = "DELETE FROM student WHERE scode = %s"
    curs.execute(sql, (code,))
    conn.commit()
    conn.close()
    return jsonify([{'result': 'OK'}])

@app.route("/update2")
def update():
    code = request.args.get("code")
    name = request.args.get("name")

    conn = connection()
    curs = conn.cursor()

    sql = """
    UPDATE student 
    SET sname = %s 
    WHERE scode = %s
    """
    curs.execute(sql, (name, code))
    conn.commit()
    return jsonify([{'result': 'OK'}])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True) # 서버ip

