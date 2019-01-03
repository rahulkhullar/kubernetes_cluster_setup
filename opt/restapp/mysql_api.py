from flask import Flask, jsonify,url_for
from flaskext.mysql import MySQL
from flask import request
from flask import make_response
from flask import request, abort
import configparser
import os
import time
import json
import requests

application = Flask(__name__)
mysql = MySQL()

config = configparser.ConfigParser()
config.read("/etc/restapp/config.ini")
# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = username= config.get('mysql','username')
application.config['MYSQL_DATABASE_PASSWORD'] = config.get('mysql','password')
application.config['MYSQL_DATABASE_DB'] = config.get('mysql','databasedb')
application.config['MYSQL_DATABASE_HOST'] = config.get('mysql','databasehost') 
application.config['MYSQL_DATABASE_PORT'] = config.getint('mysql','port') 
#app.config['MYSQL_DATABASE_HOST'] = 'localhost:13306'

mysql.init_app(application)

@application.route('/mysql/data/', methods= ['GET'])
def get_tasks():
  cur = mysql.connect().cursor()
  cur.execute("select * from addressapi.address")
  r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]

  return jsonify({'address': r})


@application.route('/mysql/data/<int:id>', methods=['GET'])
def get_task(id):
  print("Inside GET")
  cur = mysql.connect().cursor()
  cur.execute("select * from addressapi.address where name_id=%s" %(id))
  r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
  if not r:
    resp = make_response("", 404)
    return resp
  return jsonify(r[0])

# @app.route('/mysql/data/<int:id>', methods=['HEADs'])
# def head_task(id):s
#   print ("Inside head")
#   cur = mysql.connect().cursor()
#   cur.execute("select * from addressapi.address where name_id=%s" %(id))
#   r = [dict((cur.description[i][0], value)
#             for i, value in enumerate(row)) for row in cur.fetchall()]
#   print (r)
#   # if len(r) == 0:
#   #   print ("Record not found")
#   #   resp = make_response()
#   #   resp.status_code(404)
#   #   return resp
#   return


@application.route('/mysql/data/', methods=['POST'])
def add_item():
  data = request.json
  # print (data)
  # print (data['name'])
  #name_id_db = data['name_id']
  addline1_db = data['addline1']
  addline2_db = data['addline2']
  city_db = data['city']
  postcode_db = data['postcode']
  sql = "INSERT INTO address (addline1, addline2, city, postcode) VALUES (%s, %s, %s, %s)"
  data = (addline1_db, addline2_db, city_db, postcode_db)
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute(sql, data)
  conn.commit()
  resp = jsonify('User details added')
  resp.status_code = 201
  return resp


@application.route('/mysql/data/<id>', methods=['PUT'])
def update_rec(id):
  get_resp = get_task(id)
  print (get_resp)
  if get_resp.status_code == 404:
    print ("Record does not exist")
    add_item()
    return
  print("Record exists")
  data = request.json
  #data1 = json.loads(data)
  print (data)
  #print (data['addline1'])
  #name_id_db = data['name_id']
  # addline1_db = data['addline1']
  # addline2_db = data['addline2']
  # city_db = data['city']
  # postcode_db = data['postcode']
  sql = "UPDATE address SET name_id = "+ id
  where = "WHERE name_id = "+(id) +";"
  if data.__contains__("addline1"):
    sql += ", addline1 = '" + data['addline1']+"'"
  if data.__contains__("addline2"):
    sql += ", " + "addline2='" + data['addline2']+ "'"
  if data.__contains__("city"):
    sql +=  ", " + "city ='" + data['city']+ "'"
  if data.__contains__("postcode"):
    sql += ", " + "postcode = '" + data['postcode'] + "'"
  sql_query = sql + " " + where
  print(sql_query)
  # sql = "UPDATE address SET addline1 = %s, addline2 = %s, city = %s, postcode = %s WHERE condition"
  # data = (id,addline1_db, addline2_db, city_db, postcode_db)
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute(sql_query)
  conn.commit()
  resp = jsonify('User details updated')
  resp.status_code = 200
  return resp


@application.route('/mysql/data/<id>/', methods=['DELETE'])
def delete_item(id):
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute("DELETE FROM address WHERE name_id=%s",(id))
  conn.commit()
  resp = jsonify('User detail deleted!!')
  resp.status_code = 200
  cursor.close()
  conn.close()
  return resp
if __name__ == "__main__":
    application.run(host='0.0.0.0')
