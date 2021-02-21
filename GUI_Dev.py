# Tash gestion for Home Assistant or Raspberry Pi
# Application de gestion des poubelles pour Home Assistant ou Raspberry Pi

# Created by Romain COULON
# email = rcoulon44@gmail.com

# A terminer
#   - Menu à faire
#   - Configuration via un fichier json
#   - Faire une fenêtre de configuration
#   - Afficher l'historique des dates de passage
#   - Faire une fenêtre pour l'affichage des données de l'historique
#   - Voir pour une création d'onglets pour facilité la navigation


import tkinter
import datetime
import locale
import json


# Variable
Periode = {"hebdomadaire":7, "bimensuel":14, "mensuel":28}
locale.setlocale(locale.LC_TIME, '')

# Configuration de la fréquence et du jour
freq = "bimensuel"
# valeur possible => mensuel, bimensuel, hebdomadaire
first_collect_day = "2021-02-10"
# Valeur possible => 2021-05-21


# Definition des modules utiles

# Modules généraux
def Now():
    return datetime.date.today()

def Next_Collect_Day(freq, date):
    step_collect = Periode[freq]
    delta_day = datetime.timedelta(days = step_collect)
    return date + delta_day

def Yesterday_Collect_Day(date):
    return date - datetime.timedelta(days = 1)

def Read_Data_Json():
    with open("history.json", mode='r') as json_history:
        history= json.load(json_history)
        return history


# Modules liés au compteurs
def Increase_Counter_1():
    global counter_trash_1
    global last_counter_tash_1
    last_counter_tash_1 = datetime.date.today().strftime("%d %b %y")
    counter_trash_1 += 1
    Write_Counter_Data_Json("counter_trash_1", counter_trash_1, "last_counter_tash_1", last_counter_tash_1)
    label_counter1_counter.configure(text=counter_trash_1)
    label_counter1_date.configure(text=last_counter_tash_1)

def Increase_Counter_2():
    global counter_trash_2
    global last_counter_tash_2
    last_counter_tash_2 = datetime.date.today().strftime("%d %b %y")
    counter_trash_2 += 1
    Write_Counter_Data_Json("counter_trash_2", counter_trash_2, "last_counter_tash_2", last_counter_tash_2)
    label_counter2_counter.configure(text=counter_trash_2)
    label_counter2_date.configure(text=last_counter_tash_2)

def Reset_Counter():
    global counter_trash_1, counter_trash_2
    global last_counter_tash_1, last_counter_tash_2
    counter_trash_1, counter_trash_2 = 0, 0
    last_counter_tash_1 = "na"
    last_counter_tash_2 = "na"
    Write_Counter_Data_Json("counter_trash_1", counter_trash_1, "last_counter_tash_1", last_counter_tash_1)
    Write_Counter_Data_Json("counter_trash_2", counter_trash_2, "last_counter_tash_2", last_counter_tash_2)
    label_counter1_counter.configure(text=counter_trash_1)
    label_counter2_counter.configure(text=counter_trash_2)
    label_counter1_date.configure(text=last_counter_tash_1)
    label_counter2_date.configure(text=last_counter_tash_2)

def Write_Counter_Data_Json(counter_name, counter, last_counter_name, last_counter):
    year = Now().year
    history = Read_Data_Json()
    if str(year) not in history:
        year_history = {}
        year_history['history_date'] = []
        year_history["counter_history"] = {}
        history[str(year)] = year_history
        with open("history.json", "w") as json_history:
            json.dump(history, json_history, indent=4)
    counter_history = {}
    last_counter_list = {}
    year_history = {}
    # Partie du code à reprendre en fonction de l'étape d'initialisation
    if str(year) in history:
        year_history = history[str(year)]
        counter_history = year_history["counter_history"]
        counter_history[counter_name] = counter
        counter_history[last_counter_name] = last_counter
        year_history["counter_history"] = counter_history
        history[str(year)] = year_history
    else:
        counter_history[counter_name] = counter
        counter_history[last_counter_name] = last_counter
        year_history["counter_history"] = counter_history
        history[year] = year_history
    with open("history.json", "w") as json_history:
        json.dump(history, json_history, indent=4)


# Modules principaux (qui se répètent toutes les heures)
def Update(year, first_collect_day, now, next_collect, freq):
    next_collect_date = datetime.date.fromisoformat(first_collect_day)
    while next_collect_date < Now():
        next_collect_date = Next_Collect_Day(freq, next_collect_date)
    history = Read_Data_Json()
    if str(year) not in history:
        year_history = {}
        year_history['history_date'] = []
        year_history["counter_history"] = {}
        history[str(year)] = year_history
        with open("history.json", "w") as json_history:
            json.dump(history, json_history, indent=4)
    year_history = history[str(year)]
    counter_history = year_history["counter_history"]
    now = "Nous sommes le " + Now().strftime("%d %B %Y")
    next_collect = next_collect_date.strftime("%d %B %Y")
    counter_trash_1 = counter_history.get("counter_trash_1", "0")
    counter_trash_2 = counter_history.get("counter_trash_2", "0")
    last_counter_tash_1 = counter_history.get("last_counter_tash_1", "na")
    last_counter_tash_2 = counter_history.get("last_counter_tash_2", "na")
    label_now.configure(text=now)
    label_collect_2.configure(text=next_collect)
    label_counter1_counter.configure(text=counter_trash_1)
    label_counter2_counter.configure(text=counter_trash_2)
    label_counter1_date.configure(text=last_counter_tash_1)
    label_counter2_date.configure(text=last_counter_tash_2)
    # Mise à jour de l'historique des levées
    Write_Date_History_Data_Json(year, last_counter_tash_1)
    # Mise à jour de l'indicateur de passage des poubelles
    Update_Indicateur_Poubelle(next_collect_date)
    # Boucle toute les heure
    main.after(3600000, Update, year, next_collect_date)
    # main.after(10000, Update, year, next_collect_date)
    return counter_trash_1, counter_trash_2, last_counter_tash_1, last_counter_tash_2

def Write_Date_History_Data_Json(year, last_counter_tash_1):
    # print("Ecriture des dates pour les poubelles menagères")
    history = Read_Data_Json()
    year_history = history[str(year)]
    history_date = year_history["history_date"]
    if last_counter_tash_1 != "na":
        if last_counter_tash_1 not in history_date:
            history_date.append(last_counter_tash_1)
            year_history["history_date"] = history_date
            history[year] = year_history
            with open("history.json", "w") as json_history:
                json.dump(history, json_history, indent=4)

def Update_Indicateur_Poubelle(next_collect_date):
    # print("Verification de l'indicateur")
    jour = Now()
    veille = Yesterday_Collect_Day(next_collect_date)
    if jour == veille:
        canvas_indicateur.config(bg="#17f546")
    elif jour == next_collect_date:
        canvas_indicateur.config(bg="#17f546")
    else:
        canvas_indicateur.config(bg="#656565")

# Modules pour les historiques
def Display_Date_History_Json():
    year = Now().year
    history = Read_Data_Json()
    year_history = history[str(year)]
    history_date = year_history["history_date"]
    print(history_date)


# Variable global
now = "Nous sommes le - "
next_collect = " - "

counter_trash_1 = 0
counter_trash_2 = 0
last_counter_tash_1 = "na"
last_counter_tash_2 = "na"

year = Now().year



# Interface graphique

# Variable pour l'Interface
color_gui = "#45a5d9"
text_color = "white"

# Créer une nouvelle fenêtre avec sa personnalisation
main = tkinter.Tk()
main.minsize(480,360)
main.maxsize(480,360)
main.title("Gestion des poubelles")
main.geometry("480x360")
main.iconphoto(False, tkinter.PhotoImage(file="Ressources/logo.png"))
main.config(background=color_gui)

# Creation des frames
frame_title = tkinter.Frame(main, bg=color_gui)
frame_title.pack(fill="x", side="top")

# Ajout d'un séparateur avec les dates
frame_separated_1 = tkinter.Frame(main, bg="#656565", height=5)
frame_separated_1.pack(fill="x", side="top", pady=5)

frame_date = tkinter.Frame(main, bg=color_gui)
frame_date.pack(fill="x", side="top")

canvas_indicateur = tkinter.Canvas(frame_date, width=40, height=40, bg="#656565")
canvas_indicateur.grid(column=1, row=0, sticky="N")

# Ajout d'un séparateur avec les compteur
frame_separated_2 = tkinter.Frame(main, bg="#656565", height=5)
frame_separated_2.pack(fill="x", side="top", pady=5)

frame_counter = tkinter.Frame(main, bg=color_gui)
frame_counter.pack(expand=1)


# Ajouter du titre
label_title = tkinter.Label(frame_title, text="Gestion des poubelles", font=("Arial", 25), bg=color_gui, fg=text_color)
label_title.pack()

# Ajout du jour actuel
label_now = tkinter.Label(frame_date, text=now, font=("Arial", 12), bg=color_gui, fg=text_color)
label_now.grid(column=0, row=0, sticky="W", padx=5, pady=10)

# Ajout de la date de la prochaine collecte
label_collect_1 = tkinter.Label(frame_date, text="Le prochain jour de collecte est le :", font=("Arial", 12), bg=color_gui, fg=text_color)
label_collect_1.grid(column=0, row=1, sticky="W", padx=5, pady=10)
label_collect_2 = tkinter.Label(frame_date, text=next_collect, font=("Arial", 12), bg=color_gui, fg=text_color)
label_collect_2.grid(column=1, row=1, sticky="E", padx=5, pady=10)


# Création du compteur 1:
label_counter1_text = tkinter.Label(frame_counter, text="Nombre de poubelles ménagères", font=("Arial", 12), bg=color_gui, fg=text_color)
label_counter1_text.grid(column=0, row=0, sticky="W", padx=5, pady=5)
label_counter1_counter = tkinter.Label(frame_counter, text=counter_trash_1, font=("Arial", 12), bg=color_gui, fg=text_color)
label_counter1_counter.grid(column=1, row=0, sticky="N", padx=5, pady=5)
label_counter1_date = tkinter.Label(frame_counter, text=last_counter_tash_1, font=("Arial", 8), bg=color_gui, fg=text_color)
label_counter1_date.grid(column=1, row=1, sticky="N", padx=0, pady=5)
button_counter1 = tkinter.Button(frame_counter, text="+", bg=text_color, fg=color_gui, width=15, height=2, command=Increase_Counter_1)
button_counter1.grid(column=2, row=0, sticky="E", padx=20, pady=5)

# Création du compteur 2:
label_counter2_text = tkinter.Label(frame_counter, text="Nombre de poubelles jaunes", font=("Arial", 12), bg=color_gui, fg=text_color)
label_counter2_text.grid(column=0, row=2, sticky="W", padx=5, pady=5)
label_counter2_counter = tkinter.Label(frame_counter, text=counter_trash_2, font=("Arial", 12), bg=color_gui, fg=text_color)
label_counter2_counter.grid(column=1, row=2, sticky="N", padx=5, pady=5)
label_counter2_date = tkinter.Label(frame_counter, text=last_counter_tash_2, font=("Arial", 8), bg=color_gui, fg=text_color)
label_counter2_date.grid(column=1, row=3, sticky="N", padx=0, pady=5)
button_counter2 = tkinter.Button(frame_counter, text="+", bg=text_color, fg=color_gui, width=15, height=2, command=Increase_Counter_2)
button_counter2.grid(column=2, row=2, sticky="E", padx=20, pady=5)

button_reset_counter = tkinter.Button(frame_counter, text="Reset", bg=text_color, fg="red", width=15, height=2, command=Reset_Counter)
button_reset_counter.grid(column=0, row=3, sticky="W", padx=20, pady=0)

# Bouton de test pour les fonctions
button_test = tkinter.Button(frame_counter, text="Test", bg=text_color, fg="red", width=15, height=2, command=Display_Date_History_Json)
button_test.grid(column=2, row=3, sticky="E", padx=20, pady=0)

# Programme pour l'interface
# next_collect_date = initialisation()
counter_history_update = Update(year, first_collect_day, now, next_collect, freq)
counter_trash_1 = (counter_history_update[0])
counter_trash_2 = (counter_history_update[1])
last_counter_tash_1 = (counter_history_update[2])
last_counter_tash_2 = (counter_history_update[3])
main.mainloop()
