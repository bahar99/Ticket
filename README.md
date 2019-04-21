# Ticket
Network course - Tornado - Mysql 

This is Ticket Management system using Tornado Web server.

Version : 1.0

Build : Passing

Author : bahar boroomand

Language : Python 3.6.5

# PreRequirements
For This Project You Need below Requirements :

 - pyhon
 - mysql

```
$ apt install python mysql
```
 
 In Windows You Also Need:
 
 - Anaconda

# Requirement
For runnig server.py/client.py file You Need to install below pakcage for python :

* tornado
* mysql-connector
```
$ python -m pip install mysql-connector tornado
```
# Step0 : Cloning
First of All Clone the Project :

$ git clone https://github.com/bahar99/Ticket.git

# Step1 : Connect to MySQL and create a database
Connect to MySQL as a user that can create databases and users:
```
$ mysql -u root
```
Create a database named "ticket":
```
mysql> CREATE DATABASE ticket;
```
# Step2 : Create the tables in your new database
Create 2 tables Like below:
- With name new_table: 
![new_table](/table1.png)

-With name new_table2:
![new_table2](/table2.png)
Then now you must put Database information in server.py from line 29 - 34

# Step3 : Run the Ticket project
With the default user, password, and database you can just run:
```
$ python server.py
```

# Usage
Now For Sending Requests You Have 2 Options :

- Postman
- My Client Code

# POSTMAN :
Download and install Postman.

In MY Project I Support Both POST & GET Method for Requesting.

You Can See Example Below :

# MY CLIENT CODE:
Just Go To Client Folders and Run Below Code :
```
$ pip install requests
$ python client.py
```

# Support
Reach out to me at following place!
 *Yahoo at boroomand.bahar@yahoo.co.uk
