import sys
from models.employer import Employer
from models.nanny import Nanny

def print_menu():
    print("\nNanny Bureau Application")
    print("1. Add Employer")
    print("2. Add Nanny")
    print("3. View All Employers")
    print("4. View All Nannies")
    print("5. Update Employer")
    print("6. Update Nanny")
    print("7. Delete Employer")
    print("8. Delete Nanny")
    print("9. View Nannies by Employer")
    print("10. Find Employer by Name")
    print("11. Find Employer by ID")
    print("12. Find Nanny by Name")
    print("13. Find Nanny by ID")
    print("14. Exit")

def add_employer():
    name = input("Enter employer's name: ")
    location = input("Enter employer's location: ")
    number_of_kids = int(input("Enter number of kids: "))
    employer = Employer.create(name, location, number_of_kids)
    print(f"Employer added: {employer}")

def add_nanny():
    name = input("Enter nanny's name: ")
    age = int(input("Enter nanny's age: "))
    salary_expectation = float(input("Enter nanny's salary expectation: "))
    employer_id = int(input("Enter employer's ID: "))
    nanny = Nanny.create(name, age, salary_expectation, employer_id)
    print(f"Nanny added: {nanny}")

def view_all_employers():
    employers = Employer.get_all()
    for employer in employers:
        print(employer)

def view_all_nannies():
    nannies = Nanny.get_all()
    for nanny in nannies:
        print(nanny)

def update_employer():
    id = int(input("Enter employer ID to update: "))
    employer = Employer.find_by_id(id)
    if employer:
        employer.name = input("Enter new name: ")
        employer.location = input("Enter new location: ")
        employer.number_of_kids = int(input("Enter new number of kids: "))
        employer.update()
        print(f"Employer updated: {employer}")
    else:
        print("Employer not found.")

def update_nanny():
    id = int(input("Enter nanny ID to update: "))
    nanny = Nanny.find_by_id(id)
    if nanny:
        nanny.name = input("Enter new name: ")
        nanny.age = int(input("Enter new age: "))
        nanny.salary_expectation = float(input("Enter new salary expectation: "))
        nanny.employer_id = int(input("Enter new employer ID: "))
        nanny.update()
        print(f"Nanny updated: {nanny}")
    else:
        print("Nanny not found.")

def delete_employer():
    id = int(input("Enter employer ID to delete: "))
    employer = Employer.find_by_id(id)
    if employer:
        employer.delete()
        print(f"Employer deleted: {employer}")
    else:
        print("Employer not found.")

def delete_nanny():
    id = int(input("Enter nanny ID to delete: "))
    nanny = Nanny.find_by_id(id)
    if nanny:
        nanny.delete()
        print(f"Nanny deleted: {nanny}")
    else:
        print("Nanny not found.")

def view_nannies_by_employer():
    employer_id = int(input("Enter employer ID to view their nannies: "))
    employer = Employer.find_by_id(employer_id)
    if employer:
        nannies = employer.nannies()
        for nanny in nannies:
            print(nanny)
    else:
        print("Employer not found.")

def find_employer_by_name():
    name = input("Enter employer name to find: ")
    employer = Employer.find_by_name(name)
    if employer:
        print(f"Employer found: {employer}")
    else:
        print("Employer not found.")

def find_employer_by_id():
    id = int(input("Enter employer ID to find: "))
    employer = Employer.find_by_id(id)
    if employer:
        print(f"Employer found: {employer}")
    else:
        print("Employer not found.")

def find_nanny_by_name():
    name = input("Enter nanny name to find: ")
    nanny = Nanny.find_by_name(name)
    if nanny:
        print(f"Nanny found: {nanny}")
    else:
        print("Nanny not found.")

def find_nanny_by_id():
    id = int(input("Enter nanny ID to find: "))
    nanny = Nanny.find_by_id(id)
    if nanny:
        print(f"Nanny found: {nanny}")
    else:
        print("Nanny not found.")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            add_employer()
        elif choice == '2':
            add_nanny()
        elif choice == '3':
            view_all_employers()
        elif choice == '4':
            view_all_nannies()
        elif choice == '5':
            update_employer()
        elif choice == '6':
            update_nanny()
        elif choice == '7':
            delete_employer()
        elif choice == '8':
            delete_nanny()
        elif choice == '9':
            view_nannies_by_employer()
        elif choice == '10':
            find_employer_by_name()
        elif choice == '11':
            find_employer_by_id()
        elif choice == '12':
            find_nanny_by_name()
        elif choice == '13':
            find_nanny_by_id()
        elif choice == '14':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()