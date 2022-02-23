import pymysql
import datetime


class DBHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    # Login/Signup
    def loginUser(self, password, email):

        global db
        try:
            db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cur = db.cursor()
            sql = "SELECT * from app_user where password = '{0}' and email = '{1}'".format(password, email)

            cur.execute(sql)
            results = cur.fetchall()
            for r in results:
                roleid = r[1]
            if len(results) == 0:
                return False

            return roleid
        except Exception as e:
            print("In DB Handler", str(e))
            return False
        finally:
            db.close()

    def addUsers(self, userDetails):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "SELECT * from app_user where email = '{}'".format(userDetails["email"])
            cur.execute(sql)

            results = cur.fetchall()
            if len(results) != 0:
                return "U"
            x = datetime.datetime.now()

            sql = "INSERT INTO app_user (email,username,password,role_id,cnic,fullname,phone,address,created_by,created_on,updated_by,updated_on) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            sql1 = "INSERT INTO customer (email,name,cnic,phone,address,deliver_at,created_by,created_on,updated_by,updated_on) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args1 = (
                userDetails["email"], userDetails.get("name"), userDetails.get("cnic"), userDetails.get("phone"),
                userDetails.get("address"), userDetails.get("address"), 3, x, 3, x)
            args = (
                userDetails["email"], userDetails["userName"], userDetails["password"], 3, userDetails.get("cnic"),
                userDetails.get("name"), userDetails.get("phone"), userDetails.get("address"), 3, x, 3, x)
            result1 = cur.execute(sql1, args1)
            results = cur.execute(sql, args)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Cust Block

    # CUST Profile Usage
    def get_loggedIn_userData(self, c_email):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        custDetails_List = list()
        try:

            sql = "SELECT NAME,CNIC,PHONE,ADDRESS,DELIVER_AT from customer where email = '{}'".format(c_email)
            cur.execute(sql)
            db.commit()
            results = cur.fetchall()

            rowCount = cur.rowcount

            user_info = dict()
            user_info["name"] = results[0][0]
            user_info["cnic"] = results[0][1]
            user_info["phone_no"] = results[0][2]
            user_info["address"] = results[0][3]
            user_info["delivery_at"] = results[0][4]

            custDetails_List.append(user_info)
            return (custDetails_List)

        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def updateCustPofile(self, updatedProfileInfo):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            x = datetime.datetime.now()
            Email = str(updatedProfileInfo.get("email"))
            name = str(updatedProfileInfo.get("fullName"))
            cnic = str(updatedProfileInfo.get("cnic"))
            ph_no = str(updatedProfileInfo.get("ph_no"))
            address = str(updatedProfileInfo.get("address"))
            deliverAt = str(updatedProfileInfo.get("deliverAt"))

            sql = "select CUST_ID from customer where EMAIL=%s"
            cur.execute(sql, Email)
            custID = cur.fetchall()

            print(custID[0][0])

            sql = "UPDATE customer SET NAME=%s,CNIC=%s,PHONE=%s,ADDRESS=%s,DELIVER_AT=%s,UPDATED_BY=%s,UPDATED_ON=%s where CUST_ID=%s;"
            arg = (name, cnic, ph_no, address, deliverAt, 3, x, custID[0][0])
            results = cur.execute(sql, arg)
            db.commit()

            print(results)

            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Orders
    def displayCustOrders(self, email):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        orders_List = list()
        try:

            sql = "select CUST_ID from customer where EMAIL=%s"
            cur.execute(sql, email)
            custID = cur.fetchall()

            sql = "SELECT ORDER_ID,CUST_ID,PRODUCT_ID,ORDER_DATE,DELIVERY_DATE,RATE,QUANTITY,AMOUNT ,STATUS FROM orders where CUST_ID=%s; "
            cur.execute(sql, custID[0][0])
            results = cur.fetchall()

            rowCount = cur.rowcount
            db.commit()
            for r in results:
                order = dict()
                order["order_id"] = str(r[0])
                order["cust_id"] = str(r[1])
                order["product_id"] = str(r[2])
                order["order_date"] = str(r[3])
                order["delivery_date"] = str(r[4])
                order["rate"] = str(int(r[5]))
                order["quantity"] = str(r[6])
                order["amount"] = str(r[7])
                order["status"] = str(r[8])
                orders_List.append(order)
            return (orders_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def Customer_newOrder(self, newOrder_Details, email):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            x = datetime.datetime.now()
            sql = "select CUST_ID from customer where email='{}'".format(email)
            cur.execute(sql)
            db.commit()
            cust_id = cur.fetchall()
            sql = "select USER_ID from app_user where email='{}'".format(email)
            cur.execute(sql)
            db.commit()
            user_id = cur.fetchall()
            sql = "SELECT PRODUCT_ID from product where NAME = '{}'".format(newOrder_Details.get("productSize"))
            cur.execute(sql)
            db.commit()
            p_id = cur.fetchall()
            sql = "INSERT INTO orders(CUST_ID,PRODUCT_ID,USER_ID,ORDER_DATE,DELIVERY_DATE,RATE,QUANTITY,AMOUNT,REMARKS,CREATED_BY,CREATED_ON,UPDATED_BY,UPDATED_ON) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (str(cust_id[0][0]), str(p_id[0][0]), str(user_id[0][0]), newOrder_Details.get("orderDate"),
                    newOrder_Details.get("deliveryON"),
                    newOrder_Details.get("rate"), newOrder_Details.get("quantity"), newOrder_Details.get("amount"),
                    newOrder_Details.get("remarks"), 1, x, 1, x)
            results = cur.execute(sql, args)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def setCustOrderCancel(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "UPDATE orders SET status=%s WHERE order_id=%s"
            args = ('Cancelled', str(recid))
            cur.execute(sql, args)
            db.commit()
            return "Status has been changed to Cancelled successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to change status. Error: " + str(e)
        finally:
            db.close()

    def getNewOrder(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        New_Order_List = list()
        try:

            sql = "SELECT o.ORDER_ID,c.NAME,o.ORDER_DATE,o.DELIVERY_DATE,o.RATE,o.QUANTITY,o.AMOUNT,o.STATUS FROM orders as o inner join customer as c on o.cust_id = c.cust_id WHERE o.STATUS IN ('New', 'Assigned');"

            cur.execute(sql)
            results = cur.fetchall()

            rowCount = cur.rowcount

            db.commit()
            for r in results:
                New_Order = dict()

                New_Order["order_id"] = r[0]
                New_Order["Customer_name"] = r[1]
                New_Order["Order_Date"] = str(r[2])
                New_Order["Delivery_Date"] = str(r[3])
                New_Order["Rate"] = int(r[4])
                New_Order["Quantity"] = r[5]
                New_Order["Amount"] = int(r[6])
                New_Order["Status"] = r[7]

                New_Order_List.append(New_Order)

            return (New_Order_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getConfirmOrder(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        Confirm_Order_List = list()
        try:

            sql = "SELECT o.ORDER_ID,c.NAME,o.ORDER_DATE,o.DELIVERY_DATE,o.RATE,o.QUANTITY,o.AMOUNT,o.STATUS FROM orders as o inner join customer as c on o.cust_id = c.cust_id WHERE o.STATUS='Delivered';"
            cur.execute(sql)
            results = cur.fetchall()

            rowCount = cur.rowcount

            db.commit()
            for r in results:
                Confirm_Order = dict()

                Confirm_Order["order_id"] = r[0]
                Confirm_Order["Customer_name"] = r[1]
                Confirm_Order["Order_Date"] = str(r[2])
                Confirm_Order["Delivery_Date"] = str(r[3])
                Confirm_Order["Rate"] = int(r[4])
                Confirm_Order["Quantity"] = r[5]
                Confirm_Order["Amount"] = int(r[6])
                Confirm_Order["Status"] = r[7]

                Confirm_Order_List.append(Confirm_Order)
            return (Confirm_Order_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getCancelOrder(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        Cancel_Order_List = list()
        try:

            sql = "SELECT o.ORDER_ID,c.NAME,o.ORDER_DATE,o.DELIVERY_DATE,o.RATE,o.QUANTITY,o.AMOUNT,o.STATUS FROM orders as o inner join customer as c on o.cust_id = c.cust_id WHERE o.STATUS='Cancelled';"
            cur.execute(sql)
            results = cur.fetchall()

            rowCount = cur.rowcount

            db.commit()
            for r in results:
                Cancel_Order = dict()

                Cancel_Order["order_id"] = r[0]
                Cancel_Order["Customer_name"] = r[1]
                Cancel_Order["Order_Date"] = str(r[2])
                Cancel_Order["Delivery_Date"] = str(r[3])
                Cancel_Order["Rate"] = int(r[4])
                Cancel_Order["Quantity"] = r[5]
                Cancel_Order["Amount"] = int(r[6])
                Cancel_Order["Status"] = r[7]

                Cancel_Order_List.append(Cancel_Order)
            return (Cancel_Order_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Admin Block
    # Lists

    def DisplayStockOnHand(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        OnHandList = list()
        try:

            sql = "SELECT P.PRODUCT_ID, P.NAME, IFNULL(SUM(QTY_IN - S.QTY_OUT),0) AS on_hand FROM product AS P LEFT OUTER JOIN stock AS S ON S.PRODUCT_ID = P.PRODUCT_ID GROUP BY S.PRODUCT_ID, P.NAME ;"
            cur.execute(sql)
            results = cur.fetchall()

            rowCount = cur.rowcount

            db.commit()
            for r in results:
                OnHand = dict()

                OnHand["product_id"] = r[0]
                OnHand["name"] = r[1]
                OnHand["on_hand"] = str(r[2])

                OnHandList.append(OnHand)

            return (OnHandList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Size
    def addSize(self, sizeDetails):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            x = datetime.datetime.now()
            sql = "INSERT INTO Sizes (SHORT_NAME, FULL_NAME,created_by,created_on,updated_by,updated_on) values (%s,%s,%s,%s,%s,%s)"
            args = (
            sizeDetails.get("shortName"), sizeDetails.get("fullName"), 1, x, 1, x)
            results = cur.execute(sql, args)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getSize(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        P_List = list()
        try:
            sql = "SELECT Size_id,short_name,full_name,active FROM Sizes"
            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            db.commit()
            for r in results:
                P_size = dict()
                P_size["Size_id"] = r[0]
                P_size["short_name"] = r[1]
                P_size["full_name"] = r[2]
                str = r[3]
                str = str.decode('UTF-8')
                converted = ord(str)  # ord() converts unicode to decimal
                P_size["active"] = converted
                P_List.append(P_size)
            return (P_List, rowCount)
        except Exception as e:
            print(str(e))
            return False
        finally:
            db.close()

    def delSize(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "DELETE FROM sizes WHERE size_id=%s"
            cur.execute(sql, str(recid))
            db.commit()
            return "Size deleted successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to delete Size. Error: " + str(e)
        finally:
            db.close()

    def showSizeRow(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        P_List = list()
        try:
            sql = "SELECT SHORT_NAME,FULL_NAME from sizes WHERE size_id=%s"
            cur.execute(sql, str(recid))
            results = cur.fetchall()
            db.commit()
            for r in results:
                P_size = dict()
                P_size["short_name"] = r[0]
                P_size["full_name"] = r[1]

                P_List.append(P_size)
            return (P_List)
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to get Size data. Error: " + str(e)
        finally:
            db.close()

    def addSizeById(self, sizeDetails):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:

            x = datetime.datetime.now()
            sql = "Update sizes SET SHORT_NAME=%s,FULL_NAME=%s WHERE size_id=%s;"
            args = (
                sizeDetails.get("ShortName"), sizeDetails.get("FullName"), sizeDetails.get("Sizeid"))
            results = cur.execute(sql, args)

            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Roles
    def getRoles(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        P_List = list()
        try:

            sql = "SELECT role_id,description,permission_remarks,active FROM app_role"

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            db.commit()
            RolesList = list()
            for r in results:
                AppRoles = dict()
                AppRoles["role_id"] = r[0]
                AppRoles["description"] = r[1]
                AppRoles["permission_remarks"] = r[2]
                str = r[3]
                str = str.decode('UTF-8')
                converted = ord(str)  # ord() converts unicode to decimal
                AppRoles["active"] = converted
                RolesList.append(AppRoles)
            return (RolesList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Users
    def addnewUser(self, userDetails):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "SELECT * from app_user where email = '{}'".format(userDetails["email"])
            cur.execute(sql)
            results = cur.fetchall()
            if len(results) != 0:
                return False
            x = datetime.datetime.now()

            sql = "INSERT INTO app_user (email,username,password,role_id,cnic,fullname,phone,address,created_by,created_on,updated_by,updated_on) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (
                userDetails["email"], userDetails["username"], userDetails["password"], 2, userDetails.get("cnic"),
                userDetails.get("fullName"), userDetails.get("phone"), userDetails.get("address"), 1, x, 1, x)
            results = cur.execute(sql, args)
            print("Data gone to db")
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getUser(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:

            sql = "SELECT user_id,username,fullname,email,active FROM app_user"

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            db.commit()
            UsersList = list()
            for r in results:
                AppUsers = dict()
                AppUsers["user_id"] = r[0]
                AppUsers["username"] = r[1]
                AppUsers["fullname"] = r[2]
                AppUsers["email"] = r[3]
                str = r[4]
                str = str.decode('UTF-8')
                converted = ord(str)  # ord() converts unicode to decimal
                AppUsers["active"] = converted
                UsersList.append(AppUsers)
            return (UsersList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def delUser(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "DELETE FROM app_user WHERE user_id=%s"
            cur.execute(sql, str(recid))
            db.commit()
            return "User deleted successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to delete User. Error: " + str(e)
        finally:
            db.close()

    # ChargeCode
    def addChargeCode(self, ChargeDetails):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            x = datetime.datetime.now()
            sql = "INSERT INTO charge_code (DESCRIPTION, FOR_BILLING,FOR_PAYMENT,FOR_RECEIPT, CREATED_BY,CREATED_ON,updated_by,updated_on) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (
                ChargeDetails.get("description"), ChargeDetails.get("billing"), ChargeDetails.get("payment"),
                ChargeDetails.get("receipt"), 1, x, 1, x)
            results = cur.execute(sql, args)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getChargeCode(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        P_ChargeList = list()
        try:
            sql = "SELECT CHARGE_ID,DESCRIPTION,active,FOR_BILLING, FOR_PAYMENT,FOR_RECEIPT FROM charge_code"
            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            db.commit()
            for r in results:
                P_Charge = dict()
                P_Charge["CHARGE_ID"] = r[0]
                P_Charge["DESCRIPTION"] = r[1]
                str = r[2]
                str = str.decode('UTF-8')
                converted = ord(str)  # Ord() Converts Unicode to Integer
                P_Charge["active"] = converted
                str = r[3]
                str = str.decode('UTF-8')
                converted = ord(str)
                P_Charge["FOR_BILLING"] = converted
                str = r[4]
                str = str.decode('UTF-8')
                converted = ord(str)
                P_Charge["FOR_PAYMENT"] = converted
                str = r[5]
                str = str.decode('UTF-8')
                converted = ord(str)
                P_Charge["FOR_RECEIPT"] = converted
                P_ChargeList.append(P_Charge)
            return (P_ChargeList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def delChargeCode(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "DELETE FROM charge_code WHERE charge_id=%s"
            cur.execute(sql, str(recid))
            db.commit()
            return "ChargeCode deleted successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to delete ChargeCode. Error: " + str(e)
        finally:
            db.close()

    def showChargeRow(self, recid):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        P_ChargeList = list()
        try:

            sql = "SELECT description,active,FOR_BILLING,FOR_PAYMENT,FOR_RECEIPT from charge_code WHERE charge_id=%s"

            cur.execute(sql, recid)

            results = cur.fetchall()

            db.commit()
            for r in results:
                P_Charge = dict()
                P_Charge["DESCRIPTION"] = r[0]
                str = r[1]
                str = str.decode('UTF-8')

                converted = ord(str)  # Ord() Converts Unicode to Integer
                P_Charge["active"] = converted
                str = r[2]
                str = str.decode('UTF-8')
                converted = ord(str)
                P_Charge["FOR_BILLING"] = converted
                str = r[3]
                str = str.decode('UTF-8')
                converted = ord(str)
                P_Charge["FOR_PAYMENT"] = converted
                str = r[4]
                str = str.decode('UTF-8')
                converted = ord(str)
                P_Charge["FOR_RECEIPT"] = converted

                P_ChargeList.append(P_Charge)

            return (P_ChargeList)
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to get Size data. Error: " + str(e)
        finally:
            db.close()

    def addChargeById(self, ChargeDetails):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:

            x = datetime.datetime.now()
            sql = "Update charge_code SET description=%s,active=%s,FOR_BILLING=%s,FOR_PAYMENT=%s,FOR_RECEIPT=%s WHERE charge_id=%s;"
            args = (
                ChargeDetails.get("description"), ChargeDetails.get("active"), ChargeDetails.get("billing"),
                ChargeDetails.get("payment"), ChargeDetails.get("receipt"), ChargeDetails.get("Chargeid"))
            results = cur.execute(sql, args)

            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Product Page
    def showProductRow(self, p_id):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        P_List = list()
        try:
            sql = "SELECT NAME,SIZE_ID,RATE from product WHERE PRODUCT_ID=%s"
            cur.execute(sql, str(p_id))
            results = cur.fetchall()
            db.commit()

            name = str(results[0][0])
            size_id = str(results[0][1])
            rate = str(int(results[0][2]))

            sql = "SELECT FULL_NAME FROM sizes where SIZE_ID=%s"
            cur.execute(sql, size_id)
            results = cur.fetchall()
            db.commit()
            full_name = str(results[0][0])

            product = dict()
            product["product_name"] = name
            product["full_name"] = full_name
            product["rate"] = rate

            P_List.append(product)
            return (P_List)
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to get product row data. Error: " + str(e)
        finally:
            db.close()

    def updateProductRow(self, productDetails):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "select SIZE_ID from sizes where FULL_NAME=%s"
            arg = productDetails.get("fullName")
            cur.execute(sql, arg)
            size_id = cur.fetchall()

            x = datetime.datetime.now()
            sql = "Update product SET SIZE_ID=%s,NAME=%s,RATE=%s,UPDATED_BY=%s,UPDATED_ON=%s WHERE PRODUCT_ID=%s;"
            args = (size_id[0][0],
                    productDetails.get("productName"), productDetails.get("rate"), 1, x, productDetails.get("p_id"))
            results = cur.execute(sql, args)

            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def setOptions(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        P_List = list()
        try:
            sql = "select FULL_NAME from sizes"
            cur.execute(sql)
            db.commit()
            results = cur.fetchall()
            rowCount = cur.rowcount
            for r in results:
                P_options = dict()
                P_options["full-name"] = r[0]
                P_List.append(P_options)
            return (P_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def addProduct(self, Product_Details):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:

            x = datetime.datetime.now()

            sql = "select SIZE_ID from sizes where FULL_NAME=%s"
            arg = Product_Details.get("Psize")
            db.commit()
            cur.execute(sql, arg)
            result = cur.fetchall()

            sql = "INSERT INTO product (SIZE_ID,NAME,RATE,CREATED_BY,CREATED_ON,UPDATED_BY,UPDATED_ON) values (%s,%s,%s,%s,%s,%s,%s)"
            args = (result, Product_Details.get("Pname"), Product_Details.get("Prate"), 1, x, 1, x)
            results = cur.execute(sql, args)
            db.commit()

            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getProducts(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        P_List = list()
        try:

            sql = "SELECT PRODUCT_ID,NAME,SIZE_ID,RATE,active FROM product"
            cur.execute(sql)
            results = cur.fetchall()

            rowCount = cur.rowcount
            db.commit()
            for r in results:
                Product = dict()
                Product["p_id"] = r[0]
                Product["name"] = r[1]
                Product["s_id"] = r[2]
                Product["rate"] = int(r[3])
                str = r[4]
                str = str.decode('UTF-8')
                converted = ord(str)  # ord() converts unicode to decimal
                Product["active"] = converted
                P_List.append(Product)
            return (P_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def delProduct(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "DELETE FROM product WHERE product_id=%s"
            cur.execute(sql, str(recid))
            db.commit()
            return "Product deleted successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to delete Product. Error: " + str(e)
        finally:
            db.close()

    # Customer
    def addnewCustomer(self, custDetails):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "SELECT * from app_user where email = '{}'".format(custDetails["email"])
            cur.execute(sql)
            results = cur.fetchall()
            if len(results) != 0:
                return False
            x = datetime.datetime.now()
            sql1 = "INSERT INTO customer (email,name,cnic,phone,address,deliver_at,created_by,created_on,updated_by,updated_on) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args1 = (
                custDetails["email"], custDetails.get("fullName"), custDetails.get("cnic"), custDetails.get("phone"),
                custDetails.get("address"), custDetails.get("address"), 1, x, 1, x)
            sql = "INSERT INTO app_user (USERNAME,email,password,role_id,cnic,fullname,phone,address,created_by,created_on,updated_by,updated_on) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (custDetails.get("fullName"),
                    custDetails["email"], custDetails["password"], 3, custDetails.get("cnic"),
                    custDetails.get("fullName"), custDetails.get("phone"), custDetails.get("address"), 1, x, 1, x)
            results = cur.execute(sql, args)
            results1 = cur.execute(sql1, args1)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getCustomer(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:

            sql = "SELECT cust_id,name,cnic,phone,address,email,active FROM customer"

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            db.commit()
            CustomersList = list()
            for r in results:
                Customers = dict()
                Customers["cust_id"] = r[0]
                Customers["name"] = r[1]
                Customers["cnic"] = r[2]
                Customers["phone"] = r[3]
                Customers["address"] = r[4]
                Customers["email"] = r[5]
                CustomersList.append(Customers)
            return (CustomersList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def delCustomer(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "DELETE FROM customer WHERE cust_id=%s"
            cur.execute(sql, str(recid))
            db.commit()
            return "Customer deleted successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to delete customer. Error: " + str(e)
        finally:
            db.close()

    # New Order Admin Dashboard

    def displayCustomersOptions(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        customer_email_List = list()
        try:

            sql = "select EMAIL from CUSTOMER"
            cur.execute(sql)
            db.commit()
            results = cur.fetchall()

            rowCount = cur.rowcount

            for r in results:
                Cust_email_option = dict()
                Cust_email_option["email"] = r[0]
                customer_email_List.append(Cust_email_option)

            return (customer_email_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def displaySizeOptions(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        product_fullnames_List = list()
        try:

            sql = "select FULL_NAME from SIZES"
            cur.execute(sql)
            db.commit()
            results = cur.fetchall()

            rowCount = cur.rowcount

            for r in results:
                size_fullname_option = dict()
                size_fullname_option["full-name"] = r[0]
                product_fullnames_List.append(size_fullname_option)

            return (product_fullnames_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def showRate(self, PRODUCT_NAME):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        rateList = list()
        try:

            sql = "SELECT RATE from product where NAME = '{}'".format(PRODUCT_NAME)
            cur.execute(sql)
            db.commit()
            result_rate = cur.fetchall()

            rate_info = dict()
            rate_info["rate"] = int(result_rate[0][0])
            rateList.append(rate_info)

            return (rateList)

        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def admin_newOrder(self, newOrder_Details, email):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:

            x = datetime.datetime.now()

            sql = "select CUST_ID from customer where email='{}'".format(newOrder_Details.get("customerEmail"))
            cur.execute(sql)
            db.commit()
            cust_id = cur.fetchall()

            sql = "select USER_ID from app_user where email='{}'".format(email)
            cur.execute(sql)
            db.commit()
            user_id = cur.fetchall()

            sql = "SELECT PRODUCT_ID from product where NAME = '{}'".format(newOrder_Details.get("productSize"))
            cur.execute(sql)
            db.commit()
            p_id = cur.fetchall()

            sql = "INSERT INTO orders(CUST_ID,PRODUCT_ID,USER_ID,ORDER_DATE,DELIVERY_DATE,RATE,QUANTITY,AMOUNT,REMARKS,CREATED_BY,CREATED_ON,UPDATED_BY,UPDATED_ON) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            args = (str(cust_id[0][0]), str(p_id[0][0]), str(user_id[0][0]), newOrder_Details.get("orderDate"),
                    newOrder_Details.get("deliveryON"),
                    newOrder_Details.get("rate"), newOrder_Details.get("quantity"), newOrder_Details.get("amount"),
                    newOrder_Details.get("remarks"), str(user_id[0][0]), x, str(user_id[0][0]), x)

            results = cur.execute(sql, args)
            print("Insert Result: ", results)

            db.commit()

            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def setOptions_toGet_ProductName(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        P_List = list()
        try:
            sql = "select NAME from product"
            cur.execute(sql)
            db.commit()
            results = cur.fetchall()
            rowCount = cur.rowcount
            for r in results:
                P_options = dict()
                P_options["full-name"] = r[0]
                P_List.append(P_options)
            return (P_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def displayOrders(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        orders_List = list()
        try:

            sql = "SELECT O.ORDER_ID, C.NAME AS CUSTOMER_NAME, P.NAME AS PRODUCT_NAME, O.ORDER_DATE, O.DELIVERY_DATE, O.RATE, O.QUANTITY, O.AMOUNT, O.STATUS FROM orders AS O INNER JOIN customer AS C ON O.CUST_ID = C.CUST_ID INNER JOIN product AS P ON O.PRODUCT_ID = P.PRODUCT_ID WHERE UPPER(O.STATUS) NOT IN  ('BILLED','CANCELLED') "
            cur.execute(sql)
            results = cur.fetchall()

            rowCount = cur.rowcount
            db.commit()
            for r in results:
                order = dict()
                order["order_id"] = str(r[0])
                order["customer_name"] = str(r[1])
                order["product_name"] = str(r[2])
                order["order_date"] = str(r[3])
                order["delivery_date"] = str(r[4])
                order["rate"] = str(int(r[5]))
                order["quantity"] = str(r[6])
                order["amount"] = str(r[7])
                order["status"] = str(r[8])
                orders_List.append(order)
            return (orders_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def setDelivered(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "UPDATE orders SET status=%s WHERE order_id=%s"
            args = ('Delivered', str(recid))
            cur.execute(sql, args)
            db.commit()
            return "Status has been changed to Delivered successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to change status. Error: " + str(e)
        finally:
            db.close()

    def setBilled(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "UPDATE orders SET status=%s WHERE order_id=%s"
            args = ('Billed', str(recid))
            cur.execute(sql, args)

            sql = """   INSERT INTO bill
                            (ORDER_ID, CHARGE_ID, BILL_DATE, AMOUNT, NARRATION,
                            CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON)
                        SELECT
                            ORDER_ID,'1', DELIVERY_DATE AS BILL_DATE, AMOUNT, CONCAT('Order No. ', ORDER_ID) AS NARRATION,
                            CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON
                        FROM orders
                        WHERE ORDER_ID =  %s """
            args = (str(recid))
            cur.execute(sql, args)

            db.commit()
            return "Status has been changed to Billed successfully."
        except Exception as e:
            db.rollback()
            db.rollback()
            print(str(e))
            return "Unable to change status. Error: " + str(e)
        finally:
            db.close()

    def getBilledDataAgainstId(self, recid):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        orders_List = list()
        try:

            sql = " SELECT O.ORDER_ID, C.NAME AS CUSTOMER_NAME, C.EMAIL AS CUSTOMER_MAIL,C.ADDRESS AS CUSTOMER_ADDRESS,C.DELIVER_AT AS CUSTOMER_DELIVERY_ADDRESS,C.PHONE AS CUSTOMER_PHONE, P.NAME AS PRODUCT_NAME, O.ORDER_DATE, O.DELIVERY_DATE, O.RATE, O.QUANTITY, O.AMOUNT FROM orders AS O INNER JOIN customer AS C ON O.CUST_ID = C.CUST_ID INNER JOIN product AS P ON O.PRODUCT_ID = P.PRODUCT_ID WHERE UPPER(O.STATUS) = 'BILLED' and O.ORDER_ID=%s"
            cur.execute(sql, str(recid))
            results = cur.fetchall()
            db.commit()
            for r in results:
                order = dict()
                order["order_id"] = str(r[0])
                order["customer_name"] = str(r[1])
                order["customer_mail"] = str(r[2])
                order["customer_address"] = str(r[3])
                order["customer_ShippingAddress"] = str(r[4])
                order["customer_Phone"] = str(r[5])
                order["product_name"] = str(r[6])
                order["order_date"] = str(r[7])
                order["delivery_date"] = str(r[8])
                order["rate"] = str(int(r[9]))
                order["quantity"] = str(r[10])
                order["amount"] = str(r[11])

                orders_List.append(order)
            return (orders_List)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def setCancelled(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "UPDATE orders SET status=%s WHERE order_id=%s"
            args = ('Cancelled', str(recid))
            cur.execute(sql, args)
            db.commit()
            return "Status has been changed to Cancelled successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to change status. Error: " + str(e)
        finally:
            db.close()

    def setAssignedTo(self, recid, empid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "UPDATE orders SET ASSIGNED_TO=%s, STATUS='Assigned' WHERE order_id=%s"
            args = (str(empid), str(recid))
            cur.execute(sql, args)

            db.commit()
            return "Order has been assigned successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to assign order. Error: " + str(e)
        finally:
            db.close()

    def displayEmployeesOptions(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        employees_List = list()
        try:
            sql = "select USER_ID,FULLNAME from APP_USER where role_id=%s"
            cur.execute(sql, "2")
            db.commit()
            results = cur.fetchall()
            rowCount = cur.rowcount
            for r in results:
                employees = dict()
                employees["emp_id"] = r[0]
                employees["name"] = r[1]
                employees_List.append(employees)

            return (employees_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Stock
    def displayStocks(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        stocks_List = list()
        try:

            sql = "SELECT  S.REC_ID,S.REC_DATE,P.NAME AS PRODUCT_NAME,S.RATE,S.QUANTITY,S.AMOUNT FROM stock_receipt AS S INNER JOIN product AS P ON P.PRODUCT_ID = S.PRODUCT_ID"
            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            db.commit()
            for r in results:
                stock = dict()
                stock["rec_id"] = str(r[0])
                stock["rec_date"] = str(r[1])
                stock["product_name"] = str(r[2])
                stock["rate"] = str(int(r[3]))
                stock["quantity"] = str(r[4])
                stock["amount"] = str(r[5])
                stocks_List.append(stock)
            return (stocks_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def Admin_addNewStock(self, stock_Details):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:

            x = datetime.datetime.now()

            sql = "SELECT PRODUCT_ID from product where NAME = '{}'".format(stock_Details.get("productSize"))
            cur.execute(sql)
            db.commit()
            p_id = cur.fetchall()

            sql = "INSERT INTO stock_receipt(REC_DATE,PRODUCT_ID,RATE,QUANTITY,AMOUNT,CREATED_BY,CREATED_ON,UPDATED_BY,UPDATED_ON) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            args = (stock_Details.get("stockDate"), str(p_id[0][0]),
                    stock_Details.get("rate"), stock_Details.get("quantity"), stock_Details.get("amount"), 1, x, 1, x)

            results = cur.execute(sql, args)

            db.commit()

            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def delStock(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "DELETE FROM stock_receipt WHERE rec_id=%s"
            cur.execute(sql, str(recid))
            db.commit()
            return "Stock deleted successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to delete Stock. Error: " + str(e)
        finally:
            db.close()

    # Bills

    def delBill(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "DELETE FROM bill WHERE bill_id=%s"
            cur.execute(sql, str(recid))
            db.commit()
            return "Bill deleted successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to delete Bill. Error: " + str(e)
        finally:
            db.close()

    def getBills(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:

            sql = "SELECT b.bill_id,b.bill_date,b.order_id,c.description,b.amount FROM bill as b inner join charge_code as c where b.charge_id=c.charge_id"

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            db.commit()

            BillsList = list()
            for r in results:
                Bills = dict()
                Bills["bill_id"] = r[0]
                Bills["bill_date"] = str(r[1])
                Bills["order_id"] = r[2]
                Bills["description"] = r[3]
                Bills["amount"] = int(r[4])
                BillsList.append(Bills)
            return (BillsList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def setOrderNooptions(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        Orders_List = list()
        try:
            sql = "select order_id from orders where status='billed'"
            cur.execute(sql)
            db.commit()
            results = cur.fetchall()
            rowCount = cur.rowcount
            for r in results:
                Orders_options = dict()
                Orders_options["order_id"] = r[0]
                Orders_List.append(Orders_options)
            return (Orders_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def showAmountBills(self, Order_no):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        Orders_List = list()
        try:
            sql = "select amount from orders where order_id=%s"
            args = (Order_no)
            cur.execute(sql, args)
            db.commit()
            results = cur.fetchall()

            for r in results:
                Orders_options = dict()
                Orders_options["amount"] = int(r[0])
                Orders_List.append(Orders_options)

            return (Orders_List)

        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def setChargeCodeOptionsBillig(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        CC_List = list()
        try:
            sql = "select description from charge_code where for_billing=1 and active=1"

            cur.execute(sql)
            db.commit()
            results = cur.fetchall()
            rowCount = cur.rowcount
            for r in results:
                CC_options = dict()
                CC_options["description"] = r[0]
                CC_List.append(CC_options)
            return (CC_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def addBill(self, Bill_Details):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:

            x = datetime.datetime.now()

            sql = "select order_id from orders where order_id = '{}'".format(Bill_Details.get("OrderNo"))
            cur.execute(sql)
            db.commit()
            result1 = cur.fetchall()

            sql = "select charge_id from charge_code where DESCRIPTION = '{}'".format(Bill_Details.get("ChargeCode"))
            cur.execute(sql)
            db.commit()
            result2 = cur.fetchall()

            sql = "INSERT INTO bill (ORDER_ID,CHARGE_ID,AMOUNT,BILL_DATE,CREATED_ON,CREATED_BY,UPDATED_BY,UPDATED_ON,Narration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (
                result1, result2, Bill_Details.get("Amount"), Bill_Details.get("Date"), x, 1, 1, x, "ready for payment")
            results = cur.execute(sql, args)
            db.commit()

            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # For Payments

    def getPayments(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = "SELECT p.payment_id,p.order_id,p.payment_date,c.description,p.amount FROM payment as p inner join charge_code as c where p.charge_id=c.charge_id"
            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            db.commit()
            PaymentsList = list()
            for r in results:
                Payments = dict()
                Payments["payment_id"] = str(r[0])
                Payments["order_id"] = str(r[1])
                Payments["payment_date"] = str(r[2])
                Payments["charge_id"] = str(r[3])
                Payments["amount"] = str(int(r[4]))
                PaymentsList.append(Payments)
            return (PaymentsList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def setChargeCodeOptionsforPayment(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        CC_List = list()
        try:
            sql = "select description from charge_code where for_payment=1 and active=1"
            cur.execute(sql)
            db.commit()
            results = cur.fetchall()
            rowCount = cur.rowcount
            for r in results:
                CC_options = dict()
                CC_options["description"] = r[0]
                CC_List.append(CC_options)
            return (CC_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def addPayment(self, payment_Details):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            x = datetime.datetime.now()
            # To get charge id from charge code
            sql = "select CHARGE_ID from charge_code where DESCRIPTION=%s"
            arg = payment_Details.get("ChargeCode")
            db.commit()
            cur.execute(sql, arg)
            charge_id = cur.fetchall()

            orderid = payment_Details.get("OrderID")
            paymentdate = payment_Details.get("Date")
            amount = payment_Details.get("Amount")

            sql = "INSERT INTO payment (ORDER_ID,CHARGE_ID,PAYMENT_DATE,AMOUNT,NARRATION,CREATED_BY,CREATED_ON,UPDATED_BY,UPDATED_ON) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (orderid, charge_id[0][0], paymentdate, amount, "narration", 1, x, 1, x)
            results = cur.execute(sql, args)
            db.commit()

            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def delPayment(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "DELETE FROM payment WHERE payment_id=%s"
            cur.execute(sql, str(recid))
            db.commit()
            return "Payment deleted successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to delete Payment. Error: " + str(e)
        finally:
            db.close()

    # For Receipts

    '''def getReceipts(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT  r.receipt_id,c.name as customer_name,r.receipt_date, cc.description, r.amount
                    FROM receipt as r
                             inner join charge_code as cc
                             on r.charge_id = cc.charge_id
                    INNER JOIN orders AS o ON
                        r.ORDER_ID = o.ORDER_ID
                    INNER JOIN customer AS c ON
                        o.CUST_ID = c.CUST_ID
                    ORDER BY r.RECEIPT_ID;"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount=cur.rowcount
            print("GOT SOME DATA ",results)
            db.commit()
            receiptsList=list()
            for r in results:
                receipts=dict()
                receipts["receipt_id"]=str(r[0])
                receipts["customer_name"] = str(r[1])
                receipts["receipt_date"] = str(r[2])
                receipts["charge_id"] = str(r[3])
                receipts["amount"] = str(int(r[4]))
                receiptsList.append(receipts)
            print("Receipts List:", receiptsList)
            return (receiptsList,rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()'''

    def getReceipts(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = "SELECT  r.receipt_id,r.order_id,r.receipt_date,c.description,r.amount FROM receipt as r inner join charge_code as c where r.charge_id=c.charge_id"
            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            db.commit()
            receiptsList = list()
            for r in results:
                receipts = dict()
                receipts["receipt_id"] = str(r[0])
                receipts["order_id"] = str(r[1])
                receipts["receipt_date"] = str(r[2])
                receipts["charge_id"] = str(r[3])
                receipts["amount"] = str(int(r[4]))
                receiptsList.append(receipts)
            return (receiptsList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def setChargeCodeOptionsforReceipt(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        CC_List = list()
        try:
            sql = "select description from charge_code where for_receipt=1 and active=1"
            cur.execute(sql)
            db.commit()
            results = cur.fetchall()
            rowCount = cur.rowcount
            for r in results:
                CC_options = dict()
                CC_options["description"] = r[0]
                CC_List.append(CC_options)
            return (CC_List, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def receipt_Set_order_AMOUNT(self, order_no):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        amountList = list()
        try:

            sql = "SELECT AMOUNT from orders where ORDER_ID = '{}'".format(order_no)
            cur.execute(sql)
            db.commit()
            result_amount = cur.fetchall()

            amount_info = dict()
            amount_info["amount"] = int(result_amount[0][0])
            amountList.append(amount_info)

            return (amountList)

        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    '''def addReceipt(self, Receipt_Details):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            x = datetime.datetime.now()
            #To get charge id from charge code
            sql="select CHARGE_ID from charge_code where DESCRIPTION=%s"
            arg=Receipt_Details.get("ChargeCode")

            cur.execute(sql,arg)
            db.commit()
            charge_id=cur.fetchall()


            cust_name=Receipt_Details.get("Customer")
            receiptdate=Receipt_Details.get("Date")
            amount=Receipt_Details.get("Amount")

            sql = "INSERT INTO receipt (CHARGE_ID,RECEIPT_DATE,AMOUNT,NARRATION,CREATED_BY,CREATED_ON,UPDATED_BY,UPDATED_ON) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (charge_id[0][0],receiptdate,amount,cust_name,1,x,1,x)
            results = cur.execute(sql, args)
            db.commit()

            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()'''

    def addReceipt(self, Receipt_Details):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            x = datetime.datetime.now()
            # To get charge id from charge code
            sql = "select CHARGE_ID from charge_code where DESCRIPTION=%s"
            arg = Receipt_Details.get("ChargeCode")
            db.commit()
            cur.execute(sql, arg)
            charge_id = cur.fetchall()

            orderid = Receipt_Details.get("OrderID")
            receiptdate = Receipt_Details.get("Date")
            amount = Receipt_Details.get("Amount")

            sql = "INSERT INTO receipt (ORDER_ID,CHARGE_ID,RECEIPT_DATE,AMOUNT,NARRATION,CREATED_BY,CREATED_ON,UPDATED_BY,UPDATED_ON) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (orderid, charge_id[0][0], receiptdate, amount, "narration", 1, x, 1, x)
            results = cur.execute(sql, args)
            db.commit()

            return True
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def delReceipt(self, recid):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        try:
            sql = "DELETE FROM receipt WHERE receipt_id=%s"
            cur.execute(sql, str(recid))
            db.commit()
            return "Receipt deleted successfully."
        except Exception as e:
            db.rollback()
            print(str(e))
            return "Unable to delete Receipt. Error: " + str(e)
        finally:
            db.close()

    # Summaries
    # Sales Summary

    def getBillByProduct(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT p.NAME AS PRODUCT, SUM(b.AMOUNT) AS AMOUNT
                    FROM bill AS b INNER JOIN orders AS o ON
                            b.ORDER_ID = o.ORDER_ID
                        INNER JOIN product AS p ON
                            o.PRODUCT_ID = p.PRODUCT_ID
                    GROUP BY p.NAME
                    ORDER BY p.NAME;"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            print("GOT SOME DATA ", results)
            db.commit()
            myList = list()
            for r in results:
                records = dict()
                records["product"] = str(r[0])
                records["amount"] = str(r[1])
                myList.append(records)
            return (myList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getBillByCustomer(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT c.NAME CUSTOMER, SUM(b.AMOUNT) AS AMOUNT
                        FROM bill AS b INNER JOIN orders AS o ON
                                b.ORDER_ID = o.ORDER_ID
                            INNER JOIN customer AS c ON
                                o.CUST_ID = c.CUST_ID
                        GROUP BY c.NAME
                        ORDER BY c.NAME;"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            print("GOT SOME DATA ", results)
            db.commit()
            myList = list()
            for r in results:
                records = dict()
                records["customer"] = str(r[0])
                records["amount"] = str(r[1])
                myList.append(records)
            return (myList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getdetailedBills(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT b.BILL_DATE AS DOC_DATE, b.BILL_ID AS DOC_NO, p.NAME AS PRODUCT, C.NAME AS CUSTOMER, b.AMOUNT AS AMOUNT
                        FROM bill b LEFT OUTER JOIN orders as o
                                ON b.ORDER_ID = o.ORDER_ID
                            LEFT OUTER JOIN customer c ON
                                o.CUST_ID = c.CUST_ID
                            LEFT OUTER JOIN product p ON
                                o.PRODUCT_ID = p.PRODUCT_ID
                        ORDER BY b.BILL_DATE;"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            print("GOT SOME DATA ", results)
            db.commit()
            myList = list()
            for r in results:
                records = dict()
                records["doc_date"] = str(r[0])
                records["doc_no"] = str(r[1])
                records["product"] = str(r[2])
                records["customer"] = str(r[3])
                records["amount"] = str(r[4])
                myList.append(records)
            return (myList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Receipt Summaries
    def getReceiptByCharge(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT c.DESCRIPTION AS CHARGE, SUM(p.AMOUNT) AS AMOUNT
                        FROM receipt p
                                 INNER JOIN charge_code c ON
                            p.CHARGE_ID = c.CHARGE_ID
                        GROUP BY c.DESCRIPTION
                        ORDER BY c.DESCRIPTION;"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            print("GOT SOME DATA ", results)
            db.commit()
            myList = list()
            for r in results:
                records = dict()
                records["charge"] = str(r[0])
                records["amount"] = str(r[1])
                myList.append(records)
            return (myList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getReceiptByCustomer(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT cc.DESCRIPTION AS CHARGE, C.NAME AS CUSTOMER, SUM(p.AMOUNT) AS AMOUNT
                        FROM receipt p LEFT OUTER JOIN orders as o
                                ON p.ORDER_ID = o.ORDER_ID
                            LEFT OUTER JOIN customer c ON
                                o.CUST_ID = c.CUST_ID
                            LEFT OUTER JOIN charge_code cc on
                                p.CHARGE_ID = cc.CHARGE_ID
                        GROUP BY cc.DESCRIPTION, C.NAME
                        ORDER BY cc.DESCRIPTION, c.NAME;"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            print("GOT SOME DATA ", results)
            db.commit()
            myList = list()
            for r in results:
                records = dict()
                records["charge"] = str(r[0])
                records["customer"] = str(r[1])
                records["amount"] = str(r[2])
                myList.append(records)
            return (myList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getdetailedReceipts(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT p.RECEIPT_DATE AS DOC_DATE, p.RECEIPT_ID AS DOC_NO, cc.DESCRIPTION AS CHARGE, C.NAME AS CUSTOMER, p.AMOUNT AS AMOUNT
                        FROM receipt p LEFT OUTER JOIN orders as o
                                ON p.ORDER_ID = o.ORDER_ID
                            LEFT OUTER JOIN customer c ON
                                o.CUST_ID = c.CUST_ID
                            LEFT OUTER JOIN charge_code cc on
                                p.CHARGE_ID = cc.CHARGE_ID
                        ORDER BY p.RECEIPT_DATE;"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            print("GOT SOME DATA ", results)
            db.commit()
            myList = list()
            for r in results:
                records = dict()
                records["doc_date"] = str(r[0])
                records["doc_no"] = str(r[1])
                records["charge"] = str(r[2])
                records["customer"] = str(r[3])
                records["amount"] = str(r[4])
                myList.append(records)
            return (myList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Payment Summaries
    def getPaymentByCharge(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT c.DESCRIPTION AS CHARGE, SUM(p.AMOUNT) AS AMOUNT
                        FROM payment p
                                 INNER JOIN charge_code c ON
                            p.CHARGE_ID = c.CHARGE_ID
                        GROUP BY c.DESCRIPTION
                        ORDER BY c.DESCRIPTION;"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            print("GOT SOME DATA ", results)
            db.commit()
            myList = list()
            for r in results:
                records = dict()
                records["charge"] = str(r[0])
                records["amount"] = str(r[1])
                myList.append(records)
            return (myList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getPaymentByCustomer(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT cc.DESCRIPTION AS CHARGE, C.NAME AS CUSTOMER, SUM(p.AMOUNT) AS AMOUNT
                        FROM payment p LEFT OUTER JOIN orders as o
                                ON p.ORDER_ID = o.ORDER_ID
                            LEFT OUTER JOIN customer c ON
                                o.CUST_ID = c.CUST_ID
                            LEFT OUTER JOIN charge_code cc on
                                p.CHARGE_ID = cc.CHARGE_ID
                        GROUP BY cc.DESCRIPTION, C.NAME
                        ORDER BY cc.DESCRIPTION, c.NAME;
"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            print("GOT SOME DATA ", results)
            db.commit()
            myList = list()
            for r in results:
                records = dict()
                records["charge"] = str(r[0])
                records["customer"] = str(r[1])
                records["amount"] = str(r[2])
                myList.append(records)
            return (myList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    def getdetailedPayments(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()

        try:
            sql = """SELECT p.PAYMENT_DATE AS DOC_DATE, p.PAYMENT_ID AS DOC_NO, cc.DESCRIPTION AS CHARGE, C.NAME AS CUSTOMER, p.AMOUNT AS AMOUNT
                        FROM payment p LEFT OUTER JOIN orders as o
                                ON p.ORDER_ID = o.ORDER_ID
                            LEFT OUTER JOIN customer c ON
                                o.CUST_ID = c.CUST_ID
                            LEFT OUTER JOIN charge_code cc on
                                p.CHARGE_ID = cc.CHARGE_ID
                        ORDER BY p.PAYMENT_DATE;"""

            cur.execute(sql)
            results = cur.fetchall()
            rowCount = cur.rowcount
            print("GOT SOME DATA ", results)
            db.commit()
            myList = list()
            for r in results:
                records = dict()
                records["doc_date"] = str(r[0])
                records["doc_no"] = str(r[1])
                records["charge"] = str(r[2])
                records["customer"] = str(r[3])
                records["amount"] = str(r[4])
                myList.append(records)
            return (myList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

    # Dashboard Cards Data
    def getDashboardCardsData(self):
        try:
            db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cur = db.cursor()

            sql = """   SELECT UPPER(CASE O.STATUS WHEN 'Assigned' THEN 'New' ELSE O.STATUS END) AS STATUS, COUNT(1) AS COUNT
                        FROM orders AS O
                        GROUP BY  UPPER(CASE O.STATUS WHEN 'Assigned' THEN 'New' ELSE O.STATUS END)
                        ORDER BY  UPPER(CASE O.STATUS WHEN 'Assigned' THEN 'New' ELSE O.STATUS END)"""
            cur.execute(sql)
            db.commit()

            results = cur.fetchall()

            billed_orders = list()
            cancelled_orders = list()
            delivered_orders = list()
            new_orders = list()
            return_data = dict()
            for result in results:
                if result[0] == "BILLED":
                    billed_orders.append(str(result[1]))
                elif result[0] == "CANCELLED":
                    cancelled_orders.append(str(result[1]))
                elif result[0] == "DELIVERED":
                    delivered_orders.append(str(result[1]))
                else:
                    new_orders.append(str(result[1]))

            return_data["billed_orders"] = billed_orders
            return_data["cancelled_orders"] = cancelled_orders
            return_data["delivered_orders"] = delivered_orders
            return_data["new_orders"] = new_orders

            print(return_data)
            return return_data
        except Exception as e:
            print(str(e))
            return False
        finally:
            db.close()

    # Dashboard Chart Data
    def getDashboardChartData(self):
        try:
            db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cur = db.cursor()

            sql = """   SELECT T.SECTION, T.MONTH, T.AMOUNT
                        FROM
                        (
                            SELECT 'CANCELLATION' AS SECTION,IFNULL(MONTH(B.ORDER_DATE), M.MONTH) AS MONTH, SUM(IFNULL(B.AMOUNT, 0)) AS AMOUNT
                            FROM months AS M LEFT OUTER JOIN orders AS B ON
                                M.MONTH = IFNULL(MONTH(B.ORDER_DATE), M.MONTH)
                            WHERE IFNULL(UPPER(B.STATUS), 'CANCELLED') = 'CANCELLED'
                            GROUP BY MONTH
                            UNION ALL
                           SELECT 'PAYMENTS' AS SECTION,IFNULL(MONTH(B.PAYMENT_DATE), M.MONTH) AS MONTH, SUM(IFNULL(B.AMOUNT, 0)) AS AMOUNT
                            FROM months AS M LEFT OUTER JOIN payment AS B ON
                                M.MONTH = IFNULL(MONTH(B.PAYMENT_DATE), M.MONTH)
                            GROUP BY MONTH
                            UNION ALL
                            SELECT 'RECEIPTS' AS SECTION,IFNULL(MONTH(B.RECEIPT_DATE), M.MONTH) AS MONTH, SUM(IFNULL(B.AMOUNT, 0)) AS AMOUNT
                            FROM months AS M LEFT OUTER JOIN receipt AS B ON
                                M.MONTH = IFNULL(MONTH(B.RECEIPT_DATE), M.MONTH)
                            GROUP BY MONTH
                            UNION ALL
                           SELECT 'SALES' AS SECTION,IFNULL(MONTH(B.BILL_DATE), M.MONTH) AS MONTH, SUM(IFNULL(B.AMOUNT, 0)) AS AMOUNT
                            FROM months AS M LEFT OUTER JOIN bill AS B ON
                                M.MONTH = IFNULL(MONTH(B.BILL_DATE), M.MONTH)
                            GROUP BY MONTH
                        ) AS T
                        ORDER BY T.SECTION, T.MONTH"""
            cur.execute(sql)
            db.commit()

            results = cur.fetchall()

            cancellation = list()
            payments = list()
            receipts = list()
            sales = list()
            return_data = dict()
            for result in results:
                if result[0] == "CANCELLATION":
                    cancellation.append(str(result[2]))
                elif result[0] == "PAYMENTS":
                    payments.append(str(result[2]))
                elif result[0] == "RECEIPTS":
                    receipts.append(str(result[2]))
                else:
                    sales.append(str(result[2]))

            return_data["cancellation"] = cancellation
            return_data["payments"] = payments
            return_data["receipts"] = receipts
            return_data["sales"] = sales

            print(return_data)
            return return_data
        except Exception as e:
            print(str(e))
            return False
        finally:
            db.close()

    # Delivery Schedule
    def getDeliverySchedule(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = db.cursor()
        ScheduleList = list()
        try:

            sql = """SELECT O.DELIVERY_DATE,
                       IFNULL(U.FULLNAME, '(Not Assigned)') AS EMPLOYEE_NAME,
                       C.NAME AS CUSTOMER_NAME,
                       P.NAME AS PRODUCT_NAME,
                       O.QUANTITY,
                       C.PHONE,
                       C.ADDRESS
                FROM orders AS O
                         LEFT OUTER JOIN app_user AS U
                            ON O.ASSIGNED_TO = U.USER_ID
                         INNER JOIN customer AS C ON O.CUST_ID = C.CUST_ID
                         INNER JOIN product AS P ON O.PRODUCT_ID = P.PRODUCT_ID
                WHERE UPPER(O.STATUS) = 'ASSIGNED'
                ORDER BY U.FULLNAME"""

            cur.execute(sql)
            results = cur.fetchall()

            rowCount = cur.rowcount

            db.commit()
            for r in results:
                schedule = dict()

                schedule["delivery_date"] = (r[0]).strftime("%d %b %Y")
                schedule["employee_name"] = str(r[1])
                schedule["customer_name"] = str(r[2])
                schedule["product_name"] = str(r[3])
                schedule["quantity"] = str(r[4])
                schedule["phone"] = str(r[5])
                schedule["address"] = str(r[6])

                ScheduleList.append(schedule)

            return (ScheduleList, rowCount)
        except Exception as e:
            db.rollback()
            print(str(e))
            return False
        finally:
            db.close()

