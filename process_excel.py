import sqlite3
import pandas as pd
from pathlib import Path
import os
from datetime import datetime

path= Path("class")
def append_to_excel():
    conn= sqlite3.connect("database.db")
    curr= conn.cursor()
    time= datetime.now().strftime('%d-%m-%Y')
    for file in os.listdir(path):
         if(file.endswith('.xlsx')):
                filename= os.path.join(path, file)
                
                val= file.split('.')[0].split('_')
                class_= val[0]
                section_= val[1]

                curr.execute('select Roll No, time from attendance where Class= ? and Section=?', (class_, section_))
                response= list(curr.fetchall())
                
                df= pd.read_excel(filename)
                df[time]= ""
                print()
                print(df.head())
                
                for element in response:
                    df.loc[df["Roll No"]==int(element[0]), f'{time}']= element[1].datetime.strftime('%H:%M:%S')
                
                print(df.head())
                df.to_excel(f'{filename}', index=False)
                
    conn.close()
    print("Appended to Excel...")


def add_data(data):
    conn= sqlite3.connect("database.db")
    curr=conn.cursor()
    student_info= data["Name"].split('_')
    class_= student_info[0]
    section_= student_info[1]
    roll_no= student_info[2]
    curr.execute("INSERT INTO attendance VALUES(?, ?, ?, ?, ?)", (data["Name"], class_,section_,roll_no, data["Entry_Time"]))
    conn.commit()
    conn.close()
    print("\nAdded successfully...")


def show_data():
    conn = sqlite3.connect('database.db')
    curr= conn.cursor()
    curr.execute("SELECT * FROM attendance")
    record= curr.fetchall()

    for row in record:
            print(row[0], row[1], row[2], row[3], row[4])
    conn.close()

def create_database():
    conn= sqlite3.connect("database.db")
    curr= conn.cursor()
    curr.execute("CREATE TABLE IF NOT EXISTS attendance (id, Class, Section, Roll No, time)")
    conn.commit()
    conn.close()

def reset_db():
     conn= sqlite3.connect("database.db")
     curr= conn.cursor()

     curr.execute("drop from attendance")
     conn.commit()
     conn.close()
     print("\nDatabase cleared successfully...\n")

#show_data()

