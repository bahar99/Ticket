import os.path
import mysql.connector
import os
from binascii import hexlify
import tornado.web
from tornado.options import define, options
from datetime import datetime

define("port", default=1104, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # GET METHOD :
            (r"/getticketmod", getticketmod),
            (r"/getticketcli", getticketcli),
            # POST METHOD :
            (r"/signup", signup),
            (r"/login",login),
            (r"/logout", logout),
            (r"/sendticket", sendticket),
            (r"/restoticketmod", restoticketmod),
            (r"/changestatus", changestatus),
            (r"/closeticket", closeticket),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="bahar1234",
            database="ticket",
            auth_plugin = "mysql_native_password"
        )


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def check_user(self,user):
        print(user)
        temp = self.db.cursor()
        temp.execute("SELECT * FROM new_table WHERE username = '{}'".format(user))
        resuser = temp.fetchall()
        if resuser:
            print("true :]")
            return True
        else :
            print("false!")
            return False

    def check_api(self, api):
        temp = self.db.cursor()
        temp.execute("SELECT * FROM new_table WHERE token = '{}'".format(api))
        resuser = temp.fetchall()
        if resuser:
            print(resuser)
            temp.execute("UPDATE new_table SET token = %s WHERE username = %s ", ('', resuser[0][0]))
            self.db.commit()
            return True
        else:
            return False

    def check_auth(self, username, password):
        temp = self.db.cursor()
        temp.execute("SELECT * FROM new_table WHERE username = '{}' and password = '{}'".format(username, password))
        resuser = temp.fetchall()

        if resuser:
            api_token = hexlify(os.urandom(16)).decode('utf-8')
            print(api_token)
            temp.execute("UPDATE new_table SET token = %s WHERE username = %s ", (api_token, username))
            self.db.commit()
            return api_token
        else:
            return False

    def getUserName(self, token):
        temp = self.db.cursor()
        temp.execute("SELECT * FROM new_table WHERE token = '{}'".format(token))
        resuser = temp.fetchall()
        if resuser:
            return resuser[0]
        else:
            return False


# signup
class signup(BaseHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        passWord = self.get_argument('password')
        if not self.check_user(username):
            print(username, passWord)
            temp = self.db.cursor()
            temp.execute("INSERT INTO new_table (username, password, token) VALUES (%s, %s ,%s)",(username,passWord,''))
            self.db.commit()
            output = {
                    'message' : 'Signed Up :]',
                    'code': '200'
            }
            self.write(output)
        else:
            output = {
                'message': 'This username already exist!',
                'code': '400'
            }
            self.write(output)


# login
class login(BaseHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        passWord = self.get_argument('password')
        token = self.check_auth(username, passWord)
        print(token)
        if token:
            print(username, passWord)
            output = {
                      'message': 'Logged in :]',
                      'code': '200',
                      'token': token
            }
            self.write(output)
        else:
            output = {
                'message': 'your password or username is wrong :/',
                'code': '400'
            }
            self.write(output)


# logout
class logout(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        if self.check_api(token):
            output = {
                'message': 'Logged Out',
                'code': '200'
                      }
            self.write(output)
        else:
            output = {
                'message': 'Wrong Token!',
                'code': '400'
            }
            self.write(output)

# sendTicket
class sendticket(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        text = self.get_argument('text')
        subject = self.get_argument('subject')
        user = self.getUserName(token)
        time = datetime.now()
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        if user:
            temp = self.db.cursor()
            temp.execute("INSERT INTO new_table2 (username, body, status, subject, date) VALUES (%s, %s ,%s ,%s, %s)", (user[0], text, 'open', subject,date))
            self.db.commit()
            output = {
                'message': 'Ticket is Sent :]',
                'code': '200'
            }
            self.write(output)
        else:
            output = {
                'message': 'Wrong Token!',
                'code': '400'
            }
            self.write(output)

# restoticketmod
# for admin
class restoticketmod(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        text = self.get_argument('text')
        commentId = self.get_argument('commentId')
        user = self.getUserName(token)
        if user:
            if user[3] is 1:
                temp = self.db.cursor()
                temp.execute("UPDATE new_table2 SET answer = %s ,status = %s WHERE id = %s ", (text, 'closed', int(commentId)))
                self.db.commit()
                output = {
                    'message': 'Response to Ticket With id -{}- Sent Successfully'.format(commentId),
                    'code': '200'
                }

            else:
                output = {
                    'message': 'you are not admin',
                    'code': '400'
                }
            self.write(output)
        else:
            output = {
                'message': 'Wrong Token',
                'code': '400'
            }
            self.write(output)

# change status
#for admin
class changestatus(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        commentId = self.get_argument('commentId')
        status = self.get_argument('status')
        user = self.getUserName(token)
        if user:
            if user[3] is 1:
                temp = self.db.cursor()
                temp.execute("UPDATE new_table2 SET status = %s WHERE id = %s ", (status, int(commentId)))
                self.db.commit()
                output = {
                    'message': 'Status Ticket With id -{}- Changed Successfully'.format(commentId),
                    'code': '200'
                }

            else:
                output = {
                    'message': 'you are not admin',
                    'code': '200'
                }
            self.write(output)
        else:
            output = {
                'message': 'Wrong Token',
                'code': '400'
            }
            self.write(output)

# closeTicket
# for customer
class closeticket(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        commentId = self.get_argument('commentId')
        user = self.getUserName(token)
        if user:
            flag = False
            temp = self.db.cursor()
            temp.execute("SELECT * FROM new_table2 WHERE username = '{}'".format(user[0]))
            resuser = temp.fetchall()
            for index in resuser:
                if index[0] is int(commentId):
                    flag = True
                    temp = self.db.cursor()
                    temp.execute("UPDATE new_table2 SET status = %s WHERE id = %s ", ('closed', int(commentId)))
                    self.db.commit()
                    output = {
                        'message': 'Ticket With id -{} Closed Successfully'.format(commentId),
                        'code': '200'
                    }
                    self.write(output)

            if flag is False:
                output = {
                    'message': 'Id is wrong :/',
                    'code': '400'
                }
                self.write(output)

        else:
            output = {
                'message': 'Wrong Token',
                'code': '400'
            }
            self.write(output)


# getTicket
class getticketcli(BaseHandler):
    def get(self):
        token = self.get_argument('token')
        status = self.get_argument('status')
        print(type(status))
        user = self.getUserName(token)
        if user:
            temp = self.db.cursor()
            if user[3] is 0:
                temp.execute("SELECT * FROM new_table2 WHERE username = '{}'".format(user[0]))
                resuser = temp.fetchall()
                print(resuser)
                output = {
                    'code': '200'
                }
                c = 0
                for index in resuser:
                    tempout = {}
                    if index[2] == status:
                        tempout["subject"] = index[5]
                        tempout["id"] = index[0]
                        tempout["status"] = index[2]
                        tempout["body"] = index[3]
                        tempout["answer"] = index[4]
                        tempout["date"] = index[6]
                        #tempout["date"] = '2019-04-21 11:54:04'

                        output['block {}'.format(c)] = tempout
                        c = c + 1

                output["tickets"] = 'There Are -{}- Ticket'.format(c)
                self.write(output)

            else:
                output = {
                    'message': 'you are admin user',
                    'code': '400'
                }
                self.write(output)

        else:
            output = {
                'message': 'Wrong Token',
                'code': '400'
            }
            self.write(output)

# getTickeMod
class getticketmod(BaseHandler):
    def get(self):
        token = self.get_argument('token')
        status = self.get_argument('status')
        print(type(status))
        user = self.getUserName(token)
        if user:
            temp = self.db.cursor()
            if user[3] is 0:
                output = {
                    'message': 'you are normal user',
                    'code': '400'
                }
                self.write(output)
            else:
                temp.execute("SELECT * FROM new_table2")
                resuser = temp.fetchall()
                print(resuser)
                output = {
                    'code': '200'
                }
                c = 0
                for index in resuser:
                    tempout={}
                    if index[2] == status:
                        tempout["subject"] = index[5]
                        tempout["id"] = index[0]
                        tempout["status"] = index[2]
                        tempout["body"] = index[3]
                        tempout["answer"] = index[4]
                        tempout["date"] = str(index[6])
                        print(type(index[6]))
                        output['block {}'.format(c)] = tempout
                        c = c + 1

                output["tickets"] = 'There Are -{}- Ticket'.format(c)
                self.write(output)

        else:
            output = {
                'message': 'Wrong Token',
                'code': '400'
            }
            self.write(output)



def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()