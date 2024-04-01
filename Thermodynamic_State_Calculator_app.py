import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGroupBox, QLabel, QHBoxLayout, \
    QRadioButton, QPushButton, QLineEdit
from pyXSteam.XSteam import XSteam


class ThermoStateCalcApp(QMainWindow):
    """
    A QMainWindow-based application that calculates thermodynamic properties
    for two states and the change between them using the pyXSteam library.
    """

    def __init__(self):
        """
        Initializes the main window, sets the window title and geometry, and creates
        an instance of the XSteam class for thermodynamic property calculations.
        """
        super().__init__()

        self.setWindowTitle("Thermodynamic State Calculator")
        self.setGeometry(100, 100, 600, 400)

        self.steam = XSteam(XSteam.UNIT_SYSTEM_MKS)  # Initialize in SI units

        self.initUI()

    def initUI(self):
        """
        Initializes the user interface, creating and arranging all the widgets in the main window.
        """
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.specPropGroupBox = QGroupBox("Specified Properties")
        self.state1GroupBox = QGroupBox("State 1")
        self.state2GroupBox = QGroupBox("State 2")
        self.stateChangeGroupBox = QGroupBox("State Change")

        self.state1Prop1Label = QLabel("Pressure (P):")
        self.state1Prop1Edit = QLineEdit()
        self.state1Prop2Label = QLabel("Temperature (T):")
        self.state1Prop2Edit = QLineEdit()

        self.state2Prop1Label = QLabel("Pressure (P):")
        self.state2Prop1Edit = QLineEdit()
        self.state2Prop2Label = QLabel("Temperature (T):")
        self.state2Prop2Edit = QLineEdit()

        self.calculateButton = QPushButton("Calculate")
        self.calculateButton.clicked.connect(self.calculateProperties)

        self.unitsGroupBox = QGroupBox("Units")
        self.siRadioButton = QRadioButton("SI")
        self.enRadioButton = QRadioButton("English")
        self.siRadioButton.setChecked(True)  # Default to SI units

        self.state1Label = QLabel()
        self.state2Label = QLabel()
        self.stateChangeLabel = QLabel()

        self.layoutUI()

    def layoutUI(self):
        """
        Arranges the UI components within the main window.
        """
        layout = QVBoxLayout()

        unitsLayout = QHBoxLayout()
        unitsLayout.addWidget(self.siRadioButton)
        unitsLayout.addWidget(self.enRadioButton)
        self.unitsGroupBox.setLayout(unitsLayout)

        state1Layout = QVBoxLayout()
        state1Layout.addWidget(self.state1Prop1Label)
        state1Layout.addWidget(self.state1Prop1Edit)
        state1Layout.addWidget(self.state1Prop2Label)
        state1Layout.addWidget(self.state1Prop2Edit)
        self.state1GroupBox.setLayout(state1Layout)

        state2Layout = QVBoxLayout()
        state2Layout.addWidget(self.state2Prop1Label)
        state2Layout.addWidget(self.state2Prop1Edit)
        state2Layout.addWidget(self.state2Prop2Label)
        state2Layout.addWidget(self.state2Prop2Edit)
        self.state2GroupBox.setLayout(state2Layout)

        stateChangeLayout = QHBoxLayout()
        stateChangeLayout.addWidget(self.state1Label)
        stateChangeLayout.addWidget(self.state2Label)
        stateChangeLayout.addWidget(self.stateChangeLabel)
        self.stateChangeGroupBox.setLayout(stateChangeLayout)

        specPropLayout = QVBoxLayout()
        specPropLayout.addWidget(self.state1GroupBox)
        specPropLayout.addWidget(self.state2GroupBox)
        specPropLayout.addWidget(self.unitsGroupBox)
        specPropLayout.addWidget(self.calculateButton)
        self.specPropGroupBox.setLayout(specPropLayout)

        layout.addWidget(self.specPropGroupBox)
        layout.addWidget(self.stateChangeGroupBox)

        self.centralWidget.setLayout(layout)

    def calculateProperties(self):
        """
        Calculates and displays the thermodynamic properties for two states based on user inputs.
        Also calculates and displays the change between these two states.
        Assumes that the inputs are pressure and temperature for simplicity.
        """
        p1 = float(self.state1Prop1Edit.text())
        t1 = float(self.state1Prop2Edit.text())
        p2 = float(self.state2Prop1Edit.text())
        t2 = float(self.state2Prop2Edit.text())

        # Convert to SI units if English units are selected
        if self.enRadioButton.isChecked():
            p1 = self.convertToSI(p1, 'pressure')
            t1 = self.convertToSI(t1, 'temperature')
            p2 = self.convertToSI(p2, 'pressure')
            t2 = self.convertToSI(t2, 'temperature')

        h1 = self.steam.h_pt(p1, t1)
        h2 = self.steam.h_pt(p2, t2)

        delta_h = h2 - h1

        self.state1Label.setText(f"State 1 Enthalpy: {h1:.2f} kJ/kg")
        self.state2Label.setText(f"State 2 Enthalpy: {h2:.2f} kJ/kg")
        self.stateChangeLabel.setText(f"Difference in Enthalpy: {delta_h:.2f} kJ/kg")

    def convertToSI(self, value, prop_type):
        """
        Converts the given value from English units to SI units based on the property type.

        :param value: The value to convert.
        :param prop_type: The type of property ('pressure' or 'temperature').
        :return: The value converted to SI units.
        """
        if prop_type == 'pressure':
            return value * 0.06895  # Example conversion factor for psi to bar
        elif prop_type == 'temperature':
            return (value - 32) * 5.0 / 9.0  # Example conversion factor for Fahrenheit to Celsius
        return value


if __name__ == "__main__":
    app = QApplication(sys.argv)
    thermoStateCalcApp = ThermoStateCalcApp()
    thermoStateCalcApp.show()
    sys.exit(app.exec_())
