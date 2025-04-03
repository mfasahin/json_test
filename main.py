import json
import os


class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class UserRepository:
    def __init__(self):
        self.users = []
        self.isLoggedIn = False
        self.currentUser = {}
        # load users from .json file
        self.loadUsers()

    def loadUsers(self):
        if os.path.exists("users.json"):
            try:
                with open("users.json", "r", encoding="utf-8") as file:
                    users = json.load(file)
                    for user in users:
                        user = json.loads(user)
                        newUser = User(username=user["username"], password=user["password"],
                                       email=user["email"])
                        self.users.append(newUser)
                print(self.users)
            except json.JSONDecodeError as e:
                print(f"Hata: JSON dosyası okunamıyor. Detaylar: {e}")
        else:
            print("users.json dosyası bulunamadı.")

    def register(self, user: User):
        self.users.append(user)
        self.savetoFile()
        print("kullanıcı oluşturuldu.")

    def checkUser(self):
        username = input("username: ")
        while username.isspace() or ' ' in username:
            username = input("lütfen geçerli bir kullanıcı adı giriniz:")
            if username.isspace() == False and ' ' not in username:
                break

        while True:
            password = input("Şifrenizi girin (6 karakter, boşluk içermemeli): ")

            if len(password) == 6 and ' ' not in password:
                print("Şifre kabul edildi.")
                break
            else:
                print("Geçersiz şifre! Lütfen 6 karakterli ve boşluk içermeyen bir şifre girin.")

        email = input("email: ")
        # asd@email.com
        while email.endswith("@email.com"):
            break
        else:
            email = input("lütfen @email.com uzantılı bir email giriniz:")


        user = User(username=username, password=password, email=email)
        repository.register(user)

    def login(self, username, password):
        found_user = None
        for user in self.users:
            if user.username == username and user.password == password:
                found_user = user
                break

        if found_user:
            self.isLoggedIn = True
            self.currentUser = found_user
            print(f"{username} kullanıcısı giriş yaptı.")
        else:
            print("Kullanıcı adı veya şifre hatalı.")

    def logout(self):
        if self.isLoggedIn:
            print(f"{self.currentUser.username} çıkış yaptı.")
            self.isLoggedIn = False
            self.currentUser = {}
        else:
            print("Giriş yapılmadı.")

    def identity(self):
        if self.isLoggedIn:
            print(f'username: {self.currentUser.username}')
        else:
            print("giriş yapılmadı.")

    def savetoFile(self):
        try:
            list = []
            for user in self.users:
                list.append(json.dumps(user.__dict__))
            with open("users.json", "w") as file:
                json.dump(list, file)
        except Exception as e:
            print(f"Hata: Dosyaya yazma sırasında bir sorun oluştu. Detailer: {e}")

    def deleteUser(self):
        if not self.isLoggedIn:
            print("Giriş yapılmadı.")
        else:
            # Mevcut kullanıcıyı listeden sil
            self.users.remove(self.currentUser)

            # Güncellenmiş veriyi JSON dosyasına yaz
            self.savetoFile()

            # Kullanıcı çıkış yaptıktan sonra mevcut kullanıcı bilgilerini sıfırla
            self.isLoggedIn = False
            self.currentUser = {}
            print("Kullanıcı başarıyla silindi.")

repository = UserRepository()

while True:
    print("Menü".center(50, "-"))
    secim = input("1- Register\n2- Login\n3- Logout\n4- Identity\n5- Delete User\n6- Exit\nSeçiminiz: ")

    if secim == "6":
        break
    else:
        if secim == "1":
            repository.checkUser()
        elif secim == "2":
            if repository.isLoggedIn:
                print("zaten giriş yaptınız.")
            else:
                username = input("username: ")
                password = input("password: ")
                repository.login(username, password)
        elif secim == "3":
            repository.logout()
        elif secim == "4":
            repository.identity()
        elif secim == "5":
            repository.deleteUser()
        else:
            print("yanlış seçim")