# Tash gestion for Home Assistant or Raspberry Pi
# Application de gestion des poubelles pour Home Assistant ou Raspberry Pi

# Created by Romain COULON
# email = rcoulon44@gmail.com


import datetime
import locale

locale.setlocale(locale.LC_TIME, '')

Periode = {"hebdomadaire":7, "bimensuel":14, "mensuel":28}


# Configuration de la fréquence et du jour
freq = "bimensuel"
# valeur possible => mensuel, bimensuel, hebdomadaire

first_collect_day = "2021-01-13"
# Valeur possible => 2021-05-21


# Definition des modules utiles
def Now():
    return datetime.date.today()

def Next_Collect_Day(date):
    global freq
    step_collect = Periode[freq]
    delta_day = datetime.timedelta(days = step_collect)
    return date + delta_day

def Yesterday_Collect_Day(date):
    return date - datetime.timedelta(days = 1)

# Script

next_collect_date = datetime.date.fromisoformat(first_collect_day)

# date_test = Now()
# date_test = datetime.date.fromisoformat(date_test)

while True:
    if Now() == Yesterday_Collect_Day(next_collect_date):
        print("Nous sommes le",Now().strftime("%A %d %B %Y"))
        print("Le rammassage des poubelles est demain. Penser à sortir les poubelles !")
        break
    else:
        if next_collect_date < Now():
            next_collect_date = Next_Collect_Day(next_collect_date)
        else:
            print("Nous sommes le",Now().strftime("%A %d %B %Y"))
            print("Le prochain jour de collecte est le",next_collect_date.strftime("%A %d %B %Y"))
            break
