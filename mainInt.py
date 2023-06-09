import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QFont, QIcon

sys.path.append("./GestionClient/")
from GestionClient import Client
from GestionClient import editClient as ec
from GestionClient import AjoutClientForm as af
sys.path.append("./GestionVoiture/")
from GestionVoiture import car
from GestionVoiture import fuel
from GestionVoiture import brand
from GestionVoiture import transmission

sys.path.append("./Scraping/")
from Scraping import scraping

sys.path.append("./Tools/")
from Tools import Convertion
from Tools import Tool
from PyQt5.QtCore import QDate


from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QApplication, QFileDialog, QLabel, QHeaderView, QPushButton
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
        # Set row height
        self.ui.clients_data.verticalHeader().setDefaultSectionSize(50)
        self.ui.page_noire_data.verticalHeader().setDefaultSectionSize(50)

        self.ui.client_btn_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_clients))
        self.ui.client_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_clients))

        self.ui.users_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_users))

        self.ui.cars_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_cars))
        self.ui.cars_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_cars))
        self.ui.scrap_cars_Btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_scarp_cars))
        self.ui.addCars_page_Btn.clicked.connect(lambda: (self.reset_AddCarpage() , self.ui.stackedWidget.setCurrentWidget(self.ui.page_add_car)) )

        self.ui.liste_noire_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_noire_clients))

        self.ui.reserv.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_reserv))

        self.ui.clients_data.clicked.connect(lambda: self.handlClick(self.ui.clients_data.currentIndex(),self.ui.clients_data))
        self.ui.reservation_data.clicked.connect(lambda: self.handlClick(self.ui.reservation_data.currentIndex(),self.ui.reservation_data))
        self.ui.page_noire_data.clicked.connect(lambda: self.handlClick(self.ui.page_noire_data.currentIndex(),self.ui.page_noire_data))
        self.client = Client.Client()

        self.ui.add_client_btn.clicked.connect(self.AjouterClient)

        #setting the CRUD user to disabled view to the privilege of the admin :
        self.ui.users_btn.setEnabled(admin_o_n)
        if(not admin_o_n):
            self.users_btn.setStyleSheet('color: #788596')
            self.ui.user_label.setText(self.ui.user_label.text() + " Employé")
        else: self.ui.user_label.setText(self.ui.user_label.text() + " Admin")
        #linking the update button with the update method:
        self.ui.modifier_btn.clicked.connect(self.updateTable)
        self.ui.modifier_btn2.clicked.connect(self.updateTable)

        self.ui.supprimer_reser.clicked.connect(self.deleteButtonReservation)
        self.ui.supprimer_btn.clicked.connect(lambda: self.deleteButtonClient(False))
        self.ui.supprimer_btn_3.clicked.connect(lambda: self.deleteButtonClient(True))
        self.ui.comboClients.currentIndexChanged.connect(lambda: self.searchByComboClient("",self.ui.comboClients,self.ui.clients_data))
        self.ui.comboClients_3.currentIndexChanged.connect(lambda: self.searchByComboClient("yes",self.ui.comboClients_3,self.ui.page_noire_data))
        self.ui.reservation_client_btn.clicked.connect(self.selectReservationClient)

        self.client.displayClients(f"select su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser ",self.ui.clients_data)
        self.client.displayClients(f"select su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser where liste_noire = '{1}'",self.ui.page_noire_data)
        '''
        self.ui.drop_down_two.setVisible(self.visible)
        self.ui.dropBtn.clicked.connect(self.dropMenu)
        self.login_name.setText(self.login_name.text() + login)
       '''
        self.client.displayReservations(self.ui.reservation_data)
        self.fillComboClient(self.ui.comboClients, "SELECT client.idUser,nom from client join utilisateur on client.idUser = utilisateur.idUser")
        self.fillComboClient(self.ui.comboClients_3, f"SELECT client.idUser,nom from client join utilisateur on client.idUser = utilisateur.idUser WHERE liste_noire = '{1}'")

     ########################################### Car Section ##########################################################
        try:
            print("car section:")
            self.dict_brands = dict()
            self.dict_Allbrands = dict()
            self.dict_fuel = dict()
            self.dict_gearbox = dict()

            self.imagePath = ""
            self.id_SelectedCar = None
            self.add_DataJson = False


            self.scraping = scraping.scrap()
            self.car = car.Car()
            self.brand = brand.Brand()
            self.fuel = fuel.Fuel()
            self.gearBox= transmission.Transmission()
            self.tool = Tool.tool()

            # load combobox
            print("# load combobox")
            self.dict_fuel = self.tool.fill_combobox(self.ui.comboBoxFuel)
            self.dict_Allbrands = self.tool.fill_combobox(self.ui.comboAllBrands)
            self.dict_brands = self.tool.fill_combobox(self.ui.comboBoxBrand)
            self.dict_fuel = self.tool.fill_combobox(self.ui.comboBoxFuel_1)
            self.dict_brands = self.tool.fill_combobox(self.ui.comboBoxBrand_1)
            self.dict_gearbox = self.tool.fill_combobox(self.ui.comboBoxGear_1)

            # Retrieve data from the database
            print("# Retrieve data from the database")
            car_data = self.car.getAll()
            self.displayCars(car_data)

            #linking comboBox with the update methods
            print("#linking comboBox with the update methods")
            self.ui.comboBoxBrand.currentIndexChanged.connect(lambda :self.id_SelectedCombobox(self.ui.comboBoxBrand))
            self.ui.comboBoxFuel.currentIndexChanged.connect(lambda : self.id_SelectedCombobox(self.ui.comboBoxFuel))
            self.ui.comboAllBrands.currentIndexChanged.connect(lambda :self.id_SelectedCombobox(self.ui.comboAllBrands))
            self.ui.comboAllModels.currentIndexChanged.connect(lambda : self.id_SelectedCombobox(self.ui.comboAllModels))
            # handle click table wisget
            self.ui.tableWidgetCar.clicked.connect(lambda: self.edit_Car(self.tool.handlClick(self.ui.tableWidgetCar.currentIndex(),self.ui.tableWidgetCar)))
            self.ui.tableWidgeModels.clicked.connect(lambda: self.redirect_to_AddCarPage(self.scraping.getCarByModel(self.ui.comboAllBrands.currentText(),self.ui.comboAllModels.currentText())))
            # linking the update button with the update method:
            print("# linking the update button with the update method")
            self.ui.add_image_Btn.clicked.connect(self.image_dialog)
            self.ui.search_input.textChanged.connect(self.sync_SearchLine)
            self.ui.all_cars_btn.clicked.connect(lambda : self.displayCars(self.car.getAll()))
            self.addcar_Btn.clicked.connect(self.addCar)

        except Exception as e:
            print(e)

    ###############################################################################################################

    def AjouterClient(self):
        try:
            ajout_client = af.AjoutClient(self.ui.clients_data)
            ajout_client.show()
        except Exception as e:
            print(e)

    def selectReservationClient(self):
            if (bool(self.client_dict) == True):
                reservations = self.client.getValuePairDataClient(
                    f"SELECT idCar,date_depart,date_arr FROM RESERVATION WHERE idUser = '{self.client_dict['idUser']}'")
                reservation_client_ui = rc.ReservationClient(reservations)
                reservation_client_ui.show()
            else:
                print("Try to click on a client")
            self.client_dict.clear()

    def messageBox(self, field):
        message = QtWidgets.QMessageBox.warning(None, "Confirmation",f"{field} : {self.client_dict['idUser']}", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        return message

    def updateTable(self):
        try:
            if(bool(self.client_dict)) == True:

                if (self.messageBox("etes vous sure de le modifier") == QtWidgets.QMessageBox.Yes):
                    edit_client = ec.EditClient(self.client_dict,self.ui.clients_data,self.ui.page_noire_data)
                    edit_client.show()
                else:
                    print("NO")
                self.client_dict.clear()
            else:
                print("try to click on a client")
        except Exception as e:
            print(e)
    def deleteButtonClient(self,liste_noire):
        try:
            if (bool(self.client_dict)) == True:
                if (self.messageBox(
                        "Etes vous sure de le supprimer la suppression de ce client va entrainer la suppression de toutes ces reservations !") == QtWidgets.QMessageBox.Yes):
                    self.client.supprimer(f"DELETE FROM CLIENT WHERE IDUSER = '{self.client_dict['idUser']}'")
                    print(f"liste_noire = {liste_noire}")
                    if(liste_noire):
                        print("page noire")
                        self.client.displayClients(
                            f"SELECT su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser where liste_noire = 1",
                            self.ui.page_noire_data)
                    else:
                        self.client.displayClients(
                            f"SELECT su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser ",
                            self.ui.clients_data)
                else:
                    print("NO")
                self.client_dict.clear()
            else:
                print("try to click on a client")
        except Exception as e:
            print(e)

    def deleteButtonReservation(self):
        if (bool(self.client_dict)) == True:
            if (self.messageBox("Etes vous sure de le supprimer la suppression de cet reservation !")  == QtWidgets.QMessageBox.Yes):
                print(f"DELETE FROM reservation WHERE idUser = '{self.client_dict['idUser']}' and idCar = '{self.client_dict['idCar']}'")
                self.client.supprimer(f"DELETE FROM reservation WHERE idUser = '{self.client_dict['idUser']}' and idCar = '{self.client_dict['idCar']}'")
                self.client.displayReservations(self.ui.reservation_data)
            else:
                print("NO")
            self.client_dict.clear()
        else:
            print("try to click on a reservation")

    def dropMenu(self):
        if(self.visible == True):
            self.visible = False
        else:
            self.visible = True
        self.ui.drop_down_two.setVisible(self.visible)
    def exitApp(self):
        QtWidgets.QApplication.exit()
    def handlClick(self,index:QtCore.QModelIndex,table):
        try:
            row = index.row()
            # to get the current row and the idUser which is 0 order
            for column in range(table.columnCount()):
                item = table.item(row, column)
                column_name = table.horizontalHeaderItem(column).text()
                if (item is not None):
                    self.client_dict[column_name] = item.text()
        except Exception as e:
            print(e)

    def fillComboClient(self,combo,request):
        try:
            diction_client = self.client.getValuePairDataClient(request)
            combo.addItem('Selectionner client')
            for key, value in diction_client.items():
                combo.addItem(value)
                # Set the key as custom data for the item
                combo.setItemData(combo.count() - 1, key)
        except Exception as e:
            print(e)

    def searchByComboClient(self,condition,comboBox,table):
        try:
            if (condition != ""):
                if (comboBox.currentData() is not None):
                    self.client.displayClients(
                        f"SELECT su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser where su.idUser = '{comboBox.currentData()}' and liste_noire = 1",
                        table)
                else:
                    self.client.displayClients(
                        f"select su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser where liste_noire = 1 ",
                        table)
            else:
                if (comboBox.currentData() is not None):
                    self.client.displayClients(
                        f"SELECT su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser where su.idUser = '{comboBox.currentData()}'",
                        table)
                else:
                    self.client.displayClients(
                        f"select su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser ",
                        table)
        except Exception as e:
            print(e)

    ############################################## Car Section ########################################################
    def sync_SearchLine(self, text):
        # Retrieve data from the database
        car_data = self.car.searchByModel(text)
        self.displayCars(car_data)


    def addCar(self):
        try:
            brand = self.id_SelectedCombobox(self.ui.comboBoxBrand_1)
            model = self.ui.model.text()
            fuel = self.id_SelectedCombobox(self.ui.comboBoxFuel_1)
            gearbox = self.id_SelectedCombobox(self.ui.comboBoxGear_1)


            if self.add_DataJson:
                if self.imagePath == "":
                    self.imagePath = "DataJson"

            if model == "":
                self.tool.warning("Please enter a model.")
                return
            elif self.comboBoxBrand_1.currentIndex() == 0:
                self.tool.warning("Please select a brand.")
                return
            elif self.comboBoxFuel_1.currentIndex() == 0:
                self.tool.warning("Please select a fuel type.")
                return
            elif self.comboBoxGear_1.currentIndex() == 0:
                self.tool.warning("Please select a transmission type.")
                return

            elif self.ui.price.text() == "":
                self.tool.warning("Please enter a price type.")
                return
            elif self.ui.power.text() == "":
                self.tool.warning("Please enter a power type.")
                return
            elif self.ui.seats.text() == "":
                self.tool.warning("Please enter a seats type.")
                return
            elif self.ui.doors.value() == 0:
                self.tool.warning("Please enter a doors type.")
                return
            elif self.imagePath == "":
                self.tool.warning("Please select an image.")
                return

            else:
                if self.add_DataJson:
                    print(2)
                    img = bytes(self.tool.label_to_byte_array(self.image_label_car))
                else:
                    img = self.tool.convertToBinary(self.imagePath)

                idBrand = self.brand.getIdByBrand(self.ui.comboBoxBrand_1.currentText())

                if len(idBrand) == 0 :
                    self.brand.addBrand(self.ui.comboBoxBrand_1.currentText())
                    brand =self.brand.getIdByBrand(self.ui.comboBoxBrand_1.currentText())[0][0]
                    msg = "new brand has been added :"+self.ui.comboBoxBrand_1.currentText()
                    self.tool.warning(msg)
                    print("isbrand:",brand)
                if self.id_SelectedCar is not None :
                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_cars)
                    self.car.update(int(self.id_SelectedCar),int(brand), model, int(fuel), img,int(gearbox),float(self.ui.price.text()),float(self.ui.power.text()),int(self.ui.seats.text()),int(self.ui.doors.text()))
                    self.reset_AddCarpage()
                    self.imagePath = ""
                else :
                    print("gear : ",gearbox)
                    self.car.add(int(brand), model, int(fuel), img,int(gearbox),float(self.ui.price.text()),float(self.ui.power.text()),int(self.ui.seats.text()),int(self.ui.doors.text()))
                    self.add_DataJson=False
                    self.imagePath = ""

        except Exception as e:
            print(f"addCarButton : An error occurred: {e}")
            self.reset_AddCarpage()

    def edit_Car(self,idCar):
        try:
            if idCar is not None :
                self.id_SelectedCar = idCar
                self.fill_AddCarPage_database(idCar)
                self.addcar_Btn.setText("modifie")
                self.add_image_Btn.setText("modifie l'image")
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_add_car)

        except Exception as e:
            print(f"edit car : An error occurred: {e}")
            self.reset_AddCarpage()
    def redirect_to_AddCarPage(self,data):
        try:
            print(data)
            self.fill_AddCarPage_json(data[0])
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_add_car)
        except Exception as e:
            print(f"redirect_to_AddCarPage car : An error occurred: {e}")
            self.reset_AddCarpage()

    def fill_AddCarPage_database(self, idCar):
        try:
            self.add_DataJson=False
            data = self.car.getCarById(idCar)
            data = list(data[0])

            index = self.ui.comboBoxBrand_1.findData(data[1])
            self.ui.comboBoxBrand_1.setCurrentIndex(index)

            index = self.ui.comboBoxFuel_1.findData(data[2])
            self.ui.comboBoxFuel_1.setCurrentIndex(index)

            index = self.ui.comboBoxGear_1.findData(data[5])
            self.ui.comboBoxGear_1.setCurrentIndex(index)
            print(data[4])
            self.ui.model.setText(data[4])
            self.ui.price.setText(str(data[9]))
            self.ui.power.setText(str(data[6]))
            self.ui.seats.setText(str(data[7]))
            self.ui.doors.setValue(int(data[8]))

            pixmap = self.tool.getImageLabel(data[3])
            self.image_label_car.setPixmap(pixmap)
            self.image_label_car.adjustSize()

        except Exception as e:
            print(f"fill_AddCarPage car : An error occurred: {e}")
    def fill_AddCarPage_json(self, car):
        try:
            self.add_DataJson = True
            print(car["details"]["Brand"].split(" ")[0])
            index = self.ui.comboBoxBrand_1.findText(car["details"]["Brand"].split()[0])
            if index == -1:
                self.tool.warning("Brand not exist")
                self.comboBoxBrand_1.addItem(car["details"]["Brand"].split()[0])
                self.comboBoxBrand_1.setItemData(self.comboBoxBrand_1.count() - 1, None)
                self.ui.comboBoxBrand_1.setCurrentIndex(self.comboBoxBrand_1.count() - 1)
            else:
                self.ui.comboBoxBrand_1.setCurrentIndex(index)
        except Exception as e:
            print(f"brand car : An error occurred: {e}")

        print(car["details"]["Fuel Type"].split(" ")[0])
        try:
            index = self.ui.comboBoxFuel_1.findText(car["details"]["Fuel Type"].split(" ")[0])
            if index == -1:
                self.tool.warning("Fuel type not exist")
                self.comboBoxFuel_1.addItem(car["details"]["Fuel Type"].split()[0])
                self.comboBoxFuel_1.setItemData(self.comboBoxBrand_1.count() - 1, None)
                self.ui.comboBoxFuel_1.setCurrentIndex(self.comboBoxFuel_1.count() - 1)
            else:
                self.ui.comboBoxFuel_1.setCurrentIndex(index)

        except Exception as e:
            print(f"fuel type : An error occurred: {e}")

        try:
            print(car["details"]["gearbox"].split(" ")[0])
            if car["details"]["gearbox"] is not None and car["details"]["gearbox"].split(" ")[0] != "":
                gearbox = car["details"]["gearbox"].split(" ")[0]
                index = self.ui.comboBoxGear_1.findText(gearbox)
                if index != 1:
                    self.ui.comboBoxGear_1.setCurrentIndex(index)
        except Exception as e:
            print(f"gearbox : An error occurred: {e}")
        try:
            self.ui.model.setText(car["model"])
        except Exception as e:
            print(f"model car : An error occurred: {e}")

        self.ui.price.setText(None)
        try:
            print(car["details"]["Power"].split(" ")[0])
            self.ui.power.setText(car["details"]["Power"].split(" ")[0])
        except Exception as e:
            print(f"power : An error occurred: {e}")

        try:
            print(car["details"]["Doors"])
            self.ui.doors.setValue(int(car["details"]["Doors"]))
        except Exception as e:
            print(f"doors : An error occurred: {e}")

        try:
            print(car["details"]["Seats"])
            self.ui.seats.setText(car["details"]["Seats"])
        except Exception as e:
            print(f"SEATS : An error occurred: {e}")

        try:
            # Create a new QDate object with the desired date
            print(car["details"]["Start of production"].split(" ")[0])
            new_date = QDate(int(car["details"]["Start of production"].split(" ")[0]), 1, 1)
            # Set the date of the QDateEdit widget to the new date
            self.ui.production_date.setDate(new_date)
        except Exception as e:
            print(f"date : An error occurred: {e}")

        try:
            # Get the image from the URL and convert it to a QPixmap object

            # pixmap = self.scraping.get_image_from_url(car["images"][0])
            pixmap = self.scraping.download_img(car["link"])
            self.image_label_car.setScaledContents(True)
            self.image_label_car.setText("Loading...")
            self.image_label_car.setPixmap(pixmap)
        except Exception as e:
            print(f" image : An error occurred: {e}")

    def displayCars(self, data):
        try:
            self.ui.tableWidgetCar.clearContents()  # Clear the existing data in the table
            self.ui.tableWidgetCar.setColumnCount(
                13)  # Set the number of columns in the table, including the image column
            self.ui.tableWidgetCar.setHorizontalHeaderLabels(["Image", "idCar", "Brand", "Model","price","Fuel Type","gearbox","Year","Power","Seats","Doors","Edit","Delete"])  # Set the column labels
            self.ui.tableWidgetCar.setRowCount(len(data))  # Set the number of rows in the table

            for row_idx, car in enumerate(data):

                label = QLabel()  # Create a QLabel to display the image
                label.setScaledContents(True)
                pixmap = self.tool.getImageLabel(car[3])  # Get QPixmap from binary data
                label.setPixmap(pixmap)

                self.ui.tableWidgetCar.setCellWidget(row_idx, 0, label)  # Set the label as the cell widget for the image column
                if car[0] is not None:#idcar
                    self.ui.tableWidgetCar.setItem(row_idx, 1, QTableWidgetItem(str(car[0])))
                if car[1] is not None:#brand
                    self.ui.tableWidgetCar.setItem(row_idx, 2, QTableWidgetItem(str(self.dict_brands[car[1]])))

                if car[2] is not None:#fuel
                    self.ui.tableWidgetCar.setItem(row_idx,5, QTableWidgetItem(str(self.dict_fuel[car[2]])))

                if car[4] is not None:#model
                    self.ui.tableWidgetCar.setItem(row_idx,3, QTableWidgetItem(str(car[4])))

                if car[9] is not None:#price
                    self.ui.tableWidgetCar.setItem(row_idx, 4, QTableWidgetItem(str(car[9])))

                if car[5] is not None:#gearbox
                    self.ui.tableWidgetCar.setItem(row_idx, 6, QTableWidgetItem(str(self.dict_gearbox[car[5]])))
                if car[6] is not None:#power
                    self.ui.tableWidgetCar.setItem(row_idx,8, QTableWidgetItem(str(car[6])))
                if car[6] is not None:#year
                    self.ui.tableWidgetCar.setItem(row_idx, 7, QTableWidgetItem(str(car[6])))
                if car[7] is not None:#seats
                    self.ui.tableWidgetCar.setItem(row_idx,9, QTableWidgetItem(str(car[7])))
                if car[8] is not None:#doors
                    self.ui.tableWidgetCar.setItem(row_idx, 10, QTableWidgetItem(str(car[8])))

                # Create a push button for the edit icon
                edit_button = QPushButton()
                edit_button.setIcon(QIcon('./icon/edit.png'))
                edit_item = QTableWidgetItem()
                edit_item.setData(11, edit_button)
                self.tableWidgetCar.setItem(row_idx, 11, edit_item)

                # Create a push button for the delete icon
                delete_button = QPushButton()
                delete_button.setIcon(QIcon('./icon/delete.png'))
                delete_item = QTableWidgetItem()
                delete_item.setData(12, delete_button)
                self.tableWidgetCar.setItem(row_idx, 12, delete_item)

        except Exception as e:
            print(f"display car : An error occurred: {e}")

        self.ui.tableWidgetCar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Set default row height
        font = QFont()
        font.setBold(True)
        self.ui.tableWidgetCar.horizontalHeader().setFont(font)
        # Set row height
        self.ui.tableWidgetCar.verticalHeader().setDefaultSectionSize(80)

        # Set alternating row colors
        self.ui.tableWidgetCar.setAlternatingRowColors(True)
        self.ui.tableWidgetCar.setStyleSheet("alternate-background-color: gray;")
        self.ui.tableWidgetCar.setStyleSheet("background-color: white;  ")

        # Set selection mode to row selection
        self.ui.tableWidgetCar.setSelectionBehavior(QTableWidget.SelectRows)

    def id_SelectedCombobox(self, combo):
        try:
            selected_index = combo.currentIndex()
            # Get the item key using the selected index
            key = combo.itemData(selected_index, QtCore.Qt.UserRole)
            # Get the value of the selected item
            value = combo.itemText(selected_index)
            if key is not None and key != -1:
                print("value: ", value)
                print("key: ", key)
                if combo.objectName() == "comboBoxGear_1":
                    data = None
                    print(key)
                if combo.objectName() == 'comboBoxBrand' or combo.objectName() == 'comboBoxBrand_1':
                    data = self.car.searchByIdBrand(key)
                elif combo.objectName() == 'comboBoxFuel' or combo.objectName() == 'comboBoxFuel_1':
                    # Retrieve data from the database based on the selected item
                    data = self.fuel.searchByIdFuel(key)
                elif combo.objectName() == 'comboAllBrands':
                    #data = self.scraping.getCarsByBrand(value)
                    dd = self.tool.fill_combobox(self.ui.comboAllModels, value)
                    #self.displayModels(data)
                    return

                elif combo.objectName() == 'comboAllModels':
                    data = self.scraping.getCarByModel(self.ui.comboAllBrands.currentText(),self.ui.comboAllModels.currentText())
                    self.displayModels(data)
                    return
                if data is not None:
                    self.displayCars(data)
                return key

        except Exception as e:
            print(f"id_SelectedCombobox :: Error: {e}")

    def displayModels(self, data):
        try:
            self.ui.tableWidgeModels.clearContents()  # Clear the existing data in the table
            self.ui.tableWidgeModels.setColumnCount(
                9)  # Set the number of columns in the table, including the image column
            self.ui.tableWidgeModels.setHorizontalHeaderLabels(
                ["Image","Model","Fuel Type","gearbox","Year","Power","Seats","Doors","link"])  # Set the column labels
            self.ui.tableWidgeModels.setRowCount(len(data))  # Set the number of rows in the table
            image_urls = []
            for url in data:
                image_urls.append(url["link"])

            # Download the image and update the label with a loading message
            # self.ui.loading_image.setText("Loading...")
            QApplication.processEvents()
            images = self.scraping.download_images(image_urls)

            for row_idx, car in enumerate(data):
                print(car)
                label = QLabel()  # Create a QLabel to display the image
                label.setScaledContents(True)
                label.setText("Loading...")
                label.setPixmap(images[row_idx])
                # Set the label as the cell widget for the image column
                self.ui.tableWidgeModels.setCellWidget(row_idx, 0,label)
                self.ui.tableWidgeModels.setItem(row_idx, 1, QTableWidgetItem(str(car["model"])))
                self.ui.tableWidgeModels.setItem(row_idx, 2, QTableWidgetItem(str(car["details"]["Fuel Type"])))
                self.ui.tableWidgeModels.setItem(row_idx, 3, QTableWidgetItem(str(car["details"]["gearbox"])))
                self.ui.tableWidgeModels.setItem(row_idx, 4, QTableWidgetItem(str(car["details"]["Start of production"])))
                self.ui.tableWidgeModels.setItem(row_idx, 5, QTableWidgetItem(str(car["details"]["Power"])))
                self.ui.tableWidgeModels.setItem(row_idx, 6, QTableWidgetItem(str(car["details"]["Seats"])))
                self.ui.tableWidgeModels.setItem(row_idx, 7, QTableWidgetItem(str(car["details"]["Doors"])))
                self.ui.tableWidgeModels.setItem(row_idx, 8, QTableWidgetItem(str(car["link"])))

        except Exception as e:
            print(f"displayModels : An error occurred: {e}")
        # Assuming self.tableWidget is the QTableWidget object
        # Set default row height
        font = QFont()
        font.setBold(True)
        self.ui.tableWidgeModels.horizontalHeader().setFont(font)
        # Set row height
        self.ui.tableWidgeModels.verticalHeader().setDefaultSectionSize(80)

        # Set alternating row colors
        self.ui.tableWidgeModels.setAlternatingRowColors(True)
        self.ui.tableWidgeModels.setStyleSheet("alternate-background-color: gray;")
        self.ui.tableWidgeModels.setStyleSheet("background-color: white;  ")

        # Set selection mode to row selection
        self.ui.tableWidgeModels.setSelectionBehavior(QTableWidget.SelectRows)


    def reset_AddCarpage(self):

        self.id_SelectedCar = None
        self.ui.addcar_Btn.setText("ajouter")
        self.add_image_Btn.setText("Ajouter une image")
        self.ui.comboBoxBrand_1.setCurrentIndex(0)
        self.ui.comboBoxFuel_1.setCurrentIndex(0)
        self.ui.model.setText("")
        self.image_label_car.setText("Uploader une image")

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
                self.image_label_car.setPixmap(pixmap)
                self.image_label_car.adjustSize()
        except Exception as e:
            print(f"An error occurred: {e}")

