import os
import platform
import requests
import time
import sys

HOST = "localhost"
PORT = "1104"
CMD = token = ''


def __api__():
    return 'http://' + HOST + ":" + PORT + "/" + CMD


def printres(res):
    array = res["tickets"].split('-')
    c = 0
    while c < int(array[1]):
        temp = res['block {}'.format(c)]
        print('SUBJECT :'+temp['subject'])
        print('ID :'+str(temp['id']))
        print('STATUS :'+temp['status'])
        print('BODY :'+temp['ask'])
        if temp['answer']:
            print('ANSWER :'+temp['answer'])
        else:
            print('ANSWEr :' + "")
        print('DATE :' + temp['date'])
        print("*****************************")
        c = c+1


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def show_func():
    print("""Choose an action :] :
    1) Send Ticket
    2) Get Ticket(customer)
    3) Close Ticket(customer)
    4) Get Ticket Mod(admin)
    5) Response to Ticket(admin)
    6) Change Status(admin)
    7) Logout!
    8) Exit!
    """)


while True:
    clear()
    print("""Choose an action :] :
    1. SignIn
    2. Signup
    3. Exit!
    """)
    status = input()
    if status == '1':
        clear()
        while True:
            print("enter username : \n")
            username = input()
            print("enter password : \n")
            password = input()
            CMD = "login"
            req=requests.post(__api__(), data={'username': username,'password': password}).json()

            if req['code'] == '200':
                clear()
                print("you are successfully logged in")
                token = req['token']

                time.sleep(2)
            else:
                clear()
                print("INCORRECT USERNAME OR PASSWORD :/\nTRY AGAIN ...")
                time.sleep(2)
                break
            while True:
                clear()
                show_func()
                func_type = input()
                if func_type == '1':
                    clear()
                    CMD = "sendticket"
                    subject = input("what is your subject: ")
                    text = input("what is your txt: ")
                    data = requests.post(__api__(), data={'token': token, 'text': text, 'subject': subject}).json()
                    print(data['message'] + '\n')
                    input("Press Any Key To Continue ...")
                if func_type == '2':
                    clear()
                    CMD = "getticketcli"
                    status = input("enter the status you want to get: \n 1)open,2)closed,3)waiting: ")
                    data = requests.get(__api__(), params={'token': token, 'status': status}).json()
                    if data['code'] == '200':
                        i=0

                        for index in data:
                            if index[0] == "b":
                                tempout = data['block {}'.format(i)]
                                print("id : %s\n" % tempout['id'])
                                print("subject : %s\n" % tempout['subject'])
                                print("body : %s\n" % tempout['body'])
                                print("response : %s\n" % tempout['answer'])
                                print("date : %s\n" % tempout['date'])
                                i = i+1
                                print("****************")

                    else:
                        print(data["message"]+'\n')
                    input("Press Any Key To Continue ...")
                if func_type == '3':
                    clear()
                    id = input("enter ticket id : ")
                    CMD = "closeticket"
                    data = requests.post(__api__(), data={'token': token, 'commentId': id}).json()

                    print(data['message']+'\n')
                    input("Press Any Key To Continue ...")
                if func_type == '4':
                    clear()
                    CMD = "getticketmod"
                    status = input("enter the status you want to get: \n 1)open,2)closed,3)waiting: ")
                    data = requests.get(__api__(), params={'token': token, 'status': status}).json()

                    if data['code'] == '200':
                        printres(data)
                    else:
                        print(data["message"] + '\n')
                    input("Press Any Key To Continue ...")
                if func_type == '5':
                    clear()
                    CMD = "restoticketmod"
                    ans = input("enter your response : ")
                    id = input("enter ticket id :")
                    data = requests.post(__api__(), data={'token': token, 'commentId': id, 'text': ans}).json()

                    print(data['message']+'\n')
                    input("Press Any Key To Continue ...")
                if func_type == '6':
                    clear()
                    CMD = "changestatus"
                    status = input("enter the status you want to change to: \n 1)open,2)closed,3)waiting :")
                    id = input("enter ticket id :")
                    data = requests.post(__api__(), data={'token': token, 'commentId': id, 'status': status}).json()

                    print(data['message']+'\n')
                    input("Press Any Key To Continue ...")
                if func_type == '7':
                    clear()
                    CMD = "logout"
                    data = requests.post(__api__(), data={'token': token}).json()
                    print(data['message']+'\n')
                    #input("Press Any Key To Continue ...")
                    sys.exit()
                if func_type == '8':
                    sys.exit()





    elif status == '2':
        clear()
        while True:
            print("Enter The Authentication To Create New Account \n")
            username = input("USERNAME : ")

            password = input("PASSWORD : ")
            CMD = "signup"
            clear()
            data = requests.post(__api__(), data={'username': username, 'password': password}).json()

            if str(data['code']) == "200":
                print("Your Account Is Successfully Created\n"+"Your Username is:"+username+"\n")
                input("Press Any Key To Continue ...")
                break
            else:
                print(data['code']+"\n"+"Try Again")
                input("Press Any Key To Continue ...")
                clear()

    elif status == '3':
        sys.exit()
    else:
        print("Try Again\n")