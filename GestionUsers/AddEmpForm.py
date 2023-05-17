from PyQt5 import QtCore, QtGui, QtWidgets, uic
import conn
import sys
import user
import string
import random
class AddEmp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #self.tool = Tool.tool()
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.user = user.User()
        self.ui = uic.loadUi("../main/AddEmpForm_ui.ui",self)
        self.ui.genererPass.clicked.connect(self.generateRandomPassword)
        self.ui.valider_btn_emp.clicked.connect(self.AddButtonEmployee)



    def AddButtonEmployee(self):
        try:
            employee_dict= dict()
            employee_dict['nom'] = self.ui.nom.text()
            employee_dict['prenom'] = self.ui.prenom.text()
            employee_dict['login'] = self.ui.login.text()
            employee_dict['mdp'] = self.ui.mdp.text()
            employee_dict['address'] = self.ui.adresse.text()
            employee_dict['cin'] = self.ui.cin.text()

            employee_dict['phone'] = self.ui.phone.text()
            employee_dict['salary'] = float(self.ui.salary.value())

            employee_dict['admin'] = self.ui.choix_admin.currentIndex()

            if employee_dict['nom'] == "":
                self.tool.warning("Please enter a name.")
                return
            elif employee_dict['prenom'] == "":
                self.tool.warning("Please enter last name.")
                return
            elif employee_dict['login'] == "":
                self.tool.warning("enter a login.")
                return
            elif employee_dict['mdp'] == "":
                self.tool.warning("mdp")
                return
            elif employee_dict['address'] == "":
                self.tool.warning("address")
                return
            elif employee_dict['cin'] == "":
                self.tool.warning("cin")
                return
            elif employee_dict['phone'] == "":
                self.tool.warning("phone")
                return
            elif employee_dict['salary'] == "":
                self.tool.warning("salary")
                return
            elif employee_dict['phone'] == "":
                self.tool.warning("phone")
                return

            self.user.addEmployee(employee_dict)
            #self.tool.warning("user added ")


        except Exception as e:
            print(f"AddButtonEmployee :Error: {e}")




    def generateRandomPassword(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = str()
        for i in range(5):
            password += random.choice(characters)
        self.ui.mdp.setText(password)

    def clearField(self):
        self.ui.nom.seText("")
        self.ui.prenom.setText("")
        self.ui.login.setText("")
        self.ui.mdp.setText("")
        self.ui.adresse.setText("")
        self.ui.cin.setText("")
        self.ui.phone.setText("")
        self.ui.salary.setValue(0)
