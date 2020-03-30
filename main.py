# -*- coding: cp1252 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Schüler zu Projekten

import csv
import os
import sqlite3 as sqli
from tkinter import *
from tkinter import filedialog  # muss aus unbekannten Gründen extra importiert werden
from tkinter.messagebox import *


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

        print('Datenbank schuelerliste.db mit Tabellen mitarbeiter und projekte angelegt.')
        connection.commit()
        connection.close()

    def importCSV(self, slcsv, plcsv):  # sl = schuelerliste, pl = projektliste
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        # importieren der slcsv Datei
        file = open(slcsv, 'r')
        read = csv.reader(file, delimiter=',')
        for row in read:
            sql = "SELECT COUNT(*) FROM schueler WHERE sName = '" + row[0] + "' AND sVName = '" + row[
                1] + "' AND sJahrg = '" + row[2] + "';"
            cur.execute(sql)
            test = cur.fetchall()
            if not test[0][0]:
                sql = "INSERT INTO schueler(sName, sVName, sJahrg, sKla, sErst, sZweit, sDritt, sZu) VALUES('" + row[
                    0] + "', '" + row[1] + "', '" + row[2] + "', '" + row[3] + "', '" + row[4] + "', '" + row[
                          5] + "', '" + row[6] + "', NULL);"
                cur.execute(sql)
            else:
                print('Eintrag bereits vorhanden!')

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
            else:
                print('Eintrag bereits vorhanden!')
        print('CSV-Dateien importiert!')

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
                 callback_J10, callback_J11, callback_J12, callback_J13, hinzu):
        Tk.__init__(self)
        self.title("Projektwochenverwaltungsprogramm")
        self.geometry('600x300')
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
        self.menubar.add_cascade(label="Schüler", menu=self.fmenu)
        self.config(menu=self.menubar)

        self.scrollbar = Scrollbar(self.rahmen2)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self.rahmen2, yscrollcommand=self.scrollbar.set)
        for i in range(1000):
            self.listbox.insert(END, str(i))
        self.listbox.pack(side=RIGHT, fill=BOTH)
        self.scrollbar.config(command=self.listbox.yview)

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
        self.r9 = Radiobutton(self.rahmen11, text="13", variable=self.v, value=9, command=self.callback_J13).pack(
            anchor=W, side=LEFT)
        
        
    def schulerhin(self):
        neu=Tk()
        neu.title("Neue Schüler")
        neu.geometry('780x110')
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

        self.b1=Button(master=neu, text="Schüler hinzufügen", command=self.hinzufugen)
        self.b1.place(x=330,y=70,width=120, height=30)
        



class Controller(object):
    def __init__(self):
        self.model = Model()
        self.view = View(self.importieren, self.exportieren, self.beenden, self.J5, self.J6, self.J7, self.J8, self.J9,
                         self.J10, self.J11, self.J12, self.J13, self.hinzufugen)

    def importieren(self):
        slcsv = filedialog.askopenfilename(title="Schülerliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        plcsv = filedialog.askopenfilename(title="Projektliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        self.model.importCSV(slcsv, plcsv)

    def exportieren(self):
        pass

    def beenden(self):
        x = askokcancel(title='Beenden', message='Möchtest du das Programm wirklich beenden?\nNicht abgeschlossene Aktionen könnten zu fehlern führen!')
        if x:
            self.view.destroy()

    def tabelle(self, tabellen_name):
        x = self.model.ausgabe(tabellen_name)
        for i in range(len(x)):
            for j in range(len(x[0])):
                b = Label(self.view, text=str(x[i][j]), bg="lightgray")
                b.grid(row=i, column=j)
    def hinzufugen(self):
        erst=self.view.e5.get()
        zweit=self.view.e6.get()
        dritt=self.view.e7.get()
        if self.view.e7.get()=="":
            print(7)
            dritt="33"
            if self.view.e6.get()=="":
                zweit="33"
                if self.view.e5.get()=="":
                    erst="33"
        if self.view.e1.get()!="" and self.view.e2.get()!="" and self.view.e3.get()!="" and self.view.e4.get()!="" :
            connection = sqli.connect('schuelerliste.db')
            cursor = connection.cursor()
            sql="insert into schueler (sName, sVName, sJahrg, sKla, sErst, sZweit, sDritt) VALUES('"+str(self.view.e2.get())+"','"+str(self.view.e1.get())+"','"+str(self.view.e3.get())+"','"+str(self.view.e4.get())+"','"+str(erst)+"','"+str(zweit)+"','"+str(dritt)+"')"        
            cursor.execute(sql)
            connection.commit()
            connection.close()

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


c = Controller()
c.view.mainloop()
