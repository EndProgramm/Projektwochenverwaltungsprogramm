# -*- coding: utf-8 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Schüler zu Projekten

import os, time
from Model import *
from View import *
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog  # muss aus unbekannten Gründen extra importiert werden


class Controller(object):
    def __init__(self):
        self.model = Model()
        self.view = View(self.importieren, self.exportieren, self.beenden, self.J5, self.J6, self.J7, self.J8, self.J9,
                         self.J10, self.J11, self.J12, self.tabelle_update, self.tabelle_sorti, self.hinzufugen,
                         self.zuordnen, self.ande, self.tabelle_update, self.model.ausgabe('projekte'), self.a1,
                         self.a2, self.a3, self.a4, self.a5, self.a6, self.a7)
        self.popup = None
        self.wahlen = ('sErst', 'sZweit', 'sDritt')
        self.delimiter = {'imp_s': None, 'imp_p': None, 'exp': None}
        self.dchosen = None
        self.slcsv = 'schuelerliste.csv'
        self.plcsv = 'projektliste.csv'
        self.double = False
        self.andernx = ""

        self.tabelle()
        self.view.table.bind('<Double-Button-1>', self.treevent)
        # Erstimportierung
        if self.model.ausgabe('schueler'):
            self.importieren(True)

        self.view.mainloop()

    def treevent(self, event):
        if self.view.table.identify_region(event.x, event.y) == 'cell':
            self.view.schuelerandern()
            self.view.entrys['ande_Eid'].insert(0, event.widget.selection()[0])

    def zuordnen(self):
        if not self.double:
            self.double = True
            self.popup = Popup()
            self.popup.progressbar()
            for wahl in self.wahlen:
                self.model.zuordnen(wahl)
                self.popup.label.step(30)
                self.popup.update()
            erg = self.model.restzuordnung()
            if erg[0]:
                showwarning('Fehler', 'In dem Jahrgang/den Jahrgängen ' + str(
                    erg[1]) + ' gibt es mehr Schüler als Plätze in den Kursen.')
            self.popup.label.step(10)
            self.popup.update()
            time.sleep(0.5)
            self.tabelle_update()
            self.popup.destroy()
            self.double = False
        else:
            showwarning('Doppelte Operation',
                        'Es wird bereits eine Zuordnung durchgeführt, bitte warten Sie bis zur Vollendung dieser, bis Sie die nächste ausführen')

    def delimOK(self):
        if isinstance(self.dchosen, tuple):
            for d in self.dchosen:
                self.delimiter[d] = self.popup.entry.get()
        else:
            self.delimiter[self.dchosen] = self.popup.entry.get()
        if self.delimiter == '' or len(self.delimiter[self.dchosen]) != 1:
            showwarning('Angabe ungültig', 'Das angegebene Trennzeichen ist ungültig oder es wurde keines Angegeben!'
                                           '\nBitte Geben Sie ein anderes Trennzeichen ein!')
            self.delimiterFester(None)
        else:
            self.popup.destroy()
            self.dchosen = None

    def delimCanc(self):
        self.popup.destroy()

    def delimiterFester(self, d):
        self.popup = Popup()
        if isinstance(d, tuple):
            self.dchosen = list(self.delimiter.keys())[d[0]], list(self.delimiter.keys())[d[1]]
        elif self.dchosen is None:
            self.dchosen = list(self.delimiter.keys())[d]
        if d == 0:
            self.popup.textentry('Bitte geben Sie das Trennzeichen der Schuelerlisten CSV-Datei an:', self.delimOK,
                                 self.delimCanc)
        if d == 1:
            self.popup.textentry('Bitte geben Sie das Trennzeichen der Projektlisten CSV-Datei an:', self.delimOK,
                                 self.delimCanc)
        if d == 2:
            self.popup.textentry('Bitte geben Sie das Trennzeichen der CSV-Dateien an:', self.delimOK,
                                 self.delimCanc)
        while self.dchosen is not None:
            try:
                self.popup.update()
            except TclError:
                return False
        return True

    def autoimport(self):
        if os.path.exists('projektliste.csv') and os.path.exists('schuelerliste.csv') and askokcancel('Auto-import',
                                                                                                      'Es wurden passende CSV-Dateien gefunden, wollen Sie diese jetzt importieren?'):
            self.slcsv = 'schuelerliste.csv'
            self.plcsv = 'projektliste.csv'
        else:
            self.slcsv = ''
            self.plcsv = ''

    def csvimport(self):
        if self.plcsv != "" and self.delimiterFester(0) and self.delimiterFester(1) and \
                self.model.importCSV(self.slcsv, self.plcsv, self.delimiter['imp_s'], self.delimiter['imp_p']):
            showwarning('Fehler', 'Falscher Delimiter oder falsches Tabellenformat')
            self.csvimport()
        else:
            showinfo('Importiert', 'Die CSV Dateien wurden importiert!')

    def importieren(self, erstes=False):
        if not bool(self.model.ausgabe('schueler')):
            self.autoimport()

        elif not erstes and askyesno('Bereits importiert', 'Es sind bereits CSV-Dateien importiert, wollen sie diese '
                                                           'überschreiben?'):
            self.model.clearDB()
            self.model.createDB()
            self.autoimport()
        else:
            return
        if self.slcsv == "":
            self.slcsv = filedialog.askopenfilename(title="Schülerliste importieren",
                                                    filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
            if self.slcsv != "":
                self.plcsv = filedialog.askopenfilename(title="Projektliste importieren",
                                                        filetypes=(("CSV Datei", "*.csv"), ("all files", "*.*")))
        self.csvimport()

        if not bool(self.view.table.get_children()):
            self.tabelle()
        else:
            self.tabelle_update()

    def exportieren(self):
        slcsv = filedialog.asksaveasfilename(title='Schülerliste exportieren', defaultextension=".csv",
                                             initialfile='schuelerl_fertig',
                                             filetypes=(("CSV Datei", "*.csv"), ("Txt Datei", "*.txt"),
                                                        ("all files", "*.*")))
        if slcsv is not '':
            plcsv = filedialog.asksaveasfilename(title='Projektliste exportieren', defaultextension=".csv",
                                                 initialfile='projektel_fertig',
                                                 filetypes=(("CSV Datei", "*.csv"), ("Txt Datei", "*.txt"),
                                                            ("all files", "*.*")))
            if plcsv is not '':
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
        self.view.tabelle(fetch)

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
            self.view.entrys[entry].config(background='white')
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
                self.view.buttons['hin'].configure('confirm')
            else:
                showerror('Fehler', 'Schüler bereits vorhanden!')
            for entry in range(7):
                self.view.entrys[entry].delete(0, END)
                self.view.entrys[entry].configure('default')
        else:
            self.view.buttons['hin'].configure('error')
            for i in range(4):
                self.view.entrys[i].configure('default')
                if self.view.entrys[i].get() == "":
                    self.view.entrys[i].configure('error')
        self.view.update()
        time.sleep(0.3)
        self.view.buttons['hin'].configure('default')
        self.tabelle_update()

    def ande(self):
        if self.andernx != "" and self.view.entrys['ande_Eid'].get() != "":
            self.model.ande(self.andernx, self.view.entrys['ande_Eandern'].get(), self.view.entrys['ande_Eid'].get())
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
