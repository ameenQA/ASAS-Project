# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:51:14 2016

@author: Administrator
"""

from pymongo import MongoClient


class MongoConnect:
    def __init__(self):
        self.mongo_connection = MongoClient()

    def call_table(self, table_name, product_number): 
        # local is the db name
        mongo_db = self.mongo_connection.local
#        product_number = 'o14'
        cursor = mongo_db.feedback.find({"idProducts":product_number },{ "idProducts":1, "DatePublished": 1,  "Rating": 1 })
        output, date_list, rating_list  = self.print_table(cursor)  
        return output, date_list, rating_list
    
    def print_table (self, cursor):
        output = ""
        date_list = []
        rating_list = []
        for document in cursor:
            output += str(document) + "\n"
            print(document["Rating"])
            date_list.append(str(document["DatePublished"]))
            rating_list.append(float(document["Rating"]))
        return output, date_list, rating_list

