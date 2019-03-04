# -*- coding:utf-8 -*-

# 导出微信好友信息

import itchat
import xlwt
from time import time

itchat.auto_login(hotReload=True)

wbk = xlwt.Workbook()

sheet = wbk.add_sheet('sheet 1')

sheet.write(0, 0, '昵称')
sheet.write(0, 1, '备注')
sheet.write(0, 2, '性别')
sheet.write(0, 3, '签名')
sheet.write(0, 4, '城市')

friends = itchat.get_friends()[1:]

for index, friend in enumerate(friends):
    sheet.write(index + 1, 0, friend['NickName'])
    sheet.write(index + 1, 1, friend['RemarkName'])
    sex = friend['Sex']
    if sex == 1:
        sheet.write(index + 1, 2, '男')
    elif sex == 2:
        sheet.write(index + 1, 2, '女')
    else:
        sheet.write(index + 1, 2, '未设置')
    sheet.write(index + 1, 3, friend['Signature'])
    sheet.write(index + 1, 4, friend['Province']+friend['City'])

wbk.save(str(int(time())) + '.xls')

print('文件已经保存')