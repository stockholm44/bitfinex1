# from django.test import TestCase
import datetime

# Create your tests here.
# a = 10000
# b = format(a,',')
# print(b)
# print(type(b))
today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(today_date)
