
import conn
import base64
class Car:
    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")

    def getCar(self,req):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                   # req = f"SELECT * FROM voiture WHERE idVoiture = {car_id}"
                    self.connexion.cursor.execute(req)
                    result = self.connexion.cursor.fetchall()
                    return result
        except Exception as e:
            print(f"An error occurred: {e}")
    def addCar(self, brand, model, fuel, image):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    print("image_base64 ")
                    req = "INSERT INTO voiture(`idMarque`, `idCarburant`, `model`, `image`) VALUES (%s, %s, %s, %s)"
                    self.connexion.cursor.execute(req, (1, 1, 1, image))
                    self.connexion.conn.commit()
                    print("Record added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def updateCar(self, car_id, brand, model, fuel):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = f"UPDATE voiture SET idMarque = {brand}, idCarburant = {fuel}, image = '{model}' WHERE idVoiture = {car_id}"
                    self.connexion.cursor.execute(req)
                    self.connexion.conn.commit()
                    print("Record updated successfully.")

        except Exception as e:
             print(f"An error occurred: {e}")
    def deleteCar(self, car_id):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = f"DELETE FROM voiture WHERE idVoiture = {car_id}"
                    self.connexion.cursor.execute(req)
                    self.connexion.conn.commit()
                    print("Record deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

