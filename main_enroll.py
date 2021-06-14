"""
Created on Sunday Nov 13 2019
@author: Neeraj

"""
import time
from pyfingerprint.pyfingerprint import PyFingerprint
import sqlite3
import pyfingerprint
import hashlib
import sys
import sqlupdate



print("create tabel\n")
print("Y. create the tabel ")
print("other wise if table is already created enter any key except ")
p=str(input("enter the choice ="))
conn = sqlite3.connect('library_database.db')

if p == 'y':
    
    curs = conn.cursor()
    curs.execute("CREATE TABLE student_table ( college_id int(20) not null,name text not null, batch text not null,department text not null,hashval text not null, position text not null,primary key(college_id),unique(college_id))")
    curs.execute("CREATE TABLE books_table  ( college_id int(20) not null,book_id TEXT not null ,name TEXT not null,book_title TEXT not null,author TEXT not null,issue_date datetime default CURRENT_TIMESTAMP,return_date datetime default CURRENT_TIMESTAMP)")  ####,,date_time DATETIME DEFAULT CURRENT_TIMESTAMP
    curs.execute("CREATE TABLE books_record_table(book_id TEXT NOT NULL,book_title TEXT NOT NULL,author TEXT NOT NULL)")
    curs.execute("CREATE TABLE return_books(college_id TEXT NOT NULL,name TEXT NOT NULL,department TEXT NOT NULL,batch TEXT NOT NULL,book_id TEXT NOT NULL,book_title TEXT NOT NULL,author TEXT NOT NULL,return_date TEXT NOT NULL)")

## Enrolls new finger
##
while 1:

        print("\nEnter your choice \n")
        print("1. Enroll the record")
        print("2. Delete the finger print from fingerprint sensor")
        print("3. update the student table values")
        print("3. delete the student table values")
        print("3. show the student table values")





        print("\n\n*******************************************************************\n\n")
                    

####################################################################
        def delete():
             try:
                 f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                 if ( f.verifyPassword() == False ):
                     raise ValueError('The given fingerprint sensor password is wrong!')

             except Exception as e:
                  print('The fingerprint sensor could not be initialized!')
                  print('Exception message: ' + str(e))
                  exit(1)

## Gets some sensor information
             print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to delete the template of the finger
             try:
                 positionNumber = input('Please enter the template position you want to delete: ')
                 positionNumber = int(positionNumber)

                 if ( f.deleteTemplate(positionNumber) == True ):
                      print('Template deleted!')

             except Exception as e:
                print('Operation failed!')
                print('Exception message: ' + str(e))
                exit(1)

 #########################################enroll####################################################       
## Tries to initialize the sensor nnnnnn
        def enroll():
            try:
                        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                        if ( f.verifyPassword() == False ):
                                            raise ValueError('The given fingerprint sensor password is wrong!')

            except Exception as e:
                  print('The fingerprint sensor could not be initialized!')
                  print('Exception message: ' + str(e))
                  exit(1)

## Gets some sensor information
                  print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to enroll new finger
            try:
                             print('Waiting for finger...')

    ## Wait that finger is read
                             while ( f.readImage() == False ):
                                           pass

    ## Converts read image to characteristics and stores it in charbuffer 1
                             f.convertImage(0x01)

    ## Checks if finger is already enrolled
                             result = f.searchTemplate()
                             positionNumber = result[0]

                             if ( positionNumber >= 0 ):
                                   print('Template already exists at position #' + str(positionNumber))
                               #    exit(0)

                             print('Remove finger...')
                             time.sleep(2)

                             print('Waiting for same finger again...')

    ## Wait that finger is read again
                             while ( f.readImage() == False ):
                                             pass


    ## Converts read image to characteristics and stores it in charbuffer 2
                             f.convertImage(0x02)

    ## Compares the charbuffers
                             if ( f.compareCharacteristics() == 0 ):
                                             raise Exception('Fingers do not match')

    ## Creates a template
                             f.createTemplate()

    ## Saves template at new position number
                             positionNumber = f.storeTemplate()
                             c=int(input("Enter college id = "))
                             r =input("Enter the name = ")
                             d=input("Enter batch = ")
                             j=input("departmant = ")
                             
                           
                             

                             
                             
	## Loads the found template to charbuffer 1
                             f.loadTemplate(positionNumber, 0x01)

	## Downloads the characteristics of template loaded in charbuffer 1
                             characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

	## Hashes characteristics of template
                             cre_hash = hashlib.sha256(characterics).hexdigest()
                             curs = conn.cursor()
                             curs.execute('INSERT INTO student_table(college_id, name,batch,department,hashval,position) values(? ,?, ? ,?, ?,?)',( c ,r,d,j,cre_hash, positionNumber))
                             
                             conn.commit()
                ## conn.close()
                             print('Finger enrolled successfully!')
                             print('New template position #' + str(positionNumber))




            except Exception as e:
                        print('Operation failed!')
                        print('Exception message: ' + str(e))
                         #exit(1)

        x=int(input("enter your choice ="))
        
        
        if x == 1:
             enroll()
          
        elif x == 2:
             delete()

        elif x == 3:
            sqlupdate.update()

        elif x == 4:
            sqlupdate.delete()

        elif x == 5:
           sqlupdate.select()

