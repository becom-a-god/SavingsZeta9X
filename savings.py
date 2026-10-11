from datetime import datetime,date,timedelta
import json
import random

class Savings:
    def __init__(self):
        self.saving = {}
        self.auto_save_tools = {}
        self.load()
        self.id = None
        self.password = None

    def save(self):
        with open("saving.json", "w") as f:
            json.dump(self.saving, f, indent=4)

    def load(self):
         try:
             with open("saving.json", "r") as f:
                 self.saving = json.load(f)
         except FileNotFoundError:
             pass

    def create_user_id(self):
        user_id = ""
        letters_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(4):
            user_id += random.choice(letters_list)
        for i in range(4):
            user_id += random.choice(numbers_list)
        return user_id

    def id_and_password(self):
        id = input("enter your user id >> ").strip()
        if not id or not id in self.saving:
            print("Invalid User ID. Please try again.")
            return
        password = input("enter password >> ")
        if not password:
            print("password is required")
            return
        elif not password == self.saving[id]["user_password"]:
            print("wrong pasword")
            return
        elif password == self.saving[id]["user_password"]:
            print("Login Successful! Welcome,", self.saving[id]["name"], ".")
            return id, password

    def permission(self, tasks, add=False):
        while True:
            print("—"*10)
            ys = input("yes or no: ").strip().lower()
            print("—"*10)
            if ys in ["yes","y"]:
                print("Thank you for confirming it.")
                if add:
                    tasks["task1"]["success"] = True
                return True
            elif ys in ["no","n"]:
                return False
            else:
                print("Just 'Yes' or 'No', please.")
                continue

    def reset_daily_target(self):
        print("Do you want to reset your daily target too?\n"
                "[Note: If not reset, it stays saved and won't be asked again on restart] >> ")
        permission = self.permission(None,add=False)
        if permission:
            return True
        elif not permission:
            return False

    def get_user_data(self):
        return [self.saving[self.id]]

    def start_and_stop(self):
        for data in self.get_user_data():
            if data["auto_save"][0]:
                print( "Auto-save is active.\nDo you want to STOP it?")
                permission = self.permission(None,add=False)
                if permission == True:
                    data["auto_save"][0] = False
                    target_reset_per = self.reset_daily_target()
                    if target_reset_per:
                        data["auto_save"][1] = 0
                    print("Auto Save Stop")
                    return
                return
        self.auto_savings(is_running=True)

    def Adding_to_my_savings(self):
        user_data = self.get_user_data()
        count = 0
        while count < 3:
            try:
                new_amount = int(input("enter amount > "))
                if new_amount <= 0:
                    print("Please Enter Valid Amount")
                    count += 1
                    continue
                for f in user_data:
                    total_saving = f["saving"] + new_amount
                    f["saving"] = total_saving
                    today_saving = datetime.today()
                    today_saving = (today_saving.strftime("%d/%m/%Y (%H:%M)"),"Man","+₹",new_amount)
                    f["history"].append(today_saving)
                print(f"saving update")
                print("","="*30,"\n",f["name"],"your savings\n ::|::",total_saving,"₹ ::|::","\n","="*30)
                break
            except ValueError:
                print("enter amount only")
                count += 1

    def your_history(self):
        user_data = self.get_user_data()
        try:
            if not user_data[0]["history"]:
                print("history is empty")
                return
        except TypeError:
            pass
        if isinstance(user_data,list):
            print(f"{'_'*48}\n{'Date':<13}{'Time':<8}{'Days':<11}|{'Mode':<7}{'Amount'} |\n{'—'*48}")
            for f in user_data:
                for items in f["history"]:
                    if len(items) == 4:
                        daytime, mode, sign, amount = items
                        day_diff = "---"
                        print(f"{daytime:<20}({day_diff})       |{mode:<7}{sign}{amount}")
                    if len(items) == 5:
                        daytime, day_diff, mode, sign, amount = items
                        if day_diff == "New":
                            print(f"{daytime:<20} {day_diff}        |{mode:<7}{sign}{amount}")
                        if not day_diff == "New":
                            print(f"{daytime:<20}({day_diff} days)    |{mode:<7}{sign}{amount}")

    def auto_savings(self,is_running=False):
        user_data = self.get_user_data()
        if is_running and not user_data[0]["auto_save"][0]:
            print("Enable auto-save to automatically reach your set savings target.")
            user_data = self.get_user_data()
            permission = self.permission(None,add=False)
            if not permission:
                print("No problem")
                return
            user_data[0]["auto_save"][0] = True
        if user_data[0]["auto_save"][0]:
            if isinstance(user_data, list):
                target = user_data[0]["auto_save"][1]
                if not target:
                    for i in range(4):
                        try:
                            target = int(input("enter your daily amount to save >> "))
                            if target > 0:
                                user_data[0]["auto_save"][1] = target
                                break
                            continue
                        except ValueError:
                            continue
                if not target:
                    print("Failed to set a valid target amount. Exiting process.")
                    return
                try:
                    last_date_str = user_data[0]["history"][-1][0]
                    last_date = datetime.strptime(last_date_str, "%d/%m/%Y (%H:%M)").date()
                    today_date = date.today()
                    days_difference = (today_date - last_date).days
                    new_amount = days_difference * target
                    if last_date == today_date:
                        if is_running:
                            print("Auto-save is now active! 🚀\nToday's savings are already completed.\nAuto-save will automatically manage your funds starting tomorrow.\nYou can still add money manually today.")
                        return
                    today_saving = datetime.today()
                    today_saving = (today_saving.strftime("%d/%m/%Y (%H:%M)"),days_difference,"Auto","+₹",target)
                    user_data[0]["history"].append(today_saving)
                    user_data[0]["saving"] += new_amount
                except IndexError:
                    if not user_data[0]["history"]:
                        days_difference = "New"
                        now_str = datetime.today().strftime("%d/%m/%Y (%H:%M)")
                        today_saving= (now_str,days_difference,"Auto","+₹",target)
                        user_data[0]["history"].append(today_saving)
                        user_data[0]["saving"] += target
                        print(f"{user_data[0]['name']}Welcome!\nAuto-save has been successfully activated for your account.\nYour progress will now be saved automatically from today.")
                        return

    def add_new_saving(self):
        tasks = {
             "task1": {"count": 0, "success": False},
             "task2": {"count": 0, "success": False}
        }
        print("="*30)
        print("Your name would be requried for our records.\nJust an 4-letter name, please.")
        print("="*30)
        while tasks["task1"]["count"] < 5:
            name = input("enter name >: ").strip()
            if name.replace(" ","").isdigit() or not name:
                tasks["task1"]["count"]+=1
                print("name is required.You Have",5-tasks["task1"]["count"],"attempts left")
            elif name.replace(" ","").isalpha():
                if 3 < len(name) < 30:
                    print("Is this name spelled correctly?\n")
                    self.permission(tasks, add=True)
                    break
                else:
                    if self.permission(tasks,add=True):
                        print("enter 4 letter name please\n")
                        tasks["task1"]["count"] += 1
                        print("You Have",5-tasks["task1"]["count"], "attempts left.\n")
                        continue

        if not tasks["task1"]["success"]:
            print("limit reached please try again")
            return True

        while tasks["task2"]["count"] < 3:
            print("Make an minimum four-letter password.\n")
            password = input("make a password >> ").strip()
            if not password:
                print("password is required\nyou have",3-tasks["task2"]["count"],"attempts left\n")
                tasks["task2"]["count"]+=1
            elif len(password) >= 4:
                print("confirm your password.\n")
                while True:
                    con = input("confirm >> ").strip()
                    if password == con:
                        print(f"your password is {password}\n")
                        tasks["task2"]["success"] = True
                        break
                    else:
                        print("please confirm your password.\nyou have",3-tasks["task2"]["count"],"attempts left\n")
                        continue
                break
            else:
                print("please enter minimum 4 letter password")
                tasks["task2"]["count"]+=1
                continue

        if not tasks["task2"]["success"]:
            print("limit reached try again")
            return True
        today = date.today()
        user_id = self.create_user_id()
        self.saving[user_id] = {"user_password": password, "name": name,"saving": 0,"date": today.strftime("%d-%m-%Y"),"history": [],"auto_save": [False, 0]}
        print(f"{name} your new saving account created.\nyour user id: [ {user_id} ]")
        self.id = user_id
        self.password = password
        return False

    def withdraw(self):
        user_data = self.get_user_data()
        try:
            amount = int(input("enter amount >> "))
            if amount <= 0 or amount > user_data[0]["saving"]:
                print("Please enter a valid amount within your balance.")
                return
            saving_update = user_data[0]["saving"] - amount
            user_data[0]["saving"] = saving_update
            today = datetime.today()
            today = (today.strftime("%d/%m/%Y (%H:%M)"),"WDL","-₹",amount)
            user_data[0]["history"].append(today)
            print(f"Successfully withdrawn {amount}₹.")
        except ValueError:
            print("Invalid Amount")

    def savings_options(self):
        while True:
            print(f"{'='*35}\n1. add to your saving\n2. auto save \n0. exit\n{'='*35}")
            option = input("chose number >> ").strip()
            if option == "1":
                self.Adding_to_my_savings()
            elif option == "2":
                self.start_and_stop()
            elif option == "0":
                print("Thank for using")
                break
            else:
                print("Invalid Choice")

def good_by():
    goodbyes = random.choice([
    "bye", "bye-bye", "see ya", "later", "laters", "l8r", "im out", "im off", "gotta go", "gtg",
    "ttyl", "bbl", "brb", "peace", "peace out", "take care", "cheers", "toodles", "ta-ta", "so long",
    "farewell", "adieu", "adios", "ciao", "sayonara", "aloha", "au revoir", "auf wiedersehen", "shalom", "namaste",
    "catch ya later", "see you soon", "see you around", "see you tomorrow", "see you next time", "until next time", "until tomorrow", "until then", "have a good one", "have a nice day",
    "have a great day", "have a good evening", "have a good night", "good night", "sweet dreams", "rest well", "sleep tight", "talk soon", "catch up later", "speak soon",
    "im ghost", "im audi", "bounce", "gotta bounce", "gotta jet", "gotta blast", "gotta run", "gotta fly", "im heading out", "im rolling",
    "outta here", "im history", "smell ya later", "stay classy", "keep it real", "catch you on the flip side", "peace out girl scout", "later skater", "in a while crocodile", "see you later alligator",
])
    return goodbyes

def main(s):
    s.auto_savings()
    while True:
        print(f"{'='*25}\n1.See Your Savings\n2.Save Options\n3.See Your Savings History\n4.Withdraw\n0.Log-Out\n{'='*25}")
        user = input("choose >: ").strip()
        if user == "1":
            user_data = s.get_user_data()
            if isinstance(user_data, list):
                for value in user_data:
                    print("—"*40,"\n","This account was created on",value["date"],"\n","="*40,"\n",value["name"],"your savings\n ::|::",value["saving"],"::|::","\n","="*40)
        elif user == "2":
            s.savings_options()
        elif user == "3":
            s.your_history()
        elif user == "4":
            s.withdraw()
        elif user == "0":
            s.save()
            print(good_by())
            break
        else:
             print("Invalid choice")

def start_app():
    start_s = Savings()
    while True:
        print(f"{'='*15}\n1.Login\n2.Create saving Acount\n3.close App\n{'='*15}")
        choice = input("choice > ").strip()
        if choice == "1":
            ip = start_s.id_and_password()
            if ip:
                start_s.id, start_s.password = ip
                main(start_s)
                break
            elif ip is None:
                continue
        elif choice == "2":
            ans = start_s.add_new_saving()
            if not ans:
                main(start_s)
                break
        elif choice == "3":
            return

if __name__ == "__main__":
    start_app()
