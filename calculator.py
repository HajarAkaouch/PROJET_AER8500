"""
In this file you will find the functions to calculate the rates 
"""
import math
import time
# Dictionnaire contenant la liste des variables à afficher initialisées
var = {"altitude_actuelle": {"value": 35000, "string": ""}, 
        "vitesse_actuelle": {"value": 0, "string": ""},
        "vitesse_actuelle_convertit": {"value": 0, "string": ""}, 
        "puissance_moteur": {"value": 0, "string": ""},
        "etat_systeme": "GROUND",
        "altitude_desiree": {"value": 0, "string": ""},
        "taux_monte": {"value": 0, "string": ""},
        "taux_monte_convertit": {"value": 0, "string": ""},
        "angle_attaque": {"value": 0, "string": ""}}                    

# Variables globales d'alatitude et du taux de monté maximal
ALTITUDE_MAX = 40000 #pieds
VITESSE_MAX = 800 #m/min

def prochain_etat(var, dt):
        
    #********************************************** GROUND ********************************************************
    # Si les deux entrées de taux de montée et d'angle d'attaque sont nuls, en fournir
    if var["taux_monte"]["value"] == 0:
        var["taux_monte"]["value"] = 400
    if var["angle_attaque"]["value"] == 0:
        var["angle_attaque"]["value"] = 8


    # Lorsque l’avion est au sol, l’altitude du système est nulle.
    if var["altitude_actuelle"]["value"] == 0:  
        var["etat_systeme"] = "GROUND"

    #************************************** CHANG. ALTITUDE ********************************************************

    # Déterminer si on est en montée ou en descente lorsque l'utilisateur nous fournit une altitude désirée
    if var["altitude_actuelle"]["value"] < var["altitude_desiree"]["value"] and var["altitude_actuelle"]["value"] < ALTITUDE_MAX and var["angle_attaque"]["value"] > 0:
        var["mode_descente"] = "MONTÉE"
        print(var["mode_descente"])
        var["etat_systeme"] = "CHANGEMENT_ALT"

    if var["altitude_actuelle"]["value"] > var["altitude_desiree"]["value"] and var["altitude_actuelle"]["value"] < ALTITUDE_MAX and var["angle_attaque"]["value"] < 0:
        var["mode_descente"] = "DESCENTE"
        print(var["mode_descente"])
        var["etat_systeme"] = "CHANGEMENT_ALT"
        var["taux_monte"]["value"] = -1 * var["taux_monte"]["value"]

    # Déterminer si on est en montée ou en descente lorsque l'utilisateur nous fournit juste l'angle d'attaque et le taux de monté
    if var["angle_attaque"]["value"] > 0 and var["altitude_desiree"]["value"] == 0:
        var["mode_descente"] = "MONTÉE"
        var["altitude_desiree"]["value"] = ALTITUDE_MAX
        print(var["mode_descente"])
        var["etat_systeme"] = "CHANGEMENT_ALT"

    
    # Augmentation de la vitesse tant que l'altitude désirée n'est pas atteinte
    if var["etat_systeme"] == "CHANGEMENT_ALT":

        # 1 m/min -> 0.0546807 pieds/s
        # var["taux_monte"] = np.round(var["taux_monte"], 1) # Résolution
        var["taux_monte_convertit"]["value"] = var["taux_monte"]["value"]*0.0546807 # 1 m/min -> 0.0546807 pieds/s
        # var["taux_monte_convertit"] = np.round(var["taux_monte_convertit"], 1) # Résolution               

        # Calcul de la nouvelle altitude
        var["altitude_actuelle"]["value"] += var["taux_monte_convertit"]["value"]*dt
        # var["altitude_actuelle"] = np.round(var["altitude_actuelle"], -1) # Résolution

        # Calcul de la vitesse en fonction de la puissance moteur (V = TM/sin(angle))
        # var["angle_attaque"] = np.round(var["angle_attaque"], 1) # Résolution
        var["vitesse_actuelle"]["value"] = abs(var["taux_monte_convertit"]["value"]/math.sin(math.radians(var["angle_attaque"]["value"]))) # V = taux de montée/sin(angle d'attaque)
        # var["vitesse_actuelle"] = np.round(var["vitesse_actuelle"], 1) # Résolution

        # Conversion de la vitesse actuelle (pieds/s -> kt)
        var["vitesse_actuelle_convertit"]["value"] = abs(var["vitesse_actuelle"]["value"]*0.592484) # 1 pieds/s -> 0.592484 kt 
        # var["vitesse_actuelle_convertit"] = np.round(var["vitesse_actuelle_convertit"], 1) # Résolution

        # Calcul la puissance (taux_monte = 5.468 # 100m/min -> 5.48pieds/s) + puissance initiale forunit par l'agrégateur
        var["puissance_moteur"]["value"] = abs(var["taux_monte_convertit"]["value"] / 5.48 * 10)
        # var["puissance_moteur"] = np.round(var["puissance_moteur"], 1) # Résolution

        #taux_monte -= taux_monte_convertit
        # À l’approche de l’altitude désirée atteinte, la vitesse doit commencer à se décroître pour s’annuler à l’altitude désirée
        if abs(var["altitude_actuelle"]["value"] - var["altitude_desiree"]["value"]) < 1000:  
            deceleration = abs(var["altitude_actuelle"]["value"] - var["altitude_desiree"]["value"]) / 1000
            var["taux_monte_convertit"]["value"] = (var["taux_monte_convertit"]["value"] * deceleration) + 0.01

            # Calculs avec le nouveau taux de monté appliqué à la decceleration 
            var["altitude_actuelle"]["value"] += var["taux_monte_convertit"]["value"]*dt
            var["vitesse_actuelle"]["value"] = abs(var["taux_monte_convertit"]["value"]/math.sin(math.radians(var["angle_attaque"]["value"]))) # V = taux de montée/sin(angle d'attaque)
            var["vitesse_actuelle_convertit"]["value"] = abs(var["vitesse_actuelle"]["value"]*0.592484) # 1 pieds/s -> 0.592484 kt 
            var["puissance_moteur"]["value"] = abs(var["taux_monte_convertit"]["value"] / 5.48 * 10)


        if var["altitude_actuelle"]["value"] > var["altitude_desiree"]["value"] and var["mode_descente"] == "MONTÉE":
            var["altitude_actuelle"]["value"] = var["altitude_desiree"]["value"]

        if var["altitude_actuelle"]["value"] < var["altitude_desiree"]["value"] and var["mode_descente"] == "DESCENTE":
            var["altitude_actuelle"]["value"] = var["altitude_desiree"]["value"]
 

    #*************************************** VOL CROISIÈRE *********************************************************
    # Sortie de l'état si l'altitude désirée est atteinte
    if var["altitude_actuelle"]["value"] == var["altitude_desiree"]["value"] or var["altitude_actuelle"]["value"] == ALTITUDE_MAX:
        var["etat_systeme"] = "VOL_CROISIÈRE"
        # taux mis à zéro une fois l'altitude atteinte
        var["taux_monte"]["value"] = 0 
    
    if var["altitude_actuelle"]["value"] == var["altitude_desiree"]["value"] == 0:
        var["etat_systeme"] = "GROUND"
        var["taux_monte"]["value"] = 0 

    #******************************************** CHUTE LIBRE ********************************************************

    # Lorsque l'angle d'attaque est supérieur à 15 degrés, l'avion est en chute libre.
    if var["angle_attaque"]["value"] > 15:  
         var["etat_systeme"] = "CHUTE LIBRE"

         var["altitude_actuelle"]["value"] = 99999 
         var["vitesse_actuelle_convertit"]["value"] = 99999 
         var["puissance_moteur"]["value"] = 99999 
         var["altitude_desiree"]["value"] = 99999 
         var["taux_monte"]["value"] = 99999 
         var["taux_monte_convertit"]["value"]= 99999 
         var["angle_attaque"]["value"] = 99999

         var["altitude_actuelle"]["string"] = "N/A" 
         var["vitesse_actuelle_convertit"]["string"] = "N/A" 
         var["puissance_moteur"]["string"] = "N/A" 
         var["altitude_desiree"]["string"] = "N/A" 
         var["taux_monte"]["string"] = "N/A" 
         var["taux_monte_convertit"]["string"]= "N/A" 
         var["angle_attaque"]["string"] = "N/A" 
    

    return var["altitude_actuelle"], var["vitesse_actuelle_convertit"], var["puissance_moteur"], var["etat_systeme"]

def boucle_principale():
    last_frame = time.monotonic()

    while True:
        # Appel de la fonction qui reçois les inputs de l'utilisateur 
        lire_input(var)

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

# Fonction qui reçois les inputs de l'utilisateur 
def lire_input(var): 
    var["altitude_desiree"]["value"] = 0
    var["taux_monte"]["value"] = 400 
    var["angle_attaque"]["value"] = 10


