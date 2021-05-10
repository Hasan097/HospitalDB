import random

FIRST_NAME_DATASET_FILE = 'first_names.txt'
LAST_NAME_DATASET_FILE = 'last_names.txt'
STREET_NAME_DATASET_FILE = 'street_names.txt'

ROLE_TOTAL = 20

STAFF_ID_START = 1000
STAFF_ID_END = 9999

# Change these out however you like
HOSPITAL_NAME = "HOSPITAL NAME"
HOSPITAL_EMAIL_DOMAIN = "HOSPITAL.DOMAIN"
HOSPITAL_LOCATION = "Caretaker, KS"

def main():

	staffRolesList = ['Administration', 'Doctor', 'Nurse', 'Sanitation']

	# Parse first names into firstNamesList.
	with open(FIRST_NAME_DATASET_FILE, 'r') as firstNamesInput:
		firstNameList = firstNamesInput.read().splitlines()

	# Parse last names into lastNamesList.
	with open(LAST_NAME_DATASET_FILE, 'r') as lastNamesInput:
		lastNameList = lastNamesInput.read().splitlines()

	# Parse street names into streetNamesList.
	with open(STREET_NAME_DATASET_FILE, 'r') as streetNamesInput:
		streetNameList = streetNamesInput.read().splitlines()

	# For each role, generate ROLE_TOTAL insert statements.
	for role in staffRolesList:
		for i in range(ROLE_TOTAL):
			generate_staff_inserts(role, firstNameList, lastNameList, streetNameList)

# Generate staff id using the first two letters of the staff role and a random number.
def generate_staff_id(staffRole):
	return staffRole[0:2].upper() + str(random.randint(STAFF_ID_START, STAFF_ID_END))

# Generate a random first and last name using the individual names parsed from the common name datasets.
def generate_staff_name(firstNameList, lastNameList):
	return firstNameList[random.randint(0, len(firstNameList) - 1)] + ' ' + lastNameList[random.randint(0, len(lastNameList) - 1)]

def generate_birthdate():
	return str(random.randint(1, 12)) + "-" + str(random.randint(1, 27)) + "-" + str(random.randint(1946, 1990))

def generate_address(streetNameList):
	return str(random.randint(1000, 9999)) + " " + streetNameList[random.randint(0, len(streetNameList) - 1)] + ", " + HOSPITAL_LOCATION

def generate_employment_date():
	return str(random.randint(1, 12)) + "-" + str(random.randint(1, 27)) + "-" + str(random.randint(1991, 2020))

def generate_salary(staffRole):

	salary = random.randint(36, 80)

	if staffRole == "Doctor":
		salary = salary + 100

	return salary * 1000

def generate_staff_inserts(staffRole, possibleFirstNames, possibleLastNames, possibleStreetNames):

	randomName = generate_staff_name(possibleFirstNames, possibleLastNames)
	staffId = generate_staff_id(staffRole)
	randomBirthdate = generate_birthdate()
	randomAddress = generate_address(possibleStreetNames)
	randomEmail = randomName.replace(" ", ".") + "@" + HOSPITAL_EMAIL_DOMAIN + ".com"
	randomEmploymentDate = generate_employment_date()
	randomSalary = generate_salary(staffRole)

	print(f'INSERT INTO employee (\'employee_id\', \'employee_type\', \'name\', \'date_of_birth\', \'address\', \'email\', \'employment_date\', \'salary\')\
	VALUES (\'{staffId}\', \'{staffRole}\', \'{randomName}\', \'{randomBirthdate}\', \'{randomAddress}\', \'{randomEmail}\', \'{randomEmploymentDate}\', {randomSalary});')

if __name__ == "__main__":
	main()
