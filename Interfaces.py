import PySimpleGUI as gui

NO_ENTRY = None

class Interfaces:
    def __init__(self):
        gui.theme('Darkblue4')     
        state_layout = [
        [gui.Text("État:",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center"),
         gui.Text("Altitude (pieds):",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center")],
        [gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "etat"),
         gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "altitude")],
        [gui.Text("Vitesse (knots):",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center"),
         gui.Text("Puissance (%):",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center")],
        [gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "vitesse"),
         gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "puissance")]
        ]
        
        input_layout = [
        [gui.T(' ' * 50), gui.Text('Panneau usager', font =('Arial', 20), justification ='center', pad=(1,10))],
        [gui.Text('Altitude désiré (pieds):',font =('Arial', 15), size =(15, 1)), gui.InputText(do_not_clear=False)],
        [gui.Text('Taux de montée (m/min):', font =('Arial', 15), size =(15, 1)), gui.InputText(do_not_clear=False)],
        [gui.Text("Angle d'attaque (degré):", font =('Arial', 15), size =(15, 1)), gui.InputText(do_not_clear=False)],
        [gui.Text("Alt enregistrée :", font =('Arial', 10),text_color="#e5ecf5"), 
         gui.Text(font =('Arial', 10), size =(10, 1),text_color="#e5ecf5", key = "alt"),
         gui.Text("Taux enregistré :", font =('Arial', 10), text_color="#e5ecf5"), 
         gui.Text(font =('Arial', 10), size =(10, 1),text_color="#e5ecf5", key = "taux"),
         gui.Text("Angle enregistré :", font =('Arial', 10), text_color="#e5ecf5"), 
         gui.Text(font =('Arial', 10), size =(10, 1),text_color="#e5ecf5", key = "angle")],
        [gui.T(' ' * 45), gui.Submit("Confirmer",size=(10,2)), gui.T(' ' * 5), gui.Cancel("Annuler",size=(10,2))]
        ]
        self.user_input = gui.Window("Entrée de l'usager", input_layout)
        self.state_output = gui.Window('Panneau usager ', state_layout)

    def close_windows(self):
        self.user_input.close()
        self.state_output.close()

    def input_window(self):
        event, values = self.user_input.read() 

        if event == "Exit" or event == gui.WIN_CLOSED:
            return False, []
        
        values[0] = float(values[0]) if self.convertable_to_float(values[0]) else NO_ENTRY
        values[1] = float(values[1]) if self.convertable_to_float(values[1]) else NO_ENTRY
        values[2] = float(values[2]) if self.convertable_to_float(values[2]) else NO_ENTRY

        is_valid = self.check_values_validity(values)
        valid = all(element == True for element in is_valid)
        if valid:
            if event == "Confirmer":
                if values[0] != '':
                    self.user_input['alt'].update(values[0])
                if values[1] != '':
                    self.user_input['taux'].update(values[1])
                if values[2] != '':
                    self.user_input['angle'].update(values[2])
                return True, values
        return True, []

    def state_window(self, state, alt, speed, power):
        event = self.state_output.read(timeout = 20) 
        if event == "Exit" or event == gui.WIN_CLOSED:
            return False
        self.state_output["etat"].update(state)
        self.state_output["altitude"].update(alt)
        self.state_output["vitesse"].update(speed)
        self.state_output["puissance"].update(power)
        return True
    
    def check_values_validity(self, values):
        is_valid = [True, True, True]
        
        if not 0.0 < values[0] < 40000.0:
            is_valid[0] = False
            gui.popup("L'altitude entrée n'est pas valide")
        if not 0.0 < values[1] < 800.0:
            is_valid[1] = False
            gui.popup("Le taux entrée n'est pas valide")
        if not -16.0 < values[2] < 16.0:
            is_valid[2] = False
            gui.popup("L'angle entrée n'est pas valide")

        return is_valid

    def convertable_to_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False