"""
In this file you will find the functions to calculate the rates 
"""
import math
import time

#Dictionnaire contenant la liste des variables à afficher initialisées
etat = {"altitude_actuelle": 0, 
        "vitesse_actuelle": 0,
        "vitesse_actuelle_convertit": 0, 
        "puissance_moteur": 0,
        "etat_systeme": "GROUND",
        "dt": 0,  #dt représente delta_t
        "altitude_desiree": 0,
        "taux_monte": 0,
        "taux_monte_convertit": 0,
        "angle_attaque": 0}                     

ALTITUDE_MAX = 40000 #pieds
VITESSE_MAX = 800 #m/min

def prochain_etat(etat, dt):

    #********************************************** GROUND ********************************************************

    if etat["altitude_actuelle"] == 0:  
        etat["etat_systeme"] == "GROUND"

    #************************************** CHANG. ALTITUDE ********************************************************

        #Augmentation de la vitesse tant que l'altitude désirée n'est pas atteinte
        if etat["altitude_actuelle"] > 0 and etat["altitude_actuelle"] < etat["altitude_desiree"] and etat["altitude_actuelle"] < ALTITUDE_MAX:
            etat["etat_systeme"] == "CHANGEMENT_ALT"

            # 1 m/min -> 0.0546807 pieds/s
            etat["taux_monte_convertit"] = etat["taux_monte"]*0.0546807 # 1 m/min -> 0.0546807 pieds/s

            # Calcul de la nouvelle altitude
            etat["altitude_actuelle"] += etat["taux_monte_convertit"]*etat["dt"]

            # Calcul de la vitesse en fonction de la puissance moteur (V = TM/sin(angle))
            etat["vitesse_actuelle"] = etat["taux_monte_convertit"]/math.sin(math.radians(etat["angle_attaque"])) # V = taux de montée/sin(angle d'attaque)

            # Conversion de la vitesse actuelle (pieds/s -> kt)
            etat["vitesse_actuelle_convertit"] = etat["vitesse_actuelle"]*0.592484 # 1 pieds/s -> 0.592484 kt 

            # Calcul la puissance (taux_monte = 5.468 # 100m/min -> 5.48pieds/s)
            etat["puissance"] = etat["taux_monte_convertit"] / 5.48 * 10 
 
            #taux_monte -= taux_monte_convertit
            # À l’approche de l’altitude désirée atteinte, la vitesse doit commencer à se décroître pour s’annuler à l’altitude désirée (méthode par pallier).
            if abs(etat["altitude_actuelle"] - etat["altitude_desiree"]) < 1000:  
                deceleration = (etat["altitude_actuelle"] - etat["altitude_desiree"]) / 1000
                etat["taux_monte"] = (etat["taux_monte_convertit"] * deceleration) + 0.01
            else:
                etat["taux_monte"] = etat["taux_monte_convertit"]   


    #*************************************** VOL CROISIÈRE *********************************************************
    # Sortie de l'état si l'altitude désirée est atteinte
    if etat["altitude_actuelle"] == etat["altitude_desiree"] or etat["altitude_actuelle"] == ALTITUDE_MAX:
        etat_systeme = "VOL_CROISIÈRE"
        # taux mis à zéro une fois l'altitude atteinte
        etat["taux_monte"] = 0.0 


def boucle_principale():
    last_frame = time.monotonic()

    while True:
        lire_input(etat)

        # Fonction du temps
        now = time.monotonic() 
        dt = now - last_frame
        last_frame = now

        # Appel de la fonction qui déterminera le prochain état
        prochain_etat(etat, dt)

        # Rafraichissement
        time.sleep(0.005)


def lire_input(etat): 
    etat["altitude_desiree"] = 10000
    etat["taux_monte"] = 100
    etat["angle_attaque"] = 10



"""
    #Imputs de l'utilisateur 
        altitude_desiree = float(input("Entrez l'altitude désirée (pieds) : "))
        taux_monte = float(input("Entrez le taux de montée (m/min) : "))
        angle_attaque = float(input("Entrez l'angle d'attaque (degrés) : "))

    # Affichage des valeurs actuelles de l'altitude, de la vitesse et de la puissance du moteur
        print(f"Altitude actuelle (pieds) : {altitude_actuelle}")
        print(f"Vitesse actuelle (kt) : {vitesse_actuelle_convertit}")
        print(f"Puissance moteur (W) : {puissance_moteur}")
        print(f"État système : {etat_systeme}")
        print(f"Temps écoulé (s) : {temps_ecoule}")
"""


    #********************************************** GROUND CONTRAINTES ********************************************************

    # if etat["etat_systeme"] == "GROUND":
    #     # Si l'utilisateur entre une valeur d'altitude désirée de 0
    #     while etat["altitude_desiree"] == 0:
    #         etat["altitude_desiree"] = float(input("Veuillez entrez une altitude supérieure à 0 pieds : "))

    #     while etat["altitude_desiree"] > ALTITUDE_MAX:
    #         etat["altitude_desiree"] = float(input("Veuillez entrez une altitude inférieure ou égale à 40000 pieds : "))

    #     # Si angle d'attaque = 0, on a une division par zéro dans le calcul de vitesse
    #     if etat["angle_attaque"] <= 0:
    #         etat["angle_attaque"] = 10
    #         print(f"Nouvel angle d'attaque : {etat['angle_attaque']}")

    #     # Si angle d'attaque > 15, angle de décrochage (Chute libre)
    #     while etat["angle_attaque"] >= 15:
    #         etat["angle_attaque"] = float(input("**ALERTE : CHUTE LIBRE** Entrez un nouvel angle d'attaque : "))

    #     # Si les deux entrées sont nulles, fournir un taux de montée et un angle d'attaque
    #     if etat["taux_monte"] == 0 and etat["angle_attaque"] == 0:
    #         etat["taux_monte"] = 100
    #         print(f"Nouveau taux de montée : {etat['taux_monte']}")
    #         etat["angle_attaque"] = 10
    #         print(f"Nouvel angle d'attaque : {etat['angle_attaque']}")

    #     while etat["taux_monte"] > 800:
    #         etat["taux_monte"] = float(input("Veuillez entrez un taux de montée inférieure ou égale à 800 m/min : "))

    #     # Changement d'état si l'altitude désirée est fournie
    #     else:
    #         etat["etat_systeme"] = "CHANGEMENT_ALT"