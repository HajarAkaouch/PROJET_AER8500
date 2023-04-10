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
    altitude_desiree = float(input("Entrez l'altitude désirée : "))
    taux_monte = float(input("Entrez le taux de montée : "))
    angle_attaque = float(input("Entrez l'angle d'attaque : "))

    while True:
        # Affichage des valeurs actuelles de l'altitude, de la vitesse et de la puissance du moteur
        print(f"Altitude actuelle : {altitude_actuelle}")
        print(f"Vitesse actuelle : {vitesse_actuelle}")
        print(f"Puissance moteur : {puissance_moteur}")
        print(f"État système : {etat_systeme}")
        print(f"Temps écoulé : {temps_ecoule}")
        
        # Pause de 1 seconde avant d'actualiser les valeurs (va changer la réactivité de notre système)
        time.sleep(1)

        #Clock
        temps_ecoule += 1
        
        if etat_systeme == "GROUND":
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
                angle_attaque = 5
                print(f"Nouvel angle d'attaque : {angle_attaque}")

            # Changement d'état si l'altitude désirée est fournie
            else:
                etat_systeme = "CHANGEMENT_ALT"

        elif etat_systeme == "CHANGEMENT_ALT":
            # Calcul de la vitesse en fonction de la puissance moteur (V = TM/sin(angle))
            vitesse_actuelle = 100 / math.sin(math.radians(angle_attaque)) 

            # Calcul de la nouvelle altitude
            altitude_actuelle += taux_monte * temps_ecoule

            #Calcul la puissance?
            #blabla 

            # Sortie de l'état si l'altitude désirée est atteinte
            if altitude_actuelle >= altitude_desiree or altitude_actuelle >= 40000:
                etat_systeme = "VOL_CROISIÈRE"
            

        elif etat_systeme == "VOL_CROISIÈRE":  
            # taux mis à zéro une fois l'altitude atteinte
            taux_monte = 0.0  

            # Réduction de la vitesse pour se stabiliser à l'altitude désirée
            if altitude_actuelle > altitude_desiree:
                vitesse_actuelle -= 10
            elif altitude_actuelle < altitude_desiree:
                vitesse_actuelle += 10

            #Calcul la puissance? 
            #blabla




