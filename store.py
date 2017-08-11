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

@post("/category")
def add_category():
    name = request.POST.get("name")
    id = request.POST.get("id")
    print(id)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Categories (name) VALUES ('{}')".format(name)
            cursor.execute(sql)
            connection.commit()
            print(cursor.lastrowid)
            return json.dumps({"STATUS":"SUCCESS", "CAT_ID": cursor.lastrowid, "CODE": 201})

    except pymysql.err.IntegrityError as e:
        code, msg = e.args
        if code == 1062:
            return json.dumps({"STATUS":"ERROR", "MSG": msg, "CODE": 200})
        elif code == 1322 or code == 1323:
            return json.dumps({"STATUS":"ERROR", "MSG": msg, "CODE": 400})

    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": "INTERNAL ERROR", "CODE": 500})

@post('/product')
def add_product():

    item_id = request.forms.get("id")
    title = request.forms.get("title")
    desc = request.forms.get("desc")
    price = request.forms.get("price")
    img_url = request.forms.get("img_url")
    category = request.forms.get("category")
    favorite = request.forms.get("favorite")

    if favorite == 'on':
        favorite = 1
    else:
        favorite = 0

    print("item id is:" + item_id)
    print("in post product")

    try:
        with connection.cursor() as cursor:

            #New Product
            if item_id == '': # If there is no id for the item, it is a new item, so add
                sql = "INSERT INTO Products (title, description, price, img_url, category, favorite) Values " \
                      "('{0}', '{1}', '{2}', '{3}', '{4}', '{5}') ".format(title, desc, price, img_url, category, favorite)
                print("New PRoduct")
                cursor.execute(sql)
                connection.commit()
                return json.dumps({"STATUS":"SUCCESS", "PRODUCT_ID": cursor.lastrowid, "CODE": 201})

            elif item_id != '': #Need to update the category rather than add
                print("product already exists, updating it")
                sql = "UPDATE Products SET title = '{0}', description = '{1}', price = '{2}', img_url = '{3}', " \
                      "category = '{4}', favorite = '{5}' " \
                      "WHERE id = '{6}' ".format(title, desc, price, img_url, category, favorite, item_id)
                cursor.execute(sql)
                connection.commit()
                return json.dumps({"STATUS":"SUCCESS", "PRODUCT_ID": cursor.lastrowid, "CODE": 201})

    except pymysql.err.IntegrityError as e:
        code, msg = e.args

        if code == 1322 or code == 1323:
            return json.dumps({"STATUS": "ERROR", "MSG": msg, "CODE": 400})

    except Exception as e:
        return json.dumps({"STATUS":"ERROR", "MSG": "INTERNAL ERROR", "CODE": 500})

@delete('/category/<id>')
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM Categories WHERE id = '{}'".format(id)
            print(sql)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS":"SUCCESS", "CODE": 201})

    except pymysql.err.IntegrityError as e:
        code, msg = e.args
        if code == 1032:
            return json.dumps({"STATUS":"ERROR", "MSG": msg, "CODE": 404})

    except Exception as e:
        return json.dumps({"STATUS":"ERROR", "MSG": "INTERNAL ERROR", "CODE": 500})
    '''
        code = e.args
        code, msg = e.args[0], e.args[1]
    '''
@delete('/product/<id>')
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM Products WHERE id = '{}'".format(id)
            cursor.execute(sql)
            connection.commit()
            print("Successful deletion")
            return json.dumps({"STATUS":"SUCCESS", "CODE": 201})

    except Exception as e:
        return json.dumps({"STATUS":"ERROR", "MSG": repr(e), "CODE": 500})

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
