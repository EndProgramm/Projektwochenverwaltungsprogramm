# -*- coding: utf-8 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Schüler zu Projekten

import time, os
from tkinter import filedialog  # muss aus unbekannten Gründen extra importiert werden
from tkinter.messagebox import *

from Model import *
from View import *


class Controller(object):
    def __init__(self):
        self.model = Model()
        self.view = View(self.run, self.importieren, self.exportieren, self.beenden, self.J5, self.J6, self.J7, self.J8,
                         self.J9,
                         self.J10, self.J11, self.J12, self.tabellen_update, self.tabelle_sorti, self.hinzufugen,
                         self.zuordnen, self.ande, self.tabellen_update, self.tabelle_prj,
                         self.tabellen_update, self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7)
        self.wahlen = ('sErst', 'sZweit', 'sDritt')
        self.delimiter = {'imp_s': None, 'imp_p': None, 'exp': None}
        self.dchosen = None
        self.slcsv = 'schuelerliste.csv'
        self.plcsv = 'projektliste.csv'
        self.double = False
        self.andernx = ""

        self.view.radios['jahrg-Alle'].invoke()
        self.tabelle()
        self.view.table['main'].bind('<Double-Button-1>', self.treevent)
        # Erstimportierung
        if self.model.ausgabe('schueler'):
            self.importieren(True)

        self.view.mainloop()

    def treevent(self, event):
        if self.view.table['main'].identify_region(event.x, event.y) == 'cell':
            self.view.schuelerandern()
            self.view.entrys['ande_Eid'].insert(0, event.widget.selection()[0])

    def zuordnen(self):
        if not self.double:
            self.double = True
            self.view.progressbar()
            self.view.labels['popup_pro'].step(9)

            for wahl in self.wahlen:
                self.model.zuordnen(wahl)
                self.view.labels['popup_pro'].step(30)
                self.view.update()
            erg = self.model.restzuordnung()
            if erg[0]:
                showwarning('Fehler', 'In dem Jahrgang/den Jahrgängen ' + str(
                    erg[1]) + ' gibt es mehr Schüler als Plätze in den Kursen.')
            self.view.labels['popup_pro'].step(1)
            self.view.update()
            time.sleep(0.5)
            self.tabellen_update()
            self.view.labels['popup_pro'].pack_forget()
            self.double = False
        else:
            showwarning('Doppelte Operation',
                        'Es wird bereits eine Zuordnung durchgeführt, bitte warten Sie bis zur Vollendung dieser, '
                        'bis Sie die nächste ausführen')

    def delimOK(self):
        if isinstance(self.dchosen, tuple):
            for d in self.dchosen:
                self.delimiter[d] = self.view.entrys['popup_ent'].get()
        else:
            self.delimiter[self.dchosen] = self.view.entrys['popup_ent'].get()
        if self.delimiter == '' or len(self.delimiter[self.dchosen]) != 1:
            showwarning('Angabe ungültig', 'Das angegebene Trennzeichen ist ungültig oder es wurde keines Angegeben!'
                                           '\nBitte Geben Sie ein anderes Trennzeichen ein!')
            self.delimiterFester(None)
        else:
            self.view.top['popup_ent'].destroy()
            self.dchosen = None

    def delimCanc(self):
        self.view.top['popup_ent'].destroy()

    def delimiterFester(self, d):
        if isinstance(d, tuple):
            self.dchosen = list(self.delimiter.keys())[d[0]], list(self.delimiter.keys())[d[1]]
        elif self.dchosen is None:
            self.dchosen = list(self.delimiter.keys())[d]
        if d == 0:
            self.view.textentry('Bitte geben Sie das Trennzeichen der Schuelerlisten CSV-Datei an:', self.delimOK,
                                self.delimCanc)
        if d == 1:
            self.view.textentry('Bitte geben Sie das Trennzeichen der Projektlisten CSV-Datei an:', self.delimOK,
                                self.delimCanc)
        if d == 2:
            self.view.textentry('Bitte geben Sie das Trennzeichen der CSV-Dateien an:', self.delimOK,
                                self.delimCanc)
        while self.dchosen is not None:
            try:
                self.view.top['popup_ent'].update()
            except TclError:
                return False
        return True

    def autoimport(self):
        if os.path.exists('projektliste.csv') \
                and os.path.exists('schuelerliste.csv') and askokcancel('Auto-import', 'Es wurden passende CSV-Dateien '
                                                                                       'gefunden, wollen Sie diese '
                                                                                       'jetzt importieren?'):
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

        if not bool(self.view.table['main'].get_children()):
            self.tabelle()
        else:
            self.tabellen_update()

    def exportieren(self):
        slcsv = filedialog.asksaveasfilename(title='Schülerliste exportieren', defaultextension=".csv",
                                             initialfile='schuelerl_fertig',
                                             filetypes=(("CSV Datei", "*.csv"), ("Txt Datei", "*.txt"),
                                                        ("all files", "*.*")))
        if slcsv != '':
            plcsv = filedialog.asksaveasfilename(title='Projektliste exportieren', defaultextension=".csv",
                                                 initialfile='projektel_fertig',
                                                 filetypes=(("CSV Datei", "*.csv"), ("Txt Datei", "*.txt"),
                                                            ("all files", "*.*")))
            if plcsv != '':
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

    def tabelle(self):
        fetch = self.model.ausgabe('schueler')
        self.view.shlr_tabelle(fetch)
        self.tabellen_update()

    def tabelle_prj(self):
        fetch = self.model.ausgabe('projekte')
        self.view.prj_tabelle(fetch)
        self.tabellen_update()

    def tabellen_update(self, fetchshlr=None, fetchprj=None):
        if fetchshlr is None:
            fetchshlr = self.model.ausgabe('schueler')
        if fetchprj is None:
            fetchprj = self.model.ausgabe('projekte')

        try:
            for i in fetchshlr:
                self.view.table['main'].item(i[0], tags='red')
        except TclError:
            pass
        self.view.table['main'].delete(*self.view.table['main'].get_children())

        for t in fetchshlr:
            self.view.table['main'].insert('', t[0], t[0], values=t)  # , tags=t[0]

        for ele in fetchshlr:
            if ele[8] is None:
                self.view.table['main'].item(ele[0], tags='red')

        try:
            for i in fetchprj:
                try:
                    self.view.table['prj'].item(i[0], tags='white')
                except TclError:
                    pass
            self.view.table['prj'].delete(*self.view.table['prj'].get_children())

            for t in fetchprj:
                self.view.table['prj'].insert('', t[0], t[0], values=t)  # , tags=t[0]

            failed = self.model.prj_aktu()
            for prj in failed:
                try:
                    self.view.table['prj'].item(prj, tags='red')
                except TclError:
                    pass
        except KeyError:
            pass

    def tabelle_sorti(self, col, descending, tabelle):
        data = [(self.view.table[tabelle].set(tvindex, col), tvindex) for tvindex in
                self.view.table[tabelle].get_children('')]

        try:
            data = [(float(element), tvindex) for element, tvindex in data]
        except ValueError:
            pass

        data.sort(reverse=descending)

        for index, (val, k) in enumerate(data):
            self.view.table[tabelle].move(k, '', index)

        # reverse sort next time
        self.view.table[tabelle].heading(col, command=lambda: self.tabelle_sorti(col, not descending, tabelle))

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
                self.view.buttons['hin'].configure('confirm.TButton')
            else:
                showerror('Fehler', 'Schüler bereits vorhanden!')
            for entry in range(7):
                self.view.entrys[entry].delete(0, END)
                self.view.entrys[entry].configure('default.TEntry')
        else:
            self.view.buttons['hin'].configure(style='error.TButton')
            for i in range(4):
                self.view.entrys[i].configure(style='default.TEntry')
                if self.view.entrys[i].get() == "":
                    self.view.entrys[i].configure(style='error.TEntry')
        self.view.fenster['hin'].update()
        time.sleep(0.3)
        self.view.buttons['hin'].configure(style='default.TButton')
        self.tabellen_update()

    def ande(self):
        if self.andernx != "" and self.view.entrys['ande_Eid'].get() != "":
            self.model.ande(self.andernx, self.view.entrys['ande_Eandern'].get(), self.view.entrys['ande_Eid'].get())
            self.tabellen_update()
            self.view.fenster['ande'].destroy()

    def J5(self):
        self.tabellen_update(self.model.jahrgsuch('schueler', 5), self.model.jahrgsuch('projekte', 5))

    def J6(self):
        self.tabellen_update(self.model.jahrgsuch('schueler', 6), self.model.jahrgsuch('projekte', 6))

    def J7(self):
        self.tabellen_update(self.model.jahrgsuch('schueler', 7), self.model.jahrgsuch('projekte', 7))

    def J8(self):
        self.tabellen_update(self.model.jahrgsuch('schueler', 8), self.model.jahrgsuch('projekte', 8))

    def J9(self):
        self.tabellen_update(self.model.jahrgsuch('schueler', 9), self.model.jahrgsuch('projekte', 9))

    def J10(self):
        self.tabellen_update(self.model.jahrgsuch('schueler', 10), self.model.jahrgsuch('projekte', 10))

    def J11(self):
        self.tabellen_update(self.model.jahrgsuch('schueler', 11), self.model.jahrgsuch('projekte', 11))

    def J12(self):
        self.tabellen_update(self.model.jahrgsuch('schueler', 12), self.model.jahrgsuch('projekte', 12))

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

    def run(self):
        pass

c = Controller()
