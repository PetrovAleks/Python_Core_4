import os
import sys
import re
from pathlib import Path
from colorama import Fore, Style
import json

current_directory = os.getcwd()
contacts_file = "contacts.txt"
users_file = "users.txt"
cats_file = "cats.txt"
regex = r'\d+'

def get_file_path(file_name: str)->str:
    return os.path.join(current_directory, file_name)

def total_salary(file_path: str)->(float, float): 
    all_salary = []
    try:
        with open(file_path) as file:
            for line in file:
                salary_from_line = re.findall(regex, line)
                if not len(salary_from_line):
                    continue
                all_salary.append(salary_from_line)

        if(not len(all_salary)):
            return (0, 0)     

        return (sum([float(salary[0]) for salary in all_salary]) ,
            sum([float(salary[0]) for salary in all_salary]) / len(all_salary))
        
             
    except FileNotFoundError:
        print("Something went wrong!")
        

def get_cats_info(file_path: str)->list:
    cats_info =[]
    try:
        with open(file_path) as file:
            for line in file:
                cat = line.split(",")
                if not len(cat) == 3:
                    continue
                cats_info.append({
                    "name": cat[1], 
                    "age": re.findall(regex, cat[2]),
                    "id": cat[0]
                })
                
        return cats_info
    except FileNotFoundError:
        print("Something went wrong!")

def path_validation(path: str)->bool:
       if not path:
          print("No path provided")
          return False
       if not os.access(path, os.R_OK):
           print("You don't have access to this path")    
           return False
       if not os.path.exists(path):
           print("Path does not exist")
           return False
       return True 

def show_all_files_and_folders_by_path(path="",name=""): 
         new_path = sys.argv[1]
         if path:
                new_path = path
         if not path_validation(new_path):
                return
         abs_path = os.path.abspath(new_path)
         for root, dirs, files in os.walk(abs_path):
                for file in files:
                    print(f"file: {Fore.GREEN}{file}{Style.RESET_ALL}")
                for dir in dirs:
                    print(f"dir: {Fore.MAGENTA}{dir}{Style.RESET_ALL}")
                    show_all_files_and_folders_by_path(f"{root}/{dir}",dir)

def add_user(user: list):
    if not user or len(user) < 2:
        print("Name and phone are required")
        return
    name = user[0]
    phone = user[1]
    users = get_users()
    print("users",users)
    
    try:
        with open(get_file_path(contacts_file), "w") as file:
            contacts_lsit = [
                {"name": name, "phone": phone},
            ]

            if(len(users)):
                contacts_lsit.extend(users)
            data =json.dumps(contacts_lsit)
            print("users",data)

            file.write(data)
            print(Fore.CYAN + "User added successfully" + Style.RESET_ALL)   
    except FileNotFoundError as e:
        print("Something went wrong!",Fore.RED + e)


def change_user_contact(name:str):
    if not name :
        print(Fore.RED + "Username required" + Style.RESET_ALL)
        parse_input()
        return
    
    contacts:list[dict] =  get_users()    
    try:
        with open(get_file_path(contacts_file), "w") as file:
            for i in range(len(contacts)):
                if name.lower() in contacts[i].get("name").lower():
                    phone = input("Enter new phone number: ")
                    contacts[i]["phone"] = phone
                    file.write(json.dumps(contacts))
                    print(Fore.GREEN + "User contact changed successfully" + Style.RESET_ALL) 
                    return
            print(Fore.RED +"User not found")
    except FileNotFoundError as e:
        print("Something went wrong!",Fore.RED + e)

def get_user_contact(name:str):
    if not name:
        print("Name is required")
        parse_input()
        return
    try:
        with open(get_file_path(contacts_file), "r") as file:
            contacts:dict = json.loads(file.read())
            for contact in contacts:
                if name in contact:
                    print(contact.name, contact.phone)
                    return
            print(Fore.RED +"User not found" + + Style.RESET_ALL)
    except FileNotFoundError as e:
        print("Something went wrong!",Fore.RED + e)        

def print_all_users():
    try:
        users = get_users()
        if not len(users):
            print("No users found")
            return
        for user in users:
             print(user.get("name"), user.get("phone"))
    except FileNotFoundError as e:
        print("Something went wrong!",Fore.RED + e + Style.RESET_ALL)

def get_users()->list:
    try:
        with open(get_file_path(contacts_file), "r") as file:
            users = file.read()
            if not users:
                return []
            return json.loads(users)
    except FileNotFoundError as e:
        print("Something went wrong!",Fore.RED + e + Style.RESET_ALL)

def parse_input():
    comand = {
        "1": "Add",
        "2": "Change",
        "3": "All",
        "4": "Exit"
    }
    for key, value in comand.items():
        print(Fore.GREEN + f"{key}: {value}" + Style.RESET_ALL)
    
    choice = input(Fore.BLUE  + "How can I help you? Choose a command: " + Style.DIM)
    
    if not choice :
        print("Choose a command")
        return   

    choice = choice.lower()
    match choice:
        case "1" | "add":
            user = input("Enter user name and phone number: "  + Style.RESET_ALL).strip().split(" ")
            add_user(user)
        case "2" |"change":
            user = input("Enter user name : "  + Style.RESET_ALL).strip()
            change_user_contact(user)
        case "3" | "all":
            print_all_users()
        case "4" | "exit" | "close" | "quit":
            print("Goodbye!")
            exit()
        case _:
            print("Invalid choice")
            parse_input()
    parse_input()   
    

def main():
    print(Fore.GREEN + "Welcome to Halper Bot!"  + Style.RESET_ALL)
    parse_input()

if __name__ == "__main__":
    main()

# total_salary(get_file_path(users_file))
# print(get_cats_info(get_file_path(cats_file)))
# show_all_files_and_folders_by_path()
                    
main()
