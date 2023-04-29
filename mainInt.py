import sys
import json
sys.path.append("./GestionClient/")
from GestionClient import Client
from GestionClient import editClient as ec

sys.path.append("./GestionVoiture/")
from GestionVoiture import car
from GestionVoiture import brand

sys.path.append("./Scraping/")
from Scraping import scraping

sys.path.append("./Tools/")
from Tools import Tool


from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QFont

from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QLabel, QTableWidget, QHeaderView
from GestionClient import ReservationClient as rc
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,login,choix,admin_o_n):
        super().__init__()
        self.ui = uic.loadUi("main_ui.ui", self)
        self.ui.full_menu_widget.setVisible(False)
        self.client_dict = dict()
        pixmap = QtGui.QPixmap("./icon/Logo.png")
        self.ui.main_logo.setPixmap(pixmap)
        self.ui.home_Btn.setIcon(QtGui.QIcon("./icon/home-4-32.ico"))
        self.ui.home_btn_2.setIcon(QtGui.QIcon("./icon/home-4-48.ico"))
        self.ui.change_btn.setIcon(QtGui.QIcon("./icon/menu-4-32.ico"))
        self.ui.search_btn.setIcon(QtGui.QIcon("./icon/search-13-48.ico"))
        self.ui.dashborad_btn.setIcon(QtGui.QIcon("./icon/dashboard-5-32.ico"))
        self.ui.dashborad_btn_2.setIcon(QtGui.QIcon("./icon/dashboard-5-48.ico"))
        self.ui.exit_btn.setIcon(QtGui.QIcon("./icon/close-window-64.ico"))
        self.ui.exit_btn_2.setIcon(QtGui.QIcon("./icon/close-window-64.ico"))
        self.ui.client_btn.setIcon(QtGui.QIcon("./icon/group-32.ico"))
        self.ui.client_btn_2.setIcon(QtGui.QIcon("./icon/group-48.ico"))
        self.ui.exit_btn_2.setIcon(QtGui.QIcon("./icon/close-window-64.ico"))
        self.ui.cars_btn.setIcon(QtGui.QIcon("./icon/car.png"))
        self.ui.cars_btn_2.setIcon(QtGui.QIcon("./icon/car.png"))
        self.ui.users_btn.setIcon(QtGui.QIcon("./icon/activity-feed-32.ico"))
        self.ui.users_btn_2.setIcon(QtGui.QIcon("./icon/activity-feed-48.ico"))
        self.ui.user_info_btn.setIcon(QtGui.QIcon("./icon/user-48.ico"))
        self.ui.reservation_btn2.setIcon(QtGui.QIcon("./icon/user-48.ico"))

        self.ui.client_btn_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_clients))
        self.ui.client_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_clients))

        self.ui.users_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_users))

        self.ui.cars_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_cars))
        self.ui.cars_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_cars))

        self.ui.liste_noire_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_noire_clients))

        self.ui.reserv.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_reserv))

        self.ui.clients_data.clicked.connect(self.handlClick)
        self.client = Client.Client()

        #setting the CRUD user to disabled view to the privilege of the admin :
        self.ui.users_btn.setEnabled(admin_o_n)
        if(not admin_o_n):
            self.users_btn.setStyleSheet('color: #788596')
            self.ui.user_label.setText(self.ui.user_label.text() + " Employé")
        else: self.ui.user_label.setText(self.ui.user_label.text() + " Admin")
        #linking the update button with the update method:
        self.ui.modifier_btn.clicked.connect(self.updateTable)
        self.ui.supprimer_btn.clicked.connect(self.deleteButtonClient)
        self.ui.comboClients.currentIndexChanged.connect(self.searchByComboClient)
        self.ui.comboClients_2.currentIndexChanged.connect(self.searchByComboClient)
        self.ui.reservation_client_btn.clicked.connect(self.selectReservationClient)

        self.displayClients(f"select su.idUser,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser ",self.ui.clients_data)
        self.displayClients(f"select su.idUser,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser where liste_noire = '{1}'",self.ui.page_noire_data)
        '''
        self.ui.drop_down_two.setVisible(self.visible)
        self.ui.dropBtn.clicked.connect(self.dropMenu)
        self.login_name.setText(self.login_name.text() + login)
       '''
        self.displayReservations()
        self.fillComboClient(self.ui.comboClients, "SELECT client.idUser,nom from client join utilisateur on client.idUser = utilisateur.idUser")
        self.fillComboClient(self.ui.comboClients_2, f"SELECT client.idUser,nom from client join utilisateur on client.idUser = utilisateur.idUser WHERE liste_noire = '{1}'")

     ########################################### Car Section ##########################################################
        self.dict_brands = dict()
        self.dict_fuel = dict()
        self.imagePath = ""

        self.scraping = scraping.scrap()
        self.car = car.Car()
        self.brand = brand.Brand()
        self.tool = Tool.tool()


        self.ui.tableWidgetCar.clearContents()
        # load combobox
        self.fill_combobox(self.ui.comboBoxFuel)
        self.fill_combobox(self.ui.comboAllBrand)
        self.fill_combobox(self.ui.comboBoxBrand)
        print("2")
        # Retrieve data from the database
        car_data = self.car.getCar("SELECT * FROM voiture;")
        self.displayCars(car_data)
        print("5")
        # linking the update button with the update method:
        self.ui.comboBoxBrand.currentIndexChanged.connect(self.id_SelectedBrand)
        self.ui.comboBoxFuel.currentIndexChanged.connect(self.id_SelectedFuel)
        self.ui.comboAllBrand.currentIndexChanged.connect(self.id_SelectedAllBrand)
        self.ui.AddButton.clicked.connect(self.addCarButton)
        self.addImage.clicked.connect(self.image_dialog)
        self.ui.search_input.textChanged.connect(self.sync_SearchLine)
        print("6")

     ###############################################################################################################

    def selectReservationClient(self):
        if(bool(self.client_dict) == True):
            reservations = self.client.getValuePairDataClient(
                f"SELECT idCar,date_depart,date_arr FROM RESERVATION WHERE idUser = '{self.client_dict['idUser']}'")
            reservation_client_ui = rc.ReservationClient(reservations)
            reservation_client_ui.show()
        else:
            print("Try to click on a client")
            self.client_dict.clear()
    def messageBox(self, field):
        message = QtWidgets.QMessageBox.question(None, "Confirmation",f"{field} : {self.client_dict['idUser']}", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        return message
    def updateTable(self):
        if(bool(self.client_dict)) == True:

            if (self.messageBox("etes vous sure de le modifier") == QtWidgets.QMessageBox.Yes):
                edit_client = ec.EditClient(self.client_dict)
                edit_client.show()
            else:
                print("NO")
            self.client_dict.clear()
        else:
            print("try to click on a client")
    def deleteButtonClient(self):
        if (bool(self.client_dict)) == True:

            if (self.messageBox("Etes vous sure de le supprimer")  == QtWidgets.QMessageBox.Yes):
                self.client.supprimerClient(self.client_dict['idUser'])
            else:
                print("NO")
            self.client_dict.clear()
        else:
            print("try to click on a client")
    def displayClients(self,request,table):
        table.clearContents()  # Clear the existing data in the table
        table.setColumnCount(12)  # Set the number of columns in the table
        table.setHorizontalHeaderLabels(['idUser', 'Adresse', 'nom', 'prenom','societe','cin','tel','ville','permis','passport','observation','liste_noire'])  # Set the column labels

        users = self.client.getClientsData(request)
        table.setRowCount(len(users))  # Set the number of rows in the table
        #adding select check mark :

        for row_idx, user in enumerate(users):
            for col_idx, item in enumerate(user):
                table.setItem(row_idx, col_idx,
                                             QTableWidgetItem(str(item)))  # Set the table item with the data

        for row in range(table.rowCount()):
            for column in range(self.ui.clients_data.columnCount()):
                item = self.ui.clients_data.item(row, column)
                if item is not None:
                    column_name = self.ui.clients_data.horizontalHeaderItem(column).text()
                    if(column_name == "liste_noire" and int(item.text()) == 1):
                        item.setBackground(QtGui.QColor("red"))
                    elif (column_name == "liste_noire" and int(item.text()) == 0):
                        item.setBackground(QtGui.QColor("green"))
        table.resizeColumnsToContents()  # Resize the columns to fit the content
    def dropMenu(self):
        if(self.visible == True):
            self.visible = False
        else:
            self.visible = True
        self.ui.drop_down_two.setVisible(self.visible)
    def exitApp(self):
        QtWidgets.QApplication.exit()
    def handlClick(self,index:QtCore.QModelIndex):
        row = index.row()
        column = index.column()
        #to get the current row and the idUser which is 0 order
        for column in range(self.ui.clients_data.columnCount()):
            item = self.ui.clients_data.item(row, column)
            if item is not None:
                column_name = self.ui.clients_data.horizontalHeaderItem(column).text()
                self.client_dict[column_name] = item.text()


    def displayReservations(self):
        self.ui.reservation_data.clearContents()  # Clear the existing data in the table
        self.ui.reservation_data.setColumnCount(3)  # Set the number of columns in the table
        self.ui.reservation_data.setHorizontalHeaderLabels(
            ['idUser', 'idCar', 'date'])  # Set the column labels

        users = self.client.getClientsData("SELECT * FROM RESERVATION")
        print(users)
        self.ui.reservation_data.setRowCount(len(users))  # Set the number of rows in the table
        tab = ["edit.png", "voir.png"]

        # adding select check mark :

        for row_idx, user in enumerate(users):
            for col_idx, item in enumerate(user):
                self.ui.reservation_data.setItem(row_idx, col_idx,
                              QTableWidgetItem(str(item)))  # Set the table item with the data

    def fillComboClient(self,combo,request):
        diction_client = self.client.getValuePairDataClient(request)
        combo.addItem('Selectionner client')
        for key, value in diction_client.items():
            combo.addItem(value)
            # Set the key as custom data for the item
            combo.setItemData(combo.count() - 1, key)
    def searchByComboClient(self,condition):
        if (self.ui.comboClients.currentData() is not None):
            self.displayClients(f"SELECT su.idUser,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser where su.idUser = '{self.ui.comboClients.currentData()}'",self.ui.clients_data)
        else:
            self.displayClients(
                f"select su.idUser,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser ",
                self.ui.clients_data)

    ############################################## Car Section ########################################################
    def sync_SearchLine(self, text):
        # Retrieve data from the database
        car_data = self.car.searchByModel(text)
        self.displayCars(car_data)
    def addCarButton(self):
        try:
            brand = self.id_SelectedBrand()
            model = self.ui.model.text()
            fuel = self.id_SelectedFuel()

            if brand == "":
                self.tool.warning("Please enter a model.")
            elif self.comboBoxBrand.currentIndex() == 0:
                self.tool.warning( "Please select a brand.")
            elif self.comboBoxFuel.currentIndex() == 0:
                self.tool.warning( "Please select a fuel type.")
            elif self.imagePath == "":
                self.tool.warning( "Please select an image.")
            else:
                img = self.tool.convertToBinary(self.imagePath)
                self.car.addCar(brand, model, fuel,img)
                # Retrieve data from the database
                car_data = self.car.getCar("SELECT * FROM voiture;")
                self.displayCars(car_data)
        except Exception as e:
            print(f"addCarButton : An error occurred: {e}")
    def displayCars(self,data):
        try:
            self.ui.tableWidgetCar.clearContents()  # Clear the existing data in the table
            self.ui.tableWidgetCar.setColumnCount(
                5)  # Set the number of columns in the table, including the image column
            self.ui.tableWidgetCar.setHorizontalHeaderLabels(
                ["Image", "idCar", "idMarque", "idCarburant", "Model"])  # Set the column labels
            self.ui.tableWidgetCar.setRowCount(len(data))  # Set the number of rows in the table

            for row_idx, car in enumerate(data):
                label = QLabel()  # Create a QLabel to display the image
                label.setScaledContents(True)  # Set the label to scale its contents
                label.setMaximumSize(80, 80)
                pixmap = self.tool.getImageLabel(car[3])  # Get QPixmap from binary data
                label.setPixmap(pixmap)

                self.ui.tableWidgetCar.setCellWidget(row_idx, 0,  label)  # Set the label as the cell widget for the image column

                self.ui.tableWidgetCar.setItem(row_idx, 1, QTableWidgetItem(str(car[0])))

                self.ui.tableWidgetCar.setItem(row_idx, 2, QTableWidgetItem(str(self.dict_brands[car[1]])))
                self.ui.tableWidgetCar.setItem(row_idx, 3, QTableWidgetItem(str(self.dict_fuel[car[2]])))
                self.ui.tableWidgetCar.setItem(row_idx, 4, QTableWidgetItem(str(car[4])))

        except Exception as e:
            print(f"addCarButton : An error occurred: {e}")

        self.ui.tableWidgetCar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.tableWidgetCar.verticalHeader().setDefaultSectionSize(80)  # Set default row height
        font = QFont()
        font.setBold(True)
        self.ui.tableWidgetCar.horizontalHeader().setFont(font)

        # Set row height
        self.ui.tableWidgetCar.verticalHeader().setDefaultSectionSize(80)

        # Set alternating row colors
        self.ui.tableWidgetCar.setAlternatingRowColors(True)
        self.ui.tableWidgetCar.setStyleSheet("alternate-background-color: gray;")
        self.ui.tableWidgetCar.setStyleSheet("background-color: white;  ")

        # Set table dimensions
        self.ui.tableWidgetCar.setMinimumSize(500, 500)

        # Set sorting behavior for columns
        self.ui.tableWidgetCar.setSortingEnabled(True)

        # Set selection mode to row selection
        self.ui.tableWidgetCar.setSelectionBehavior(QTableWidget.SelectRows)

    def id_SelectedBrand(self):
        selected_index = self.comboBoxBrand.currentIndex()
        # Get the item key using the selected index
        key = self.comboBoxBrand.itemData(selected_index, QtCore.Qt.UserRole)  # Retrieve custom data using UserRole
        # Get the value of the selected item
        value = self.comboBoxBrand.itemText(selected_index)
        # Print the retrieved text and data
        print("value: ", value)
        print("key: ", key)

        if key is not None:
            # Retrieve data from the database based on the selected item
            car_data = self.car.searchByIdBrand(key)
            self.displayCars(car_data)
            return key
    def id_SelectedFuel(self):
        selected_index = self.comboBoxFuel.currentIndex()
        # Get the item key using the selected index
        key = self.comboBoxFuel.itemData(selected_index, QtCore.Qt.UserRole)  # Retrieve custom data using UserRole
        # Get the value of the selected item
        value = self.comboBoxFuel.itemText(selected_index)
        # Print the retrieved text and data
        print("value: ", value)
        print("key: ", key)

        if key is not None:
            # Retrieve data from the database based on the selected item
            car_data = self.car.searchByIdFuel(key)
            self.displayCars(car_data)
            return key
    def id_SelectedAllBrand(self):
        selected_index = self.comboAllBrand.currentIndex()
        # Get the item key using the selected index
        key = self.comboAllBrand.itemData(selected_index, QtCore.Qt.UserRole)  # Retrieve custom data using UserRole
        # Get the value of the selected item
        value = self.comboAllBrand.itemText(selected_index)
        # Print the retrieved text and data
        print("value: ", value)
        print("key: ", key)

        if key is not None:
            # Retrieve data from the database based on the selected item
            car_data = self.scraping.getCarsByBrand(value)
            print(car_data)

    def image_dialog(self):
        try:
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Image files (*.jpg *.jpeg *.png *.bmp)")
            if file_dialog.exec_():
                file_path = file_dialog.selectedFiles()[0]

                self.imagePath = file_path
                pixmap = QPixmap(file_path)
                # Set the desired size
                desired_size = QtCore.QSize(250, 250)  # Width, Height
                # Scale the pixmap to the desired size
                pixmap = pixmap.scaled(desired_size, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap)
                self.image_label.adjustSize()
        except Exception as e:
            print(f"An error occurred: {e}")


    def fill_combobox(self,combo):
        print(1)
        try:
            self.comboBoxBrand.clear()
            data = dict()
            if combo.objectName() == 'comboBoxBrand':
                combo.addItem('Select Brand')
                data = self.brand.getBrands()
                self.dict_brands = data
            elif combo.objectName() == 'comboBoxFuel':
                combo.addItem('Select Carburant')
                data = self.car.getFuel()
                self.dict_fuel = data
            elif combo.objectName() == 'comboAllBrand':
                combo.addItem('Select Brand')
                data = self.scraping.getCarBrandAll()

            for key, value in data.items():
                combo.addItem(value)
                combo.setItemData(combo.count() - 1, key)

        except Exception as e:
            print(f"Error: {e}")
