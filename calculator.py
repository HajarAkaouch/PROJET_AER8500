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
        #time.sleep(1)

        #Clock
        #temps_ecoule += 1
 

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
            while altitude_actuelle < altitude_desiree:
                time.sleep(1)
                temps_ecoule += 1

                # 1 m/min -> 0.0546807 pieds/s
                taux_monte_convertit = taux_monte*0.0546807 # 1 m/min -> 0.0546807 pieds/s

                # Calcul de la nouvelle altitude
                altitude_actuelle += taux_monte_convertit*temps_ecoule

                # Calcul de la vitesse en fonction de la puissance moteur (V = TM/sin(angle))
                vitesse_actuelle = taux_monte_convertit/math.sin(math.radians(angle_attaque)) # V = taux de montée/sin(angle d'attaque)

                # Conversion de la vitesse actuelle (pieds/s -> kt)
                vitesse_actuelle_convertit = vitesse_actuelle*0.592484 # 1 pieds/s -> 0.592484 kt 

                # Calcul la puissance (taux_monte = 5.468 # 100m/min -> 5.48pieds/s)?
                # À faire 


                # À l’approche de l’altitude désirée atteinte, la vitesse doit commencer à se décroître pour s’annuler à l’altitude désirée (méthode par pallier).
                if altitude_desiree - altitude_actuelle < 2000:  #if altitude_actuelle >= (altitude_desiree - 2000):
                    time.sleep(1)
                    temps_ecoule += 1
                    taux_monte -= 0.1*taux_monte_convertit

                    # Sortie de l'état si l'altitude désirée est atteinte
                    if altitude_actuelle >= altitude_desiree or altitude_actuelle >= 40000:
                        time.sleep(1)
                        temps_ecoule += 1 
                        # taux mis à zéro une fois l'altitude atteinte
                        taux_monte = 0.0 
                        etat_systeme = "VOL_CROISIÈRE"   


            # Affichage des valeurs actuelles de l'altitude, de la vitesse et de la puissance du moteur
                print(f"Altitude actuelle (pieds) : {altitude_actuelle}")
                print(f"Vitesse actuelle (kt) : {vitesse_actuelle_convertit}")
                print(f"Puissance moteur (W) : {puissance_moteur}")
                print(f"État système : {etat_systeme}")
                print(f"Temps écoulé (s) : {temps_ecoule}")

        #*************************************** VOL CROISIÈRE ******************************************

        elif etat_systeme == "VOL_CROISIÈRE":  
            # taux mis à zéro une fois l'altitude atteinte
            #taux_monte = 0.0  
            time.sleep(1)
            temps_ecoule += 1

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
# Demander à l'utilisateur l'altitude désirée et le taux de montée
altitude_desiree = float(input("Entrez l'altitude désirée en mètres : "))
taux_de_montee = float(input("Entrez le taux de montée en mètres par seconde : "))

# Définir la vitesse initiale et l'altitude initiale
vitesse_initiale = 0
altitude_initiale = 0

# Boucle de simulation
while altitude_initiale < altitude_desiree:
    # Calculer la nouvelle altitude en fonction du taux de montée et du temps écoulé
    altitude_initiale += taux_de_montee

    # Si l'altitude de destination approche, réduire progressivement le taux de montée
    if altitude_desiree - altitude_initiale < 1000 and taux_de_montee > 0:
        taux_de_montee -= 0.1*taux_de_montee

    # Afficher l'altitude et le taux de montée à chaque itération
    print("Altitude : {:.2f} m - Taux de montée : {:.2f} m/s".format(altitude_initiale, taux_de_montee))

# Arrivé à l'altitude désirée, mettre le taux de montée à zéro
taux_de_montee = 0

# Afficher l'altitude et le taux de montée finaux
print("Altitude : {:.2f} m - Taux de montée : {:.2f} m/s".format(altitude_initiale, taux_de_montee))

"""



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