# -*- coding: cp1252 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Schüler zu Projekten

import csv, os, random, time
import sqlite3 as sqli
from tkinter import *
from tkinter import filedialog  # muss aus unbekannten Gründen extra importiert werden
from tkinter.messagebox import *


class Model(object):
    def __init__(self):
        self.wahlen = ('sErst', 'sZweit', 'sDritt')
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

    def auswahl(self):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()
        for wahl in self.wahlen:
            jahrg = 4  # Jahrgang
            while jahrg <= 11:
                jahrg += 1
                b = 1  # Projekt
                sql = "select max(pNum) FROM projekte WHERE '" + str(
                    jahrg) + "' like pJahrg;"  # max Projektnummer wird ermittelt
                cur.execute(sql)
                x = cur.fetchall()  # max Projektnummer
                xx = x[0][0]
                while b <= xx:
                    liste = []
                    sql = "select max(sID) FROM schueler WHERE '" + str(jahrg) + "' like sJahrg and '" + str(
                        b) + "' like " + wahl + ";"  # max sID wird ermittelt
                    cur.execute(sql)
                    zz = cur.fetchall()
                    z = 0
                    if zz[0][0]:
                        z = zz[0][0]
                    y = 0  # zaehler sID
                    while y <= z:
                        sql = "select sID FROM schueler WHERE '" + str(
                            jahrg) + "' like sJahrg and sZu is NULL and '" + str(
                            b) + "' like " + wahl + " and '" + str(
                            y) + "' like sID;"  # Ermittlung von Schülern in jahrg jahrgang und b erstwahl
                        cur.execute(sql)
                        f = cur.fetchall()
                        if f:
                            ff = f[0][0]
                            liste.append(ff)
                        y += 1
                    sql = "select pMaxS FROM projekte WHERE '" + str(jahrg) + "' like pJahrg and '" + str(
                        b) + "' like pNum;"
                    cur.execute(sql)
                    maxanz0 = cur.fetchall()
                    if maxanz0:
                        if wahl == 'sErst':
                            maxanz = maxanz0[0][0]
                        else:
                            sql = "select count(sID) FROM schueler WHERE '" + str(
                                jahrg) + "' like sJahrg and '" + str(
                                b) + "' like sZu;"
                            cur.execute(sql)
                            maxanz1 = cur.fetchall()
                            maxanz = maxanz0[0][0] - maxanz1[0][0]
                    else:
                        maxanz = 0
                    if maxanz > 0 and liste:
                        if len(liste) <= maxanz:
                            m = 0  # zähler der schüler
                            while m < len(liste):
                                sql = "update schueler set sZu='" + str(b) + "' where '" + str(liste[m]) + "'like sID;"
                                cur.execute(sql)
                                m += 1
                        else:
                            m = 0  # zähler der schüler
                            listeaus1 = random.choices(liste, k=maxanz)
                            while m < maxanz:
                                sql = "update schueler set sZu='" + str(b) + "' where '" + str(
                                    listeaus1[m]) + "'like sID;"
                                cur.execute(sql)
                                m += 1
                    b = b + 1
        sql = "select count(sID) from schueler WHERE 8 like sJahrg"
        cur.execute(sql)
        schuler = cur.fetchall()
        jahrg = 4  # Jahrgang
        while jahrg <= 11:
            jahrg += 1
            sql = "select pNum from projekte WHERE '" + str(jahrg) + "' like pJahrg"
            cur.execute(sql)
            projekte = cur.fetchall()
            sql = "select sID from schueler WHERE '" + str(jahrg) + "' like sJahrg and sZu is NULL"
            cur.execute(sql)
            schuler = cur.fetchall()
            while len(schuler) > 0 and len(projekte) > 0:
                sql = "select pMaxS from projekte WHERE '" + str(jahrg) + "' like pJahrg and '" + str(
                    projekte[0][0]) + "' like pNum"
                cur.execute(sql)
                maxanz0 = cur.fetchall()
                if maxanz0:
                    sql = "select count(sID) from schueler WHERE '" + str(jahrg) + "' like sJahrg and '" + str(
                        projekte[0][0]) + "' like sZu"
                    cur.execute(sql)
                    maxanz1 = cur.fetchall()
                    maxanz = maxanz0[0][0] - maxanz1[0][0]
                    if maxanz <= 0:
                        projekte.pop(0)
                    else:
                        sql = "update schueler set sZu='" + str(projekte[0][0]) + "' where '" + str(
                            schuler[0][0]) + "'like sID ;"
                        cur.execute(sql)
                        schuler.pop(0)
            con.commit()
            con.close()

    def einfuegen(self, tabelle, spalten_namen_tuple, value_tuple):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()
        sql = "INSERT INTO " + tabelle + "("
        for i in range(len(spalten_namen_tuple)):
            if i == len(spalten_namen_tuple) - 1:
                sql += spalten_namen_tuple[i] + ")"
            else:
                sql += spalten_namen_tuple[i] + ", "
        sql += " VALUES('"
        for i in range(len(value_tuple)):
            if i == len(value_tuple) - 1:
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
    def __init__(self, callback_imp, callback_exp, callback_bee, callback_j5, callback_j6, callback_j7, callback_j8,
                 callback_j9,
                 callback_j10, callback_j11, callback_j12, callback_j13, callback_hin):
        Tk.__init__(self)
        self.title("Projektwochenverwaltungsprogramm")
        self.geometry('600x300')
        # bestimmen der Callbacks
        self.callback_imp = callback_imp
        self.callback_exp = callback_exp
        self.callback_bee = callback_bee
        self.callback_J5 = callback_j5
        self.callback_J6 = callback_j6
        self.callback_J7 = callback_j7
        self.callback_J8 = callback_j8
        self.callback_J9 = callback_j9
        self.callback_J10 = callback_j10
        self.callback_J11 = callback_j11
        self.callback_J12 = callback_j12
        self.callback_J13 = callback_j13
        self.callback_hin = callback_hin
        self.schue_labels = {}
        self.labelnames = ["Vorname", "Nachname", "Klasse", "Jahrg", "Erst Wunsch", "Zweit Wunsch", "Dritt Wunsch"]
        self.schue_entrys = []

        self.ro_botton = None  # your ordinary buttom
        self.rahmen1 = Frame(master=self)
        self.rahmen2 = Frame(master=self)
        self.rahmen11 = Frame(master=self.rahmen1)

        # erstellen des Menüs
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Import", command=self.callback_imp)
        self.filemenu.add_command(label="Export", command=self.callback_exp)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Beenden", command=self.callback_bee)
        self.menubar.add_cascade(label="Datei", menu=self.filemenu)
        self.fmenu = Menu(self.menubar, tearoff=0)
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
        neu = Tk()
        neu.title("Neue Schüler")
        neu.geometry('780x110')
        for i in range(len(self.labelnames)):
            self.schue_labels.update({self.labelnames[i]: Label(neu, text=self.labelnames[i])})
            self.schue_labels[self.labelnames[i]].place(x=10 + (110 * i), y=10, width=100)
        for i in range(len(self.labelnames)):
            self.schue_entrys.append(Entry(neu))
            self.schue_entrys[-1].place(x=10 + (110 * i), y=40, width=100)

        self.ro_botton = Button(master=neu, text="Schüler hinzufügen", command=self.callback_hin)
        self.ro_botton.place(x=330, y=70, width=120, height=30)


class Controller(object):
    def __init__(self):
        self.model = Model()
        self.view = View(self.importieren, self.exportieren, self.beenden, self.J5, self.J6, self.J7, self.J8, self.J9,
                         self.J10, self.J11, self.J12, self.J13, self.hinzufugen)
        if os.path.exists('projektliste.csv') and os.path.exists('schuelerliste.csv'):
            self.model.importCSV('schuelerliste.csv', 'projektliste.csv')

    def importieren(self):
        slcsv = filedialog.askopenfilename(title="Schülerliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        plcsv = filedialog.askopenfilename(title="Projektliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        self.model.importCSV(slcsv, plcsv)

    def exportieren(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def beenden(self):
        x = askokcancel(title='Beenden',
                        message='Möchtest du das Programm wirklich beenden?'
                                '\nNicht abgeschlossene Aktionen könnten zu fehlern führen!')
        if x:
            self.view.destroy()

    def tabelle(self, tabellen_name):
        x = self.model.ausgabe(tabellen_name)
        for i in range(len(x)):
            for j in range(len(x[0])):
                b = Label(self.view, text=str(x[i][j]), bg="lightgray")
                b.grid(row=i, column=j)

    def hinzufugen(self):
        for entry in self.view.schue_entrys:
            entry.config(bg='white')
        erst = self.view.schue_entrys[4].get()
        zweit = self.view.schue_entrys[5].get()
        dritt = self.view.schue_entrys[6].get()
        if dritt == "":
            dritt = "33"
        if zweit == "":
            zweit = "33"
        if erst == "":
            erst = "33"
        if self.view.schue_entrys[0].get() != "" and self.view.schue_entrys[1].get() != "" and \
                self.view.schue_entrys[2].get() != "" and self.view.schue_entrys[3].get() != "":
            self.model.einfuegen('schueler', ('sName', 'sVName', 'sJahrg', 'sKla', 'sErst', 'sZweit', 'sDritt'),
                                 (self.view.schue_entrys[1].get(), self.view.schue_entrys[0].get(),
                                  self.view.schue_entrys[2].get(), self.view.schue_entrys[3].get(), erst, zweit, dritt))
            self.view.ro_botton.config(bg="green")
            for entry in self.view.schue_entrys:
                entry.delete(0, 'end')
        else:
            self.view.ro_botton.config(bg="red")
            for i in range(4):
                if self.view.schue_entrys[i].get() == "":
                    self.view.schue_entrys[i].config(bg='red')
        self.view.update()
        time.sleep(0.1)
        self.view.ro_botton.config(bg="white")

    def J5(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def J6(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def J7(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def J8(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def J9(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def J10(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def J11(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def J12(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def J13(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')


c = Controller()
c.view.mainloop()
