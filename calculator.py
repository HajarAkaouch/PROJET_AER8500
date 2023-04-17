"""
In this file you will find the functions to calculate the rates 
"""
import math
import time
import numpy as np

# Dictionnaire contenant la liste des variables à afficher initialisées
var = {"altitude_actuelle": 10000, 
        "vitesse_actuelle": 0,
        "vitesse_actuelle_convertit": 0, 
        "puissance_moteur": 0,
        "etat_systeme": "GROUND",
        "altitude_desiree": 0,
        "taux_monte": 0,
        "taux_monte_convertit": 0,
        "angle_attaque": 0}                    

# Variables globales d'alatitude et du taux de monté maximal
ALTITUDE_MAX = 40000 #pieds
VITESSE_MAX = 800 #m/min

def prochain_etat(var, dt):
        
    #********************************************** GROUND ********************************************************
    #Si les deux entrées de taux de montée et d'angle d'attaque sont nuls, en fournir pour la montée
    if var["taux_monte"] == 0 and var["altitude_actuelle"] < var["altitude_desiree"]:
        var["taux_monte"] = 400
    if var["angle_attaque"] == 0 and var["altitude_actuelle"] < var["altitude_desiree"]:
        var["angle_attaque"] = 8
        
    # Si les deux entrées de taux de montée et d'angle d'attaque sont nuls, en fournir pour la descente
    if var["taux_monte"] == 0 and var["altitude_actuelle"] > var["altitude_desiree"]:
        var["taux_monte"] = 400
    if var["angle_attaque"] == 0 and var["altitude_actuelle"] > var["altitude_desiree"]:
        var["angle_attaque"] = -8

    # Lorsque l’avion est au sol, l’altitude du système est nulle.
    if var["altitude_actuelle"] == 0:  
        var["etat_systeme"] = "GROUND"

    #************************************** CHANG. ALTITUDE ********************************************************

    # Déterminer si on est en montée ou en descente lorsque l'utilisateur nous fournit une altitude désirée
    if var["altitude_actuelle"] < var["altitude_desiree"] and var["altitude_actuelle"] < ALTITUDE_MAX and var["angle_attaque"] > 0:
        var["mode_descente"] = "MONTÉE"
        print(var["mode_descente"])
        var["etat_systeme"] = "CHANGEMENT_ALT"

    if var["altitude_actuelle"] > var["altitude_desiree"] and var["altitude_actuelle"] < ALTITUDE_MAX and var["angle_attaque"] < 0:
        var["mode_descente"] = "DESCENTE"
        print(var["mode_descente"])
        var["etat_systeme"] = "CHANGEMENT_ALT"
        #var["taux_monte"] = -1 * var["taux_monte"]

    # Déterminer si on est en montée ou en descente lorsque l'utilisateur nous fournit juste l'angle d'attaque et le taux de monté
    if var["angle_attaque"] > 0 and var["altitude_desiree"] == 0:
        var["mode_descente"] = "MONTÉE"
        var["altitude_desiree"] = ALTITUDE_MAX
        print(var["mode_descente"])
        var["etat_systeme"] = "CHANGEMENT_ALT"

    
    # Augmentation de la vitesse tant que l'altitude désirée n'est pas atteinte
    if var["etat_systeme"] == "CHANGEMENT_ALT":

        # 1 m/min -> 0.0546807 pieds/s
        var["taux_monte_convertit"] = var["taux_monte"]*0.0546807 # 1 m/min -> 0.0546807 pieds/s

        #Taux de monté négatif si on est en descente
        if var["mode_descente"] == "DESCENTE":
            var["taux_monte_convertit"] = -1 * var["taux_monte_convertit"]

        # Calcul de la nouvelle altitude
        var["altitude_actuelle"] += var["taux_monte_convertit"]*dt

        # Calcul de la vitesse en fonction de la puissance moteur (V = TM/sin(angle))
        # var["angle_attaque"] = np.round(var["angle_attaque"], 1) # Résolution
        var["vitesse_actuelle"] = abs(var["taux_monte_convertit"]/math.sin(math.radians(var["angle_attaque"]))) # V = taux de montée/sin(angle d'attaque)

        # Conversion de la vitesse actuelle (pieds/s -> kt)
        var["vitesse_actuelle_convertit"] = abs(var["vitesse_actuelle"]*0.592484) # 1 pieds/s -> 0.592484 kt 

        # Calcul la puissance (taux_monte = 5.468 # 100m/min -> 5.48pieds/s) + puissance initiale forunit par l'agrégateur
        var["puissance_moteur"] = abs(var["taux_monte_convertit"] / 5.48 * 10)

        #taux_monte -= taux_monte_convertit
        # À l’approche de l’altitude désirée atteinte, la vitesse doit commencer à se décroître pour s’annuler à l’altitude désirée
        if abs(var["altitude_actuelle"] - var["altitude_desiree"]) < 1000:  
            deceleration = abs(var["altitude_actuelle"] - var["altitude_desiree"]) / 1000
            var["taux_monte_convertit"] = (var["taux_monte_convertit"] * deceleration) + 0.01

            # Calculs avec le nouveau taux de monté appliqué à la decceleration 
            var["altitude_actuelle"] += var["taux_monte_convertit"]*dt
            var["vitesse_actuelle"] = abs(var["taux_monte_convertit"]/math.sin(math.radians(var["angle_attaque"]))) # V = taux de montée/sin(angle d'attaque)
            var["vitesse_actuelle_convertit"] = abs(var["vitesse_actuelle"]*0.592484) # 1 pieds/s -> 0.592484 kt 
            var["puissance_moteur"] = abs(var["taux_monte_convertit"] / 5.48 * 10)


        if var["altitude_actuelle"] > var["altitude_desiree"] and var["mode_descente"] == "MONTÉE":
            var["altitude_actuelle"] = var["altitude_desiree"]

        if var["altitude_actuelle"] < var["altitude_desiree"] and var["mode_descente"] == "DESCENTE":
            var["altitude_actuelle"] = var["altitude_desiree"]
 

    #*************************************** VOL CROISIÈRE *********************************************************
    # Sortie de l'état si l'altitude désirée est atteinte
    if var["altitude_actuelle"] == var["altitude_desiree"] or var["altitude_actuelle"] == ALTITUDE_MAX:
        var["etat_systeme"] = "VOL_CROISIÈRE"
        # taux mis à zéro une fois l'altitude atteinte
        var["taux_monte"] = 0 
    
    if var["altitude_actuelle"] == var["altitude_desiree"] == 0:
        var["etat_systeme"] = "GROUND"
        var["taux_monte"] = 0 

    #******************************************** CHUTE LIBRE ********************************************************

    # Lorsque l'angle d'attaque est supérieur à 15 degrés, l'avion est en chute libre.
    if var["angle_attaque"] > 15:  
        var["etat_systeme"] = "CHUTE LIBRE"
        var["altitude_actuelle"] = 99999 
        var["vitesse_actuelle_convertit"] = 99999 
        var["puissance_moteur"] = 99999 
        var["altitude_desiree"] = 99999 
        var["taux_monte"] = 99999 
        var["taux_monte_convertit"]= 99999 
        var["angle_attaque"] = 99999 
    

    return var["altitude_actuelle"], var["vitesse_actuelle_convertit"], var["puissance_moteur"], var["etat_systeme"]

def boucle_principale():
    last_frame = time.monotonic()

    while True:
        # Appel de la fonction qui reçois les inputs de l'utilisateur 
        lire_input(altitude_desiree, taux_monte, angle_attaque)

        # Fonction du temps
        now = time.monotonic() 
        dt = now - last_frame
        last_frame = now

        # Appel de la fonction qui déterminera le prochain état
        #prochain_etat(var, dt)
        print(prochain_etat(var, dt))

        # Rafraichissement
        time.sleep(0.005)
        # print(var) # Juste pour les tests

#juste pour les tests
altitude_desiree = 8000
taux_monte = None 
angle_attaque = None

# Fonction qui reçois les inputs de l'utilisateur 
def lire_input(altitude_desiree, taux_monte_desire, angle_attaque):
    if altitude_desiree is not None:
        var["altitude_desiree"] = altitude_desiree
    if taux_monte is not None:
        var["taux_monte_desire"] = taux_monte_desire
    if angle_attaque is not None:
        var["angle_attaque"] = angle_attaque


