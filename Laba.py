class UserAccount:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.__password = password

    def set_password(self, new_password):
        self.__password = new_password

    def check_password(self, password):
        return self.__password == password

user = UserAccount("us", "us@mail.ru", "pass")

user.set_password("new_pass")

print(user.check_password("new_pass"))
print(user.check_password("pass"))  


class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def get_info(self):
        return f"{self.make} {self.model}"

class Car(Vehicle):
    def __init__(self, make, model, fuel_type):
        super().__init__(make, model)
        self.fuel_type = fuel_type

    def get_info(self):
        return super().get_info() + f" {self.fuel_type} fuel"



car = Car("T", "C", "g")
print(car.get_info())  
