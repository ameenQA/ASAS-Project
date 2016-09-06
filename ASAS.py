# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 13:29:08 2016

@author: Ameen
"""
import sys

import MySQLAdapter
import MongoConnect
import csv
from functools import partial


class ASAS:
    def __init__(self):
        menu_option = int(input("\t \t Welcome to NB Gardens ASAS System. \nChoose one of teh following options;\n\n 1 - print a list of products, customer, orders \n 2 - Discover product ratings over a period of time \n 3 - graph one particular product's ratings\
        \n 4 - graph all product ratings over a period of time. \n 5 - display particular item reviews from mongodb \n 6 - graph mongo product over time \n 0 - exit system \n\n"))
        self.run_query = MySQLAdapter.MySQLAdapter()
        self.run_mongo_queries = MongoConnect.MongoConnect()
        self.userMenuSystem(menu_option)
    
    def printLists(self):
        getInput = partial(self.run_query.typeList)
        print ('You have chosen to print a list of certain attibute of a table')
        attribute_list = input('Please type your attributes\n')
        table_name = input('Please type your table name\n')
        getInput(attribute_list, table_name)
    
    def productRating(self):
        product_number = input('Please provide a product number.\n')
        start_date = input('Please provide a start date.\n')
        end_date = input('Please provide a end date.\n')
        results, cursor = self.run_query.ratingsOverTime(product_number, start_date, end_date)
        to_save = (input('Do you want to save the data (y/n)?\n')).lower()
        if to_save == 'y':
            print ('---- Saving data to file ----\n')
            file_name = (input('Please enter file name?\n')).lower()

            with open(file_name + '.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
#                writer.writerows([i for i in cursor.description])
                writer.writerows(results)
            print ('---- Saved data to file ----\n')
            menu_option = int(input("\t \t Welcome to NB Gardens ASAS System. \nChoose\n"))
            self.userMenuSystem(menu_option)
        else: 
            menu_option = int(input("\t \t Welcome to NB Gardens ASAS System. \nChoose\n"))
            self.userMenuSystem(menu_option)
            
    
    def graphOneProducts(self):
#        product_number = input('Please provide a product number.\n')
#        start_date = input('Please provide a start date.\n')
#        end_date = input('Please provide a end date.\n')
#        self.run_query.plotting_one_product(product_number, start_date, end_date)
        self.run_query.plotting_one_product('o4', '2016-01-01', '2019-01-01')
    
    def graphAllProducts(self):
#        start_date = input('Please provide a start date.\n')
#        end_date = input('Please provide a end date.\n')
#        self.run_query.plotting_one_product(start_date, end_date)
        self.run_query.plotting_all_products('2016-01-01', '2019-01-01')
        
    def exitSystem(self):
        print('System is existing. Please restart!')
        sys.exit()
    
    def displayMongoData(self):
        product_number = input('Please provide a product number.\n')
        table_name = input('Please provide a table name.\n')
        output, date_list, rating_list  = self.run_mongo_queries.call_table(table_name, product_number)
        to_save = (input('Do you want to save the data (y/n)?\n')).lower()
        if to_save == 'y':
            print ('---- Saving data to file ----\n')
            file_name = (input('Please enter file name?\n')).lower()
            text_file = open(file_name + '.txt', "w")
            text_file.write(str(output))
            text_file.close()
            print ('---- Saved data to file ----\n')
            self.exitSystem()
        else: 
            self.exitSystem()
            
            
    def graphMongoData(self):        
        product_number = input('Please provide a product number.\n')
        table_name = input('Please provide a table name.\n')
        output, date_list, rating_list = self.run_mongo_queries.call_table(table_name, product_number)
        print (date_list)
        print(rating_list)
        self.run_query.linePlot(date_list, rating_list)
        
        
    def userMenuSystem(self, menu_option):
        switcher = {
            0: self.exitSystem,
            1: self.printLists,
            2: self.productRating,
            3: self.graphOneProducts,
            4: self.graphAllProducts,
            5: self.displayMongoData,
            6: self.graphMongoData
        }
        # Get the function from switcher dictionary
        run_method = switcher.get(menu_option, lambda: self.exitSystem())
        # Execute the function
        return run_method()
    


# run program
runSys = ASAS()
