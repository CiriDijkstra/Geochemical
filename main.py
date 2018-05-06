from openpyxl import *
from Sample import *
from Element import *
import numpy as np
import time

time_start = time.time()
wb = load_workbook('samples.xlsx')
sheet = wb.worksheets[0]

sample_list = []
for i in range(2,1862):
    sample_one = Sample(sheet.cell(row=i,column=1).value, sheet.cell(row=i,column=2).value,
                    sheet.cell(row=i,column=31).value, sheet.cell(row=i,column=25).value,
                    sheet.cell(row=i,column=23).value, sheet.cell(row=i,column=33).value,
                    sheet.cell(row=i,column=42).value)
    for j in range(35,42):
        sample_one.macro_element.append(sheet.cell(row=i,column=j).value)
    sample_list.append(sample_one)

W = ElementList('W')
Sn = ElementList('Sn')
Pb = ElementList('Pb')
Zn = ElementList('Zn')
temp_list = [W, Sn, Pb, Zn]
wb1 = Workbook()
sheet_ca = wb1.worksheets[0]
sheet_ca.append(['类标号', '样品数量', '元素', '分布模型', '背景上限'])
for i in range(1,6):
    for each in sample_list:
        if each.class_id == i:
            W.append(each.W)
            Sn.append(each.Sn)
            Pb.append(each.Pb)
            Zn.append(each.Zn)
    for element in temp_list:
        sheet_ca.append([i, len(element), element.element_name, element.distribution_pattern(), element.c_a()])
        del element[ : ]
wb1.save('分类情况.xlsx')

sheet2 = wb1.worksheets[0]
c_a = [{'W': None, 'Sn': None, 'Pb': None, 'Zn': None}, {'W': None, 'Sn': None, 'Pb': None, 'Zn': None},
       {'W': None, 'Sn': None, 'Pb': None, 'Zn': None}, {'W': None, 'Sn': None, 'Pb': None, 'Zn': None},
       {'W': None, 'Sn': None, 'Pb': None, 'Zn': None}]
for i in range(0,5):
    c_a[i]['W'] = sheet2.cell(row=i*4+2, column=5).value
    c_a[i]['Sn'] = sheet2.cell(row=i*4+3, column=5).value
    c_a[i]['Pb'] = sheet2.cell(row=i*4+4, column=5).value
    c_a[i]['Zn'] = sheet2.cell(row=i*4+5, column=5).value

for each in sample_list:
    neighborhood = []
    for another in sample_list:
        if another != each and another.class_id == each.class_id and another.is_adjacency(each):
           neighborhood.append(another)
    W, Sn, Pb, Zn = [], [], [], []
    for each_neighbor in neighborhood:
        W.append(each_neighbor.W)
        Sn.append(each_neighbor.Sn)
        Pb.append(each_neighbor.Pb)
        Zn.append(each_neighbor.Zn)
    if len(W) > 0:
        each.W_contrast = (each.W - np.mean(W)) / c_a[each.class_id - 1]['W']
    else:
        each.W_contrast = 0
    if len(Sn) > 0:
        each.Sn_contrast = (each.Sn - np.mean(Sn)) / c_a[each.class_id - 1]['Sn']
    else:
        each.Sn_contrast = 0
    if len(Pb) > 0:
        each.Pb_contrast = (each.Pb - np.mean(Pb)) / c_a[each.class_id - 1]['Pb']
    else:
        each.Pb_contrast = 0
    if len(Zn) > 0:
        each.Zn_contrast = (each.Zn - np.mean(Zn)) / c_a[each.class_id - 1]['Zn']
    else:
        each.Zn_contrast = 0

wb2 = Workbook()
sheet_contrast = wb2.worksheets[0]
sheet_contrast.append(['XX', 'YY', 'W', 'Sn', 'Pb', 'Zn'])
for each_sample in sample_list:
    sheet_contrast.append([each_sample.XX, each_sample.YY, each_sample.W_contrast, each_sample.Sn_contrast,
                           each_sample.Pb_contrast, each_sample.Zn_contrast])
wb2.save('变差衬度值.xlsx')

print('分类情况及各区元素背景上限值输出至文件 “分类情况.xlsx” 中\n变差衬度值计算结果输出至文件 “变差衬度值.xlsx” 中')

time_end = time.time()
print('共用时: ', time_end - time_start, 's', sep='')
