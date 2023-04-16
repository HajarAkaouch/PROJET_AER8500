import PySimpleGUI as gui

# Define the layout
gui.theme('Darkblue4')  
input_layout = [
    [gui.Text("État:",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center"),
     gui.Text("Altitude:",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center")],
    [gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "etat"),
     gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "altitude")],
    [gui.Text("Vitesse:",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center"),
     gui.Text("Puissance:",font =('Arial', 20), size=(15, 1), text_color="white", justification = "center")],
    [gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "vitesse"),
     gui.Text(font =('Arial', 20), size=(15, 4), text_color="white", justification = "center", background_color='#a8a2dc', border_width=10, key = "puissance")]
]
# Create the window
window = gui.Window('Box Example', input_layout)

# Read events from the window
while True:
    event, values = window.read()
    if event == gui.WIN_CLOSED:
        break

# Close the window
window.close()
