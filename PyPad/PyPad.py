import os
import sys
import threading
import PySimpleGUI as sg

version = "0.0.1"

class PyPadGUI:    
    def saveMenu(self):
        sg.theme("DarkBlue")
        layout = [
            [sg.Text("Save Untitled as")],
            [sg.FileSaveAs(), sg.InputText(key="saveLocation")],
            [sg.Button("Save"), sg.Button("Cancel")],
        ]
        window = sg.Window("Save file as", layout=layout)
        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == "Cancel":
                window.close()
                return None
            
            if event == "Save":
                window.close()
                return values['saveLocation']
    
    def openFileMenu(self, currentWindowInstance):
        sg.theme("DarkBlue")
        layout = [
            [sg.Text("Open file")],
            [sg.FileBrowse(), sg.InputText(key="openFile")],
            [sg.Button("Open"), sg.Button("Cancel")],
        ]
        window = sg.Window("Open file", layout=layout)
        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == "Cancel":
                window.close()
                break
            
            if event == "Open":
                window.close()
                currentWindowInstance.close()
                self.editor(values["openFile"])
                break
    
    def newFile(self, currentWindowInstance):
        currentWindowInstance.close()
        self.blankEditor()

    def blankEditor(self):
        sg.theme("DarkBlue")
        layout = [
            [sg.Text(f"Untitled", font=("Arial", 10)), sg.Button("New"),sg.Button("Save"), sg.Button("Open"), sg.Button("Close")],
            [sg.Multiline(f"", size=(100, 50), key="editArea")],
        ]
        window = sg.Window(f"PyPad v{version} - Untitled", layout=layout)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == "Close":
                if not values["editArea"]:
                    break

                enter = sg.popup_yes_no("Alert\nYou have unsaved work\nAre you sure you want to close?")
                if enter == "Yes":
                    break

            if event == "Save":
                saveFile = self.saveMenu()
                if saveFile:
                    with open(saveFile, "w") as f:
                        f.write(values["editArea"])
                    window.close()
                    self.editor(saveFile)
                    break
            
            if event == "Open":
                self.openFileMenu(window)
                break

            if event == "New":
                enter = sg.popup_yes_no("Alert\nYou are about to create a new instance. This will make you loose all of your current work!\nCreate new instance anyway")
                if enter == "Yes":
                    self.newFile(window)
                    break

    def editor(self, file):
        with open(file, "r") as f:
            fileData = f.read()
            
        sg.theme("DarkBlue")
        layout = [
            [sg.Text(f"{file}", font=("Arial", 10)), sg.Button("New"), sg.Button("Save"), sg.Button("Open"), sg.Button("Close")],
            [sg.Multiline(f"{fileData}", size=(100, 50), key="editArea")],
        ]
        window = sg.Window(f"PyPad v{version} - {file}", layout=layout)

        while True:
            event, values = window.read()

            with open(file) as f:
                currentState = f.read()

            if event == sg.WINDOW_CLOSED:
                break
            
            if event == "Close":
                if values["editArea"] != currentState:
                    enter = sg.popup_yes_no("Alert\nYou have unsaved work\nAre you sure you want to close?")
                    if enter == "Yes":
                        break
                else:
                    break

            if event == "Save":
                with open(file, "w") as f:
                    f.write(values["editArea"])
            
            if event == "Open":
                self.openFileMenu(window)
                break

            if event == "New":
                enter = sg.popup_yes_no("Alert\nYou are about to create a new instance. This will make you loose all of your current work!\nCreate new instance anyway")
                if enter == "Yes":
                    self.newFile(window)
                    break

gui = PyPadGUI()

if len(sys.argv) == 2:
    if os.path.exists(sys.argv[1]):
        gui.editor(sys.argv[1])
    else:
        print(f"Could not locate {sys.argv[1]}")
elif len(sys.argv) == 1:
    gui.blankEditor()