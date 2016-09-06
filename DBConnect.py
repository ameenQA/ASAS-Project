# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 14:42:16 2016

@author: Administrator
"""

import pymysql


class DBConnect:
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "Pa$$w0rd", "mydb")
        
    def test(self):
        print('helllooooooooooooooooooo')
        
    def setup_connection(self, query_statement): 
        cursor = self.db.cursor()
        
        sql = query_statement
        cursor.execute(sql)
        
        results = cursor.fetchall()
        #print (results)
        return results, cursor
    
    
    def print_records(self, results, cursor):
    
        for row in results:
            id_customer = row[0]
            first_name = row[1]
            surname = row[2]
            print ("ID: " + id_customer + "\t\t First Name: " + first_name + "\t\t Surname: " + surname)
        
        cursor.close()
        self.db.close()


#query_statement = int(input("Please enter a SQL query (Syntax: SELECT * FROM Customer)"))
##query_statement = "SELECT * FROM Customer"
#my_connection = DBConnect()
#results, cursor = my_connection.setup_connection(query_statement)
#my_connection.print_records(results, cursor)