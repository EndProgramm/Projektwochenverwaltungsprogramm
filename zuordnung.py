import sqlite3 as sqli
import random

def auswahl():
    #Herstellen der Verbindung mit der Datenbank
    connection = sqli.connect("pwvwp.db")
    #Über den sogenannten Cursor können Anfragen an die Datenbank gestellt werden
    cursor = connection.cursor()
    
    a = 4 #Jahrgang
    while a <= 11:
        a+=1        
        b=1 #Projekt

        sql="select max(pNum) from projekte WHERE '"+str(a)+"' like pJahrg" #max Projektnummer wird ermittelt
        cursor.execute(sql)
        x=cursor.fetchall() #max Projektnummer
        
        xx=x[0][0]
        if xx== None:
            xx=0
        while b<=xx:
            
            liste=[]
            sql="select max(sID) from schueler WHERE '"+str(a)+"' like sJahrg and '"+str(b)+"' like sErst " #max sID wird ermittelt
            cursor.execute(sql)
            zz=cursor.fetchall()
            z=0
            
            if zz != [(None,)]:
                z=zz[0][0]
                
                
                
            y=0 #zaehler sID
            while y<=z:
                sql="select sID from schueler WHERE '"+str(a)+"' like sJahrg and '"+str(b)+"' like sErst and '"+str(y)+"' like sID  " # Ermittlung von Schülern in a jahrgang und b erstwahl
                cursor.execute(sql)
                f=cursor.fetchall()
                
                if f != []:
                    
                    ff=f[0][0]
                    
                    liste.append(ff)
                y +=1
            
            
            
            sql="select pMaxS from projekte WHERE '"+str(a)+"' like pJahrg and '"+str(b)+"' like pNum"
            cursor.execute(sql)
            maxanz0=cursor.fetchall()
            if maxanz0 != []:
                xyzabcdef=(maxanz0)
                maxanz=maxanz0[0][0]
                
            else:
                maxanz=0
                
                
            if len(liste)<=maxanz:
                m=0 #zähler der schüler
                
                while m<len(liste):
                    sql="update schueler set sZu='"+str(b)+"' where '"+str(liste[m])+"'like sID;"
                    cursor.execute(sql)
                    m +=1
                    
            else:
                m=0 #zähler der schüler
                
                listeaus1 = random.choices(liste, k=maxanz)
                
                while m<maxanz:
                    
                    sql="update schueler set sZu='"+str(b)+"' where '"+str(listeaus1[m])+"'like sID ;"
                    cursor.execute(sql)
                    m+=1
                
            b = b+1
            

    a = 4 #Jahrgang
    while a <= 11:
        a+=1
        
        b=1 #Projekt

        sql="select max(pNum) from projekte WHERE '"+str(a)+"' like pJahrg" #max Projektnummer wird ermittelt
        cursor.execute(sql)
        x=cursor.fetchall() #max Projektnummer
        xx=x[0][0]
        if xx== None:
            xx=0
        while b<=xx:
            
            liste=[]
            sql="select max(sID) from schueler WHERE '"+str(a)+"' like sJahrg and '"+str(b)+"' like sZweit " #max sID wird ermittelt
            cursor.execute(sql)
            zz=cursor.fetchall()
            z=0
            
            if zz != [(None,)]:
                z=zz[0][0]
                
                
                
                
            y=0 #zaehler sID
            while y<=z:
                sql="select sID from schueler WHERE '"+str(a)+"' like sJahrg and sZu is NULL and '"+str(b)+"' like sZweit and '"+str(y)+"' like sID  " # Ermittlung von Schülern in a jahrgang und b erstwahl
                cursor.execute(sql)
                f=cursor.fetchall()
                
                if f != []:
                    
                    ff=f[0][0]
                    
                    liste.append(ff)
                y +=1
            
            
            
            sql="select pMaxS from projekte WHERE '"+str(a)+"' like pJahrg and '"+str(b)+"' like pNum"
            cursor.execute(sql)
            maxanz0=cursor.fetchall()
            if maxanz0 != []:
                sql="select count(sID) from schueler WHERE '"+str(a)+"' like sJahrg and '"+str(b)+"' like sZu"
                cursor.execute(sql)
                maxanz1=cursor.fetchall()
                maxanz=maxanz0[0][0]-maxanz1[0][0]
            else:
                maxanz=0
            
            if maxanz>0 and liste!=[]:
                
                
                if len(liste)<=maxanz:
                    m=0 #zähler der schüler
                    
                    while m<len(liste):
                        
                        sql="update schueler set sZu='"+str(b)+"' where '"+str(liste[m])+"'like sID;"
                        cursor.execute(sql)
                        m +=1
                        
                else:
                    m=0 #zähler der schüler
                    
                    listeaus1 = random.choices(liste, k=maxanz)
                    
                    while m<maxanz:
                        
                        sql="update schueler set sZu='"+str(b)+"' where '"+str(listeaus1[m])+"'like sID ;"
                        cursor.execute(sql)
                        m+=1
                
            b = b+1
            
    a = 4 #Jahrgang
    while a <= 11:
        a+=1
        if a>6:
            
            b=1 #Projekt

            sql="select max(pNum) from projekte WHERE '"+str(a)+"' like pJahrg" #max Projektnummer wird ermittelt
            cursor.execute(sql)
            x=cursor.fetchall() #max Projektnummer
            xx=x[0][0]
            if xx== None:
                xx=0
            while b<=xx:
                
                liste=[]
                sql="select max(sID) from schueler WHERE '"+str(a)+"' like sJahrg and sZu is NULL and '"+str(b)+"' like sDritt " #max sID wird ermittelt
                cursor.execute(sql)
                zz=cursor.fetchall()
                z=0
                
                if zz != [(None,)]:
                    z=zz[0][0]
                    
                    
                    
                    
                y=0 #zaehler sID
                while y<=z:
                    sql="select sID from schueler WHERE '"+str(a)+"' like sJahrg and sZu is NULL and '"+str(b)+"' like sDritt and '"+str(y)+"' like sID  " # Ermittlung von Schülern in a jahrgang und b erstwahl
                    cursor.execute(sql)
                    f=cursor.fetchall()
                    
                    if f != []:
                        
                        ff=f[0][0]
                        
                        liste.append(ff)
                    y +=1
                
                
                
                sql="select pMaxS from projekte WHERE '"+str(a)+"' like pJahrg and '"+str(b)+"' like pNum"
                cursor.execute(sql)
                maxanz0=cursor.fetchall()
                if maxanz0 != []:
                    sql="select count(sID) from schueler WHERE '"+str(a)+"' like sJahrg and '"+str(b)+"' like sZu"
                    cursor.execute(sql)
                    maxanz1=cursor.fetchall()
                    maxanz=maxanz0[0][0]-maxanz1[0][0]
                else:
                    maxanz=0
                
                if maxanz>0 and liste!=[]:
                    
                    
                    if len(liste)<=maxanz:
                        m=0 #zähler der schüler
                        
                        while m<len(liste):
                            
                            sql="update schueler set sZu='"+str(b)+"' where '"+str(liste[m])+"'like sID;"
                            cursor.execute(sql)
                            m +=1
                            
                    else:
                        m=0 #zähler der schüler
                        
                        listeaus1 = random.choices(liste, k=maxanz)
                        
                        while m<maxanz:
                            
                            sql="update schueler set sZu='"+str(b)+"' where '"+str(listeaus1[m])+"'like sID ;"
                            cursor.execute(sql)
                            m+=1
                    
                b = b+1


                
    a = 4 #Jahrgang
    while a <= 11:
        a+=1
        
        sql="select pNum from projekte WHERE '"+str(a)+"' like pJahrg"
        cursor.execute(sql)
        projekte=cursor.fetchall()
        sql="select sID from schueler WHERE '"+str(a)+"' like sJahrg and sZu is NULL"
        cursor.execute(sql)
        schuler=cursor.fetchall()
        while len(schuler)>0 and len(projekte)>0:
            sql="select pMaxS from projekte WHERE '"+str(a)+"' like pJahrg and '"+str(projekte[0][0])+"' like pNum"
            cursor.execute(sql)
            maxanz0=cursor.fetchall()
            if maxanz0 != []:
                sql="select count(sID) from schueler WHERE '"+str(a)+"' like sJahrg and '"+str(projekte[0][0])+"' like sZu"
                cursor.execute(sql)
                maxanz1=cursor.fetchall()
                maxanz=maxanz0[0][0]-maxanz1[0][0]
                if maxanz<=0: 
                    projekte.pop(0)
                else:
                    sql="update schueler set sZu='"+str(projekte[0][0])+"' where '"+str(schuler[0][0])+"'like sID ;"
                    cursor.execute(sql)
                    schuler.pop(0)
    
        
         
    
    connection.commit()
    connection.close()
