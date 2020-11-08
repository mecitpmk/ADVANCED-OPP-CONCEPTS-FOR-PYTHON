
class Messages(dict):
    def __init__(self):
        self.readed = {}
        self.sended = {}
    def show(self,inbox=False,readed=False,sended=False):
        dictionary = None
        if inbox:
            dictionary = self
        elif readed:
            dictionary = self.readed
        elif sended:
            dictionary = self.sended
        print("Messages Displaying....")
        for index,user in enumerate(dictionary,start=1):
            print(f"{index} - User: {user}  Messages : {dictionary[user]}")
    def mark_readed(self,given_number): ## PRINT BEFORE ALL MESSAGES WITH NUMER EX: 1- HUSEYIN : MECIT NABER YA...
        for index,key in enumerate(self,start=1):
            if index == given_number:
                self.readed[key] = self[key]
                del self[key]
                print("Sucessfulyy Marked as Readed")
                break
    def print_messages(self,normal=False,readed=False,sended=False):
        dictionary = None
        if normal:
            dictionray = self
        elif readed:
            dictionary = self.readed
        elif sended :
            dictionary = self.sended
        for index,person in enumerate(dictionary,start=1):
            print(f"{index} - {person} : {dictionary[person]}")
    def delete_message(self,given_number,in_sended=False,in_readed=False,in_normal=False): 
        current_dict = None
        if in_sended:
            current_dict = self.sended
        elif in_readed:
            current_dict = self.readed
        elif in_normal:
            current_dict = self
        for index,messages in enumerate(current_dict,start=1):
            if given_number == index:
                del current_dict[messages] 
                print("Successfully Deleted Messages..")
                break
    def search(self,given_str : str,in_readed=False,in_sended=False,in_normal=False,):
        current_dict = None
        if in_readed:
            current_dict = self.readed
        elif in_sended:
            current_dict = self.sended
        elif in_normal:
            current_dict = self
        for u_obj , messages in current_dict.items():
            given_str = given_str.lower()
            current_messages = messages.lower()
            current_messages = current_messages.split()
            founded  = {}
            for walk in current_messages:
                if given_str in walk:
                    founded[u_obj] = messages
            if len(founded) > 0 :
                return founded



class Contact(list):
    def search_by_number(self,given_number : int):
        """

        Args:
            given_number (int): [description]

        Returns:
            User: object
        """
        for obj in self:
            if obj.number == given_number:
                return obj
    def search_by_name(self,name : str):
        for obj in self:
            if obj.name == name:
                return obj
class User:
    def __init__(self,name : str ,number : int):
        self.name = name
        self.number = number
        self.contact = Contact()
        self.messages = Messages()
        System.all_users.append(self)

    def print_contact(self):
        print("Available Contact Listing...")
        for index,contact in enumerate(self.contact,start=1):
            print(f'{index} - {contact}')
    def send_message_to_contact(self,contact , message :  "str"):
        self.messages.sended[contact] = message
        contact.messages[self] = message
        print("Message sended Successfully")
        
    def search_contact(self,contact_):
        if type(contact_) is int:
            return self.contact.search_by_number(contact_)
        else:
            return self.contact.search_by_name(contact_)
    def fetch_user_from_database(self):
        for users in System.all_users:
            if users == self or users in self.contact:
                continue
            else:
                self.contact.append(users)
        self.print_contact()
    def __repr__(self):
        return self.name


class System:
    all_users = []
    def __init__(self):
        self.logged = False
        self.current_obj = None
        self.unlogged_dict = {"Log in":self.log_in,"Create User":self.create_user}
        self.logged_dict = {"Send Message To Contact":self.send_ms,"Search Contact":self.search_ct,"Search Message in Inbox":self.search_in_normal,
                        "Search Message in Sended":self.search_in_sended,"Search Message in Readed":self.search_in_readed,
                            "Add Contact from Database":self.fetch_user,
                                "Add Contact Manually":self.create_user,"Show Inbox Messages":self.show_mes_in,"Show Readed Messages":self.show_mes_readed,
                                    "Show Sended Messages":self.show_mes_sended,"Show all Contact":self.pr_contact,"Log Out":self.log_out}
    def pr_contact(self):
        self.current_obj.print_contact()
    def fetch_user(self):
        self.current_obj.fetch_user_from_database()        
    def show_mes_in(self):
        self.current_obj.messages.show(inbox=True)
    def show_mes_readed(self):
        self.current_obj.messages.show(readed=True)
    def show_mes_sended(self):
        self.current_obj.messages.show(sended=True)
    def menu(self):
        while True:
            dictionry= None
            if self.logged:
                dictionary = self.logged_dict
                normal_menu = False
            else:
                dictionary = self.unlogged_dict
                normal_menu = True
            # print("\nWelcome...")
            print("-------------------")
            for index,menu in enumerate(dictionary,start=1):
                print(f"{index} - {menu}")
            inputs = int(input("What do you want to do:"))
            self.return_menu(inputs,normal_menu=normal_menu)()
        
    
    def log_out(self):
        self.logged = False
        self.current_obj = None
        print("Logged off..")
        ##BURAYA MENU EKLE...
    def create_user(self):
        name = input("Name :")
        phone = input("Phone: ")
        u = User(name,phone)
        if self.logged:
            self.current_obj.contact.append(u)
            print("Your Contact added succesfully...")
        else:
            print("Created Succesfully.")
        print(System.all_users)
    def log_in(self):
        name = input("Name:")
        phone = input("Phone:")
        for users in System.all_users:
            if users.name == name and users.number == phone:
                self.current_obj = users
                self.logged = True
                print("Logged in Successfully.")
        if self.logged:
            print(f"Welcome.. You are logged as {self.current_obj}")
        else:
            print("Couldnt Found...")

    def search_ct(self):
        inp = input(" Enter Contact Name or Number:")
        obj = self.current_obj.search_contact(inp)
        if obj:
            print(f"Founded : {obj}")
        else:
            print("Couldnt founded...")
    def send_ms(self):
        self.current_obj.print_contact()
        inp = int(input("Which Contact:"))
        mes = input("Your Message : ")
        self.current_obj.send_message_to_contact(self.current_obj.contact[inp-1],mes)
    def search_in_readed(self):
        inputs = input("Enter Message to Search")
        mes = self.current_obj.messages.search(inputs,in_readed=True)
        if mes:
            print(f"Message founded")
            for user,message in mes.items():
                print(f"From user {user}  Message : {message}")
        else:
            print("Couldnt founded..")
    def search_in_normal(self):
        inputs = input("Enter Message to Search")
        mes = self.current_obj.messages.search(inputs,in_normal=True)
        if mes:
            print(f"Message founded")
            for user,message in mes.items():
                print(f"From user {user}  Message : {message}")
        else:
            print("Couldnt founded..")
    def search_in_sended(self):
        inputs = input("Enter Message to Search")
        mes = self.current_obj.messages.search(inputs,in_sended=True)
        if mes:
            print(f"Message founded")
            for user,message in mes.items():
                print(f"From user {user}  Message : {message}")
        else:
            print("Couldnt founded..")
    def return_menu(self,given_number,normal_menu=True):
        """Returns Functions.

        Args:
            given_number ([type]): [description]

        Returns:
            [type]: [description]
        """
        dictionary = None
        if normal_menu:
            dictionary = self.unlogged_dict
        else:
            dictionary = self.logged_dict
        for index,functs in enumerate(dictionary,start=1):
            if index == given_number:
                return dictionary[functs]


email_system = System()
email_system.menu()





    
        

