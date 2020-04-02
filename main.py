# -*- coding: cp1252 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Sch�ler zu Projekten

import csv
import os
import sqlite3 as sqli
from tkinter import *
from tkinter import filedialog  # muss aus unbekannten Gr�nden extra importiert werden
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
        read = csv.reader(file, delimiter=';')
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
        read = csv.reader(file, delimiter=';')
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

    def einfuegen(self, tabelle, spalten_namen_tuple, value_tuple):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()
        sql = "insert into "+tabelle+"("
        for i in range(len(spalten_namen_tuple)):
            if i == len(spalten_namen_tuple)-1:
                sql += spalten_namen_tuple[i] + ")"
            else:
                sql += spalten_namen_tuple[i] + ", "
        sql += " VALUES('"
        for i in range(len(value_tuple)):
            if i == len(value_tuple)-1:
                sql += value_tuple[i] + "');"
            else:
                sql += value_tuple[i] + "', '"
        print(sql)
        cur.execute(sql)
        con.commit()
        con.close()

    def ausgabe(self, tabelle):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        sql = "SELECT * FROM " + tabelle + ";"
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
    def __init__(self, callback_imp, callback_exp, callback_bee, callback_J5, callback_J6, callback_J7, callback_J8,
                 callback_J9,
                 callback_J10, callback_J11, callback_J12, callback_J13, callback_hin):
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
        self.callback_hin = callback_hin
        self.schue_labels = {}
        self.labelnames = ["Vorname", "Nachname", "Klasse", "Jahrg", "Erst Wunsch", "Zweit Wunsch", "Dritt Wunsch"]
        self.schue_entrys = []

        self.ro_botton = None   # your ordinary buttom
        self.rahmen1 = Frame(master=self)
        self.rahmen2 = Frame(master=self)
        self.rahmen11 = Frame(master=self.rahmen1)

        # erstellen des Men�s
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Import", command=self.callback_imp)
        self.filemenu.add_command(label="Export", command=self.callback_exp)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Beenden", command=self.callback_bee)
        self.menubar.add_cascade(label="Datei", menu=self.filemenu)
        self.fmenu = Menu(self.menubar, tearoff=0)
        self.fmenu.add_command(label="Sch�ler hinzuf�gen", command=self.schulerhin)
        self.menubar.add_cascade(label="Sch�ler", menu=self.fmenu)
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
        neu = Tk()
        neu.title("Neue Sch�ler")
        neu.geometry('780x110')
        for i in range(len(self.labelnames)):
            self.schue_labels.update({self.labelnames[i]:Label(neu, text=self.labelnames[i])})
            self.schue_labels[self.labelnames[i]].place(x=10+(110*i), y=10, width=100)
        for i in range(len(self.labelnames)):
            self.schue_entrys.append(Entry(neu))
            self.schue_entrys[-1].place(x=10+(110*i), y=40, width=100)

        self.ro_botton = Button(master=neu, text="Sch�ler hinzuf�gen", command=self.callback_hin)
        self.ro_botton.place(x=330, y=70, width=120, height=30)


class Controller(object):
    def __init__(self):
        self.model = Model()
        self.view = View(self.importieren, self.exportieren, self.beenden, self.J5, self.J6, self.J7, self.J8, self.J9,
                         self.J10, self.J11, self.J12, self.J13, self.hinzufugen)

    def importieren(self):
        slcsv = filedialog.askopenfilename(title="Sch�lerliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        plcsv = filedialog.askopenfilename(title="Projektliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        self.model.importCSV(slcsv, plcsv)

    def exportieren(self):
        pass

    def beenden(self):
        x = askokcancel(title='Beenden',
                        message='M�chtest du das Programm wirklich beenden?'
                                '\nNicht abgeschlossene Aktionen k�nnten zu fehlern f�hren!')
        if x:
            self.view.destroy()

    def tabelle(self, tabellen_name):
        x = self.model.ausgabe(tabellen_name)
        for i in range(len(x)):
            for j in range(len(x[0])):
                b = Label(self.view, text=str(x[i][j]), bg="lightgray")
                b.grid(row=i, column=j)

    def hinzufugen(self):
        erst = self.view.schue_entrys[4].get()
        zweit = self.view.schue_entrys[5].get()
        dritt = self.view.schue_entrys[6].get()
        if self.view.schue_entrys[6].get() == "":
            print(7)
            dritt = "33"
            if self.view.schue_entrys[5].get() == "":
                zweit = "33"
                if self.view.schue_entrys[4].get() == "":
                    erst = "33"
        if self.view.schue_entrys[0].get() != "" and self.view.schue_entrys[1].get() != "" and\
                self.view.schue_entrys[2].get() != "" and self.view.schue_entrys[3].get() != "":
            self.model.einfuegen('schueler', ('sName', 'sVName', 'sJahrg', 'sKla', 'sErst', 'sZweit', 'sDritt'),
                                 (self.view.schue_entrys[1].get(), self.view.schue_entrys[0].get(),
                                  self.view.schue_entrys[2].get(), self.view.schue_entrys[3].get(), erst, zweit, dritt))

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
