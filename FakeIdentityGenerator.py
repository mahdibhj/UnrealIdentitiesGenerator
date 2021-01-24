import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from time import sleep
import tkinter as tk
import urllib.request
from urllib.request import urlopen
import io
import random
#from tkinter import ttk


HEIGHT=500
WIDTH=700
big_list=[]
information_list=[]
def generate_person(entry):
    #print(entry)
    global big_list
    global information_list
    requete = requests.get("https://www.fakepersongenerator.com/Random1/generate_identity")
    parser=BeautifulSoup(requete.content,'html.parser')
    person_information_titles= parser.find_all(class_="info-title")
    person_information_details= parser.find_all(class_="info-detail")


    """
    person_images= parser.find_all(class_="img-responsive")
    person_profile_image_name=person_images[1]
    person_profile_image_url='https://www.fakepersongenerator.com'+person_profile_image_name['src']
    #urllib.request.urlretrieve(person_profile_image_url,person_profile_image_name)
    image_data = io.BytesIO(urlopen(person_profile_image_url).read())
    """
    information_list=[]
    for i in (0,3,1):
        #print(len(person_information_details))
        if len(person_information_details)>2:
            #print(len(person_information_details))
            person_information_details_value=person_information_details[i].find(class_="form-control")
            person_information_titles_value=str(person_information_titles[i])[30:-13]
            information_title=str(person_information_titles[i])[30:-13]
            information_value=str(person_information_details_value)[47:-3]
            #print(person_information_titles_value)
            if information_title=="Name":
                name_list=information_value.split("\xa0")
                first_name=name_list[0]
                family_name=name_list[-1]
                #print(name_list)
                information_list.append(str(first_name))
                information_list.append(str(family_name))
            elif information_title=="Birthday":
                date_object=datetime.datetime.strptime(information_value, '%m/%d/%Y').date()
                #print(date_object)
                information_list.append(date_object)
                information_list.append(str(first_name)+'__'+str(family_name)+str(random.randint(50,500)))
            else:
                #print(information_title,':',information_value)
                information_list.append(information_value)
            #information_list.append(psycopg2.Binary(image_data))
        else:
            pass
    if len(information_list)>1:
        big_list.append(information_list)
        print(information_list[0]+' '+information_list[1]+' has been created')
        label['text']=information_list[0]+" "+information_list[1]+" has been created."
        sleep(1)


def generate_people(entry):
    for j in range(int(entry)):
        generate_person(entry)
        global information_list


#print(big_list)
    df = pd.DataFrame(big_list,columns=("name", "family_name", "date_of_birth", "identifier", "gender"))
    print(df)
    alchemyEngine           = create_engine('postgresql+psycopg2://postgres:Mahdi25120894@localhost/InstaNationDB')
    postgreSQLConnection    = alchemyEngine.connect()
    postgreSQLTable         = 'Generated Identity'
    try:
        frame = df.to_sql(postgreSQLTable, postgreSQLConnection, if_exists='replace')
        postgreSQLConnection.execute('ALTER TABLE public."Generated Identity" RENAME COLUMN index TO id;')
    except ValueError as vx:
        print(vx)
    except Exception as ex:
        print(ex)
    else:
        label['text']="PostgreSQL Table has been created successfully.\n" +str(df.iloc[:,:])
    finally:
        postgreSQLConnection.close()



root = tk.Tk()
root.title("Identity Generator")

canvas=tk.Canvas(root, height=HEIGHT , width=WIDTH )
canvas.pack()

frame=tk.Frame(root, bg='#99ceff',bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry=tk.Entry(frame, font=40 )
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Generate Identities", bg="gray", font=40, command=lambda:generate_people(entry.get()))
button.place(relx=0.7, rely=0,relwidth=0.3, relheight=1)

lower_frame= tk.Frame(root,bg='#99ceff',bd=5)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame, font=('modern',12), anchor='nw', justify='left')
label.place(relx=0, rely=0,relwidth=1, relheight=1)
#myscroll = ttk.Scrollbar(label, orient='vertical')




root.mainloop()
