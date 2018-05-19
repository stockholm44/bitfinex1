from classes import PDF
from xlwt import *

   # logging.propagate = False
    # logging.getLogger().setLevel(logging.ERROR)

# def pytest_funcarg__doc():
#     with open('1.pdf', 'rb') as f:
#         return PDF(f)

# def pytest_funcarg__doc():
with open('1.pdf', 'rb') as f:
    doc = PDF(f)

action_no_list = []
response_list = []
line_list = []

pdf_txt = '1.txt'

text_file = open("1.txt", "w")

for i, page in enumerate(doc):
    # print('*****************')
    # print(i, page)
    text_file.write(page)

text_file.close()

# readline.py
text_file_read = open("1.txt", 'r')

lines = text_file_read.readlines()
# 빈칸지우기
for line in lines:
    line_split = line.split('\n')
    for line_split_line in line_split:
        if line_split_line:
            line_list.append(line_split_line)
text_file_read.close()

for i, line in enumerate(line_list):
    #1 Action No. 읽고 +3 행을 추가하기.
    if line == 'Action No.':
        action_no_list_temp = line_list[i+3]
        action_no_list.append(action_no_list_temp)
    if line == 'Response':
        response_temp = ''
        for j in range(1,10):
            if line_list[i+j] != 'CONTRACTOR':
                response_temp += line_list[i+j]
            else:
                response_list.append(response_temp)

# for i, line in enumerate(action_no_list):
#     print(i, action_no_list[i], '\n',response_list[i])

book = Workbook()
sheet1 = book.add_sheet("PDF")

cols = ['No.','Action No.','Response']
# for i, c in enumerate(cols):
#     if i == 0:
#         sheet1.row(0).write(i, c)

for i in range(len(action_no_list)+1):
    for j, c in enumerate(cols):
        if i == 0:
            sheet1.row(i).write(j, c)
        elif i > 0:
            if j == 0:
                sheet1.row(i).write(j, i)
            elif j == 1:
                sheet1.row(i).write(j, action_no_list[i-1])
            elif j == 2:
                sheet1.row(i).write(j, response_list[i-1])

book.save("1.xls")

# for line in lines:
#     print(line, len(line))
# text_file_read.close()
