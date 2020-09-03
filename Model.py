# -*- coding: utf-8 -*-
# Autoren: Martin, Max, Vincent, Christoph, Lia; erstellt: 24.02.2020
# Der Projektwochenmanager zum zuordnen aller Schüler zu Projekten

import os, csv, random
import sqlite3 as sqli


class Model(object):
    def __init__(self):
        if not os.path.exists('pwvwp.db'):
            self.createDB()

    @staticmethod
    def createDB():
        connection = sqli.connect('pwvwp.db')
        cursor = connection.cursor()

        # Tabellen erzeugen
        sql = "CREATE TABLE projekte(pID INTEGER PRIMARY KEY, pName TEXT, sJahrg INTEGER, pNum INTEGER, pS INTEGER, " \
              "pMaxS INTEGER);"
        cursor.execute(sql)

        sql = "CREATE TABLE schueler(sID INTEGER PRIMARY KEY, sVName TEXT, sName TEXT, sJahrg INTEGER, sKla INTEGER, " \
              "sErst INTEGER, sZweit INTEGER, sDritt INTEGER, sZu INTEGER); "
        cursor.execute(sql)

        connection.commit()
        connection.close()

    @staticmethod
    def clearDB():
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()
        sql = "Drop TABLE IF EXISTS projekte"
        cur.execute(sql)
        sql = "Drop TABLE IF EXISTS schueler"
        cur.execute(sql)
        con.commit()
        con.close()

    @staticmethod
    def importCSV(slcsv, plcsv, delis, delip):  # sl = schuelerliste, pl = projektliste
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        # importieren der slcsv Datei
        try:
            file = open(slcsv, 'r')
            read = csv.reader(file, delimiter=delis)
            for row in read:
                sql = "SELECT COUNT(*) FROM schueler WHERE sName = '" + row[0] + "' AND sVName = '" + row[
                    1] + "' AND sJahrg = '" + row[2] + "';"
                cur.execute(sql)
                test = cur.fetchall()
                if not test[0][0]:
                    sql = "INSERT INTO schueler(sName, sVName, sJahrg, sKla, sErst, sZweit, sDritt, sZu) VALUES('" + \
                          row[0] + "', '" + row[1] + "', '" + row[2] + "', '" + row[3] + "', '" + row[4] + "', '" + row[
                              5] + "', '" + row[6] + "', NULL);"
                    cur.execute(sql)

            # importieren der plcsv Datei
            file = open(plcsv, 'r')
            read = csv.reader(file, delimiter=delip)
            for row in read:
                sql = "SELECT COUNT(*) FROM projekte WHERE pName = '" + row[0] + "' AND sJahrg = '" + row[1] + "';"
                cur.execute(sql)
                test = cur.fetchall()
                if not test[0][0]:
                    sql = "INSERT INTO projekte(pName, sJahrg, pNum, pMaxS) VALUES('" + row[0] + "', '" + row[
                        1] + "', '" + \
                          row[2] + "', '" + row[3] + "');"
                    cur.execute(sql)
            con.commit()
            con.close()
            return False
        except KeyError:
            return True

    @staticmethod
    def exportCSV(slcsv, plcsv, delimiter):
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

    @staticmethod
    def zuordnen(wahl):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()
        jahrg = 4  # Jahrgang
        while jahrg <= 11:
            jahrg += 1
            b = 1  # Projekt
            sql = "select max(pNum) FROM projekte WHERE '" + str(
                jahrg) + "' like sJahrg;"  # max Projektnummer wird ermittelt
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
                sql = "select pMaxS FROM projekte WHERE '" + str(jahrg) + "' like sJahrg and '" + str(
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

    @staticmethod
    def restzuordnung():
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        jahrg = 4  # Jahrgang
        check = []
        while jahrg <= 11:
            jahrg += 1
            sql = "select pNum from projekte WHERE '" + str(jahrg) + "' like sJahrg"
            cur.execute(sql)
            projekte = cur.fetchall()
            sql = "select sID from schueler WHERE '" + str(jahrg) + "' like sJahrg and sZu is NULL"
            cur.execute(sql)
            schuler = cur.fetchall()
            while len(schuler) > 0 and len(projekte) > 0:
                sql = "select pMaxS from projekte WHERE '" + str(jahrg) + "' like sJahrg and '" + str(
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
            check.append(
                (len(schuler) != 0 and len(projekte) == 0, jahrg))  # Überprüfung auf zu wenig Plätze in den Projekten

        # Auswertung der Überprüfung
        re = False
        failedjahrg = []
        for e in check:
            if e[0]:
                failedjahrg.append(e[1])
            re = re or e[0]
        con.commit()
        con.close()
        return re, failedjahrg

    @staticmethod
    def prj_aktu():
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        failed = []
        for i in range(5, 13):
            sql = "SELECT pID, sJahrg, pNum FROM projekte WHERE sJahrg = " + str(i) + ";"
            cur.execute(sql)
            prj = cur.fetchall()
            for pid, jahrg, nr in prj:
                sql = "SELECT COUNT(sID) FROM schueler WHERE sZu = " + str(nr) + " AND sJahrg = " + str(i) + ";"
                cur.execute(sql)
                erg = cur.fetchall()
                if erg[0][0] < 5:
                    failed.append(pid)
                sql = "UPDATE projekte SET pS = '" + str(erg[0][0]) + "' WHERE pID = " + str(pid) + ";"
                cur.execute(sql)

        con.commit()
        con.close()
        return failed

    @staticmethod
    def einfuegen(tabelle, spalten_namen_tuple, value_tuple):
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
            con.commit()
            con.close()
            return False

    @staticmethod
    def ande(eigenschaft, eingabe, sID):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()
        sql = "UPDATE schueler SET " + eigenschaft + "= '" + eingabe + "' WHERE sID like '" + sID + "';"
        cur.execute(sql)
        con.commit()
        con.close()

    @staticmethod
    def ausgabe(tabelle):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        sql = "SELECT * FROM " + tabelle + ";"
        cur.execute(sql)
        erg = cur.fetchall()

        con.close()
        return erg

    @staticmethod
    def jahrgsuch(tabelle, jahrgang):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        sql = "SELECT * FROM " + tabelle + " WHERE sJahrg LIKE '" + str(jahrgang) + "'"
        cur.execute(sql)
        erg = cur.fetchall()

        con.close()
        return erg

    @staticmethod
    def ausfuhren(sql):
        con = sqli.connect('pwvwp.db')
        cur = con.cursor()

        cur.execute(sql)
        erg = cur.fetchall()

        con.close()
        return erg
