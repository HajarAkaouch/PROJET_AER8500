import PySimpleGUI as gui

class Interface:
    def __init__(self, name, age):
        gui.theme('Darkblue4')     
        state_layout = [
        [gui.Text("État:",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center"),
         gui.Text("Altitude:",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center")],
        [gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "etat"),
         gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "altitude")],
        [gui.Text("Vitesse:",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center"),
         gui.Text("Puissance:",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center")],
        [gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "vitesse"),
         gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "puissance")]
        ]
        
        input_layout = [
            [gui.T(' ' * 50), gui.Text('Panneau usager', font =('Arial', 20), justification ='center', pad=(1,10))],
            [gui.Text('Altitude désiré:',font =('Arial', 15), size =(15, 1)), gui.InputText(do_not_clear=False)],
            [gui.Text('Taux de montée:', font =('Arial', 15), size =(15, 1)), gui.InputText(do_not_clear=False)],
            [gui.Text("Angle d'attaque:", font =('Arial', 15), size =(15, 1)), gui.InputText(do_not_clear=False)],
            [gui.Text("Alt enregistrée :", font =('Arial', 10),text_color="#e5ecf5"), 
             gui.Text(font =('Arial', 10), size =(10, 1),text_color="#e5ecf5", key = "alt"),
             gui.Text("Taux enregistré :", font =('Arial', 10), text_color="#e5ecf5"), 
             gui.Text(font =('Arial', 10), size =(10, 1),text_color="#e5ecf5", key = "taux"),
             gui.Text("Angle enregistré :", font =('Arial', 10), text_color="#e5ecf5"), 
             gui.Text(font =('Arial', 10), size =(10, 1),text_color="#e5ecf5", key = "angle")],
            [gui.T(' ' * 45), gui.Submit("Confirmer",size=(10,2)), gui.T(' ' * 5), gui.Cancel("Annuler",size=(10,2))]
        ]
        self.user_input = gui.Window('Panneau usager', input_layout)
        self.state_output = gui.Window('Panneau usager', state_layout)

    def close_windows(self):
        self.user_input.close()
        self.state_output.close()

    def input_window(self):
        event, values = self.user_input.read(timeout=20) 
        if event == "Exit" or event == gui.WIN_CLOSED:
            return False
        if event == "Confirmer":
            if values[0] != '':
                self.user_input['alt'].update(values[0])
            if values[1] != '':
                self.user_input['taux'].update(values[1])
            if values[2] != '':
                self.user_input['angle'].update(values[2])
        return True
            

    def state_window(self, state, alt, speed, power):
        event = self.user_input.read(timeout=20) 
        if event == "Exit" or event == gui.WIN_CLOSED:
            return False
        self.state_output["etat"].update(state)
        self.state_output["altitude"].update(alt)
        self.state_output["vitesse"].update(speed)
        self.state_output["puissance"].update(power)
        
        return True
           