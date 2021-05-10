import mariadb
import sys

# Connect to MariaDB Platform
def connect():
    try:
        conn = mariadb.connect(
            user = "root",
            password = "toor",
            database = "hospital",
            port = 3306
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    return conn

# refactoring of query execution
    # prevents program failure upon query error
def execute(cur, query):
    try:
        cur.execute(query)
    except mariadb.Error as e:
        print(f"Error executing query: {e}")
        print()
        
    return cur

# displays the main menu
def main_menu():
    print("Enter the number of the action you wish to make:")
    print("1. Show all tables")
    print("2. Select all from a table")
    print("3. Insert into table")
    print("4. Delete from table")
    print("0. Exit")

    try:
        selection = int(input())
    except:
        selection = -1

    print()
    return selection

# generates a menu based on an arbitrary list of items, with "Go Back" option
def generic_menu(header, items):
    if header != "":
        print(header)

    i = 1
    for item in items:
        # fixes formatting if the item is a cursor-generated value
        if (str(item).startswith("('")):
            print(str(i) + ". " + str(item)[2:len(str(item)) - 3])
        # leaves item as is if it's a custom value
        else:
            print(str(i) + ". " + str(item))
        i += 1
    print("0. [Go Back]")
    
    try:
        selection = int(input())
    except:
        selection = -1

    print()
    return selection

def main():    
    conn = connect()
    cur = conn.cursor()

    main_menu_selection = 1
    while main_menu_selection != 0:
        main_menu_selection = main_menu()

        if main_menu_selection == 0:
            print("Exiting the program.")

        # show all tables
        elif main_menu_selection == 1:
            cur = execute(cur, "SHOW TABLES")
            print("All tables:")
            for table_name, in cur:
                print(table_name)
            print()
        # select all
        elif main_menu_selection == 2:
            cur = execute(cur, "SHOW TABLES")
            tables = cur.fetchall()            
            
            this_menu_selection = 1
            while this_menu_selection != 0:
                this_menu_selection = generic_menu("Choose a table", tables)
                if this_menu_selection > 0 and this_menu_selection <= len(tables):
                    table_name = str(tables[this_menu_selection - 1])
                    table_name = table_name[2:len(table_name) - 3]
                    
                    cur = execute(cur, "SHOW COLUMNS FROM " + table_name)
                    columns = cur.fetchall()
                    for column in columns:
                        print(str(column[0]) + "\t", end = '', flush = True)
                    print()

                    cur = execute(cur, "SELECT * FROM " + table_name)
                    for row in cur:
                        for item in row:
                            print(str(item) + "\t", end = '', flush = True)
                        print()
                    print()

                    this_menu_selection = 0

                elif this_menu_selection != 0:
                    print("Invalid selection. Please try again:")
        # insert
        elif main_menu_selection == 3:
            cur = execute(cur, "SHOW TABLES")
            tables = cur.fetchall()
            
            this_menu_selection = 1
            while this_menu_selection != 0:
                this_menu_selection = generic_menu("Choose a table", tables)
                if this_menu_selection > 0 and this_menu_selection <= len(tables):
                    table_name = str(tables[this_menu_selection - 1])
                    table_name = table_name[2:len(table_name) - 3]
                    
                    cur = execute(cur, "SHOW COLUMNS FROM " + table_name)
                    columns = cur.fetchall()
                    values = []
                    query = "INSERT INTO " + table_name + " ("

                    print("Enter each column's value; leave blank to enter NULL or to follow AUTO_INCREMENT:")
                    for column in columns:
                        print(str(column[0]) + "\t", end = '', flush = True)
                        
                        # getting correct type for the column
                        temp_input = input()
                        if temp_input != "":
                            values.append(temp_input)
                            query += str(column[0]) + ", "
                    print()

                    query = query[0:len(query) - 2]
                    query += ") VALUES ("
                    for value in values:
                        query += value + ", "
                    query = query[0:len(query) - 2]
                    query += ") "

                    # inserts row here
                    cur = execute(cur, query)
                    conn.commit()
                    this_menu_selection = 0

                elif this_menu_selection != 0:
                    print("Invalid selection. Please try again:")
        # delete
        elif main_menu_selection == 4:
            cur = execute(cur, "SHOW TABLES")
            tables = cur.fetchall()
            
            this_menu_selection = 1
            while this_menu_selection != 0:
                this_menu_selection = generic_menu("Choose a table", tables)
                if this_menu_selection > 0 and this_menu_selection <= len(tables):
                    table_name = str(tables[this_menu_selection - 1])
                    table_name = table_name[2:len(table_name) - 3]
                    
                    delete_menu_selection = 1
                    while delete_menu_selection != 0:
                        delete_menu_items = ["Delete with conditions", "Delete all data from table"]
                        delete_menu_selection = generic_menu("", delete_menu_items)

                        if delete_menu_selection == 1:
                            cur = execute(cur, "SHOW COLUMNS FROM " + table_name)
                            columns = cur.fetchall()
                            query = "DELETE FROM " + table_name + " WHERE "

                            print("Enter equals condition for column, or \"(NOT) NULL\"; leave blank to skip column")
                            where_conditions = 0
                            for column in columns:                        
                                print(str(column[0]) + " = ", end = '', flush = True)
                                temp_input = input()
                                if temp_input != "":
                                    where_conditions += 1
                                    if where_conditions > 1:
                                        query += " AND "
                                    if temp_input == "NOT NULL" or temp_input == "NULL":
                                        query += str(column[0]) + " IS " + temp_input
                                    else:
                                        query += str(column[0]) + " = " + temp_input

                            if where_conditions > 0:
                                cur = execute(cur, query)
                            else:
                                print("No conditions found.")
                            # sends the menu back regardless; repeated deletes on the same table are probably not desirable
                            delete_menu_selection = 0
                            print()

                        elif delete_menu_selection == 2:
                            print("This will delete the entire contents of " + table_name + ". Are you sure? [Y/N]")
                            delete_confirmation = input()
                            if (delete_confirmation == "Y" or delete_confirmation == "y"):
                                cur = execute(cur, "DELETE FROM " + table_name)

                            delete_menu_selection = 0
                            print()

                        elif delete_menu_selection != 0:
                            print("Invalid selection. Please try again:")

                    conn.commit()
                    this_menu_selection = 0

                elif this_menu_selection != 0:
                    print("Invalid selection. Please try again:")

        else:
            print("Invalid selection. Please try again:")

    conn.close()
    
if __name__ == "__main__":
	main()
