# -*- coding: cp1252 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Sch�ler zu Projekten

import csv, os, random, time
import sqlite3 as sqli
from tkinter import *
from tkinter import filedialog  # muss aus unbekannten Gr�nden extra importiert werden
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

        print('Datenbank pwvwp.db mit Tabellen mitarbeiter und projekte angelegt.')
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

    def exportCSV(self, slcsv, plcsv):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        # auslesen der datenbankliste schueler in eine CSV-Datei
        slfile = csv.writer(slcsv, delimiter=';', quoting=csv.QUOTE_NONE)
        sql = "SELECT * FROM schueler;"
        cur.execute(sql)
        dboutput = cur.fetchall()
        for spalte in dboutput:
            spalte = list(spalte)
            del spalte[0]
            slfile.writerow(spalte)

        # auslesen der datenbankliste projekte in eine CSV-Datei
        plfile = csv.writer(plcsv, delimiter=';', quoting=csv.QUOTE_NONE)
        sql = "SELECT * FROM schueler;"
        cur.execute(sql)
        dboutput = cur.fetchall()
        for spalte in dboutput:
            plfile.writerow(spalte)

        print('Die Ergebnisse wurden in zwei CSV-Dateien Ausgegeben! Die Trennzeichen sind ";".')
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
                            y) + "' like sID;"  # Ermittlung von Sch�lern in jahrg jahrgang und b erstwahl
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
                            m = 0  # z�hler der sch�ler
                            while m < len(liste):
                                sql = "update schueler set sZu='" + str(b) + "' where '" + str(liste[m]) + "'like sID;"
                                cur.execute(sql)
                                m += 1
                        else:
                            m = 0  # z�hler der sch�ler
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
                 callback_j9, callback_j10, callback_j11, callback_j12, callback_ja, callback_hin, callback_aus,
                 callback_ande, callback_a1, callback_a2, callback_a3, callback_a4, callback_a5, callback_a6,
                 callback_a7):
        Tk.__init__(self)
        self.title("Projektwochenverwaltungsprogramm")
        self.geometry('750x300')
        self.maxsize(750, 300)
        self.minsize(750, 300)
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
        self.callback_JA = callback_ja
        self.callback_aus = callback_aus
        self.callback_hin = callback_hin
        self.callback_ande = callback_ande
        self.callback_a1 = callback_a1
        self.callback_a2 = callback_a2
        self.callback_a3 = callback_a3
        self.callback_a4 = callback_a4
        self.callback_a5 = callback_a5
        self.callback_a6 = callback_a6
        self.callback_a7 = callback_a7
        self.labels = {}
        self.labelnames = ("Vorname", "Nachname", "Klasse", "Jahrg", "Erst Wunsch", "Zweit Wunsch", "Dritt Wunsch")
        self.entrys = {}
        self.buttons = {}
        self.rahmen = {1: Frame(master=self), 2: Frame(master=self)}
        self.rahmen.update({11: Frame(master=self.rahmen[1])})
        self.fenster = {}

        self.ande_v = None
        self.ande_r1 = None
        self.ande_r2 = None
        self.ande_r3 = None
        self.ande_r4 = None
        self.ande_r5 = None
        self.ande_r6 = None
        self.ande_r7 = None

        # erstellen des Men�s
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="importieren", command=self.callback_imp)
        self.filemenu.add_command(label="exportieren", command=self.callback_exp)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Beenden", command=self.callback_bee)
        self.menubar.add_cascade(label="Datei", menu=self.filemenu)
        self.fmenu = Menu(self.menubar, tearoff=0)
        self.fmenu.add_command(label="hinzuf�gen", command=self.schulerhin)
        self.fmenu.add_command(label="�ndern", command=self.andern)
        self.menubar.add_cascade(label="Sch�ler", menu=self.fmenu)
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
        self.canvas = Canvas(self.rahmen[2], width=1000)
        self.frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.rahmen[2], orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.frame.bind("<Configure>", myfunction)

        self.rahmen[1].pack()
        self.rahmen[2].pack(side=LEFT)
        self.rahmen[11].pack(side=LEFT, fill=X)
        # self.rahmen12.pack(sie=LEFT, fill=X)

        self.b2=Button(text="Zuordnen")
        self.b2.place(x=10,y=260,width=600, height=30)

        self.v = IntVar()
        self.r1 = Radiobutton(self.rahmen[11], text="5", variable=self.v, value=1, command=self.callback_J5).pack(
            anchor=W, side=LEFT)
        self.r2 = Radiobutton(self.rahmen[11], text="6", variable=self.v, value=2, command=self.callback_J6).pack(
            anchor=W, side=LEFT)
        self.r3 = Radiobutton(self.rahmen[11], text="7", variable=self.v, value=3, command=self.callback_J7).pack(
            anchor=W, side=LEFT)
        self.r4 = Radiobutton(self.rahmen[11], text="8", variable=self.v, value=4, command=self.callback_J8).pack(
            anchor=W, side=LEFT)
        self.r5 = Radiobutton(self.rahmen[11], text="9", variable=self.v, value=5, command=self.callback_J9).pack(
            anchor=W, side=LEFT)
        self.r6 = Radiobutton(self.rahmen[11], text="10", variable=self.v, value=6, command=self.callback_J10).pack(
            anchor=W, side=LEFT)
        self.r7 = Radiobutton(self.rahmen[11], text="11", variable=self.v, value=7, command=self.callback_J11).pack(
            anchor=W, side=LEFT)
        self.r8 = Radiobutton(self.rahmen[11], text="12", variable=self.v, value=8, command=self.callback_J12).pack(
            anchor=W, side=LEFT)
        self.r9 = Radiobutton(self.rahmen[11], text="Alle", variable=self.v, value=9, command=self.callback_JA).pack(
            anchor=W, side=LEFT)

        self.zuord_but = Button(text="Zuordnen", command=self.callback_aus)
        self.zuord_but.place(x=10, y=260, width=600, height=30)

    def popup_textentry(self, text, call_ok, call_cancel):
        self.fenster.update({'popup': Tk()})
        self.fenster['popup'].title('Aktion erforderlich!')
        self.fenster['popup'].geometry("300x125")
        self.fenster['popup'].resizable(0, 0)
        self.labels.update({'popup': Label(self.fenster['popup'], text=text, font=('Arial', 13), wraplength=275)})
        self.entrys.update({'popup': Entry(self.fenster['popup'])})
        self.rahmen.update({'popup': Frame(self.fenster['popup'])})
        self.buttons.update({'popup_OK': Button(self.rahmen['popup'], text='Ok', command=call_ok, width=10)})
        self.buttons.update({'popup_Cancel': Button(self.rahmen['popup'], text='Cancel', command=call_cancel, width=10)})
        self.labels['popup'].pack(fill=X)
        self.entrys['popup'].pack(pady=15)
        self.rahmen['popup'].pack()
        self.buttons['popup_OK'].pack(side=LEFT)
        self.buttons['popup_Cancel'].pack(side=LEFT)

    def schulerhin(self):
        self.fenster.update({'hin': Tk()})
        self.fenster['neu'].title("Neue Sch�ler")
        self.fenster['neu'].geometry('780x110')
        for i in range(len(self.labelnames)):
            self.labels.update({self.labelnames[i]: Label(self.fenster['neu'], text=self.labelnames[i])})
            self.labels[self.labelnames[i]].place(x=10 + (110 * i), y=10, width=100)
        for i in range(len(self.labelnames)):
            self.entrys.update({i: Entry(self.fenster['neu'])})
            self.entrys[i].place(x=10 + (110 * i), y=40, width=100)
        self.buttons.update({'hin_B': Button(self.fenster['neu'], text="Sch�ler hinzuf�gen", command=self.callback_hin)})
        self.buttons['hin_B'].place(x=330, y=70, width=120, height=30)

    def andern(self):
        self.fenster.update({'ande': Tk()})
        self.fenster['ande'].title("Sch�ler �ndern")
        self.fenster['ande'].geometry('600x110')

        self.rahmen.update({'ande': Frame(self.fenster['ande'])})
        self.ande_v = IntVar()
        self.ande_r1 = Radiobutton(self.rahmen['ande'], text="Vorname", variable=self.ande_v, value=1,
                                   command=self.callback_a1).pack(anchor=W, side=LEFT)
        self.ande_r2 = Radiobutton(self.rahmen['ande'], text="Nachname", variable=self.ande_v, value=2,
                                   command=self.callback_a2).pack(anchor=W, side=LEFT)
        self.ande_r3 = Radiobutton(self.rahmen['ande'], text="Klasse", variable=self.ande_v, value=3,
                                   command=self.callback_a3).pack(anchor=W, side=LEFT)
        self.ande_r4 = Radiobutton(self.rahmen['ande'], text="Jahrgang", variable=self.ande_v, value=4,
                                   command=self.callback_a4).pack(anchor=W, side=LEFT)
        self.ande_r5 = Radiobutton(self.rahmen['ande'], text="Erst Wunsch", variable=self.ande_v, value=5,
                                   command=self.callback_a5).pack(anchor=W, side=LEFT)
        self.ande_r6 = Radiobutton(self.rahmen['ande'], text="Zweit Wunsch", variable=self.ande_v, value=6,
                                   command=self.callback_a6).pack(anchor=W, side=LEFT)
        self.ande_r7 = Radiobutton(self.rahmen['ande'], text="Dritt Wunsch", variable=self.ande_v, value=7,
                                   command=self.callback_a7).pack(anchor=W, side=LEFT)

        self.labels.update({'ande_Lab': Label(self.fenster['ande'], text="sID")})
        self.labels['ande_Lab'].place(x=10, y=20, width=30)

        self.entrys.update({'ande_Eaktuell': Entry(self.fenster['ande'])})
        self.entrys['ande_Eaktuell'].place(x=10, y=40, width=30)
        self.entrys.update({'ande_Eandern': Entry(self.fenster['ande'])})
        self.entrys['ande_Eandern'].place(x=50, y=40, width=540)

        self.buttons.update({'ande_B': Button(self.fenster['ande'], text="�ndern", command=self.callback_ande)})
        self.buttons['ande_B'].place(x=10, y=70, width=580, height=30)

        self.rahmen['ande'].pack(side=LEFT, fill=X)


class Controller(object):
    def __init__(self):
        self.model = Model()
        self.view = View(self.importieren, self.exportieren, self.beenden, self.J5, self.J6, self.J7, self.J8, self.J9,
                         self.J10, self.J11, self.J12, self.JA, self.hinzufugen, self.model.auswahl, self.ande, self.J5,
                         self.J6, self.J7, self.J8, self.J9, self.J10, self.J11)
        self.delimiter = None
        self.slcsv = None
        self.plcsv = None

        if os.path.exists('projektliste.csv') and os.path.exists('schuelerliste.csv'):
            self.model.importCSV('schuelerliste.csv', 'projektliste.csv')
        self.tabelle()
        self.view.b2.config(command=lambda: self.b2command())

    def b2command(self):
        self.model.auswahl()
        self.tabelleanpassen()

    def delimOK(self):
        self.delimiter = self.view.txt_Ent.get()
        if self.delimiter == '':
            showwarning('Angabe ung�ltig', 'Das angegebene Trennzeichen ist ung�ltig oder es wurde keines Angegeben!'
                                           '\nBitte Geben Sie ein anderes Trennzeichen ein!')
            self.fenster_zerst�ren(self.view.popup)
            self.delimiterFester()
        else:
            self.fenster_zerst�ren(self.view.popup)
            self.model.importCSV(self.slcsv, self.plcsv, self.delimiter)
            self.delimiter = None

    def delimCanc(self):
        self.fenster_zerst�ren(self.view.popup)

    def delimiterFester(self):
        self.view.popup_textentry('Bitte giben sie das Trennzeichen der CSV-Datei an:', self.delimOK, self.delimCanc)

    def importieren(self):
        slcsv = filedialog.askopenfilename(title="Sch�lerliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        plcsv = filedialog.askopenfilename(title="Projektliste importieren",
                                           filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        self.model.importCSV(slcsv, plcsv)
        self.tabelle()

    def exportieren(self):
        slcsv = filedialog.asksaveasfile(mode='w', title='Sch�lerliste exportieren', defaultextension=".csv",
                                         initialfile='schuelerl_fertig',
                                         filetypes=(("CSV Datei", "*.csv"), ("Txt Datei", "*.txt"),
                                                    ("all files", "*.*")))
        if slcsv is not None:
            plcsv = filedialog.asksaveasfile(mode='w', title='Projektliste exportieren', defaultextension=".csv",
                                             initialfile='projektel_fertig',
                                             filetypes=(("CSV Datei", "*.csv"), ("Txt Datei", "*.txt"),
                                                        ("all files", "*.*")))
            if plcsv is not None:
                self.model.exportCSV(slcsv, plcsv)
        else:
            showinfo('Exportiert', "Die Tabellen wurden in zwei CSV-Dateien mit ';' als Trennzeichen ausgegeben!")

    def beenden(self):
        x = askokcancel(title='Beenden',
                        message='M�chtest du das Programm wirklich beenden?'
                                '\nNicht abgeschlossene Aktionen k�nnten zu fehlern f�hren!')
        if x:
            self.fenster_zerst�ren(self.view)

    def tabelle(self):
        x = self.model.ausgabe("schueler")
        for i in range(len(x)):
            for j in range(len(x[0])):
                self.b = Label(self.view.frame, text=str(x[i][j]))
                self.b.grid(row=i, column=j)

    def myfunction(self,event):
            self.view.canvas.configure(scrollregion=self.view.canvas.bbox("all"))
    def tabelleanpassen(self):
        self.view.canvas.destroy()

        self.view.canvas=Canvas(self.view.rahmen2,width=1000)
        self.view.frame=Frame(self.view.canvas)
        self.view.scrollbar.config(command=self.view.canvas.yview)
        self.view.canvas.configure(yscrollcommand=self.view.scrollbar.set)

        self.view.scrollbar.pack(side="right",fill="y")
        self.view.canvas.pack(side="left")
        self.view.canvas.create_window((0,0),window=self.view.frame,anchor='nw')
        self.view.frame.bind("<Configure>",self.myfunction)

        x = self.model.ausgabe("schueler")
        for i in range(len(x)):
            for j in range(len(x[0])):
                self.b = Label(self.view.frame, text=str(x[i][j]))
                self.b.grid(row=i, column=j)

    def hinzufugen(self):
        for entry in self.view.entrys:
            self.view.entrys[entry].config(bg='white')
        erst = self.view.entrys[4].get()
        zweit = self.view.entrys[5].get()
        dritt = self.view.entrys[6].get()
        if dritt == "":
            dritt = "33"
        if zweit == "":
            zweit = "33"
        if erst == "":
            erst = "33"
        if self.view.entrys[0].get() != "" and self.view.entrys[1].get() != "" and \
                self.view.entrys[2].get() != "" and self.view.entrys[3].get() != "":
            self.model.einfuegen('schueler', ('sName', 'sVName', 'sJahrg', 'sKla', 'sErst', 'sZweit', 'sDritt'),
                                 (self.view.entrys[1].get(), self.view.entrys[0].get(),
                                  self.view.entrys[2].get(), self.view.entrys[3].get(), erst, zweit, dritt))
            self.view.ro_botton.config(bg="green")
            for entry in self.view.entrys:
                entry.delete(0, 'end')
        else:
            self.view.ro_botton.config(bg="red")
            for i in range(4):
                if self.view.entrys[i].get() == "":
                    self.view.entrys[i].config(bg='red')
        self.view.update()
        time.sleep(0.1)
        self.view.ro_botton.config(bg="white")
        self.tabelle()

    def ande(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

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

    def JA(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')

    def fenster_zerst�ren(self, fenster):
        fenster.destroy()

c = Controller()
c.view.mainloop()
