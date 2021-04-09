# INF142-mandatory-assignment
INF142 Mandatory assignment for group 38 due 09.04.21
Teammates: Trym Ettestøl Osland, Anas Almelhem, Linh My Vu and Stian Rykkje.  


# How to run the project

How to initialize the project (Sql stuff)

First you will need some external software, something to hold the database (such as XAMPP or MySQL Server), 
something to view the database (MySQL workbench) is also recommended, and the python package mysql-connector.
To establish a connection to the database, set up the MySQL Server with port 3306 
(mysql-connector by default uses port 3306). Remember the password you set for the MySQL Server. 
Once this is done, running StorageServer1 will prompt you asking for the password of the MySQL Server, type it in and hit enter.
Now run WeatherStation1 which will send requests to the StorageServer to create a database and some tables (if they do not exist)
WeatherStation1 will then continue running, sending data to StorageServer, which stores the data in the appropriate tables. 
When this is done, a user will be able to retrieve and read data through the Flask website.

How to run the Flask website: 
1. Run app.py
2. Click the link to localhost in terminal (http://127.0.0.1:5000/)
3. Return to app.py terminal and follow questions to specify weather location and data amount
4. Weather data will should now be shown on the localhost webpage

If all steps are done correctly you should see a simple list representation of the weather data from that location

In case you're getting an import error with the SQL library used, use the following command to install the library:
pip install mysql-connector-python

# The general structure of our project

WeatherStation1 uses station.py simulate weather data, 
WeatherStation1 sends this data to StorageStation1 throught the UDP socket. 
StorageStation1 receives data which is stored in it's database. 
StorageStation1 establishes a TCP socket which listens to incoming requests. 
Client can request data from StorageStation1, which StorageStation1 sends through the TCP socket. 
app uses Client to display the incoming data for the user in a Flask website. 

# What we have achieved
We have achieved all the MVP requirements. 

We have added extra functionality in form of an SQL database and a Flask website

SQL:
In StorageServer1 we have used a python SQL library to create a database with tables for each weatherstation connected

Flask: 
A simple list representation of the weather data from a specified location

# Sources 
HTML template copied from this (template.html):
https://realpython.com/primer-on-jinja-templating/