import subprocess
import time
import datetime

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

date = str(datetime.datetime.now())
d=date.split()
filename = "RC-"+d[0]+".txt"

def mail1(fname):
    # server = smtplib.SMTP("smtp.mailtrap.io", 2525)
    # server.login("79cd5012d01532", "56c7ed3712c865")
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('ogi.informatique2021@gmail.com', 'vhmtsyjpbqsyxysa')
    toaddr = cc = ['donald.sounlin@ogi-informatique.com','niels.abatti@ogi-informatique.com','frederic.doheto@ogi-informatique.com']
    cc = ['niels.abatti@ogi-informatique.com','frederic.doheto@ogi-informatique.com']
    msg = MIMEMultipart()
    msg['From'] = 'AFRICABOURSE'
    msg['to'] = 'donald.sounlin@ogi-informatique.com'
    msg['Cc'] = ','.join(cc)
    msg['Subject'] = 'Rapport Connectivité'

    message = """
    Rapport de Connectivité

    A Analyser.
    
    Cordialement
    """

    msg.attach(MIMEText(message, 'plain'))

    filename = fname
    attachment = open(filename, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())

    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(p)

    text = msg.as_string()
    server.sendmail('AFB Connectivité TEST', toaddr, text)
    server.quit()



ip_table = {
    "Pare - Feu" : "192.168.0.1",
    "AP Godomey ": "172.16.10.50",
    "Station Godomey" : "172.16.10.52",
    "AP Fidjrosse" : "172.16.10.40",
    "Station Fidjrossè" : "172.16.10.42",
    "AP Porto" : "172.16.10.10",
    "Station Porto ": "172.16.10.12",
    "AP Sènandé" : "172.16.10.20",
    "Station Sènandé" : "172.16.10.22",
    "Router siège + AA2: B24": "192.168.1.126",
    "Router Sènandé" : "192.168.20.1",
    "Router Godomey" : "192.168.4.1",
    "Router Fidjrosse" : "192.168.3.1",
    "Router Porto" : "192.168.6.1",
    "Serveur AAM" : "192.168.3.20",
    "Serveur AFB": "192.168.3.10",
    "Serveur Financia" : "192.168.1.20",
    "Serveur Test 1 " : "192.168.1.17",
    "Serveur Test 2" : "192.168.1.23",
    "Serveur de fichier Ancien" : "192.168.1.13",
    "Serveur d'Antivirus" : "192.168.1.12",
    "Serveur de fichier Actuel" : "192.168.1.11",
    "NAS AAM" : "192.168.3.19",
    "Scanner Fidjrosse" : "192.168.3.10",
    "Copieur Godomey" : "192.168.4.16",
    "Copieur Fidjrosse AFB" : "192.168.3.16",
    "Copieur Fidjrosse AAM" : "192.168.3.17"
}


r = open(filename, 'a')
newip = ''

def ping(ip):
    ping_reply = subprocess.run(["ping","-c2", ip], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    result =""
    if ping_reply.returncode == 0:      #ping will return 0 => success or  1 => Fail
        if ("unreachable" in str(ping_reply.stdout)):
            result = ("\n*  %s Ne Répond ===> OFFLINE  " % ip)
        else:
            result= ("\n* %s Répond ===> ONLINE  " % ip)
    elif ping_reply.returncode == 1:
        result= ("\n*  %s Ne Répond ===> OFFLINE  " % ip)
    return result


def add():
    global r
    global newip
    r.write(newip)

def generator(date,r):
    r.write(f"Rapport de Connectivité des équipements Clé (Local et Distant) du {date} \n")
    r.write(" \n")
    for name, ip in ip_table.items():
        print(name, end=' ')
        print(ping(ip))
        print("----")
        r.write(name)
        r.write(ping(ip) + '\n')
        r.write("----" + '\n')

    r.close()

for l in ip_table:
    print(l+' : '+ ip_table[l])

#ans = input('Voulez vous modifier la liste ? O/N : \n => ')
#ans = ans.lower()
ans = "n"
print('')

if ans == "n":
    generator(date,r)
    mail1(filename)
elif ans == 'o':
    an = input("""
    1- Ajout
    2- Modification  \n => 
    """)

    if an == "1":
        cc = True
        while cc:
            nam = input("Nom de l'équipement : \n => ")
            ip = input("Adresse IP: : \n => ")
            ip_table[nam] = ip
            cho1 = input('Voulez vous faire un autre changement ? O/N : \n => ')
            cho1 = cho1.lower()
            if cho1 == 'o':
                cc = True
            elif cho1 == 'n':
                cc = False
                break
            else:
                break

    elif an == "2":
        choice = input("""
        Voulez vous modifier ?
        1- Nom et IP
        2- Nom
        3- IP : \n => """)
        choice = choice.lower()
        if choice == "1":
            c = True
            while c:
                nam = input("Nom de l'équipement à mofifier : \n =>  ")
                if nam in ip_table.values():
                    nnam = input("Nouveau Nom de l'équipement : \n => ")
                    nip = input("Nouvelle adresse IP : \n => ")
                    ip_table[nnam] = ip_table.pop(nam)
                    ip_table[nnam] = nip
                    cho = input('Voulez vous faire un autre changement ? O/N : \n => ')
                    cho = cho.lower()
                    if cho =='o':
                        c=True
                    elif cho =='n':
                        c=False
                        break
                    else:
                        break
                else:
                    print("Entrée erronée")
                    cho = input('Voulez vous faire un autre changement ? O/N : \n => ')
                    cho = cho.lower()
                    if cho == 'o':
                        c = True
                    elif cho == 'n':
                        c = False
                        break
                    else:
                        break
            generator(date, r)
        if choice == "2":
            c = True
            while c:
                nam = input("Nom de l'équipement à mofifier : \n => ")
                if nam in ip_table.values():
                    nnam = input("Nouveau Nom de l'équipement : \n => ")
                    ip_table[nnam] = ip_table.pop(nam)
                    cho = input('Voulez vous faire un autre changement ? O/N : \n => ')
                    cho = cho.lower()
                    if cho == 'o':
                        c = True
                    elif cho == 'n':
                        c = False
                        break
                    else:
                        break
                else:
                    print("Entrée erronée")
                    cho = input('Voulez vous faire un autre changement ? O/N : \n => ')
                    cho = cho.lower()
                    if cho == 'o':
                        c = True
                    elif cho == 'n':
                        c = False
                        break
                    else:
                        break
                generator(date, r)
            if choice == "3":
                c = True
                while c:
                    nam = input("Nom de l'équipement à mofifier : \n => ")
                    if nam in ip_table.values():
                        nip = input("Nouvelle adresse IP : \n => ")
                        ip_table[nnam] = nip
                        cho = input('Voulez vous faire un autre changement ? O/N : \n => ')
                        cho = cho.lower()
                        if cho == 'o':
                            c = True
                        elif cho == 'n':
                            c = False
                            break
                        else:
                            break
                    else:
                        print("Entrée erronée")
                        cho = input('Voulez vous faire un autre changement ? O/N : \n => ')
                        cho = cho.lower()
                        if cho == 'o':
                            c = True
                        elif cho == 'n':
                            c = False
                            break
                        else:
                            break
                    generator(date, r)
    generator(date,r)
    mail1(filename)
