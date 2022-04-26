

import cgi
from ast import Delete, Try
from distutils.log import error
from msilib.schema import ListBox
from optparse import Values
from tkinter import ttk,messagebox
from tkinter import *
from turtle import update
import mysql.connector
from mysql.connector import Error

from gettext import install

# def connect(hostname,username,password):
#     con=mysql.connector.connect(host=hostname,
#                             user=username,
#                             password=password,)
#     return con
# print("connectivity done")

# con=connect("localhost","root","rohit@2310")

def connect_db(hostname,username,password,db_name):
    con=mysql.connector.connect(host=hostname,
                            user=username,
                            password=password,
                            db=db_name)
    return con
print("Connected to database")

con=connect_db("localhost","root","rohit@2310","stud_info")

def create_tb(con,query):
    cur1 = con.cursor()
    try:
        cur1.execute(query)
        print("Table has been created successfully")
    except Error as e:
        print(f"Error : {e}")
        
tb="""Create table if not exists stud_reco(
    stu_id int(10),
    stu_name varchar(20),
    course varchar(20),
    fee int(5)
)"""
create_tb(con,tb)

def Add():
    i1=e1.get()
    n1=e2.get()
    c1=e3.get()
    f1=e4.get()

    if i1==""or n1==""or c1=="" or f1=="":
        print("Field are Empty")
    else:
        cur=con.cursor()
        query="insert into stud_reco values({},'{}','{}',{})".format(i1,n1,c1,f1)
        cur.execute(query)
        con.commit()
        messagebox.showinfo("Information","Data Insert Successfully.")
        e1.delete(0,'end')
        e2.delete(0,'end')
        e3.delete(0,'end')
        e4.delete(0,'end')
        show()
        

def show():
    cur=con.cursor()
    query=""" SELECT* FROM stud_reco"""
    cur.execute(query)
    records=cur.fetchall()

    for i,(stud_id,stud_name,course,fee) in enumerate(records,start=1):
        Listbox.insert("","end",values=(stud_id,stud_name,course,fee))
        cur.close()

def delete():
    cur=con.cursor()
    d1=e1.get()
    query="Delete from stud_reco where stu_id={}".format(d1)
    cur.execute(query)
    con.commit()
    messagebox.showinfo("Information","Data Delete Sucessfully.")
    show()
    
    

def update():
    sid=e1.get()
    sname=e2.get()
    co=e3.get()
    f=e4.get()
    cur=con.cursor()
    qurey="Update stud_reco set stu_name='{}',course='{}',fee={} where stu_id={} ".format(sname,co,f,sid)
    cur.execute(qurey)
    con.commit()
    messagebox.showinfo("Information","Updated successfully...")
    show()
    e1.delete(0,'end')
    e2.delete(0,'end')
    e3.delete(0,'end')
    e4.delete(0,'end')



def GetValues():
    e1.delete(0,'end')
    e2.delete(0,'end')
    e3.delete(0,'end')
    e4.delete(0,'end')
    row_id=Listbox.selection()[0]
    select=Listbox.set(row_id)
    try:
        e1.insert(0,select['stu_id'])
        e2.insert(0,select['stu_name'])
        e3.insert(0,select['course'])
        e4.insert(0,select['fee'])
    except error as e:
        print(e)


root=Tk()
root.geometry("800x500")
global e1
global e2
global e3
global e4

l1=Label(root,text="Student Registation",fg="black",font=(None,30))
l1.place(x=400,y=5)
l2=Label(root,text="Student Id")
l2.place(x=10,y=10)
l3=Label(root,text="Student Name")
l3.place(x=10,y=40)
l4=Label(root,text="Course")
l4.place(x=10,y=70)
l5=Label(root,text="Fee")
l5.place(x=10,y=100)

e1=Entry(root)
e1.place(x=140,y=10)
e2=Entry(root)
e2.place(x=140,y=40)
e3=Entry(root)
e3.place(x=140,y=70)
e4=Entry(root)
e4.place(x=140,y=100)

b1=Button(root,text="Add",command=Add,height=3,width=13)
b1.place(x=30,y=130)
b2=Button(root,text="Update",command=update,height=3,width=13)
b2.place(x=140,y=130)
b3=Button(root,text="Delete",command=delete,height=3,width=13)
b3.place(x=250,y=130)

cols=("Id","Name","Course","Fee")
Listbox=ttk.Treeview(root,columns=cols,show="headings")

for col in cols:
    Listbox.heading(col,text=col)
    Listbox.grid(row=1,column=0,columnspan=2)
    Listbox.place(x=10,y=200)

show()
Listbox.bind('<Double-Button-1>',GetValues)

root.mainloop()