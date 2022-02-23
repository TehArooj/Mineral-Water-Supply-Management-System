import re
from flask import Flask, render_template, request, jsonify, json, session
from DBHandler import DBHandler
import smtplib
from email.message import EmailMessage

HOSTNAME = 'localhost'
USERNAME = 'root'
PASSWORD = ''
DATABASENAME = 'mwms'

app = Flask(__name__)
app.secret_key = "jf3j98j4jfowijf98"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        email_valid = re.search('[a-zA-Z0-9._]+[@]+[a-zA-Z0-9]+[.]{1}[a-zA-Z]+$', response["email"])
        if email_valid == None:
            return "Invalid Email Format"
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        if dbhandler.addUsers(response) == "U":
            return "Email Already Exist!"
        if not (dbhandler.addUsers(response)):
            return "Something went wrong!"
        session["email"] = response["email"]
        return "Account Created Sucessfully"
    else:
        return render_template("index.html")


@app.route('/signin', methods=["POST", "GET"])
def login():
    try:
        response = request.data

        response = json.loads(response.decode())

        session["email"] = response["email"]
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        roleid = dbhandler.loginUser(response["password"], response["email"])

        return jsonify(roleid)
    except Exception as e:
        error = str(e)
        ##print(error)
        return render_template('index.html')


@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return render_template("index.html")


@app.route('/Dashboard')
def dashboard():
    if session.get("email") != None:
        ##print("admin")
        return render_template("Dashboard.html")
    else:
        ##print("wolrd111")
        return render_template("index.html")


@app.route('/Schedule')
def schedule():
    if session.get("email") != None:
        ##print("admin")
        return render_template("schedule.html")
    else:
        ##print("wolrd111")
        return render_template("index.html")


@app.route('/custDashboard')
def CustDashboard():
    if session.get("email") != None:
        ##print("customer")
        return render_template("CustDashboard.html")
    else:
        ##print("wolrd123")
        return render_template("index.html")


@app.route('/custProfile')
def CustProfile():
    if session.get("email") != None:
        ##print("customer profile")
        e = session.get("email")
        ##print(e)
        return render_template("cust_myProfile.html", email=e)
    else:
        ##print("wolrd123")
        return render_template("index.html")


@app.route('/cust_newOrder')
def CustNewOrder():
    if session.get("email") != None:
        ##print("customer")
        return render_template("cust_newOrder.html")
    else:
        ##print("wolrd123")
        return render_template("index.html")


@app.route('/Customer', methods=['GET', 'POST'])
def cust():
    if session.get("email") != None:
        ##print("Hi i am a customer")
        return render_template("customer.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/add_new_customer')
def add_new_cust():
    if session.get("email") != None:
        ##print("Hi i am new customer")
        return render_template("new_customer.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/orders')
def order():
    if session.get("email") != None:
        ##print("Hi i am the one who ordered <3")
        return render_template("orders.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/place_new_order')
def place_new_order():
    if session.get("email") != None:
        ##print("Hi i am the one who ordered <3")
        return render_template("place_new_order.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/new_orders')
def new_orders():
    if session.get("email") != None:
        ##print("New Order <3")
        return render_template("new_orders.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/delivered_orders')
def delivered_orders():
    if session.get("email") != None:
        ##print("Delivered <3")
        return render_template("delivered_orders.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/cancelled_orders')
def cancelled_orders():
    if session.get("email") != None:
        ##print("cancelled_orders<3")
        return render_template("cancelled_orders.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/ac_bills')
def ac_bills():
    if session.get("email") != None:
        ##print("ac_bills<3")
        return render_template("ac_bills.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/ac_receipts')
def ac_receipts():
    if session.get("email") != None:
        ##print("ac_receipts<3")
        return render_template("ac_receipts.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/ac_payments')
def ac_payments():
    if session.get("email") != None:
        ##print("ac_payments<3")
        return render_template("ac_payments.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/rpt_Receive_Stock')
def rpt_Receive_Stock():
    if session.get("email") != None:
        ##print("rpt_StockPage<3")
        return render_template("rpt_Receive_Stock.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/add_new_stock')
def add_new_stock():
    if session.get("email") != None:
        ##print("NewStockPage<3")
        return render_template("add_new_stock.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/rpt_salesSummary')
def rpt_salesSummary():
    if session.get("email") != None:
        ##print("rpt_salesSummary<3")
        return render_template("rpt_salesSummary.html")
    else:
        ##print("Error")
        return render_template("index.html")


@app.route('/rpt_receiptsSummary')
def rpt_receiptsSummary():
    if session.get("email") != None:
        ##print("rpt_receiptsSummary<3")
        return render_template("rpt_receiptsSummary.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/rpt_paymentSummary')
def rpt_paymentSummary():
    if session.get("email") != None:
        ##print("rpt_paymentSummary<3")
        return render_template("rpt_paymentSummary.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/am_Size')
def am_Size():
    if session.get("email") != None:
        ##print("am_Size<3")
        return render_template("am_Size.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/am_chargeCodes')
def am_chargeCodes():
    if session.get("email") != None:
        ##print("am_chargeCodes<3")
        return render_template("am_chargeCodes.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/am_users')
def am_users():
    if session.get("email") != None:
        ##print("am_users<3")
        return render_template("am_users.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/am_newUser')
def am_newUser():
    if session.get("email") != None:
        ##print("am_Newuser<3")
        return render_template("am_newUser.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/am_roles')
def am_roles():
    if session.get("email") != None:
        ##print("am_roles<3")
        return render_template("am_roles.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/product')
def product():
    if session.get("email") != None:
        ##print("product<3")
        return render_template("product.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


@app.route('/stockOnHand')
def stockOnHand():
    if session.get("email") != None:
        ##print("StockOnHand<3")
        return render_template("rpt_stockOnHand.html")
    else:
        ##print("wolrd")
        return render_template("index.html")


# db functions calling
# Size
@app.route('/addSize', methods=["POST", "GET"])
def addsize():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.addSize(response)
        if status:
            return jsonify(status)
        else:
            ##print("size record fail")
            return status


@app.route('/getSize', methods=["POST", "GET"])
def getSize():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getSize()
        data = result[0]
        RowCount = result[1]
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        ##print(error)
        return render_template('index.html', error=error)


@app.route('/delSize', methods=['POST', 'GET'])
def delSize():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.delSize(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/showSizeRow', methods=['POST', 'GET'])
def showSizeRow():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.showSizeRow(recid)
        ##print(result)
        return jsonify(result)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/addSizeById', methods=["POST", "GET"])
def addSizeById():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print("response: ", response)
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.addSizeById(response)
        if status == True:
            return jsonify(status)
        else:
            ##print("size record fail")
            return status


# Roles
@app.route('/getRoles', methods=["POST", "GET"])
def getRoles():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getRoles()
        data = result[0]
        RowCount = result[1]

        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# Users
@app.route('/addnewUser', methods=["POST", "GET"])
def addnewUser():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print(response)
        emailValid = re.search('[a-zA-Z0-9._]+[@]+[a-zA-Z0-9]+[.]{1}[a-zA-Z]+$', response["email"])
        if emailValid == None:
            return "Invalid Email Format"
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.addnewUser(response)

        if status == True:
            ##print("Email Not!!!!!!!!!!!")
            return jsonify(status)
        else:
            ##print("Status Gone")
            ##print("Email Already Exist!")
            return jsonify(status)


@app.route('/getUsers', methods=["POST", "GET"])
def getUser():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getUser()
        data = result[0]
        RowCount = result[1]

        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/delUser', methods=['POST', 'GET'])
def delUser():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.delUser(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# Charge Code
@app.route('/addChargeCode', methods=["POST", "GET"])
def addCharge():
    error = None
    db = None
    try:
        if request.method == "POST":
            response = request.data
            response = json.loads(response.decode())
            dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
            status = dbhandler.addChargeCode(response)
            if status == True:
                return jsonify(status)
            else:
                ##print("charge code record fail")
                return status
    except Exception as e:
        error = str(e)
        return "error occured"


@app.route('/getChargeCode', methods=["POST", "GET"])
def getCharge():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getChargeCode()
        data = result[0]
        RowCount = result[1]
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return "error occured"


@app.route('/delChargeCode', methods=['POST', 'GET'])
def delChargeCode():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.delChargeCode(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/showChargeRow', methods=['POST', 'GET'])
def showChargeRow():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.showChargeRow(recid)
        ##print(result)
        return jsonify(result)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/addChargeById', methods=["POST", "GET"])
def addChargeById():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print("response: ", response)
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.addChargeById(response)
        if status == True:
            return jsonify(status)
        else:
            ##print("size record fail")
            return status


# Product Page
@app.route('/showProductRow', methods=['POST', 'GET'])
def showProductRow():
    error = None
    db = None
    try:
        ##print("I am here in showProductRow app.py ")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        p_id = request.args.get('p_id')
        ##print('p_id: ', p_id)
        result = dbhandler.showProductRow(p_id)
        ##print("dear result: ")
        ##print(result)
        return jsonify(result)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/updateProductRow', methods=["POST", "GET"])
def updateProductRow():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print("response: ", response)
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.updateProductRow(response)
        if status == True:
            return jsonify(status)
        else:
            ##print("udpating product failed")
            return status


@app.route('/setOptions', methods=["POST", "GET"])
def setOptions():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.setOptions()
        data = result[0]
        RowCount = result[1]
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/addProduct', methods=["POST", "GET"])
def addProduct():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print(response)
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.addProduct(response)
        if status == True:
            return jsonify(status)
        else:
            ##print("Adding product failed")
            return status


@app.route('/getProducts', methods=["POST", "GET"])
def getproducts():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getProducts()
        data = result[0]
        RowCount = result[1]
        ##print("in get product root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/delProduct', methods=['POST', 'GET'])
def delProduct():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)

        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.delProduct(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# Customers
@app.route('/addnewCustomer', methods=["POST", "GET"])
def addnewCustomer():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print(response)
        emailValid = re.search('[a-zA-Z0-9._]+[@]+[a-zA-Z0-9]+[.]{1}[a-zA-Z]+$', response["email"])
        if emailValid == None:
            return "Invalid Email Format"
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.addnewCustomer(response)

        if status == True:
            ##print("Email Not!!!!!!!!!!!")
            return jsonify(status)
        else:
            ##print("Status Gone")
            ##print("Email Already Exist!")
            return jsonify(status)


@app.route('/getCustomers', methods=["POST", "GET"])
def getCustomer():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getCustomer()
        data = result[0]
        RowCount = result[1]

        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/delCustomer', methods=['POST', 'GET'])
def delCustomer():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)

        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.delCustomer(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# new order, admin dashboard
@app.route('/displayCustomersOptions', methods=["POST", "GET"])
def displayCustomersOptions():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.displayCustomersOptions()
        data = result[0]
        RowCount = result[1]
        ##print("Im im root displayCustomersOptions after getting data from db here is the data:")
        ##print('data', data)
        ##print('RowCount', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/displaySizeOptions', methods=["POST", "GET"])
def displaySizeOptions():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.displaySizeOptions()
        data = result[0]
        RowCount = result[1]
        ##print("Im im root displayCustomersOptions after getting data from db here is the data:")
        ##print('data', data)
        ##print('RowCount', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# orders
@app.route('/displayEmployeesOptions', methods=["POST", "GET"])
def displayEmployeesOptions():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.displayEmployeesOptions()
        data = result[0]
        RowCount = result[1]

        ##print('Employee Options: ', data)
        ##print('Employee Options RowCount:', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/showRate', methods=["POST", "GET"])
def showRate():
    error = None
    db = None
    if request.method == "POST":
        try:
            response = request.data
            response = json.loads(response.decode())

            dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
            results = dbhandler.showRate(response)
            data = results[0]

            return jsonify(data)
        except Exception as e:
            error = str(e)
            return render_template('index.html')


@app.route('/admin_newOrder', methods=["POST", "GET"])
def admin_newOrder():
    error = None
    db = None
    if request.method == "POST":
        try:
            response = request.data
            response = json.loads(response.decode())
            ##print("Order Details: ", response)
            dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)

            email = session.get("email")
            status = dbhandler.admin_newOrder(response, email)

            if status == True:
                return jsonify(status)
            else:
                ##print("Adding new order failed.")
                return status
        except Exception as e:
            error = str(e)
            return render_template('index.html')


@app.route('/setOptions_toGet_ProductName', methods=["POST", "GET"])
def setOptions_toGet_ProductName():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.setOptions_toGet_ProductName()
        data = result[0]
        RowCount = result[1]
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/displayOrders', methods=["POST", "GET"])
def displayOrders():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.displayOrders()
        data = result[0]
        RowCount = result[1]
        ##print("in display Orders root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/setDelivered', methods=['POST', 'GET'])
def setDelivered():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.setDelivered(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/setBilled', methods=['POST', 'GET'])
def setBilled():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.setBilled(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/setCancelled', methods=['POST', 'GET'])
def setCancelled():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.setCancelled(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/setAssignedTo', methods=['POST', 'GET'])
def setAssignedTo():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        empid = request.args.get('empid')
        ##print('recid ', recid)
        ##print('empid ', empid)

        result = dbhandler.setAssignedTo(recid, empid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# Send Email to Billed Orders
@app.route('/getBilledDataAgainstId', methods=['POST','GET'])
def getBilledDataAgainstId():
    ##print("getbilled")
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ' ,recid)
        result=dbhandler.getBilledDataAgainstId(recid)
        ##print(result)
        Order_ID=result[0]['order_id']
        customer_name=result[0]['customer_name']
        customer_mail=result[0]["customer_mail"]
        customer_address=result[0]["customer_address"]
        customer_ShippingAddress=result[0]["customer_ShippingAddress"]
        customer_Phone=result[0]["customer_Phone"]
        product_name=result[0]['product_name']
        ##print("jinha")
        order_date=result[0]["order_date"]
        delivery_date=result[0]["delivery_date"]
        rate=result[0]["rate"]
        quantity=result[0]["quantity"]
        amount=result[0]["amount"]
        mymail = "fizaleem1030@gmail.com"
        receiverEmail = customer_mail
        msg=EmailMessage()
        msg['Subject']='MWMS Invoices'
        msg['From']=mymail
        msg['To']=receiverEmail
        msg.set_content('Please go to main office branch to receive invoices against your order')
        msg.add_alternative("""\
       <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Invoice</title>
  </head>
  <body style=" position: relative;width: 20cm;height: 21cm; margin: 0 auto; color: #001028;background: #FFFFFF; font-family: Arial, sans-serif; font-size: 12px; font-family: Arial;">
    <header style=" padding: 10px 0;margin-bottom: 30px;">

  <div style="text-align: center;margin-bottom: 10px;">
      <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQc1DbXRTagIWrCV5Gz3KDXV9R1SJdD8Jiang&usqp=CAU"
      style="width:90px;">
  </div>
      <h1 style="border-top: 1px solid  #5D6975;border-bottom: 1px solid  #5D6975;color: #5D6975;font-size: 2.4em;line-height: 1.4em;font-weight: normal;text-align: center;margin: 0 0 20px 0;background:url(https://www.toptal.com/designers/subtlepatterns/patterns/bush.png)">INVOICE</h1>
      <div style="float: right;  text-align: right;">
        <div style="white-space: nowrap;">Mineral water Managment System</div>
        <div style="white-space: nowrap;">455-E New Muslim Town,<br /> Lahore, Pakistan</div>
        <div style="white-space: nowrap;">(602) 519-0450</div>
        <div style="white-space: nowrap;"><a href="mailto:admin123@gmail.com" style="color: #5D6975;text-decoration: underline;">admin123@gmail.com</a></div>
      </div>
      <div >
        <div style="white-space: nowrap;"><span style="color: #5D6975;text-align: right;width: 52px;margin-right: 10px;display: inline-block;font-size: 0.8em;">PROJECT</span> Fresh Mineral Water </div>
        <div style="white-space: nowrap;"><span style="color: #5D6975;text-align: right;width: 52px;margin-right: 10px;display: inline-block;font-size: 0.8em;">CLIENT</span> {customer_name}</div>
        <div style="white-space: nowrap;"><span style="color: #5D6975;text-align: right;width: 52px;margin-right: 10px;display: inline-block;font-size: 0.8em;">ADDRESS</span> {customer_ShippingAddress}</div>
        <div style="white-space: nowrap;"><span style="color: #5D6975;text-align: right;width: 52px;margin-right: 10px;display: inline-block;font-size: 0.8em;">EMAIL</span> <a href="mailto:john@example.com" style="color: #5D6975;text-decoration: underline;">{customer_mail}</a></div>
         <div style="white-space: nowrap;"><span style="color: #5D6975;text-align: right;width: 52px;margin-right: 10px;display: inline-block;font-size: 0.8em;">PHONE</span>  {customer_Phone} </div>
        <div style="white-space: nowrap;"><span style="color: #5D6975;text-align: right;width: 52px;margin-right: 10px;display: inline-block;font-size: 0.8em;">DATE</span>  {order_date} </div>
        <div style="white-space: nowrap;"><span style="color: #5D6975;text-align: right;width: 52px;margin-right: 10px;display: inline-block;font-size: 0.8em;">DUE DATE</span> {delivery_date}</div>
      </div>
    </header>
    <main>
      <table style=" width: 100%;border-collapse: collapse;border-spacing: 0;margin-bottom: 20px;">
        <thead>
          <tr>
            <th style="text-align: center;padding: 5px 20px;color: #5D6975;border-bottom: 1px solid #C1CED9;white-space: nowrap;font-weight: normal;">Order No #</th>
            <th style="text-align: center;padding: 5px 20px;color: #5D6975;border-bottom: 1px solid #C1CED9;white-space: nowrap;font-weight: normal;">PRODUCT </th>
            <th style="text-align: center;padding: 5px 20px;color: #5D6975;border-bottom: 1px solid #C1CED9;white-space: nowrap;font-weight: normal;">PRICE</th>
            <th style="text-align: center;padding: 5px 20px;color: #5D6975;border-bottom: 1px solid #C1CED9;white-space: nowrap;font-weight: normal;">QTY</th>
            <th style="text-align: center;padding: 5px 20px;color: #5D6975;border-bottom: 1px solid #C1CED9;white-space: nowrap;font-weight: normal;">TOTAL</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="text-align: center; padding: 20px; text-align: center; background: #F5F5F5;"> {Order_ID} </td>
            <td style="text-align: center; padding: 20px; text-align: center; background: #F5F5F5;">{product_name}</td>
            <td style="text-align: center; padding: 20px; text-align: center; background: #F5F5F5;">{rate}</td>
            <td style="text-align: center; padding: 20px; text-align: center; background: #F5F5F5;">{quantity}</td>
            <td style="text-align: center; padding: 20px; text-align: right; background: #F5F5F5;">{amount}</td>
          </tr>
          <tr>
            <td colspan="4" style=" padding: 20px;text-align: right;"></td>
            <td style="font-size: 1.2em; padding: 20px;text-align: right;"></td>
          </tr>
          <tr>
            <td colspan="4" style="border-top: 1px solid #5D6975;font-size: 1.2em; padding: 20px; text-align: right;background: #F5F5F5;">GRAND TOTAL</td>
            <td style="border-top: 1px solid #5D6975;font-size: 1.2em; padding: 20px;text-align: right;background: #F5F5F5;">{amount}</td>
          </tr>
        </tbody>
      </table>
      <div>
        <div>NOTICE:</div>
        <div style="color: #5D6975;font-size: 1.2em;">A finance charge of 1.5% will be made on unpaid balances after 30 days.</div>
      </div>
    </main>
    <footer style=" color: #5D6975;width: 100%;height: 30px;position: absolute;bottom: 0;border-top: 1px solid #C1CED9;padding: 8px 0;text-align: center;">
      Invoice was created on a computer and is valid without the signature and seal.
    </footer>
  </body>
</html>
""".format(customer_mail=customer_mail,customer_address=customer_address,customer_ShippingAddress=customer_ShippingAddress,customer_Phone=customer_Phone,customer_name=customer_name,Order_ID=Order_ID,product_name=product_name,rate=rate,quantity=quantity,amount=amount,order_date=order_date,delivery_date=delivery_date),subtype='html')

        smtplibObj = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtplibObj.login("fizaleem1030@gmail.com", "dfmlvpnfyaiobvgy")
        smtplibObj.send_message(msg)
        smtplibObj.quit()
        res="Email Sent"
        return jsonify(str(res))
    except Exception as e:
        error = str(e)
        return "Data not get against id something wrong!!!"



# Bills
@app.route('/delBill', methods=['POST', 'GET'])
def delBill():
    error = None
    db = None
    try:
        ##print("I am here in delBill.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.delBill(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getBills', methods=["POST", "GET"])
def getBills():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getBills()
        data = result[0]
        RowCount = result[1]
        ##print("in get Bills root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/setOrderNooptions', methods=["POST", "GET"])
def setOrderNooptions():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.setOrderNooptions()
        data = result[0]
        RowCount = result[1]
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/showAmountBills', methods=["POST", "GET"])
def showAmount_bills():
    error = None
    db = None
    if request.method == "POST":
        try:
            response = request.data
            response = json.loads(response.decode())
            ##print("jo admin_newBills me app.py ko mila ha data:")
            ##print(response)
            dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
            status = dbhandler.showAmountBills(response)
            return jsonify(status)
        except Exception as e:
            error = str(e)
            return render_template('index.html')


@app.route('/setChargeCodeOptionsBillig', methods=["POST", "GET"])
def setChargeCodeOptionsforBilling():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        ##print("Calling CC for Billing")
        result = dbhandler.setChargeCodeOptionsBillig()
        data = result[0]
        RowCount = result[1]
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/addBill', methods=["POST", "GET"])
def addBill():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print(response)
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.addBill(response)
        if status == True:
            return jsonify(status)
        else:
            ##print("Adding Bill failed")
            return status


# Payments
@app.route('/delPayment', methods=['POST', 'GET'])
def delPayment():
    error = None
    db = None
    try:
        ##print("I am here in delPayment.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)

        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.delPayment(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getPayments', methods=["POST", "GET"])
def getPayments():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getPayments()
        data = result[0]
        RowCount = result[1]
        ##print("in get Payments root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/addPayment', methods=["POST", "GET"])
def addPayment():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print("in app.py add Payment root here's the data recieved: ")
        ##print(response)
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.addPayment(response)
        if status == True:
            return jsonify(status)
        else:
            ##print("Adding Receipt failed")
            return status


@app.route('/setChargeCodeOptionsforPayment', methods=["POST", "GET"])
def setChargeCodeOptionsforPayment():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.setChargeCodeOptionsforPayment()
        data = result[0]
        RowCount = result[1]
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# Receipts
@app.route('/delReceipt', methods=['POST', 'GET'])
def delReceipt():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)

        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.delReceipt(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getReceipts', methods=["POST", "GET"])
def getReceipts():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getReceipts()
        data = result[0]
        RowCount = result[1]
        ##print("in getReceipts root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/setChargeCodeOptionsforReceipt', methods=["POST", "GET"])
def setChargeCodeOptionsforReceipt():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.setChargeCodeOptionsforReceipt()
        data = result[0]
        RowCount = result[1]
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/receipt_Set_order_AMOUNT', methods=["POST", "GET"])
def receipt_Set_order_AMOUNT():
    error = None
    db = None
    if request.method == "POST":
        try:
            response = request.data
            response = json.loads(response.decode())
            ##print("yelllo order number jiski amount dikhana ha in app.py:::::")
            ##print(response)
            dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
            results = dbhandler.receipt_Set_order_AMOUNT(response)
            data = results[0]
            ##print("wapis db me amount le k agaye")
            ##print(data)
            return jsonify(data)
        except Exception as e:
            error = str(e)
            return render_template('index.html')


@app.route('/addReceipt', methods=["POST", "GET"])
def addReceipt():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print("in app.py add Receipt root here;s the data recieved: ")
        ##print(response)
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.addReceipt(response)
        if status == True:
            return jsonify(status)
        else:
            ##print("Adding Receipt failed")
            return status


# Management Lists
@app.route('/getNewOrder', methods=["POST", "GET"])
def getNewOrder():
    error = None
    db = None
    try:
        ##print("jinja")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        ##print("get new order fun")
        result = dbhandler.getNewOrder()
        data = result[0]
        ##print("data: ", data)
        RowCount = result[1]
        ##print("rowCount", RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getConfirmOrder', methods=["POST", "GET"])
def getConfirmOrder():
    error = None
    db = None
    try:
        ##print("jinja")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        ##print("get new order fun")
        result = dbhandler.getConfirmOrder()
        data = result[0]
        ##print("data: ", data)
        RowCount = result[1]
        ##print("rowCount", RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getCancelOrder', methods=["POST", "GET"])
def getCancelOrder():
    error = None
    db = None
    try:
        ##print("jinja")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        ##print("get new order fun")
        result = dbhandler.getCancelOrder()
        data = result[0]
        ##print("data: ", data)
        RowCount = result[1]
        ##print("rowCount", RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/DisplayStockOnHand', methods=["POST", "GET"])
def DisplayStockOnHand():
    error = None
    db = None
    try:
        ##print("jinja")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        ##print("get DisplayStockOnHand")
        result = dbhandler.DisplayStockOnHand()
        data = result[0]
        ##print("data: ", data)
        RowCount = result[1]
        ##print("rowCount", RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# Stocks

@app.route('/displayStocks', methods=["POST", "GET"])
def displayStocks():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.displayStocks()
        data = result[0]
        RowCount = result[1]
        ##print("in display Orders root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/Admin_addNewStock', methods=["POST", "GET"])
def Admin_addNewStock():
    error = None
    db = None
    if request.method == "POST":
        try:
            response = request.data
            response = json.loads(response.decode())
            ##print("jo admin_newStock  me app.py ko mila ha data:")
            ##print(response)
            dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)

            status = dbhandler.Admin_addNewStock(response)

            if status == True:
                return jsonify(status)
            else:
                ##print("Adding Admin's new stock failed")
                return status

        except Exception as e:
            error = str(e)
            return render_template('index.html')


@app.route('/delStock', methods=['POST', 'GET'])
def delStock():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)

        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.delStock(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


####### cust  Dashboard data
@app.route('/get_loggedIn_userData', methods=["POST", "GET"])
def get_loggedIn_userData():
    error = None
    db = None
    if request.method == "POST":
        try:
            response = request.data
            response = json.loads(response.decode())
            ##print("yelllo email:::::")
            ##print(response)
            dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
            results = dbhandler.get_loggedIn_userData(response)
            data = results[0]
            ##print("here im in get_loggedIn_userData root, after getting data fron db here the data is:")
            ##print("lalallal")
            ##print(data)
            return jsonify(data)

        except Exception as e:
            error = str(e)
            return render_template('index.html')


# Update_Customer_profile

@app.route('/updateCustPofile', methods=["POST", "GET"])
def updateCustPofile():
    if request.method == "POST":
        response = request.data
        response = json.loads(response.decode())
        ##print("updated customer info app.py got: ")
        ##print(response)

        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        status = dbhandler.updateCustPofile(response)
        if status == True:
            return jsonify(status)
        else:
            ##print("Updating customer profile failed")
            return status


@app.route('/displayCustOrders', methods=["POST", "GET"])
def displayCustOrders():
    error = None
    db = None
    try:
        e = session.get("email")
        ##print(e)
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.displayCustOrders(e)
        data = result[0]
        RowCount = result[1]
        ##print("in display Orders root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/Customer_newOrder', methods=["POST", "GET"])
def Customer_newOrder():
    error = None
    db = None
    if request.method == "POST":
        try:
            response = request.data
            response = json.loads(response.decode())
            ##print("jo cust_newOrder me app.py ko mila ha data:")
            ##print(response)
            e = session.get("email")
            dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
            status = dbhandler.Customer_newOrder(response, e)
            if status == True:
                return jsonify(status)
            else:
                ##print("Addind Cust's new order failed")
                return status

        except Exception as e:
            error = str(e)
            return render_template('index.html')


@app.route('/setCustOrderCancel', methods=['POST', 'GET'])
def setCustOrderCancel():
    error = None
    db = None
    try:
        ##print("I am here.")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        recid = request.args.get('recid')
        ##print('recid ', recid)
        result = dbhandler.setCustOrderCancel(recid)
        return jsonify(str(result))
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# Summaries
# Sales Summary
@app.route('/getBillByProduct', methods=["POST", "GET"])
def getBillByProduct():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getBillByProduct()
        data = result[0]
        RowCount = result[1]
        ##print("in getBillByProduct root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getBillByCustomer', methods=["POST", "GET"])
def getBillByCustomer():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getBillByCustomer()
        data = result[0]
        RowCount = result[1]
        ##print("in getBillByCustomer root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getdetailedBills', methods=['POST', 'GET'])
def getdetailedBills():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getdetailedBills()
        data = result[0]
        RowCount = result[1]
        ##print("in getdetailedBills root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# Receipts Summary

@app.route('/getReceiptByCharge', methods=["POST", "GET"])
def getReceiptByCharge():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getReceiptByCharge()
        data = result[0]
        RowCount = result[1]
        ##print("in getReceiptByCharge root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getReceiptByCustomer', methods=["POST", "GET"])
def getReceiptByCustomer():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getReceiptByCustomer()
        data = result[0]
        RowCount = result[1]
        ##print("in getBillByCustomer root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getdetailedReceipts', methods=['POST', 'GET'])
def getdetailedReceipts():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getdetailedReceipts()
        data = result[0]
        RowCount = result[1]
        ##print("in getdetailedReceipts root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


# Payments Summary


@app.route('/getPaymentByCharge', methods=["POST", "GET"])
def getPaymentByCharge():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getPaymentByCharge()
        data = result[0]
        RowCount = result[1]
        ##print("in getReceiptByCharge root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getPaymentByCustomer', methods=["POST", "GET"])
def getPaymentByCustomer():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getPaymentByCustomer()
        data = result[0]
        RowCount = result[1]
        ##print("in getPaymentByCustomer root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getdetailedPayments', methods=['POST', 'GET'])
def getdetailedPayments():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getdetailedPayments()
        data = result[0]
        RowCount = result[1]
        ##print("in getdetailedPayments root after getting data from db")
        ##print('data  ', data)
        ##print('RowCount  ', RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        return render_template('index.html', error=error)


@app.route('/getDashboardCardsData', methods=['POST', 'GET'])
def getDashboardCardsData():
    try:
        ##print("Dashboard Rout Begin")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getDashboardCardsData()
        return jsonify(result)
    except Exception as e:
        error = str(e)
        ##print(error)
        return render_template('Dashboard.html', error=error)


@app.route('/getDashboardChartData', methods=['POST', 'GET'])
def getDashboardChartData():
    error = None
    db = None
    try:
        ##print("Dashboard Rout Begin")
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        result = dbhandler.getDashboardChartData()
        ##print(result)
        return jsonify(result)
    except Exception as e:
        error = str(e)
        ##print(error)
        return render_template('Dashboard.html', error=error)


@app.route('/getDeliverySchedule', methods=["POST", "GET"])
def getDeliverySchedule():
    error = None
    db = None
    try:
        dbhandler = DBHandler(HOSTNAME, USERNAME, PASSWORD, DATABASENAME)
        ##print("get getDeliverySchedule")
        result = dbhandler.getDeliverySchedule()
        data = result[0]
        ##print("data: ", data)
        RowCount = result[1]
        ##print("rowCount", RowCount)
        return jsonify(data, RowCount)
    except Exception as e:
        error = str(e)
        ##print(error)
        return render_template('index.html', error=error)


if __name__ == "__main__":
    app.debug = True
    app.run()
