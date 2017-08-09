from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host='sql11.freesqldatabase.com',
                             user='sql11189249',
                             password='1NZl1z5RAf',
                             db='sql11189249',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/categories")
def get_categories():
    try:
        with connection.cursor() as cursor:
            # returns list of dictionaries (json)
            sql = "Select * from Categories order by ID"
            cursor.execute(sql)
            categories = cursor.fetchall()
            return json.dumps({"STATUS":"SUCCESS", "CATEGORIES": categories, "CODE":200})

    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 500})

@get("/category/<id>/products")
def products_in_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "select * from Products where Products.category = '{}'".format(id)
            cursor.execute(sql)
            products_in_this_category = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": products_in_this_category, "CODE": 200})

    except Exception as e:
        return json.dumps({"STATUS":"ERROR", "MSG": repr(e), "CODE": 500})

@get("/products")
def get_products():
    try:
        with connection.cursor() as cursor:
            sql = "Select * from Products"
            cursor.execute(sql)
            products = cursor.fetchall()
            return json.dumps({"STATUS":"SUCCESS", "PRODUCTS": products, "CODE": 200})

    except Exception as e:
        return json.dumps({"STATUS":"ERROR", "MSG":str(repr(e)), "CODE": 500})

@get("/product/<id>")
def get_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "Select * from Products WHERE id = '{}'".format(id)
            cursor.execute(sql)
            product = cursor.fetchall()
            return json.dumps({"STATUS":"SUCCESS", "PRODUCT": product, "CODE": 200})

    except Exception as e:
        if repr(e) == '404':
            return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 404})

        elif repr(e) == '500':
            return json.dumps({"STATUS": "ERROR", "MSG": repr(e), "CODE": 500})


#index automatically invokes a get request on endpoint categories
@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port="7000")
