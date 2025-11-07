import maya.cmds as mc
from maya import OpenMayaUI as omui
from shiboken6 import wrapInstance
from PySide6 import QtUiTools, QtCore, QtWidgets
import pathlib





COLOUR_INDEX = {'Dark Red': 4, 'Red': 13, 
                'Dark Brown': 11, 'Dark Orange': 12, 'Brown': 10, 'Light Brown': 24, 'Beige': 21, 
                'Dark Yellow': 25, 'Yellow': 17,  'Light Yellow': 22,
                'Dark Green': 7, 'Medium Green': 23, 'Green': 14, 'Light Green': 26,
                'Dark Turquoise': 27, 'Turquoise': 28, 'Light Turquoise': 19,  
                'Navy Blue': 5, 'Dark Blue': 15, 'Blue': 6, 'Medium Blue': 29, 'Light Blue': 18, 
                'Dark Purple': 8, 'Lavender': 30, 
                'Magenta': 9, 'Pink': 31, 'Light Pink': 20,
                'Black': 1, 'Dark Grey': 2, 'Light Grey': 3, 'White': 16,
                'Default': 0 
                }



class CtrlColourPicker(QtWidgets.QWidget):
    def __init__(self, parent = None):
        """
        Initialize class.
        """
        super(CtrlColourPicker, self).__init__(parent = parent)
        self.setWindowFlags(QtCore.Qt.Window)
        #Set the filePath to wherever this file is located.
        self.widgetPath = pathlib.Path(__file__).parent.resolve()
        print(f"Searching in {self.widgetPath} for widget.")
        #Set the fileName.
        self.widget = QtUiTools.QUiLoader().load(str(self.widgetPath) + '\\CtrlColourPickerUI.ui')
        self.widget.setParent(self)
        # set initial window size
        self.resize(360, 130)      
        # locate and set up UI widgets
        self.colourCtrlBtn = self.widget.findChild(QtWidgets.QPushButton, 'ColourButton')
        self.colourCtrlBtn.clicked.connect(self.colourCtrls)
        self.savedCtrls = []

        self.comboBox = self.widget.findChild(QtWidgets.QComboBox, "ColourPicker_ComboBox")
        #Populate the comboBox with the colours from the COLOUR_INDEX dictionary
        for colour in COLOUR_INDEX.keys():
            self.comboBox.addItem(colour)

        self.displayFrame = self.widget.findChild(QtWidgets.QFrame, "DisplayFrame")  
        # self.colourDisplay = mc.canvas(parent=self.displayFrame, hsvValue=(0.5, 0.5, 0.5))
        



    def colourCtrls(self, *args):
        """
        Recolours the currently or last selected controls using the colour selected in the comboBox.
        """
        ctrls = mc.ls(sl=True, type="transform")
        if len(ctrls) < 1:
            if len(self.savedCtrls) > 0:
                ctrls = self.savedCtrls
            else:
                print("Select at least one curve to colour.")
        for x in range(0, len(ctrls)):
                    chosenCtrl = ctrls[x]
                    #List all shape nodes under the selected control.
                    ctrlShapes = mc.listRelatives(chosenCtrl, shapes=True)
                    for ctrlShape in ctrlShapes:
                        try:
                            #Enable drawing Overrides on the selected shape node.
                            mc.setAttr(ctrlShape+".overrideEnabled", 1)
                            #Get the currently selected colour from the comboBox and its index value.
                            selectedColour = self.comboBox.currentText()
                            colourIndex = COLOUR_INDEX[selectedColour]
                            #Set the control's colour.
                            mc.setAttr(ctrlShape+".overrideColor", int(colourIndex))
                        except RuntimeError:
                            print(f"Something is preventing {ctrlShape} from being recoloured.")
                            continue
        mc.select(clear=True)
        self.savedCtrls = ctrls




def openWindow():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QtWidgets.QApplication.allWindows()):
            if 'myToolWindowName' in win.objectName(): # update this name to match name below
                win.destroy()

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    CtrlColourPicker.window = CtrlColourPicker(parent = mayaMainWindow)
    CtrlColourPicker.window.setObjectName('myToolWindowName') # code above uses this to ID any existing windows
    CtrlColourPicker.window.setWindowTitle('Control Colour Picker')
    CtrlColourPicker.window.show()

