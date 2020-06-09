#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 02:40:37 2020

@author: davimercatelli
"""

import pandas as pd
import numpy as np
import datetime
from matplotlib import pyplot as plt

pd.set_option("display.precision", 3)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_rows", 150)
pd.options.display.float_format = '{:.0f}'.format

class csv_from_url:
    
    min_total_cases = 5000
    
    def __init__(self, url_path):
        self.url_path = url_path

    def download_csv(self):
        return pd.read_csv(self.url_path)
    
    def columns_name(self):
        return pd.read_csv(self.url_path).columns.values
    
    def column_list(self):
        return list(pd.read_csv(self.url_path).columns.values.tolist())
    
    def column_list_sorted(self):
        return sorted(list(pd.read_csv(self.url_path).columns.values.tolist()))
    
    def csv_usecols(self, **kwarg):
        self.usecols_df = pd.read_csv(self.url_path, dtype = dict(**kwarg), 
                                     usecols = list(dict(**kwarg)) + ["date"], parse_dates = ["date"])
        return self.usecols_df
    
    def today_cases(self):      
        self.filter_today = self.usecols_df[(self.usecols_df['date'] == self.usecols_df['date'].max())
                                          & (self.usecols_df['total_deaths'] > csv_from_url.min_total_cases) 
                                          & (self.usecols_df['location'] != 'World')]
        return self.filter_today

    def previous_day_cases(self):      
        self.previous_date = self.usecols_df['date'].max() - datetime.timedelta(days=1)
        self.filter_previous_day = self.usecols_df[(self.usecols_df['date'] == self.previous_date)
                                                  & (self.usecols_df['total_deaths'] > csv_from_url.min_total_cases) 
                                                  & (self.usecols_df['location'] != 'World')]
        return self.filter_previous_day
    
    def brazil_cases(self):
        self.brazil = self.usecols_df.loc[(self.usecols_df['location'] == 'Brazil')
                                    & (self.usecols_df['total_cases'] != 0)]
        return self.brazil
    
    def merge_table(self):
        self.merged = pd.merge(self.filter_today, self.filter_previous_day,
                               on = 'location', how = 'outer', indicator = False)       
        if self.merged['total_cases_x'].isnull().any() == True:       
            self.merged.loc[self.merged['total_cases_x'].isnull(), 'total_cases_x'] = self.merged['total_cases_y']
        
        if self.merged['total_cases_y'].isnull().any() == True:       
            self.merged.loc[self.merged['total_cases_y'].isnull(), 'total_cases_y'] = self.merged['total_cases_x']
        return self.merged.rename(columns={'date_x':'today', 'total_cases_x':'total_cases', 'total_deaths_x':'death_toll',
                                                   'date_y':'previous_day', 'total_cases_y':'previous_cases', 'total_deaths_y':'previous_death_toll'})

    def total_cases(self):
        self.result = self.merged.iloc[:, [0, 2, 5]]
        self.result_sort = self.result.sort_values(by = 'total_cases_x', ascending = False)    
        return self.result_sort.rename(columns={'total_cases_x':'Today Cases', 'total_cases_y':'Previous Day Cases'})
    
    def bar_display(self):
        bar_width = 0.4
        r1 = np.arange(len(self.result['location'])) 
        r2 = [x + bar_width for x in r1]
        plt.bar(r1, self.result_sort['total_cases_y'], color = '#ffaf33', width = bar_width, edgecolor = 'white', label = 'Yesterday Cases')
        plt.bar(r2, self.result_sort['total_cases_x'], color = '#338aff', width = bar_width, edgecolor = 'white', label = 'Today Cases')
        plt.ylabel('Total Cases - Greater than 2000 cases')
        plt.xlabel('Country')
        plt.xticks([r + bar_width for r in range(len(self.result['location']))], self.result_sort['location'], rotation = 90)  
        plt.grid(color = 'black', linestyle = '-', linewidth = 0.2)
        plt.legend() 
        plt.show()
        
    def row_display(self):
        plt.plot(self.brazil['date'], self.brazil['total_cases'], label='Total Cases')
        plt.plot(self.brazil['date'], self.brazil['total_deaths'], marker = 'x', label='Total Deaths')
        plt.xticks(rotation = 60)
        plt.grid(color = 'black', linestyle = '-', linewidth = 0.2)
        plt.ylabel('Total Brazilian Cases')
        plt.xlabel('Date')
        plt.legend() 
        plt.show()
        
csv_url = csv_from_url('https://covid.ourworldindata.org/data/owid-covid-data.csv')

kwarg = {"location": "category",
         #"new_cases": "int64",
         "total_cases": "int64",
         "total_deaths": "int64",
         "total_cases": "int64"}

csv_url.csv_usecols(**kwarg)
csv_url.today_cases()
csv_url.previous_day_cases()
csv_url.merge_table()
csv_url.total_cases()
csv_url.brazil_cases()
csv_url.bar_display()
csv_url.row_display()


print()
print(csv_url.merge_table())

print()
print(csv_url.brazil_cases())

print()
print(csv_url.total_cases())
# print(csv_url.column_list_sorted())
# print(csv_url.csv_usecols(**kwarg))
# csv_url.row_display()
# print(csv_url.total_cases())
# print(csv_url.display())
