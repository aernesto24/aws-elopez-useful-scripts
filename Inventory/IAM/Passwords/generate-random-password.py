"""Simple script to generate random passwords 
The idea is to use this piece of software to put it in a user creation script"""

from random import choice
from dotenv import load_dotenv
from pathlib import Path


def check_user_input(input):
    #This function will look if the input is between acceptable values for a password
    min_password_lenght = 8
    max_password_lenght = 16
    
    val = input
    if val >= min_password_lenght and val <= max_password_lenght:
        return val
    else:
        print("the value must be an integer between 8 and 16, will default to 8")
        val = 8
        return val


def generate_password(password_element_selection, list_of_password_characters):
    #This function receive an element selection and a list of password characters empty list
    #It will fill list_of_password_characters with the values selected
    lower_case_letters = "abcdefghijklmnopqrstuvwxyz"
    upper_case_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    allowed_special_characters = "._-()%#/<>*^"

    choose_password_components = int(input("""Select your passwords components:
            1. Lower case letters
            2. UPPER CASE LETTERS
            3. Numbers
            4. Special Characters
            : """))

    if choose_password_components not in password_element_selection:
        password_element_selection.append(choose_password_components)
        if choose_password_components == 1:
            list_of_password_characters.append(lower_case_letters)
        elif choose_password_components == 2:
            list_of_password_characters.append(upper_case_letters)
        elif choose_password_components == 3:
            list_of_password_characters.append(numbers)
        elif choose_password_components == 4:
            list_of_password_characters.append(allowed_special_characters)
        else:
            print("Please insert a valid option")
    else:
        print("That selection is already in place")
           
    print(list_of_password_characters, password_element_selection)
    return list_of_password_characters, password_element_selection


def list_to_string(list_of_password_characters):
    #Convert list to string
    string_of_password_characters = ""

    for element in list_of_password_characters:
        string_of_password_characters += element

    list_of_password_characters = string_of_password_characters
    return list_of_password_characters


def run():

    char_of_password = int(input("write your password lenght [8 to 16 characters]: "))
    len_of_password = check_user_input(char_of_password)

    password_element_selection = []
    list_of_password_characters =[]
    question_password = True

    while question_password:
        generate_password(password_element_selection, list_of_password_characters)


        answer = input(str("\nDo you want to execute other option?? (yes/no) "))
        
        if answer == 'yes' or answer == 'y':
            question_password = True
        elif answer == 'no' or answer == 'n':
            question_password = False
        else:
            print("This is not a valid option!!!!")
            question_password = False

    #generate a password based on the inpits selected 
    list_of_password_characters = list_to_string(list_of_password_characters)
    #print(list_of_password_characters)
    random_password = "".join(choice(list_of_password_characters) for each_character in range(len_of_password))
    print('Your random password is: '+ random_password)


if __name__ == '__main__':
    load_dotenv()
    env_path = Path('.')/'.env'
    load_dotenv(dotenv_path=env_path)
    question = True

    while question:
        run()
        
        answer = input(str("\nDo you want to execute other option?? (yes/no) "))
        
        if answer == 'yes' or answer == 'y':
            question = True
        elif answer == 'no' or answer == 'n':
            question = False
        else:
            print("This is not a valid option!!!!")
            question = False