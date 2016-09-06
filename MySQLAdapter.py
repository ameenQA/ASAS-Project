# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 14:42:16 2016

@author: Administrator
"""

import pymysql
from pylab import *



class MySQLAdapter:
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "Pa$$w0rd", "mydb")
    
        
    def typeList (self, param1, param2):
        cursor = self.db.cursor()
        query_string = 'select ' + param1 + ' from ' + param2 + ';'
        cursor.execute(query_string)
        results = cursor.fetchone()
        self.print_records( results, cursor)
        
    
    def ratingsOverTime(self, product_number, start_date, end_date):
        query_string = "Select c.idCustomer as 'Customer ID', c.FirstName as 'First Name', c.LastName as 'Surname', f.DatePublished as 'Date Published' , round(f.rating,2) as 'Average Product Rating' From Customer as c Join Feedback as f On c.idCustomer = f.Customer_idCustomer WHERE f.Products_idProducts = '" + product_number + "' AND f.DatePublished BETWEEN '" + start_date + "' AND '" + end_date+ "' group by f.DatePublished;"
        cursor = self.db.cursor()
        second_cursor = self.db.cursor()
        cursor.execute(query_string)
        second_cursor.execute(query_string)
        all_results = cursor.fetchall()    
        results = second_cursor.fetchone()
        self.print_records( results, second_cursor)
        cursor.close()
        return all_results, cursor
        
        
    def print_records(self, row, cursor):
        for i in range(len(cursor.description)):
            print (cursor.description[i][0], " ", end="")
        print('\n')
        while row is not None:
            print (row)
            row = cursor.fetchone()   
        cursor.close()
        self.db.close()

    def plotting_one_product(self, product_number, start_date, end_date):
        date_list = []
        rating_list = []
        query_string = "Select f.DatePublished as 'Date Published' , round(avg(f.rating),2)  as 'Average Product Rating' From Customer as c Join Feedback as f On c.idCustomer = f.Customer_idCustomer WHERE f.Products_idProducts = '" + product_number + "' AND f.DatePublished BETWEEN '" + start_date + "' AND '" + end_date+ "' group by f.DatePublished;"
        cursor = self.db.cursor()
        cursor.execute(query_string)
        results = cursor.fetchall()
        cursor.close()
        
        for i in range (len(results)):
            date_list.append(str(results[i][0]))
            rating_list.append(float( (results[i][1])))
        self.linePlot(date_list, rating_list)
        
    def linePlot(self, date_list, rating_list ):
        tick_spred = arange(len(date_list))+.5
        ylabel('Average rating')
        title('Graph of ratings for a particular product over time.')
        plot(tick_spred, rating_list, 'b', tick_spred, rating_list, 'ro' )
        xticks(tick_spred, (date_list))
        xlabel('Dates for ratings published')
        grid(True)
        savefig('hello.png', bbox_inches = 'tight') 
        show()

        
    def plotting_all_products(self, start_date, end_date):
        rating_list = []
        product_list = []
        query_string = "Select f.Products_idProducts as 'Product ID', round(avg(f.rating),2)as 'Average Product Rating' From Customer as c Join Feedback as f On c.idCustomer = f.Customer_idCustomer AND f.DatePublished BETWEEN '"+ start_date +"' AND '"+ end_date +"' group by f.Products_idProducts;"
        cursor = self.db.cursor()
        cursor.execute(query_string)
        results = cursor.fetchall()
        cursor.close()
        
        for i in range (len(results)):
            product_list.append(str(results[i][0]))
            rating_list.append(float( (results[i][1])))
        tick_spread = arange(len(product_list))+.5    # the bar centers on the y axis
        figure(1)
        barh(tick_spread,rating_list, xerr=rand(len(product_list)), ecolor='r', align='center')
        yticks(tick_spread, (product_list))
        xlabel('Average rating')
        ylabel('Products')
        title('Graph of average ratings for all products over time.')
        grid(True)
        show()
        