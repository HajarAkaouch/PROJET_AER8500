"""
In this file you will find the functions to calculate the rates 
"""
import math
import time

#Dictionnaire contenant la liste des variables à afficher initialisées
var = {"altitude_actuelle": 5000, 
        "vitesse_actuelle": 0,
        "vitesse_actuelle_convertit": 0, 
        "puissance_moteur": 0,
        "etat_systeme": "GROUND",
        "altitude_desiree": 0,
        "taux_monte": 0,
        "taux_monte_convertit": 0,
        "angle_attaque": 0,}                     

ALTITUDE_MAX = 40000 #pieds
VITESSE_MAX = 800 #m/min

def prochain_etat(var, dt):

    #********************************************** GROUND ********************************************************

    if var["altitude_actuelle"] == 0:  
        var["etat_systeme"] = "GROUND"

    #************************************** CHANG. ALTITUDE ********************************************************

    # Déterminer si on est en montée ou en descente
    if var["altitude_actuelle"] < var["altitude_desiree"] and var["altitude_actuelle"] < ALTITUDE_MAX:
        var["mode_descente"] = "MONTÉE"
        var["etat_systeme"] = "CHANGEMENT_ALT"

    if var["altitude_actuelle"] > var["altitude_desiree"] and var["altitude_actuelle"] < ALTITUDE_MAX:
        var["mode_descente"] = "DESCENTE"
        var["etat_systeme"] = "CHANGEMENT_ALT"
        var["taux_monte"] = -1 * var["taux_monte"]
    
    # Augmentation de la vitesse tant que l'altitude désirée n'est pas atteinte
    if var["etat_systeme"] == "CHANGEMENT_ALT":
        print("etat_systeme :", var["etat_systeme"])

        # 1 m/min -> 0.0546807 pieds/s
        var["taux_monte_convertit"] = var["taux_monte"]*0.0546807 # 1 m/min -> 0.0546807 pieds/s
        print("taux_monte_convertit :", var["taux_monte_convertit"])

        # Calcul de la nouvelle altitude
        var["altitude_actuelle"] += var["taux_monte_convertit"]*dt
        print("altitude_actuelle :", var["altitude_actuelle"])

        # Calcul de la vitesse en fonction de la puissance moteur (V = TM/sin(angle))
        var["vitesse_actuelle"] = var["taux_monte_convertit"]/math.sin(math.radians(var["angle_attaque"])) # V = taux de montée/sin(angle d'attaque)
        print("vitesse_actuelle :", var["vitesse_actuelle"])

        # Conversion de la vitesse actuelle (pieds/s -> kt)
        var["vitesse_actuelle_convertit"] = var["vitesse_actuelle"]*0.592484 # 1 pieds/s -> 0.592484 kt 
        print("vitesse_actuelle_convertit :", var["vitesse_actuelle_convertit"])

        # Calcul la puissance (taux_monte = 5.468 # 100m/min -> 5.48pieds/s)
        var["puissance_moteur"] = var["taux_monte_convertit"] / 5.48 * 10 
        print("puissance_moteur :", var["puissance_moteur"])

        #taux_monte -= taux_monte_convertit
        # À l’approche de l’altitude désirée atteinte, la vitesse doit commencer à se décroître pour s’annuler à l’altitude désirée (méthode par pallier).
        if abs(var["altitude_actuelle"] - var["altitude_desiree"]) < 1000:  
            deceleration = abs(var["altitude_actuelle"] - var["altitude_desiree"]) / 1000
            var["taux_monte_convertit"] = (var["taux_monte_convertit"] * deceleration) + 0.01

        if var["altitude_actuelle"] > var["altitude_desiree"] and var["mode_descente"] == "MONTÉE":
            var["altitude_actuelle"] = var["altitude_desiree"]

        if var["altitude_actuelle"] < var["altitude_desiree"] and var["mode_descente"] == "DESCENTE":
            var["altitude_actuelle"] = var["altitude_desiree"]
 

    #*************************************** VOL CROISIÈRE *********************************************************
    # Sortie de l'état si l'altitude désirée est atteinte
    if var["altitude_actuelle"] == var["altitude_desiree"] or var["altitude_actuelle"] == ALTITUDE_MAX:
        var["etat_systeme"] = "VOL_CROISIÈRE"
        # taux mis à zéro une fois l'altitude atteinte
        var["taux_monte"] = 0.0 


def boucle_principale():
    last_frame = time.monotonic()

    while True:
        lire_input(var)

        # Fonction du temps
        now = time.monotonic() 
        dt = now - last_frame
        last_frame = now

        # Appel de la fonction qui déterminera le prochain état
        prochain_etat(var, dt)

        # Rafraichissement
        time.sleep(0.005)
        print(var)


def lire_input(var): 
    var["altitude_desiree"] = 3800
    var["taux_monte"] = 800 
    var["angle_attaque"] = 10



"""
    #Imputs de l'utilisateur 
        altitude_desiree = float(input("Entrez l'altitude désirée (pieds) : "))
        taux_monte = float(input("Entrez le taux de montée (m/min) : "))
        angle_attaque = float(input("Entrez l'angle d'attaque (degrés) : "))

    # Affichage des valeurs actuelles de l'altitude, de la vitesse et de la puissance du moteur
        print(f"Altitude actuelle (pieds) : {altitude_actuelle}")
        print(f"Vitesse actuelle (kt) : {vitesse_actuelle_convertit}")
        print(f"Puissance moteur (W) : {puissance_moteur}")
        print(f"État système : {var_systeme}")
        print(f"Temps écoulé (s) : {temps_ecoule}")
"""


    #********************************************** GROUND CONTRAINTES ********************************************************

    # if var["var_systeme"] == "GROUND":
    #     # Si l'utilisateur entre une valeur d'altitude désirée de 0
    #     while var["altitude_desiree"] == 0:
    #         var["altitude_desiree"] = float(input("Veuillez entrez une altitude supérieure à 0 pieds : "))

    #     while var["altitude_desiree"] > ALTITUDE_MAX:
    #         var["altitude_desiree"] = float(input("Veuillez entrez une altitude inférieure ou égale à 40000 pieds : "))

    #     # Si angle d'attaque = 0, on a une division par zéro dans le calcul de vitesse
    #     if var["angle_attaque"] <= 0:
    #         var["angle_attaque"] = 10
    #         print(f"Nouvel angle d'attaque : {var['angle_attaque']}")

    #     # Si angle d'attaque > 15, angle de décrochage (Chute libre)
    #     while var["angle_attaque"] >= 15:
    #         var["angle_attaque"] = float(input("**ALERTE : CHUTE LIBRE** Entrez un nouvel angle d'attaque : "))

    #     # Si les deux entrées sont nulles, fournir un taux de montée et un angle d'attaque
    #     if var["taux_monte"] == 0 and var["angle_attaque"] == 0:
    #         var["taux_monte"] = 100
    #         print(f"Nouveau taux de montée : {var['taux_monte']}")
    #         var["angle_attaque"] = 10
    #         print(f"Nouvel angle d'attaque : {var['angle_attaque']}")

    #     while var["taux_monte"] > 800:
    #         var["taux_monte"] = float(input("Veuillez entrez un taux de montée inférieure ou égale à 800 m/min : "))

    #     # Changement d'état si l'altitude désirée est fournie
    #     else:
    #         var["var_systeme"] = "CHANGEMENT_ALT"