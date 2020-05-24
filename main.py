# -*- coding: utf-8 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Schüler zu Projekten

import csv, os, random, time
import sqlite3 as sqli
from tkinter import *
from tkinter import filedialog  # muss aus unbekannten Gründen extra importiert werden
from tkinter.messagebox import *
from tkinter.ttk import *
import ttkthemes


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

        sql = "CREATE TABLE schueler(sID INTEGER PRIMARY KEY, sVName TEXT, sName TEXT, sJahrg INTEGER, sKla INTEGER, " \
              "sErst INTEGER, sZweit INTEGER, sDritt INTEGER, sZu INTEGER); "
        cursor.execute(sql)

        connection.commit()
        connection.close()

    def importCSV(self, slcsv, plcsv, delis, delip):  # sl = schuelerliste, pl = projektliste
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        # importieren der slcsv Datei
        file = open(slcsv, 'r')
        read = csv.reader(file, delimiter=delis)
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

        # importieren der plcsv Datei
        file = open(plcsv, 'r')
        read = csv.reader(file, delimiter=";")
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

    def exportCSV(self, slcsv, plcsv, delimiter):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        # auslesen der datenbankliste schueler in eine CSV-Datei
        slcsv = open(slcsv, 'w', newline='')
        slfile = csv.writer(slcsv, delimiter=delimiter, quoting=csv.QUOTE_NONE)
        sql = "SELECT * FROM schueler;"
        cur.execute(sql)
        dboutput = cur.fetchall()
        for spalte in dboutput:
            spalte = list(spalte)
            del spalte[0]
            for i in range(2):
                err = spalte[i].find(';')
                if err != -1:
                    spalte[i] = spalte[i].replace(';', ',')
            slfile.writerow(spalte)

        # auslesen der datenbankliste projekte in eine CSV-Datei
        plcsv = open(plcsv, 'w', newline='')
        plfile = csv.writer(plcsv, delimiter=delimiter, quoting=csv.QUOTE_NONE)
        sql = "SELECT * FROM projekte;"
        cur.execute(sql)
        dboutput = cur.fetchall()
        for spalte in dboutput:
            spalte = list(spalte)
            del spalte[0]
            err = spalte[0].find(';')
            if err != -1:
                spalte[0] = spalte[0].replace(';', ',')
            plfile.writerow(spalte)
        con.close()

    def zuordnen(self, wahl):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()
        jahrg = 4  # Jahrgang
        while jahrg <= 11:
            jahrg += 1
            b = 1  # Projekt
            sql = "select max(pNum) FROM projekte WHERE '" + str(
                jahrg) + "' like pJahrg;"  # max Projektnummer wird ermittelt
            cur.execute(sql)
            x = cur.fetchall()  # max Projektnummer
            xx = x[0][0]
            if xx is None:
                xx = 0
            while b <= xx:
                liste = []
                sql = "select max(sID) FROM schueler WHERE '" + str(jahrg) + "' like sJahrg and '" + str(
                    b) + "' like " + wahl + " and sZu is NULL;"  # max sID wird ermittelt
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
                    sql = "select count(sID) FROM schueler WHERE '" + str(jahrg) + "' like sJahrg and '" + str(
                        b) + "' like sZu;"
                    cur.execute(sql)
                    maxanz1 = cur.fetchall()
                    if maxanz1:
                        maxanz = maxanz0[0][0] - maxanz1[0][0]
                    else:
                        maxanz = maxanz0[0][0]
                else:
                    maxanz = 0
                if maxanz > 0:
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
        con.commit()
        con.close()

    def restzuordnung(self):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

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
            if len(schuler) != 0 and len(projekte) == 0:
                showwarning('Fehler', 'Im ' + str(jahrg) + '. Jahrgang gibt es mehr Schüler als Plätze in den Kursen.')

        con.commit()
        con.close()

    def einfuegen(self, tabelle, spalten_namen_tuple, value_tuple):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()
        sql = "SELECT count(*) FROM " + tabelle + " WHERE "
        for i, e in enumerate(value_tuple):
            if i < len(value_tuple) - 1:
                sql += spalten_namen_tuple[i] + " = '" + e + "' AND "
            else:
                sql += spalten_namen_tuple[i] + " = '" + e + "';"
        cur.execute(sql)
        erg = cur.fetchall()
        if not erg[0][0]:
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
            cur.execute(sql)
            con.commit()
            con.close()
            return True
        else:
            showerror('Fehler', 'Schüler bereits vorhanden!')
            con.commit()
            con.close()
            return False

    def ausgabe(self, tabelle):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        sql = "SELECT * FROM " + tabelle + ";"
        cur.execute(sql)
        erg = cur.fetchall()

        con.close()
        return erg

    def jahrgsuch(self, jahrgang):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        sql = "SELECT * FROM schueler WHERE sJahrg LIKE '" + str(
            jahrgang) + "'"
        cur.execute(sql)
        erg = cur.fetchall()

        con.close()
        return erg

    def ausfuhren(self, sql):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        cur.execute(sql)
        erg = cur.fetchall()

        con.close()
        return erg


class View(ttkthemes.ThemedTk):
    def __init__(self, imp, exp, bee, j5, j6, j7, j8, j9, j10, j11, j12, ja, hin, zord, ande, a1, a2, a3, a4, a5, a6,
                 a7):
        # print(ttkthemes.THEMES)
        ttkthemes.ThemedTk.__init__(self, theme='breeze')
        self.title("Projektwochenverwaltungsprogramm")
        self.geometry('800x285')
        self.maxsize(800, 285)
        self.minsize(800, 285)
        # bestimmen der Callbacks
        self.callback_imp = imp
        self.callback_exp = exp
        self.callback_bee = bee
        self.radiocom = {'jahrg': [j5, j6, j7, j8, j9, j10, j11, j12, ja], 'ande': [a1, a2, a3, a4, a5, a6, a7]}
        self.callback_zord = zord
        self.callback_hin = hin
        self.callback_ande = ande
        self.names = {'schueler': ("Vorname", "Nachname", "Jahrg", "Klasse", "Erst Wunsch", "Zweit Wunsch",
                                   "Dritt Wunsch"),
                      'jahrg': ('5', '6', '7', '8', '9', '10', '11', '12', 'Alle')}
        self.labels = {}
        self.entrys = {}
        self.buttons = {}
        self.vars = {'jahrg': IntVar(), 'ande': IntVar()}
        self.radios = {}
        self.rahmen = {1: Frame(master=self), 2: Frame(master=self)}
        self.rahmen.update({11: Frame(master=self.rahmen[1])})
        self.fenster = {}

        # erstellen des Menüs
        self.menu = {'main': Menu(self)}
        self.menu['file'] = Menu(self.menu['main'], tearoff=0)
        self.menu['file'].add_command(label="importieren", command=self.callback_imp)
        self.menu['file'].add_command(label="exportieren", command=self.callback_exp)
        self.menu['file'].add_separator()
        self.menu['file'].add_command(label="Beenden", command=self.callback_bee)
        self.menu['main'].add_cascade(label="Datei", menu=self.menu['file'])
        self.menu['schueler'] = Menu(self.menu['main'], tearoff=0)
        self.menu['schueler'].add_command(label="hinzufügen", command=self.schulerhin)
        self.menu['schueler'].add_command(label="ändern", command=self.schuelerandern)
        self.menu['main'].add_cascade(label="Schüler", menu=self.menu['schueler'])
        self.menu['tools'] = Menu(self.menu['main'], tearoff=0)
        self.menu['tools'].add_command(label="Schüler Projekten zuordnen", command=self.callback_zord)
        self.menu['main'].add_cascade(label="Tools", menu=self.menu['tools'])
        self.config(menu=self.menu['main'])

        for i in range(len(self.names['jahrg'])):
            self.radios['jahrg-' + self.names['jahrg'][i]] = Radiobutton(self.rahmen[11], text=self.names['jahrg'][i],
                                                                         variable=self.vars['jahrg'], value=i,
                                                                         command=self.radiocom['jahrg'][i])
            self.radios['jahrg-' + self.names['jahrg'][i]].pack(side=LEFT)
        self.radios['jahrg-Alle'].invoke()

        # Tabelle
        self.scrollbar = Scrollbar(self.rahmen[2], orient="vertical")
        self.table = Treeview(self.rahmen[2], yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.rahmen[1].pack()
        self.rahmen[2].pack(fill=X)
        self.rahmen[11].pack(side=LEFT, fill=X)

    def popup_textentry(self, text, call_ok, call_cancel):
        self.fenster['popup'] = Tk()
        self.fenster['popup'].title('Aktion erforderlich!')
        self.fenster['popup'].geometry("300x125")
        self.fenster['popup'].resizable(0, 0)
        self.labels['popup'] = Label(self.fenster['popup'], text=text, font=('Arial', 13), wraplength=275)
        self.entrys['popup'] = Entry(self.fenster['popup'])
        self.rahmen['popup'] = Frame(self.fenster['popup'])
        self.buttons['popup_OK'] = Button(self.rahmen['popup'], text='Ok', command=call_ok, width=10)
        self.buttons['popup_Cancel'] = Button(self.rahmen['popup'], text='Cancel', command=call_cancel, width=10)
        self.labels['popup'].pack(fill=X)
        self.entrys['popup'].pack(pady=15)
        self.rahmen['popup'].pack()
        self.buttons['popup_OK'].pack(side=LEFT)
        self.buttons['popup_Cancel'].pack(side=LEFT)

    def popup_Progressbar(self):
        self.fenster['popup'] = Tk()
        self.fenster['popup'].title('In Bearbeitung!')
        self.fenster['popup'].resizable(0, 0)
        self.labels['popup'] = Progressbar(self.fenster['popup'], orient='horizontal', length=250, mode='determinate')
        self.labels['popup'].pack()

    def schulerhin(self):
        self.fenster['hin'] = Tk()
        self.fenster['hin'].title("Neue Schüler")
        self.fenster['hin'].geometry('780x110')
        for i in range(len(self.names['schueler'])):
            self.labels[self.names['schueler'][i]] = Label(self.fenster['hin'], text=self.names['schueler'][i])
            self.labels[self.names['schueler'][i]].place(x=10 + (110 * i), y=10, width=100)
        for i in range(len(self.names['schueler'])):
            self.entrys[i] = Entry(self.fenster['hin'])
            self.entrys[i].place(x=10 + (110 * i), y=40, width=100)
        self.buttons['hin'] = Button(self.fenster['hin'], text="Schüler hinzufügen", command=self.callback_hin)
        self.buttons['hin'].place(x=330, y=70, width=120, height=30)

    def schuelerandern(self):
        try:
            self.fenster['ande'].destroy()
        except TclError:
            pass
        self.fenster.update({'ande': Tk()})
        self.fenster['ande'].title("Schüler ändern")
        self.fenster['ande'].geometry('725x110')

        self.rahmen['ande'] = Frame(self.fenster['ande'])

        self.rahmen['ande_ID'] = Frame(self.rahmen['ande'])
        self.labels['ande_idLab'] = Label(self.rahmen['ande_ID'], text="ID")
        self.labels['ande_idLab'].pack(fill=X, pady=2)
        self.entrys['ande_Eid'] = Entry(self.rahmen['ande_ID'])
        self.entrys['ande_Eid'].pack(side=LEFT)
        self.rahmen['ande_ID'].pack(side=LEFT)

        self.rahmen['ande_change'] = Frame(self.rahmen['ande'])

        self.rahmen['ande_r'] = Frame(self.rahmen['ande_change'])
        for i in range(len(self.names['schueler'])):
            self.radios['ande-' + self.names['schueler'][i]] = Radiobutton(self.rahmen['ande_r'],
                                                                           text=self.names['schueler'][i],
                                                                           variable=self.vars['ande'], value=i,
                                                                           command=self.radiocom['ande'][i])
            self.radios['ande-' + self.names['schueler'][i]].pack(side=LEFT, fill=X)
        self.radios['ande-Vorname'].invoke()
        self.rahmen['ande_r'].pack(fill=X)

        self.rahmen['ande_e'] = Frame(self.rahmen['ande_change'])
        self.entrys['ande_Eandern'] = Entry(self.rahmen['ande_e'])
        self.entrys['ande_Eandern'].pack(fill=X)
        self.rahmen['ande_e'].pack(fill=X)
        self.rahmen['ande_change'].pack(fill=X, padx=4, pady=2)

        self.rahmen['ande'].pack(fill=X, padx=6, pady=6)

        self.buttons['ande_B'] = Button(self.fenster['ande'], text="ändern", command=self.callback_ande)
        self.buttons['ande_B'].pack(fill=X, padx=8, pady=6)


class Controller(object):
    def __init__(self):
        self.model = Model()
        self.view = View(self.importieren, self.exportieren, self.beenden, self.J5, self.J6, self.J7, self.J8, self.J9,
                         self.J10, self.J11, self.J12, self.tabelle_update, self.hinzufugen, self.zuordnen, self.ande,
                         self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7)
        self.wahlen = ('sErst', 'sZweit', 'sDritt')
        self.delimiter = {'imp_s': None, 'imp_p': None, 'exp': None}
        self.dchosen = None
        self.slcsv = 'schuelerliste.csv'
        self.plcsv = 'projektliste.csv'
        self.andernx = ""
        self.tabelle()
        self.view.table.bind('<Double-Button-1>', self.treevent)
        self.warten = False

        if os.path.exists('projektliste.csv') and os.path.exists('schuelerliste.csv') \
                and not self.model.ausfuhren('SELECT * FROM schueler') \
                and not self.model.ausfuhren('SELECT * FROM projekte'):
            if askokcancel('Auto-import',
                           'Es wurden passende CSV-Dateien gefunden, wollen Sie diese jetzt importieren?'):
                self.importieren()

        self.view.mainloop()

    def treevent(self, event):
        if self.view.table.identify_region(event.x, event.y) == 'cell':
            self.view.schuelerandern()
            self.view.entrys['ande_Eid'].insert(0, event.widget.selection()[0])

    def zuordnen(self):
        if not self.warten:
            self.warten = True
            self.view.popup_Progressbar()
            self.view.fenster['popup'].update()
            for wahl in self.wahlen:
                self.model.zuordnen(wahl)
                self.view.labels['popup'].step(30)
                self.view.fenster['popup'].update()
            self.model.restzuordnung()
            self.view.labels['popup'].step(9.9999999999)
            self.view.fenster['popup'].update()
            time.sleep(0.5)
            self.tabelle_update()
            self.view.fenster['popup'].destroy()
            self.warten = False

    def delimOK(self):
        if isinstance(self.dchosen, tuple):
            for d in self.dchosen:
                self.delimiter[d] = self.view.entrys['popup'].get()
        else:
            self.delimiter[self.dchosen] = self.view.entrys['popup'].get()
        if self.delimiter == '' or len(self.delimiter[self.dchosen]) != 1:
            showwarning('Angabe ungültig', 'Das angegebene Trennzeichen ist ungültig oder es wurde keines Angegeben!'
                                           '\nBitte Geben Sie ein anderes Trennzeichen ein!')
            self.view.fenster['popup'].destroy()
            self.delimiterFester(None)
        else:
            self.view.fenster['popup'].destroy()
            self.dchosen = None

    def delimCanc(self):
        self.view.fenster['popup'].destroy()

    def delimiterFester(self, d):
        if isinstance(d, tuple):
            self.dchosen = list(self.delimiter.keys())[d[0]], list(self.delimiter.keys())[d[1]]
        elif self.dchosen is None:
            self.dchosen = list(self.delimiter.keys())[d]
        if d == 0:
            self.view.popup_textentry('Bitte geben Sie das Trennzeichen der Schuelerlisten CSV-Datei an:', self.delimOK,
                                      self.delimCanc)
        if d == 1:
            self.view.popup_textentry('Bitte geben Sie das Trennzeichen der Projektlisten CSV-Datei an:', self.delimOK,
                                      self.delimCanc)
        if d == 2:
            self.view.popup_textentry('Bitte geben Sie das Trennzeichen der CSV-Dateien an:', self.delimOK,
                                      self.delimCanc)
        while self.dchosen is not None:
            try:
                self.view.fenster['popup'].update()
            except TclError:
                return False
        return True

    def importieren(self):
        if not bool(self.model.ausgabe('schueler')):
            pass
        elif askyesno('Bereits importiert', 'Es sind bereits CSV-Dateien importiert, wollen sie diese wirklich '
                                            'überschreiben?'):
            pass
        else:
            return
        if not isinstance(self.slcsv, str):
            self.slcsv = filedialog.askopenfilename(title="Schülerliste importieren",
                                                    filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
            if bool(self.slcsv):  # keine Ausgabe von None bei askopenfile, deswegen als bool interpretieren
                # (nichts=False)
                self.plcsv = filedialog.askopenfilename(title="Projektliste importieren",
                                                        filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        if (self.delimiter['imp_s'], self.delimiter['imp_p']) == (None, None) and bool(self.plcsv):
            if self.delimiterFester(0) and self.delimiterFester(1):
                self.model.importCSV(self.slcsv, self.plcsv, self.delimiter['imp_s'], self.delimiter['imp_p'])
                showinfo('Importiert', 'Die CSV Dateien wurden importiert!')
        if not bool(self.view.table.get_children()):
            self.tabelle()
        else:
            self.tabelle_update()

    def exportieren(self):
        slcsv = filedialog.asksaveasfilename(title='Schülerliste exportieren', defaultextension=".csv",
                                             initialfile='schuelerl_fertig',
                                             filetypes=(("CSV Datei", "*.csv"), ("Txt Datei", "*.txt"),
                                                        ("all files", "*.*")))
        if slcsv is not None:
            plcsv = filedialog.asksaveasfilename(title='Projektliste exportieren', defaultextension=".csv",
                                                 initialfile='projektel_fertig',
                                                 filetypes=(("CSV Datei", "*.csv"), ("Txt Datei", "*.txt"),
                                                            ("all files", "*.*")))
            if plcsv is not None:
                if self.delimiterFester(2):
                    self.model.exportCSV(slcsv, plcsv, self.delimiter['exp'])
                    showinfo('Exportiert', "Die Tabellen wurden in zwei CSV-Dateien mit '" + self.delimiter['exp'] +
                             "' als Trennzeichen ausgegeben!")

    def beenden(self):
        x = askokcancel(title='Beenden',
                        message='Möchtest du das Programm wirklich beenden?'
                                '\nNicht abgeschlossene Aktionen könnten zu fehlern führen!')
        if x:
            self.view.destroy()

    def tabelle(self, fetch=None):
        if fetch is None:
            fetch = self.model.ausgabe('schueler')
        width = [35, 75, 75, 50, 50, 100, 100, 100, 75]
        ml = ['ID']
        for namen in self.view.names['schueler']:
            ml.append(namen)
        ml.append('Zugeordned zu')
        self.view.table['columns'] = ml
        self.view.table['show'] = 'headings'
        for i in range(len(ml)):
            self.view.table.column(ml[i], width=width[i], minwidth=width[i])
        for i in range(len(ml)):
            self.view.table.heading(ml[i], text=ml[i], command=lambda col=i: self.tabelle_sorti(col, False))
        for t in fetch:
            self.view.table.insert('', t[0], t[0], values=t)
        self.view.scrollbar.config(command=self.view.table.yview)
        self.view.table.pack(fill=X)

    def tabelle_update(self, fetch=None):
        try:
            self.view.table.delete(*self.view.table.get_children())
            if fetch is None:
                fetch = self.model.ausgabe('schueler')
            for t in fetch:
                self.view.table.insert('', t[0], t[0], values=t)
        except AttributeError:
            pass

    def tabelle_sorti(self, col, descending):
        data = [(self.view.table.set(tvindex, col), tvindex) for tvindex in self.view.table.get_children('')]

        try:
            data = [(float(element), tvindex) for element, tvindex in data]
        except ValueError:
            pass

        data.sort(reverse=descending)

        for index, (val, k) in enumerate(data):
            self.view.table.move(k, '', index)

        # reverse sort next time
        self.view.table.heading(col, command=lambda: self.tabelle_sorti(col, not descending))

    def hinzufugen(self):
        for entry in range(7):
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
            if self.model.einfuegen('schueler', ('sName', 'sVName', 'sJahrg', 'sKla', 'sErst', 'sZweit', 'sDritt'),
                                    (self.view.entrys[1].get(), self.view.entrys[0].get(), self.view.entrys[2].get(),
                                     self.view.entrys[3].get(), erst, zweit, dritt)):
                for entry in range(7):
                    self.view.entrys[entry].delete(0, END)
                self.view.buttons['hin'].config(bg="green")
            for entry in range(7):
                self.view.entrys[entry].delete(0, END)
                self.view.entrys[entry].config(bg='white')
        else:
            self.view.buttons['hin'].config(bg="red")
            for i in range(4):
                self.view.entrys[i].config(bg='white')
                if self.view.entrys[i].get() == "":
                    self.view.entrys[i].config(bg='red')
        self.view.update()
        time.sleep(0.3)
        self.view.buttons['hin'].config(bg="SystemButtonFace")
        self.tabelle_update()

    def ande(self):
        if self.andernx != "" and self.view.entrys['ande_Eid'].get() != "":
            connection = sqli.connect('pwvwp.db')
            cursor = connection.cursor()
            sql = "update schueler set " + self.andernx + "='" + str(
                self.view.entrys['ande_Eandern'].get()) + "' where sID " \
                                                          "like '" + str(
                self.view.entrys['ande_Eid'].get()) + "';"
            cursor.execute(sql)
            connection.commit()
            connection.close()
            self.tabelle_update()
            self.view.fenster['ande'].destroy()

    def J5(self):
        self.tabelle_update(self.model.jahrgsuch(5))

    def J6(self):
        self.tabelle_update(self.model.jahrgsuch(6))

    def J7(self):
        self.tabelle_update(self.model.jahrgsuch(7))

    def J8(self):
        self.tabelle_update(self.model.jahrgsuch(8))

    def J9(self):
        self.tabelle_update(self.model.jahrgsuch(9))

    def J10(self):
        self.tabelle_update(self.model.jahrgsuch(10))

    def J11(self):
        self.tabelle_update(self.model.jahrgsuch(11))

    def J12(self):
        self.tabelle_update(self.model.jahrgsuch(12))

    def a1(self):
        self.andernx = "sVName"

    def a2(self):
        self.andernx = "sName"

    def a3(self):
        self.andernx = "sJahrg"

    def a4(self):
        self.andernx = "sKla"

    def a5(self):
        self.andernx = "sErst"

    def a6(self):
        self.andernx = "sZweit"

    def a7(self):
        self.andernx = "sDritt"

    def unreif(self):
        showwarning('Noch nicht ausgereift', 'Dieser Teil wurde noch nicht Programmiert')


c = Controller()
