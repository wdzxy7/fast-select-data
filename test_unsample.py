import pymysql
from pandas import DataFrame
from decimal import Decimal
import pandas as pd
import random
import xlrd
import time
from openpyxl import Workbook


if __name__ == '__main__':
    wb = Workbook()
    excel = wb.active
    excel['A1'] = 'index'
    excel['B1'] = 'stand'
    excel['C1'] = 'sample'
    excel['D1'] = 'accuracy'
    count = 2
    res_dict = {}
    connect = pymysql.connect(host='localhost', port=3308, user='root', passwd='', db='', charset='utf8')
    cursor = connect.cursor()
    sql = 'select `index`, avg(score) from unknown_data.data3 group by `index`;'
    cursor.execute(sql)
    res = cursor.fetchall()
    for i in res:
        index = i[0]
        avg = i[1]
        res_dict[index] = []
        res_dict[index].append(avg)
    sql = 'select `index`, avg(score) from unknown_data.test_sample group by `index`;'
    cursor.execute(sql)
    res = cursor.fetchall()
    c = len(res)
    for i in res:
        index = i[0]
        avg = i[1]
        try:
            res_dict[index].append(avg)
        except:
            res_dict[index] = []
            res_dict[index].append(avg)
    s = 0
    for key in res_dict.keys():
        stand = res_dict[key][0]
        sample = res_dict[key][1]
        try:
            accuracy = round(abs(stand - sample) / abs(stand), 10) * 100
        except:
            accuracy = 0
        res_dict[key].append(accuracy)
    res_dict = sorted(res_dict.items(), key=lambda x: x[1][2], reverse=True)
    accuracy_dict = {}
    for i in res_dict:
        accuracy_dict[i[0]] = list(i[1])
    for key in accuracy_dict.keys():
        stand = accuracy_dict[key][0]
        sample = accuracy_dict[key][1]
        accuracy = accuracy_dict[key][2]

        excel['A' + str(count)] = key
        excel['B' + str(count)] = stand
        excel['C' + str(count)] = sample
        excel['D' + str(count)] = str(accuracy) + '%'
        count = count + 1
    wb.save('undata_accuracy_data3w.xlsx')
print()