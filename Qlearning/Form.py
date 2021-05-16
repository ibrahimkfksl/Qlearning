import PySimpleGUI as sg
  

sg.theme('LightGrey 6')     
  
layout = [
    [sg.Text('Please enter information')],
    [sg.Text('Matrix Size', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
  
window = sg.Window('Qlearning App', layout)
event, value = window.read()
window.close()
size = value[0]
size = size.split(",") #matrix size as array

