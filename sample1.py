import os
import sqlite3

#str= "name_town.xlsx"
#print(str.split('.')[0].split('_'))

conn= sqlite3.connect("sample.db")
curr= conn.cursor()
curr.execute("create table if not exists attendance (id, class, section, rollno)")
#curr.execute("insert into attendance values('XII_A_4', 'XII', 'A', 4)")
#curr.execute("insert into attendance values('XII_A_23', 'XII', 'A', 23)")
#curr.execute("insert into attendance values('XI_B_12', 'XI', 'B', 12)")
#curr.execute("insert into attendance values('XI_B_34', 'XI', 'B', 34)")
#conn.commit()

curr.execute("select rollno from attendance where class='XII' and section='A' ")
response= list(curr.fetchall())

for element in response:
    print(element[0])
conn.close()


'''
for file in os.listdir("class"):
    if(file.endswith('.xlsx')):
        lis= file.split('.')[0].split('_')
        conn= sqlite3.connect("sample.db")
        curr= conn.cursor()
        curr.execute("select rollno from attendance group")
'''

