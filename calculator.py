"""
In this file you will find the functions to calculate the rates 
"""
import math
import time

def user_input(altitude_desiree, taux_monte, angle_attaque):
    #initialisation des variables
    altitude_actuelle = 0.0
    vitesse_actuelle = 0.0
    puissance_moteur = 0.0
    etat_systeme = "GROUND"

    temps_ecoule = 0

    #Imputs de l'utilisateur (À mettre dans le while, mais pour l'instant à l'extérieur juste pour les tests)
    altitude_desiree = float(input("Entrez l'altitude désirée (pieds) : "))
    taux_monte = float(input("Entrez le taux de montée (m/min) : "))
    angle_attaque = float(input("Entrez l'angle d'attaque (degrés) : "))

    while True:
        #************************************* RAFRAICHISSEMENT & CLOCK **********************************************

        # Pause de 1 seconde avant d'actualiser les valeurs (va changer la réactivité de notre système)
        time.sleep(1)

        #Clock
        temps_ecoule += 1


        #************************************** FONCTIONS DE CONVERSION ******************************************
        
        # Conversion de la vitesse actuelle (pieds/s -> km/h)
        # vitesse_actuelle_convertit = vitesse_actuelle*1.09728 # 1 pieds/s -> 1.09728 km/h 

        # Conversion de la vitesse actuelle (pieds/s -> km/h) -> convertir en kt 
        # vitesse_actuelle_convertit = vitesse_actuelle*0.592484 # 1 pieds/s -> 0.592484 kt 


        #********************************************** GROUND ******************************************

        if etat_systeme == "GROUND":
            # Vitesse initiale nulle
            vitesse_actuelle_convertit = 0

            # Si l'utilisateur entre une valeur d'altitude désirée de 0
            while altitude_desiree == 0:
                altitude_desiree = float(input("Veuillez entrez une altitude supérieure à 0 : "))

            # Si angle d'attaque = 0, on a une division par zéro dans le calcul de vitesse
            if angle_attaque <= 0:
                angle_attaque = 5
                print(f"Nouvel angle d'attaque : {angle_attaque}")

            # Si angle d'attaque > 15, angle de décrochage (Chute libre)
            while angle_attaque >= 15:
                angle_attaque = float(input("**ALERTE : CHUTE LIBRE** Entrez un nouvel angle d'attaque : "))

            # Si les deux entrées sont nulles, fournir un taux de montée et un angle d'attaque
            if taux_monte == 0 and angle_attaque == 0:
                taux_monte = 100
                print(f"Nouveau taux de montée : {taux_monte}")
                angle_attaque = 10
                print(f"Nouvel angle d'attaque : {angle_attaque}")

            # Changement d'état si l'altitude désirée est fournie
            else:
                etat_systeme = "CHANGEMENT_ALT"


        #************************************** CHANG. ALTITUDE ******************************************

        elif etat_systeme == "CHANGEMENT_ALT":
            #Augmentation de la vitesse tant que l'altitude désirée n'est pas atteinte
            while altitude_actuelle < (altitude_desiree - 5000):
                taux_monte_convertit = taux_monte*0.0546807 # 1 m/min -> 0.0546807 pieds/s

                # Calcul de la nouvelle altitude
                altitude_actuelle += taux_monte * temps_ecoule

                # Calcul de la vitesse en fonction de la puissance moteur (V = TM/sin(angle))
                vitesse_actuelle = taux_monte / math.sin(math.radians(angle_attaque)) # V = taux de montée/sin(angle d'attaque)

                # Conversion de la vitesse actuelle (pieds/s -> km/h) -> convertir en kt 
                vitesse_actuelle_convertit = vitesse_actuelle*0.592484 # 1 pieds/s -> 0.592484 kt 

                # Calcul la puissance (taux_monte = 5.468 # 100m/min -> 5.48pieds/s)?
                # À faire 

                # À l’approche de l’altitude désirée atteinte, la vitesse doit commencer à se décroître pour s’annuler à l’altitude désirée (méthode par pallier).
            while altitude_actuelle >= (altitude_desiree - 5000):
                    if altitude_actuelle >= altitude_desiree - 5000 and altitude_actuelle < altitude_desiree - 2500:
                        taux_monte_1 = taux_monte_convertit / 2
                        altitude_actuelle += taux_monte_1 * temps_ecoule 
                        vitesse_actuelle = taux_monte_1 / math.sin(math.radians(angle_attaque))
                        vitesse_actuelle_convertit = vitesse_actuelle*0.592484

                    elif altitude_actuelle >= altitude_desiree - 2500 and altitude_actuelle < altitude_desiree - 3750:
                        taux_monte_2 = taux_monte_convertit / 2
                        altitude_actuelle += taux_monte_2 * temps_ecoule 
                        vitesse_actuelle = taux_monte_2 / math.sin(math.radians(angle_attaque))
                        vitesse_actuelle_convertit = vitesse_actuelle*0.592484

                    elif altitude_actuelle >= altitude_desiree - 3750 and altitude_actuelle < altitude_desiree:
                        taux_monte_3 = taux_monte_convertit / 2
                        altitude_actuelle += taux_monte * temps_ecoule 
                        vitesse_actuelle = taux_monte_3 / math.sin(math.radians(angle_attaque))
                        vitesse_actuelle_convertit = vitesse_actuelle*0.592484

            # Sortie de l'état si l'altitude désirée est atteinte
            if altitude_actuelle >= altitude_desiree or altitude_actuelle >= 40000:
                etat_systeme = "VOL_CROISIÈRE"
            

        #*************************************** VOL CROISIÈRE ******************************************

        elif etat_systeme == "VOL_CROISIÈRE":  
            # taux mis à zéro une fois l'altitude atteinte
            taux_monte = 0.0  

            # Cas dans lequel on dépasse l'altitude désirée : Réduction de la vitesse pour se stabiliser à l'altitude désirée (Établir une mesure de sécurité si l'avion est trop élevé?)
            # while altitude_actuelle > altitude_desiree:
            #     print(f"Altitude désirée dépassée, réduction de la vitesse.")
            #     taux_monte = 5.468 # 100m/min -> 5.48pieds/s
            #     vitesse_actuelle_convertit -= 1 # À enlever sinon vitesse négative
            #     altitude_actuelle -= taux_monte_convertit * temps_ecoule

            # Calcul la puissance (taux_monte = 5.468 # 100m/min -> 5.48pieds/s)?
            # À faire 

        #******************************************* AFFICHAGE **********************************************

        # Affichage des valeurs actuelles de l'altitude, de la vitesse et de la puissance du moteur
        print(f"Altitude actuelle (pieds) : {altitude_actuelle}")
        print(f"Vitesse actuelle (kt) : {vitesse_actuelle_convertit}")
        print(f"Puissance moteur (W) : {puissance_moteur}")
        print(f"État système : {etat_systeme}")
        print(f"Temps écoulé (s) : {temps_ecoule}")



"""
import time

class PIDController:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.last_error = 0
        self.integral = 0

    def update(self, measured_value):
        error = self.setpoint - measured_value
        self.integral += error
        derivative = error - self.last_error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.last_error = error
        return output

# Variables initiales
altitude = 0  # en mètres
vitesse = 100  # en mètres par seconde
altitude_desiree = 5000  # en mètres
dt = 0.1  # en secondes

# Constantes du PID
kp = 0.1
ki = 0.01
kd = 0.01

# Initialisation du PID
pid = PIDController(kp, ki, kd, altitude_desiree)

# Boucle de contrôle
while altitude < altitude_desiree:
    altitude += vitesse * dt
    vitesse += pid.update(altitude) * dt

    # Limite de la vitesse à zéro à l'altitude désirée
    if altitude >= altitude_desiree and vitesse > 0:
        vitesse = 0

    print(f"Altitude: {altitude:.2f} m, Vitesse: {vitesse:.2f} m/s")
    time.sleep(dt)
"""