# -*- coding: cp1252 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Schüler zu Projekten

import csv
import os
import sqlite3 as sqli
from tkinter import *
from tkinter import filedialog  # muss aus unbekannten Gründen extra importiert werden
from tkinter.messagebox import *
from zuordnung import auswahl



                

class Model(object):
    def __init__(self):
        if not os.path.exists('pwvwp.db'):
            self.dbAnlegen()

    def dbAnlegen(self):
        connection = sqli.connect('pwvwp.db')
        cursor = connection.cursor()

        # Tabellen erzeugen
        sql = "CREATE TABLE projekte(pID INTEGER PRIMARY KEY, pName TEXT, pJahrg INTEGER, pNum INTEGER, pMaxS INTEGER)"
        cursor.execute(sql)

        sql = "CREATE TABLE schueler(sID INTEGER PRIMARY KEY, sName TEXT, sVName TEXT, sJahrg INTEGER, sKla INTEGER, sErst INTEGER, sZweit INTEGER, sDritt INTEGER, sZu INTEGER);"
        cursor.execute(sql)

        print('Datenbank pwvwp.db mit Tabellen mitarbeiter und projekte angelegt.')
        connection.commit()
        connection.close()

    def importCSV(self, slcsv, plcsv):  # sl = schuelerliste, pl = projektliste
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        # importieren der slcsv Datei
        file = open(slcsv, 'r')
        read = csv.reader(file, delimiter=',')
        for row in read:
            sql = "SELECT COUNT(*) FROM schueler WHERE sName = '" + row[0] + "' AND sVName = '" + row[1] + "' AND sJahrg = '" + row[2] + "';"
            cur.execute(sql)
            test = cur.fetchall()
            if not test[0][0]:
                sql = "INSERT INTO schueler(sName, sVName, sJahrg, sKla, sErst, sZweit, sDritt, sZu) VALUES('" + row[0] + "', '" + row[1] + "', '" + row[2] + "', '" + row[3] + "', '" + row[4] + "', '" + row[5] + "', '" + row[6] + "', NULL);"
                cur.execute(sql)
            

        # importieren der plcsv Datei
        file = open(plcsv, 'r')
        read = csv.reader(file, delimiter=',')
        for row in read:
            sql = "SELECT COUNT(*) FROM projekte WHERE pName = '" + row[0] + "' AND pJahrg = '" + row[1] + "';"
            cur.execute(sql)
            test = cur.fetchall()
            if not test[0][0]:
                sql = "INSERT INTO projekte(pName, pJahrg, pNum, pMaxS) VALUES('" + row[0] + "', '" + row[1] + "', '" + \
                      row[2] + "', '" + row[3] + "');"
                cur.execute(sql)
            

        con.commit()
        con.close()

    def ausgabe(self, tabellen_name):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        sql = "SELECT * FROM "+tabellen_name+";"
        cur.execute(sql)
        erg = cur.fetchall()

        con.close()
        return erg

#    def dbAuslesen(self):
#        con = sqli.connect('pwvwp.db')
#        cur = con.cursor()
#        
#        sql = "SELECT sName FROM schueler"


class View(Tk):
    def __init__(self, callback_imp, callback_exp, callback_bee, callback_J5, callback_J6, callback_J7, callback_J8, callback_J9,
                 callback_J10, callback_J11, callback_J12, callback_J13, hinzu, callback_a1, callback_a2, callback_a3, callback_a4, callback_a5,
                 callback_a6, callback_a7, callback_andern):
        Tk.__init__(self)
        self.title("Projektwochenverwaltungsprogramm")
        self.geometry('750x300')
        self.maxsize(750,300)
        self.minsize(750,300)
        # bestimmen der Callbacks
        self.callback_imp = callback_imp
        self.callback_exp = callback_exp
        self.callback_bee = callback_bee
        self.callback_J5 = callback_J5
        self.callback_J6 = callback_J6
        self.callback_J7 = callback_J7
        self.callback_J8 = callback_J8
        self.callback_J9 = callback_J9
        self.callback_J10 = callback_J10
        self.callback_J11 = callback_J11
        self.callback_J12 = callback_J12
        self.callback_J13 = callback_J13
        self.callback_a1 = callback_a1
        self.callback_a2 = callback_a2
        self.callback_a3 = callback_a3
        self.callback_a4 = callback_a4
        self.callback_a5 = callback_a5
        self.callback_a6 = callback_a6
        self.callback_a7 = callback_a7
        self.callback_andern = callback_andern
        self.hinzufugen=hinzu
        self.rahmen1 = Frame(master=self)
        self.rahmen2 = Frame(master=self)
        
        self.rahmen11 = Frame(master=self.rahmen1)

        # erstellen des Menüs
        self.menubar=Menu(self)
        self.filemenu=Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Import", command=self.callback_imp)
        self.filemenu.add_command(label="Export", command=self.callback_exp)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.destroy)
        self.menubar.add_cascade(label="Datei", menu=self.filemenu)
        self.fmenu=Menu(self.menubar, tearoff=0)
        self.fmenu.add_command(label="Schüler hinzufügen", command=self.schulerhin)
        self.fmenu.add_command(label="Schüler �ndern", command=self.andern)
        self.menubar.add_cascade(label="Schüler", menu=self.fmenu)
        self.config(menu=self.menubar)

        #scrollbar
        def myfunction(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas=Canvas(self.rahmen2,width=1000)
        self.frame=Frame(self.canvas)
        self.scrollbar = Scrollbar(self.rahmen2, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.frame,anchor='nw')
        self.frame.bind("<Configure>",myfunction)

        self.rahmen1.pack()
        self.rahmen2.pack(side=LEFT)
        self.rahmen11.pack(side=LEFT, fill=X)
        # self.rahmen12.pack(sie=LEFT, fill=X)

        self.v = IntVar()
        self.r1 = Radiobutton(self.rahmen11, text="5", variable=self.v, value=1, command=self.callback_J5).pack(
            anchor=W, side=LEFT)
        self.r2 = Radiobutton(self.rahmen11, text="6", variable=self.v, value=2, command=self.callback_J6).pack(
            anchor=W, side=LEFT)
        self.r3 = Radiobutton(self.rahmen11, text="7", variable=self.v, value=3, command=self.callback_J7).pack(
            anchor=W, side=LEFT)
        self.r4 = Radiobutton(self.rahmen11, text="8", variable=self.v, value=4, command=self.callback_J8).pack(
            anchor=W, side=LEFT)
        self.r5 = Radiobutton(self.rahmen11, text="9", variable=self.v, value=5, command=self.callback_J9).pack(
            anchor=W, side=LEFT)
        self.r6 = Radiobutton(self.rahmen11, text="10", variable=self.v, value=6, command=self.callback_J10).pack(
            anchor=W, side=LEFT)
        self.r7 = Radiobutton(self.rahmen11, text="11", variable=self.v, value=7, command=self.callback_J11).pack(
            anchor=W, side=LEFT)
        self.r8 = Radiobutton(self.rahmen11, text="12", variable=self.v, value=8, command=self.callback_J12).pack(
            anchor=W, side=LEFT)
        self.r9 = Radiobutton(self.rahmen11, text="Alle", variable=self.v, value=9, command=self.callback_J13).pack(
            anchor=W, side=LEFT)
        
        self.b2=Button(text="Zuordnen", command=auswahl())
        self.b2.place(x=10,y=260,width=600, height=30)
        
        
        
    def schulerhin(self):
        neu=Tk()
        neu.title("Neue Schüler")
        neu.geometry('780x110')
        neu.maxsize(780,110)
        neu.minsize(780,110)
        self.l1=Label(master=neu, text="Vorname")
        self.l1.place(x=10,y=10,width=100)
        self.l2=Label(master=neu, text="Nachname")
        self.l2.place(x=120,y=10,width=100)
        self.l3=Label(master=neu, text="Klasse")
        self.l3.place(x=230,y=10,width=100)
        self.l4=Label(master=neu, text="Jahrg")
        self.l4.place(x=340,y=10,width=100)
        self.l5=Label(master=neu, text="Erst Wunsch")
        self.l5.place(x=450,y=10,width=100)
        self.l6=Label(master=neu, text="Zweit Wunsch")
        self.l6.place(x=560,y=10,width=100)
        self.l7=Label(master=neu, text="Dritt Wunsch")
        self.l7.place(x=670,y=10,width=100)

        
        self.e1=Entry(master=neu)
        self.e1.place(x=10,y=40,width=100)
        self.e2=Entry(master=neu)
        self.e2.place(x=120,y=40,width=100)
        self.e3=Entry(master=neu)
        self.e3.place(x=230,y=40,width=100)
        self.e4=Entry(master=neu)
        self.e4.place(x=340,y=40,width=100)
        self.e5=Entry(master=neu)
        self.e5.place(x=450,y=40,width=100)
        self.e6=Entry(master=neu)
        self.e6.place(x=560,y=40,width=100)
        self.e7=Entry(master=neu)
        self.e7.place(x=670,y=40,width=100)

        
        connection = sqli.connect('pwvwp.db')
        cursor = connection.cursor()
        self.b1=Button(master=neu, text="Schüler hinzufügen", command=self.hinzufugen)
        self.b1.place(x=10,y=70,width=760, height=30)
        connection.commit()
        connection.close()

    def andern(self):
        ande=Tk()
        ande.title("Sch�ler �ndern")
        ande.geometry('600x110')

        
        self.rahmen16 = Frame(master=ande)
        self.rahmen15 = Frame(master=self.rahmen16)
        self.rahmen16.pack()
        self.rahmen15.pack(side=LEFT, fill=X)
        self.v = IntVar()
        self.au1 = Radiobutton(self.rahmen15, text="Vorname", variable=self.v, value=1, command=self.callback_a1).pack(
            anchor=W, side=LEFT)
        self.au2 = Radiobutton(self.rahmen15, text="Nachname", variable=self.v, value=2, command=self.callback_a2).pack(
            anchor=W, side=LEFT)
        self.au3 = Radiobutton(self.rahmen15, text="Klasse", variable=self.v, value=3, command=self.callback_a3).pack(
            anchor=W, side=LEFT)
        self.au4 = Radiobutton(self.rahmen15, text="Jahrgang", variable=self.v, value=4, command=self.callback_a4).pack(
            anchor=W, side=LEFT)
        self.au5 = Radiobutton(self.rahmen15, text="Erst Wunsch", variable=self.v, value=5, command=self.callback_a5).pack(
            anchor=W, side=LEFT)
        self.au6 = Radiobutton(self.rahmen15, text="Zweit Wunsch", variable=self.v, value=6, command=self.callback_a6).pack(
            anchor=W, side=LEFT)
        self.au7 = Radiobutton(self.rahmen15, text="Dritt Wunsch", variable=self.v, value=7, command=self.callback_a7).pack(
            anchor=W, side=LEFT)
        self.la1=Label(master=ande, text="sID")
        self.la1.place(x=10,y=20,width=30)
        self.ea1=Entry(master=ande)
        self.ea1.place(x=10,y=40,width=30)
        self.ea2=Entry(master=ande)
        self.ea2.place(x=50,y=40,width=540)
        self.b3=Button(master=ande, text="�ndern", command=self.callback_andern)
        self.b3.place(x=10,y=70,width=580, height=30)
         

class Controller(object):
    def __init__(self):
        self.model = Model()
        self.view = View(self.importieren, self.exportieren, self.beenden, self.J5, self.J6, self.J7, self.J8, self.J9,
                         self.J10, self.J11, self.J12, self.J13, self.hinzufugen, self.a1, self.a2, self.a3, self.a4, self.a5,
                         self.a6, self.a7, self.andernnn)
        if os.path.exists('projektliste.csv') and os.path.exists('schuelerliste.csv'):
            self.model.importCSV('schuelerliste.csv', 'projektliste.csv')
        self.andernx=""
        auswahl()
        self.tabelle()
        
    
    def importieren(self):
        slcsv = filedialog.askopenfilename(title="Schülerliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        plcsv = filedialog.askopenfilename(title="Projektliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        self.model.importCSV(slcsv, plcsv)
        self.tabelle()

    def exportieren(self):
        pass

    def beenden(self):
        x = askokcancel(title='Beenden', message='Möchtest du das Programm wirklich beenden?\nNicht abgeschlossene Aktionen könnten zu fehlern führen!')
        if x:
            self.view.destroy()

    def tabelle(self):
        x = self.model.ausgabe("schueler")
        for i in range(len(x)):
            for j in range(len(x[0])):
                self.b = Label(self.view.frame, text=str(x[i][j]))
                self.b.grid(row=i, column=j)
    def hinzufugen(self):
        erst=self.view.e5.get()
        zweit=self.view.e6.get()
        dritt=self.view.e7.get()
        if self.view.e7.get()=="":
            dritt="33"
            if self.view.e6.get()=="":
                zweit="33"
                if self.view.e5.get()=="":
                    erst="33"
        if self.view.e1.get()!="" and self.view.e2.get()!="" and self.view.e3.get()!="" and self.view.e4.get()!="" :
            connection = sqli.connect('pwvwp.db')
            cursor = connection.cursor()
            sql = "SELECT COUNT(*) FROM schueler WHERE sName = '"+str(self.view.e2.get())+"' AND sVName = '"+str(self.view.e1.get())+"' AND sKla = '"+str(self.view.e3.get())+"';"
            cursor.execute(sql)
            test = cursor.fetchall()
            if not test[0][0]:
                sql="insert into schueler (sName, sVName, sJahrg, sKla, sErst, sZweit, sDritt) VALUES('"+str(self.view.e2.get())+"','"+str(self.view.e1.get())+"','"+str(self.view.e4.get())+"','"+str(self.view.e3.get())+"','"+str(erst)+"','"+str(zweit)+"','"+str(dritt)+"')"        
                cursor.execute(sql)
            else:
                self.view.b1.config(bg="red")
            connection.commit()
            connection.close()
            self.view.b1.config(bg="green")
        else:
            self.view.b1.config(bg="red")
        self.tabelle()

    def andernnn(self):
        if self.andernx!="" and self.view.ea1.get()!="":
            connection = sqli.connect('pwvwp.db')
            cursor = connection.cursor()
            sql="update schueler set "+self.andernx+"='"+str(self.view.ea2.get())+"' where sID like '"+str(self.view.ea1.get())+"'"        
            cursor.execute(sql)
            connection.commit()
            connection.close()
        self.tabelle()

    def J5(self):
        pass

    def J6(self):
        pass

    def J7(self):
        pass

    def J8(self):
        pass

    def J9(self):
        pass

    def J10(self):
        pass

    def J11(self):
        pass

    def J12(self):
        pass

    def J13(self):
        pass

    def a1(self):
        self.andernx="sVName"

    def a2(self):
        self.andernx="sName"

    def a3(self):
        self.andernx="sKla"

    def a4(self):
        self.andernx="sJahrg"

    def a5(self):
        self.andernx="sErst"

    def a6(self):
        self.andernx="sZweit"

    def a7(self):
        self.andernx="sDritt"



c = Controller()
c.view.mainloop()