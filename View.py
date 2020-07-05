# -*- coding: utf-8 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Schüler zu Projekten

from tkinter import *
from tkinter import filedialog  # muss aus unbekannten Gründen extra importiert werden
from tkinter.messagebox import *
from tkinter.ttk import *
import ttkthemes


class View(ttkthemes.ThemedTk):
    def __init__(self, imp, exp, bee, j5, j6, j7, j8, j9, j10, j11, j12, ja, tabsort, hin, zord, ande, scht,
                 prjt, a1, a2, a3, a4, a5, a6, a7):
        # print(ttkthemes.THEMES)   # zum Ausgeben der verfügbaren Themes
        ttkthemes.ThemedTk.__init__(self, theme='breeze')
        self.title("Projektwochenverwaltungsprogramm")
        self.geometry('800x300')
        self.maxsize(800, 300)
        self.minsize(800, 300)

        # Ttk Styles
        self.styles = Style().configure('confirm', background='green')
        self.styles = Style().configure('error', background='red')
        self.styles = Style().configure('default', background='SystemButtonFace')

        # bestimmen der Callbacks
        self.callback_imp = imp
        self.callback_exp = exp
        self.callback_bee = bee
        self.radiocom = {'jahrg': [j5, j6, j7, j8, j9, j10, j11, j12, ja], 'ande': [a1, a2, a3, a4, a5, a6, a7]}
        self.tabelle_sorti = tabsort
        self.callback_zord = zord
        self.callback_hin = hin
        self.callback_ande = ande
        self.callback_scht = scht
        self.callback_prjt = prjt
        self.names = {'schueler': ("Vorname", "Nachname", "Jahrg", "Klasse", "Erst Wunsch", "Zweit Wunsch",
                                   "Dritt Wunsch"),
                      'projekte': ("Name", "Jahrgang", "Nummer", "zugeordnete Schüler", "max Schüler"),
                      'jahrg': ('5', '6', '7', '8', '9', '10', '11', '12', 'Alle')}
        self.width = {'schueler': [35, 121, 122, 50, 50, 100, 100, 100, 100], 'projekte': [35, 343, 75, 75, 150, 100]}
        self.labels = {}
        self.entrys = {}
        self.buttons = {}
        self.vars = {'jahrg': IntVar(), 'ande': IntVar(), 'menu': IntVar()}
        self.radios = {}
        self.rahmen = {1: Frame(master=self), 2: Frame(master=self)}
        self.rahmen.update({11: Frame(master=self.rahmen[1])})
        self.fenster = {}

        # erstellen des Menüs
        self.menus = {}
        self.menu((('Datei', (
            (None, "importieren", self.callback_imp,), (None, "exportieren", self.callback_exp,), ('-', None),
            (None, "beenden", self.callback_bee,))),
                   ('Schüler', ((None, "hinzufügen", self.schulerhin,), (None, "ändern", self.schuelerandern,))),
                   ('Tools', ((None, "Schüler Projekten zuordnen", self.callback_zord,),)),
                   ('Tabelle', (('.', "Schüler", self.callback_scht, self.vars['menu']),
                                ('.', "Projekte", lambda head='projekte': self.callback_scht(head),
                                 self.vars['menu'])))))
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

    def menu(self, menu):
        # angabe von Commands, normal ohne präfix. Bei Checkbox ']' und bei Radiobutton '.' als präfix.
        # Bei beiden muss auch eine Konreollvariable wie IntVar angegeben werden. Für Seperator '-' ohne index 1 und 2.
        # bsp.: self.menu(('Menuname', (("Command", callback, None), ("Radiobutton", callback, IntVar()), ("-", None,)))
        self.menus = {'main': Menu(self)}
        for cas, com in menu:
            self.menus[cas] = Menu(self.menus['main'], tearoff=0)
            for i, command in enumerate(com):
                if command[0] == '-':
                    self.menus[cas].add_separator()
                elif command[0] == '.':
                    if command[3] is None:
                        print('Es muss eine Kontrollvariable angegeben werden')
                        raise ValueError
                    self.menus[cas].add_radiobutton(label=command[1], command=command[2], variable=command[3], value=i)
                elif command[0] == ']':
                    if command[3] is None:
                        print('Es muss eine Kontrollvariable angegeben werden')
                        raise ValueError
                    self.menus[cas].add_checkbutton(label=command[1], command=command[2], variable=command[3], value=i)
                else:
                    self.menus[cas].add_command(label=command[1], command=command[2])
            self.menus['main'].add_cascade(label=cas, menu=self.menus[cas])
        self.config(menu=self.menus['main'])

    def tabelle(self, fetch, header='schueler'):
        ml = ['ID']
        for name in self.names[header]:
            ml.append(name)
        if header == 'schueler':
            ml.append('Zugeordned zu')
        self.table['columns'] = ml
        self.table['show'] = 'headings'
        for i in range(len(ml)):
            self.table.column(ml[i], width=self.width[header][i], minwidth=self.width[header][i])
        for i in range(len(ml)):
            self.table.heading(ml[i], text=ml[i], command=lambda col=i: self.tabelle_sorti(col, False))
        for t in fetch:
            self.table.insert('', t[0], t[0], values=t, tags=t[0])
        self.scrollbar.config(command=self.table.yview)
        self.table.pack(fill=X)

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
        except KeyError:
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


class Popup(ttkthemes.ThemedTk):
    def __index__(self):
        ttkthemes.ThemedTk.__init__(self, theme='breeze')
        self.title("BLANK")
        self.resizable(0, 0)

        self.label = None
        self.entry = None
        self.button = None
        self.rahmen = None

    def textentry(self, text, call_ok, call_cancel):
        self.title('Aktion erforderlich!')
        self.geometry("300x125")
        self.label = Label(self, text=text, font=('Arial', 13), wraplength=275, anchor='center')
        self.entry = Entry(self)
        self.rahmen = Frame(self)
        self.button = Button(self.rahmen, text='Ok', command=call_ok, width=10)
        # self.buttons['popup_Cancel'] = Button(self.rahmen['popup'], text='Cancel', command=call_cancel, width=10)
        self.label.pack(fill=X)
        self.entry.pack(pady=15)
        self.rahmen.pack()
        self.button.pack(side=LEFT)
        # self.buttons['popup_Cancel'].pack(side=LEFT)

    def progressbar(self):
        self.title('In Bearbeitung!')
        self.label = Progressbar(self, orient='horizontal', length=250, mode='determinate')
        self.label.pack()
