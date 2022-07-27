import os

import sys

import _sqlite3

from pathlib import Path

from email.message import EmailMessage
import ssl
import smtplib

from twilio.rest import Client


class menu:
    def __init__(self, choice):
        self.choice = choice

        if choice == "A":
            count = 0
            print('№\t   #Name    #Room   #Date\t    #Gmail\t    #Phone')
            for row in cursor.execute("SELECT * FROM example"):
                count += 1
                print(count, end=f"\t{row}\n")



        elif choice == "B":
            name = input("Enter Name  (John Doe): ")
            room_num = input("Enter one of the room number [1,2,3,4,5]: ")
            date = input("Enter Date (YYYY/mm/dd): ")
            gmail = input("Enter your gmail (abs@gmail.com): ")
            phone = input("Enter your phone (991234567): ")

            cursor.execute("SELECT * FROM example where room_number=:c and release_date=:d",
                           {'c': room_num, 'd': date, })
            booked = cursor.fetchall()
            list = []
            for row in booked:
                list.append(row)
            if len(list) > 0:
                for row in booked:
                    print('#Name    #Date   #Time 1')
                    print(row)
                print("Room is Booked, Please choose another room!")
            else:
                cursor.execute("INSERT INTO example values (?,?,?,?,?)", (name, room_num, date, gmail, phone))
                conn.commit()

                ##### Email #####

                email_sender = 'emailsenderalif@gmail.com'
                email_password = 'uhxbgeiviejiwnem'
                email_receiver = gmail

                subject = 'Office Room'
                body = f"Name: {name},\nRoom Number: {room_num},\nDate: {date},\nPhone: +998{phone}"

                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())

                ##### SMS #####  number:  +18593281951

                account_sid = 'ACf17c808b3552ba9d8324ef0549599a80'
                auth_token = '238701a0645079ba42f371a6cce98780'

                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body=f"\nName: {name},\nRoom Number: {room_num},\nDate: {date},\nPhone: +998{phone}",
                    from_='+18593281951',
                    to=f"+998{phone}"
                )
                print("\n\nRoom is booked by you!")

        elif choice == "C":
            import sys
            sys.exit("Thank you!")
        else:
            print("Invalid response. Please try again.")


while True:
    try:
        conn = _sqlite3.connect("example.db")
        cursor = conn.cursor()
        cursor.execute(
            "create table example (release_name TEXT, room_number INTEGER, release_date DATETIME, gmail TEXT, phone_number Numeric)")
    except _sqlite3.OperationalError:
        print('\n_____')

    print("ROOM REVERSATION SYSTEM")
    print("System Menu:")
    print("\tA. View all Reservations\n\tB. Make Reservation\n\tC. Exit\n")

    selection_menu = input('Enter selection: ').upper()
    menu(selection_menu)
