#update 23-04-2024 Somehow i dont know why this code only works in python idle from microsoft store
#update 24-04-2024to run it without the ms py app need to remove all the properties of .env file 
#(that means the file will not be secure to type user and password in front of a rachter)
#update 20-06-2024but not now cause i have integrated "rich" module
#520
import time
from rich.progress import track
for i in track(range(15),description="[green]Loading..."):
    time.sleep(0.1)

import mysql.connector as ms
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

load_dotenv()

# Global variables for MySQL connection
myConnection = None
userName = ""
passWord = ""

console = Console()

def MYSQLconnectionCheck():
    global passWord

    console.print(Panel.fit("ENTER MYSQL SERVER'S PASSWORD", title="Password"))
    pW = Prompt.ask("Password", password=True)
    try:
        passWord = os.getenv(pW) or pW
        myConnection = ms.connect(host="localhost", user='root', password=passWord, auth_plugin='mysql_native_password')
        if myConnection.is_connected():
            console.print(Panel.fit("CONGRATULATIONS! YOUR MYSQL CONNECTION HAS BEEN ESTABLISHED 🤖!", title="Connection Status"))
            with myConnection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS A_N_DB")
                cursor.execute("USE A_N_DB")
            return myConnection
        else:
            console.print(Panel.fit("ERROR ESTABLISHING MYSQL CONNECTION CHECK USERNAME AND PASSWORD!", title="Error", style="bold red"))
            return None
    except ms.Error as e:
        console.print(Panel.fit(f"Database connection failed: {e}", title="Error", style="bold red"))
        return None

def createTables():
    try:
        with myConnection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ASeries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    status VARCHAR(50),
                    episodes INT,
                    seasons INT
                )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS AMovies (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    status VARCHAR(50),
                    movies INT
                )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS NMovies (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    status VARCHAR(50),
                    movies INT
                )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS NSeries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    status VARCHAR(50),
                    episodes INT,
                    seasons INT
                )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS VdGames (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    status VARCHAR(50),
                    platform VARCHAR(100)
                )""")
            console.print(Panel.fit("WELCOME TO A_N_ DATABASE - YOUR 😎 PERSONALISED SHOWBOX!👀📦  ✔ ✨", title="Welcome"))
    except ms.Error as e:
        console.print(Panel.fit(f"Database operation failed: {e}", title="Error", style="bold red"))

def getStatusChoices(table):
    if table == "VdGames":
        return {
            '1': 'Playing',
            '2': 'On Hold',
            '3': 'Completed'
        }
    else:
        return {
            '1': 'Watching',
            '2': 'Planned',
            '3': 'Completed',
            '4': 'COMICs'
        }

def addRecord():
    try:
        while True:
            with myConnection.cursor() as cursor:
                console.print(Panel.fit("Select the category to add a record:", title="Add Record"))
                options = (
                    "[1] ASeries",
                    "[2] AMovies",
                    "[3] NMovies",
                    "[4] NSeries",
                    "[5] VdGames"
                )
                console.print("\n".join(options))
                choice = input("Enter your choice: ")

                tables = {
                    '1': "ASeries",
                    '2': "AMovies",
                    '3': "NMovies",
                    '4': "NSeries",
                    '5': "VdGames"
                }
                table = tables.get(choice)
                if not table:
                    console.print(Panel.fit("Invalid choice.", title="Error", style="bold red"))
                    continue
                
                title = Prompt.ask("Enter title")
                status_dict = getStatusChoices(table)

                console.print(Panel.fit("Select the status:", title="Status"))
                for k, v in status_dict.items():
                    console.print(f"[{k}] {v}")
                status_choice = input("Enter your choice for status: ")
                status = status_dict.get(status_choice, 'Invalid')
                
                if status == 'Invalid':
                    console.print(Panel.fit("Invalid status choice. Please try again.", title="Error", style="bold red"))
                    continue
                
                if table in ['ASeries', 'NSeries']:
                    episodes = Prompt.ask("Enter number of episodes", default="0")
                    seasons = Prompt.ask("Enter number of seasons", default="0")
                    sql = f"INSERT INTO {table} (title, status, episodes, seasons) VALUES (%s, %s, %s, %s)"
                    values = (title, status, int(episodes), int(seasons))
                elif table == 'VdGames':
                    platform = Prompt.ask("Enter the platform")
                    sql = f"INSERT INTO {table} (title, status, platform) VALUES (%s, %s, %s)"
                    values = (title, status, platform)
                else:
                    movies = Prompt.ask("Enter number of movies", default="0")
                    sql = f"INSERT INTO {table} (title, status, movies) VALUES (%s, %s, %s)"
                    values = (title, status, int(movies))

                cursor.execute(sql, values)
                myConnection.commit()
                console.print(Panel.fit("Record added successfully!", title="Success", style="bold green"))

                if not Confirm.ask("Do you want to add another record?"):
                    break
    except Exception as e:
        console.print(Panel.fit(f"Something went wrong: {e}", title="Error", style="bold red"))

def viewAllRecords():
    try:
        with myConnection.cursor() as cursor:
            console.print(Panel.fit("Viewing records from all categories:", title="View Records"))

            tables = {
                "ASeries": ["ID", "Title", "Status", "Episodes", "Seasons"],
                "AMovies": ["ID", "Title", "Status", "Movies"],
                "NMovies": ["ID", "Title", "Status", "Movies"],
                "NSeries": ["ID", "Title", "Status", "Episodes", "Seasons"],
                "VdGames": ["ID", "Title", "Status", "Platform"]
            }

            for table, columns in tables.items():
                cursor.execute(f"SELECT * FROM {table}")
                records = cursor.fetchall()
                if records:
                    record_table = Table(show_header=True, header_style="bold magenta")
                    for col in columns:
                        record_table.add_column(col, style="dim" if col == "ID" else None)
                    for record in records:
                        record_table.add_row(*map(str, record))
                    console.print(Panel(record_table, title=table.replace("N", "Netflix ").replace("A", "Anime ").replace("Vd", "Video ")))
    except Exception as e:
        console.print(Panel.fit(f"Something went wrong: {e}", title="Error", style="bold red"))

def deleteRecord():
    try:
        with myConnection.cursor() as cursor:
            console.print(Panel.fit("Select the category from which to delete a record:", title="Delete Record"))
            options = (
                "[1] ASeries",
                "[2] AMovies",
                "[3] NMovies",
                "[4] NSeries",
                "[5] VdGames"
            )
            console.print("\n".join(options))
            choice = Prompt.ask("Enter your choice")

            tables = {
                '1': "ASeries",
                '2': "AMovies",
                '3': "NMovies",
                '4': "NSeries",
                '5': "VdGames"
            }
            table = tables.get(choice)
            if not table:
                console.print(Panel.fit("Invalid choice.", title="Error", style="bold red"))
                return

            record_id = Prompt.ask("Enter the ID of the record to delete")
            if not record_id.isdigit():
                console.print(Panel.fit("Invalid input for record ID. Please enter a numeric value.", title="Error", style="bold red"))
                return  

            sql = f"DELETE FROM {table} WHERE id = %s"
            cursor.execute(sql, (record_id,))
            myConnection.commit()

            if cursor.rowcount > 0:
                console.print(Panel.fit("Record deleted successfully!", title="Success", style="bold green"))
            else:
                console.print(Panel.fit("Record not found.", title="Error", style="bold red"))
    except Exception as e:
        console.print(Panel.fit(f"Something went wrong: {e}", title="Error", style="bold red"))

def updateRecord():
    try:
        with myConnection.cursor() as cursor:
            console.print(Panel.fit("Select the category in which to update a record:", title="Update Record"))
            options = (
                "[1] ASeries",
                "[2] AMovies",
                "[3] NMovies",
                "[4] NSeries",
                "[5] VdGames"
            )
            console.print("\n".join(options))
            choice = Prompt.ask("Enter your choice")
            
            if choice == '1' or choice == '4':
                table = "ASeries" if choice == '1' else "NSeries"
                update_fields = "title, status, episodes, seasons"
            elif choice == '2' or choice == '3':
                table = "AMovies" if choice == '2' else "NMovies"
                update_fields = "title, status, movies"
            elif choice == '5':
                table = "VdGames"
                update_fields = "title, status, platform"
            else:
                console.print(Panel.fit("Invalid choice.", title="Error", style="bold red"))
                return
            
            record_id = Prompt.ask("Enter the ID of the record to update")
            console.print(f"Enter new values for {update_fields}")
            values = Prompt.ask("Enter values separated by commas (e.g., Title, Status, 10, 2)").split(',')
            
            if choice in ['1', '4']:  # Anime Series or Series
                sql = f"UPDATE {table} SET title = %s, status = %s, episodes = %s, seasons = %s WHERE id = %s"
            elif choice == '5':  # VdGames
                sql = f"UPDATE {table} SET title = %s, status = %s, platform = %s WHERE id = %s"
            else:  # Movies or Netflix Movies
                sql = f"UPDATE {table} SET title = %s, status = %s, movies = %s WHERE id = %s"
            
            values.append(record_id)  # Add record_id at the end for the WHERE clause
            cursor.execute(sql, values)
            myConnection.commit()
            
            if cursor.rowcount > 0:
                console.print(Panel.fit("Record updated successfully!", title="Success", style="bold green"))
            else:
                console.print(Panel.fit("Record not found or no changes made.", title="Error", style="bold red"))
    except Exception as e:
        console.print(Panel.fit(f"Something went wrong: {e}", title="Error", style="bold red"))

def searchRecord():
    try:
        with myConnection.cursor() as cursor:
            search_type = Prompt.ask("Do you want to search by title or status? (Enter 't' or 's')").lower()
            
            tables = ["ASeries", "AMovies", "NMovies", "NSeries", "VdGames"]
            results = []
            
            if search_type == 't':
                search_title = Prompt.ask("Enter the title or part of the title to search for")
                search_pattern = f"%{search_title}%"
        
                for table in tables:
                    sql = f"SELECT * FROM {table} WHERE title LIKE %s"
                    cursor.execute(sql, (search_pattern,))
                    results.extend(cursor.fetchall())

            elif search_type == 's':
                console.print(Panel.fit("Select the category to search status:", title="Search Status"))
                options = (
                    "[1] All Categories",
                    "[6] VdGames"
                )
                console.print("\n".join(options))
                category_choice = Prompt.ask("Enter your choice")

                if category_choice == '6':  # VdGames
                    console.print(Panel.fit("Select the status:", title="Status"))
                    status_options = (
                        "[1] Playing",
                        "[2] On Hold",
                        "[3] Completed"
                    )
                    console.print("\n".join(status_options))
                    status_choice = Prompt.ask("Enter your choice for status")
                    status_dict = {'1': 'Playing', '2': 'On Hold', '3': 'Completed'}
                else:
                    console.print(Panel.fit("Select the status:", title="Status"))
                    status_options = (
                        "[1] Watching",
                        "[2] Planned",
                        "[3] Completed",
                        "[4] COMICs"
                    )
                    console.print("\n".join(status_options))
                    status_choice = Prompt.ask("Enter your choice for status")
                    status_dict = {'1': 'Watching', '2': 'Planned', '3': 'Completed', '4': 'COMICs'}
                
                status = status_dict.get(status_choice, 'Invalid')
                if status == 'Invalid':
                    console.print(Panel.fit("Invalid status choice.", title="Error", style="bold red"))
                    return
                
                if category_choice == '1':  # All Categories
                    for table in tables:
                        sql = f"SELECT * FROM {table} WHERE status = %s"
                        cursor.execute(sql, (status,))
                        results.extend(cursor.fetchall())
                else:
                    table = tables[int(category_choice) - 1]
                    sql = f"SELECT * FROM {table} WHERE status = %s"
                    cursor.execute(sql, (status,))
                    results.extend(cursor.fetchall())
                
            else:
                console.print(Panel.fit("Invalid search type.", title="Error", style="bold red"))
                return

            if results:
                console.print(Panel.fit(f"Found {len(results)} record(s):", title="Results"))
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="dim")
                table.add_column("Title")
                table.add_column("Status")
                
                for result in results:
                    table.add_row(str(result[0]), result[1], result[2])
                
                console.print(table)
            else:
                console.print(Panel.fit("No records found matching the search criteria.", title="Results", style="bold red"))
    except Exception as e:
        console.print(Panel.fit(f"Something went wrong: {e}", title="Error", style="bold red"))

def main():
    global myConnection 
    myConnection = MYSQLconnectionCheck()
    if myConnection:
        createTables()
        while True:
            console.print(Panel.fit("What would you like to do?", title="Menu", border_style="blue"))
            options = (
                "[1] Add a new record",
                "[2] View all records",
                "[3] Delete a record",
                "[4] Update a record",
                "[5] Search a record",
                "[6] Exit"
            )
            console.print("\n".join(options))
            choice = input("Enter your choice<1-6>: ")

            if choice == '1':
                addRecord()
            elif choice == '2':
                viewAllRecords()
            elif choice == '3':
                deleteRecord()
            elif choice == '4':
                updateRecord()
            elif choice == '5':
                searchRecord()
            elif choice == '6':
                console.print(Panel.fit("Thank you for using this application. Have a great day🤖!", title="Goodbye", border_style="green"))
                for i in track(range(15),description="[red]Exiting..."):
                    time.sleep(0.1)
                break
            else:
                console.print(Panel.fit("Invalid choice. Please try again.", title="Error", style="bold red"))
    else:
        console.print(Panel.fit("Failed to connect to MySQL. Exiting the program.", title="Error", style="bold red"))

    
if __name__ == "__main__":
    main()

















#Anime-October20,2020Parasyte
#COde-January21,2024