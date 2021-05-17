import PySimpleGUI as sg
from Matrix import Matrix

class Form:
    def FormPage(self):
        sg.theme('LightGrey 6')     
        layout = [
            [sg.Text('Please enter information')],
            [sg.Text('Start Location', size =(15, 1)), sg.InputText()],
            [sg.Text('Finish Location', size =(15, 1)), sg.InputText()],
            [sg.Text('Matrix Size', size =(15, 1)), sg.InputText()],
            [sg.Submit(), sg.Cancel()]
        ]
        
        window = sg.Window('Qlearning App', layout)
        event, value = window.read()
        window.close()
        return value


form = Form()
value = form.FormPage()

start = value[0]
finish = value[1]
size = value[2]
size = size.split(",") #matrix size as array
Matrix(size[0],size[1], start, finish)