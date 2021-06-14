"""
Created on Sunday Nov 13 2019
@author: Neeraj

"""

from tkinter import*
try:
    import Tkinter as tk
except:
    import tkinter as tk

import os
from PIL import Image, ImageTk
from datetime import datetime

import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2,GPIO.IN)
  

import time
from pyfingerprint.pyfingerprint import PyFingerprint
import sqlite3
import pyfingerprint
import hashlib
import sys
import random

from time import sleep
time_stamp=time.time()

print("****************************************START*****************************************************")
path1 = os.path.normpath("/home/pi/Desktop/smart_attendence_system/complete attendance system/images/f2.png")
path2 = os.path.normpath("/home/pi/Desktop/smart_attendence_system/complete attendance system/images/f4.jpg")


root = Tk()
root.title('smart library')


lbl=Label(root,text ="SMART LIBRARY SYSTEM",fg ='black' , font =("times new roman", 100),bg='white')
lbl.place(x=170,y=10)


lbl3=Label(root,text ="Developed By",fg ='black' , font =("times new roman", 40),bg='white')
lbl3.place(x=30,y=500)

lbl3=Label(root,text ="Mr. Neeraj Rawat",fg ='black' , font =("times new roman", 40),bg='white')
lbl3.place(x=30,y=580)


txt='Please Enter Your Thumb Impression'
lbl6=Label(root,fg ='red' , font =("times new roman", 70),bg='white')
lbl6.place(x=300,y=850)

def labelconfig():
     p=txt
     color = '#'+("%09x" % random.randint(0,0xFFFFFF))
     lbl6.config(text=p,fg=str(color))
     root.after(300,labelconfig)
labelconfig()


root.geometry('1920x1080')
root['bg'] = 'white'



load = Image.open(path1)
load=load.resize((300,300),Image.ANTIALIAS)
render = ImageTk.PhotoImage(load)

img = Label(root, image=render)
img.image = render
img.place(x=900, y=400)




load1 = Image.open(path2)
load1=load1.resize((300,300),Image.ANTIALIAS)
render1 = ImageTk.PhotoImage(load1)

img1 = Label(root, image=render1)
img1.image = render1
img1.place(x=600, y=400)





value=0

def my_callback1(channel1):
                                                count=0
                                                global time_stamp
                                                time_now = time.time()

                                                try:

                                                    #print("\nscan the finger print of student for getting info. from database \n")
                                                    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                                                    if ( f.verifyPassword() == False ):
                                                        raise ValueError('The given fingerprint sensor password is wrong!')

                                                except Exception as e:
                                                    print('The fingerprint sensor could not be initialized!')
                                                    print('Exception message: ' + str(e))
                                                    exit(1)

                                                ## Gets some sensor information
                                                print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

                                                ## Tries to search the finger and calculate hash
                                                try:
                                                    #print('Waiting for finger...')

                                                    ## Wait that finger is read
                                                    while ( f.readImage() == False ):
                                                        pass

                                                    ## Converts read image to characteristics and stores it in charbuffer 1
                                                    f.convertImage(0x01)

                                                    ## Searchs template
                                                    result = f.searchTemplate()

                                                    positionNumber = result[0]
                                                    accuracyScore = result[1]

                                                    if ( positionNumber == -1 ):
                                                        print('No match found!')
                                                        #exit(1)
                                                    else:
                                                        print('Found template at position #' + str(positionNumber))
                                                        ##print('The accuracy score is: ' + str(accuracyScore))

                                                    ## Loads the found template to charbuffer 1
                                                    f.loadTemplate(positionNumber, 0x01)
                                                    ## Downloads the characteristics of template loaded in charbuffer 1
                                                    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
                                                    ## Hashes characteristics of template
                                                    
                                                     ##print('SHA-2 hash of template: ' )
                                                    global fp
                                                    fp=hashlib.sha256(characterics).hexdigest()
                                                    global value
                                                    value=value+1
                                                    #print("value is.............................................................................................................. = ",value)
                                                    #fig()
                                                    
                                                    print("value is = ",value)
                                                    fig()
                                                    

                                                except Exception as e:
                                                    
                                                    print('Operation failed!')
                                                    print('Exception message: ' + str(e))      

                                                    
                                                    txt='Error In Matching Please Try again'
                                                    lbl6=Label(root,fg ='red' , font =("times new roman", 50),bg='white')
                                                    lbl6.place(x=300,y=730)

                                                    def labelconfig():
                                                         p=txt
                                                         color = '#'+("%06x" % random.randint(0,0xFFFFFF))
                                                         lbl6.config(text=p,fg=str(color))
                                                         root.after(500,labelconfig)
                                                    labelconfig()

                         #fg()           
 

GPIO.add_event_detect(2, GPIO.RISING, callback=my_callback1, bouncetime=6000) # ir sensor
                             
def fig():                                    
                                    top=Toplevel()
                                    top.title("top window")
                                    top.geometry('1920x1080')
                                    top['bg'] = 'black'
                                    

                                    lbl=Label(top,text ="SMART LIBRARY SYSTEM",fg ='white' , font =("times new roman", 60),bg='black')
                                    lbl.place(x=450,y=10)

                                    lbl1=Label(top,text ="User Information",fg ='white' , font =("times new roman", 50),bg='black')
                                    lbl1.place(x=50,y=200)

                                    lbl2=Label(top,text ="Book Issue Details",fg ='white' , font =("times new roman", 50),bg='black')
                                    lbl2.place(x=950,y=200)

                                    c_id_label = Label(top ,text = "University ID:",font =("Arial Bold", 30),bg='black',fg ='white' )
                                    c_id_label.grid(row=0, column=0, pady=2, padx=1)
                                    c_id_label.place(x=50,y=300)

                                    name_label = Label(top, text = "Name           :",font =("Arial Bold", 30),bg='black',fg ='white' )
                                    name_label.grid(row=1, column=0)
                                    name_label.place(x=50,y=350)

                                    college_rollnum_label = Label(top, text = "Batch            :",font =("Arial Bold", 30),bg='black',fg ='white' )
                                    college_rollnum_label.grid(row=2, column=0)
                                    college_rollnum_label .place(x=50,y=400)

                                    class_rollnum_label = Label(top, text = "Department  :",font =("Arial Bold", 30),bg='black',fg ='white' )
                                    class_rollnum_label.grid(row=3, column=0)
                                    class_rollnum_label.place(x=50,y=450)

                                    


            # ***************************************************************************************************************************


                                    c_id_label1 = Label(top ,text = "Book Title ",font =("Arial Bold", 30),bg='black',fg ='sky blue' )
                                    c_id_label1.grid(row=0, column=0, pady=2, padx=1)
                                    c_id_label1.place(x=800,y=300)

                                    name_label1 = Label(top, text = "Author  ",font =("Arial Bold", 30),bg='black',fg ='sky blue' )
                                    name_label1.grid(row=1, column=0)
                                    name_label1.place(x=1100,y=300)

                                    name_label1 = Label(top, text = "Issue Date ",font =("Arial Bold", 30),bg='black',fg ='sky blue' )
                                    name_label1.grid(row=1, column=0)
                                    name_label1.place(x=1450,y=300)

                                    w = Label(top, text = "For logout please scan your university ID , by default logout after 1 minute  ",font =("Arial Bold", 35),bg='black',fg ='spring green' )  ############
                                    w.grid(row=1, column=0)
                                    w.place(x=48,y=820)



                                    e1 = Label(top, text = "Scan Books",font =("Arial Bold", 30),bg='black',fg ='white' )     ######  show scan books on 2nd window 
                                    e1.grid(row=4, column=0)
                                    e1.place(x=100,y=700)


                                    def countdown1(count):
                                        # change text in label        
                                        message1['text'] = count

                                        if count > 0:
                                            # call countdown again after 1000ms (1s)
                                            top.after(1000, countdown1, count-1)
                                            #print("ok")
                                            if count ==1:
                                                #print("complete")
                                                top.destroy()
                                                global value
                                                value=0
                                                
                        
                                    message1=Label(top,font =("times new roman", 60),bg='black',fg ='orange')######message whether book is insert and delete
                                    message1.grid(row=8,column=0,columnspan=2)
                                    message1.place(x=1600,y=10)
                                    countdown1(30)

                                    global book_id
                                    large_font=('Verdana',20)

                                    book_id = Entry(top,text='?',width=15,font=large_font)                    #scan books
                                    book_id .grid(row=4, column=2)
                                    book_id .place(x=350,y=700)
                                    book_id.focus()      # focus on book  
                                    print("print l1 =",book_id.get())
                                    value=0
                                    
                        

                                    
                                    def issue():

                                                            global book_id
                                                            conn=sqlite3.connect('library_database.db')
                                                            c=conn.cursor()
                                                            #it search the book from book id in the book_record_table
                                                            c.execute("SELECT book_id,book_title,author FROM books_record_table WHERE book_id='%s'"%book_id.get())
                                                            records12=c.fetchall()
                                                            y=["Empty","Empty","Empty"]
                                                            for y in records12:
                                                                     global bt
                                                                     global ba
                                                                     bt=y[1]
                                                                     print("bt =",y[1])
                                                                     ba=y[2]

                                                            conn.commit()
                                                            c.close()

                                                            conn=sqlite3.connect('library_database.db')
                                                            curs=conn.cursor()
                                                            r=book_id.get()
                                                    
                                                            curs.execute( "SELECT college_id,book_id  FROM books_table WHERE book_id ='%s' "%book_id.get())
                                                            records3 = curs.fetchall()
                                                            x=["Empty","Empty","Empty"]
                                                            for x in records3:
                                                                     print("print x is = ",x[1])

                                                            conn.commit()
                  
                                                            curs.close()
                                                                    
                                                            if(book_id.get()==x[1]):
                                                            
                                                                try:
                                                                      conn = sqlite3.connect('library_database.db')
                                                                      curs= conn.cursor()
                                                                      curs.execute("SELECT book_id FROM books_table WHERE book_id ='%s' "%book_id.get())
                                                                      records0 = curs.fetchall()
                                                                                                
                                                                      print0_records= ' '
                                                                      deta=["Empty"]

                                                                      for deta in records0:
                                                                         print("re = ",deta[0])

                                                                      conn.commit()
                                                                      curs.close()  

                                                                      if book_id.get()==deta[0]:

                                                                           conn = sqlite3.connect('library_database.db')
                                                                           now1=datetime.now()
                                                                           current_time=now1.strftime("%d-%m-%Y %I:%M%p")
                                                                           curs= conn.cursor()
                                                                           curs.execute  ('INSERT INTO return_books (college_id,name,department,batch,book_id,book_title,author,return_date)values( ?,?,?,?,?,?,?,?)',( ff,jj,dd,lk,deta[0],bt,ba,current_time))
                                                                           conn.commit()
                                                                           curs.close() 

                                                                      conn = sqlite3.connect('library_database.db')
                                                                      curs= conn.cursor()
                                                                      curs.execute("DELETE FROM books_table WHERE book_id  ='%s' "%book_id.get())
                                                                      conn.commit()
                                                                      curs.close()
                                                                      book_id.delete(0, END)
                                                                      nn="Book Return Successfull"
                                                                      
                                                                      coll_id=ff
                                                                      college_id = Entry(top, width=15,font=large_font)
                                                                      print("college id after delete 11= ",coll_id)
                                                                      
                                                                      college_id.insert(0,coll_id)
                                                                      conn=sqlite3.connect('library_database.db')
                                                                      c=conn.cursor()
                                                                      print("college id1",college_id.get())
                                                                      c.execute("SELECT books_record_table.book_title, books_record_table.author,books_table.issue_date FROM student_table  JOIN books_table ON student_table.college_id= books_table.college_id JOIN books_record_table  ON books_record_table.book_id=books_table.book_id  WHERE student_table.college_id= '%s' "%college_id.get())
                                                                      records2 = c.fetchall()
                                                                                                
                                                                      print1_records= ' '
                                                                      det=["Empty","Empty","Empty"]

                                                                      for det in records2:
                                                                                   print1_records +=str(det[0]) +'                 '+ str(det[1]) + '            '+str(det[2]) +" \n "

                                                                      conn.commit()
                                                                      c.close()
                                                                                                                
                                                                      college_id.delete(0, END)
                                                                      query_label7=Label(top, text=print1_records ,font =("times new roman", 30),bg='black',fg ='yellow')
                                                                      query_label7.grid(row=8,column=0,columnspan=2)
                                                                      query_label7.place(x=800,y=380)
                                                                      message=Label(top, text=nn,font =("times new roman", 40),bg='black',fg ='orange')######message whether book is insert and delete
                                                                      message.grid(row=8,column=0,columnspan=2)
                                                                      message.place(x=1000,y=730)
                                                                      
                                                                except Exception as e:
                                                                         print('Operation failed!')
                                                                         print('Exception message: ' + str(e))
                                                        
                                                            else:
                                                                       try:
                                                                                          
                                                                                    conn = sqlite3.connect('library_database.db')
                                                                                    curs= conn.cursor()
                                                                                    print("print r = ",r)
                                                                                    curs.execute("SELECT books_record_table.book_id FROM books_record_table WHERE books_record_table.book_id =?",(r, ))
                                                                                    records2 = curs.fetchall()
                                                                                    infor=["Empty"]
                                                                                    for infor in records2:
                                                                                          
                                                                                          print("book id is =: ",infor[0])

                                                                                    if str(r)==str(infor[0]):


                                                                                            
                                                                                            conn = sqlite3.connect('library_database.db')
                                                                                            curs= conn.cursor()
                                                                                            print("print r = ",ff)
                                                                                            curs.execute("SELECT COUNT(*),books_table.book_id   FROM books_table  WHERE books_table.college_id =? ",(ff , ))
                                                                                            records2a = curs.fetchall()
                                                                                            inform=["Empty"]
                                                                                            for inform in records2a:
                                                                                                  
                                                                                                  kl=inform[0]
                                                                                                  print("limit =",kl)

                                                                                            conn.commit()
                                                                                            c.close()
                                                                                            


                                                                                            if kl<=4:
                                                                                                
                                                                                                    conn = sqlite3.connect('library_database.db')
                                                                                                    now1=datetime.now()
                                                                                                    current_time=now1.strftime("%d-%m-%Y %I:%M%p")
                                                                                                    curs= conn.cursor()
                                                                                                    curs.execute  ('INSERT INTO books_table (college_id,name,book_id,book_title,author,issue_date)values( ?,?,?,?,?,?)',( ff,jj,r,bt,ba,current_time))
                                                                                                    
                                                                                                    conn.commit()
                                                                                                    book_id.delete(0, END)
                                                                                                    bb="Book Issue Successfull"
                                                                                                    coll_id=ff
                                                                                                    college_id = Entry(top, width=15,font=large_font)
                                                                                                    print("college id after delete = ",coll_id)
                                                                                                    college_id.insert(0,coll_id)
                                                                                                    conn=sqlite3.connect('library_database.db')
                                                                                                    c=conn.cursor()
                                                                                                    c.execute("SELECT books_record_table.book_title, books_record_table.author,books_table.issue_date FROM student_table  JOIN books_table ON student_table.college_id= books_table.college_id JOIN books_record_table  ON books_record_table.book_id=books_table.book_id  WHERE student_table.college_id= '%s' "%college_id.get())
                                                                                                    records2 = c.fetchall()
                                                                                                                            
                                                                                                    print1_records= ' '
                                                                                                    det=["Empty","Empty","Empty"]

                                                                                                    
                                                                                                    for det in records2:
                                                                                                               print1_records +=str(det[0]) +'                 '+ str(det[1]) + '            '+str(det[2]) +" \n "

                                                                                                    conn.commit()
                                                                                                    c.close()
                                                                                                                                            
                                                                                                    college_id.delete(0, END)
                                                                                                    query_label7=Label(top, text=print1_records ,font =("times new roman", 30),bg='black',fg ='yellow')
                                                                                                    query_label7.grid(row=8,column=0,columnspan=2)
                                                                                                    query_label7.place(x=800,y=380)

                                                                                                    message1=Label(top, text=bb,font =("times new roman", 40),bg='black',fg ='orange')######message whether book is insert and delete
                                                                                                    message1.grid(row=8,column=0,columnspan=2)
                                                                                                    message1.place(x=1000,y=730)
                                                                                                    

                                                                                            elif kl<4:
                                                                                                    book_id.delete(0, END)
                                                                                                    pp1="Limit Is Full                        "
                                                                                                    message21=Label(top, text=pp1,font =("times new roman", 40),bg='black',fg ='orange')######message whether book is insert and delete
                                                                                                    message21.grid(row=8,column=0,columnspan=2)
                                                                                                    message21.place(x=1000,y=730)
                                                                                                
                                                                                    elif str(r)!=str(infor[0]):
                                                                                         book_id.delete(0, END)
                                                                                         pp="Book Is  Not In Database "
                                                                                         message2=Label(top, text=pp,font =("times new roman", 40),bg='black',fg ='orange')######message whether book is insert and delete
                                                                                         message2.grid(row=8,column=0,columnspan=2)
                                                                                         message2.place(x=1000,y=730)
                                                                                    
                                                                       except Exception as e:
                                                                                         print('Operation failed!')
                                                                                         print('Exception message: ' + str(e))

                                    
                                    code = ''   
                                    def get_key2(event2):
                                                global code

                                                if event2.char in '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM':
                                                   code += event2.char
                                                   

                                                elif event2.keysym == 'Return':
                                                    print('result:', code)

                                                    if str(code)==str(ff):
                                                            book_id.delete(0, END)
                                                            top.destroy()
                                                            code=""

                                                    elif str(code)!=str(ff):
                                                            issue()
                                                            code=""

                                                    
                                    code=""
                                    top.bind('<Key>', get_key2)


                                                                        

                                    try:
                                                                large_font=('Verdana',20)
                                                                hashval = Entry(top, width=15,font=large_font)
                                                                hashval.insert(0,fp)
                                                                conn=sqlite3.connect('library_database.db')
                                                                c=conn.cursor()
                                                                c.execute( "SELECT *  FROM student_table WHERE hashval='%s'  " %hashval.get())
                                                                records1 = c.fetchall()
                                                                print_records= ' '
                                                                global ff
                                                                global jj
                                                                global dd
                                                                global lk
                                                                row=["Empty","Empty","Empty","Empty","Empty"]
                                                                for row in records1:
                                                                        print_records =str(row) +"\n"
                                                                        
                                                                        ff=row[0]  ###### college id
                                                                        jj=row[1]  ##### name
                                                    
                                                                        dd=row[3]####### department
                                                                        lk=row[2]#######  batch
                                                           
                                                                conn.commit()
                                                                conn.close()
                                                                        
                                                                query_label0=Label(top, text=row[0],font =("times new roman", 30),bg='black',fg ='white')
                                                                query_label0.grid(row=8,column=0,columnspan=2)
                                                                query_label0.place(x=335,y=300)

                                                                query_label1=Label(top, text=row[1],font =("times new roman", 30),bg='black',fg ='white')
                                                                query_label1.grid(row=8,column=0,columnspan=2)
                                                                query_label1.place(x=335,y=350)

                                                                query_label2=Label(top, text=row[2],font =("times new roman", 30),bg='black',fg ='white')
                                                                query_label2.grid(row=8,column=0,columnspan=2)
                                                                query_label2.place(x=335,y=400)

                                                                query_label3=Label(top, text=row[3],font =("times new roman", 30),bg='black',fg ='white')
                                                                query_label3.grid(row=8,column=0,columnspan=2)
                                                                query_label3.place(x=335,y=450)

                                                                conn=sqlite3.connect('library_database.db')
                                                                c=conn.cursor()
                                                                c.execute("SELECT books_record_table.book_title, books_record_table.author,books_table.issue_date  FROM student_table  JOIN books_table ON student_table.college_id= books_table.college_id JOIN books_record_table  ON books_record_table.book_id=books_table.book_id  WHERE student_table.hashval = '%s' "%hashval.get())
                                                                records2 = c.fetchall()
                                                                print1_records= ' '
                                                                det=["Empty","Empty","Empty"]
                                       
                                                                for det in records2:
                                                                                print1_records +=str(det[0]) +'                 '+ str(det[1]) + '          '+str(det[2]) +" \n "

                                                                query_label7=Label(top, text=print1_records  ,font =("times new roman", 30),bg='black',fg ='yellow')
                                                                query_label7.grid(row=8,column=0,columnspan=2)
                                                                query_label7.place(x=800,y=380)
                                                                
                                                              
                                    
                                    except Exception as e:
                                                      print('Operation failed!')
                                                      print('Exception message: ' + str(e))      
                                                         
                                               
                                    fg()

def get_key(event):
    global code

    if event.char in '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM':
       code += event.char
       #print('>', code)
       #label['text'] = code
       #print("mst")

    elif event.keysym == 'Return':
        print('result:', code)
        #college_id.delete(0, END)
        submit1()
        code=""


code = ''                        
root.bind('<Key>', get_key)

root.mainloop()                                                      
                                    
