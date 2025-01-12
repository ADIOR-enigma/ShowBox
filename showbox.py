from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
import mysql.connector as ms
import os
from dotenv import load_dotenv

load_dotenv()

# Global variables for MySQL connection
myConnection = None
passWord = ""

console = Console()

def MYSQLconnectionCheck():
    global myConnection
    global passWord
    try:
        passWord = os.getenv("MYSQL_PASSWORD") or Prompt.ask("Password", password=True)
        myConnection = ms.connect(host="localhost", user='root', password=passWord, auth_plugin='mysql_native_password')
        if myConnection.is_connected():
            console.print(Panel.fit("        ok", title="Connection Status",style="bold green"))
            cursor = myConnection.cursor()  # Create the cursor
            cursor.execute("CREATE DATABASE IF NOT EXISTS A_N_DB")
            cursor.execute("USE A_N_DB")
            cursor.close()  # Close the cursor after use
            return myConnection
        else:
            console.print(Panel.fit("       ERROR", title="Connection Status", style="bold red"))
            return None
    except ms.Error as e:
        console.print(Panel.fit(f"Database connection failed: {e}", title="Error", style="bold red"))
        return None

def createTables():
    global myConnection
    cursor = None
    try:
        cursor = myConnection.cursor()  # Create the cursor
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ASeries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                status VARCHAR(50),
                episodes INT
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AMovies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                status VARCHAR(50)
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS NMovies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                status VARCHAR(50)
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS NSeries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                status VARCHAR(50),
                episodes INT
            )""")
        console.print(Panel.fit("WELCOME TO A_N_ DATABASE - YOUR PERSONALISED SHOWBOX!👀📦", title="Welcome"))
    except ms.Error as e:
        console.print(Panel.fit(f"Database operation failed: {e}", title="Error", style="bold red"))
    finally:
        if cursor:
            cursor.close()  # Ensure the cursor is closed
            return myConnection

def getStatusChoices(table):
    return {
        '1': 'Watching',
        '2': 'Watch',
        '3': 'Watched'
    }

def addRecord():
    try:
        while True:
            cursor = myConnection.cursor()  # Create the cursor
            console.print(Panel.fit("Select the category to add a record:", title="Add Record"))
            options = (
                "[0] Exit",
                "[1] ASeries",
                "[2] NSeries",
                "[3] AMovies",
                "[4] NMovies"

            )
            console.print("\n".join(options))
            choice = input("Enter your choice: ")

            if choice == '0':
                console.print(Panel.fit("Exiting the add record menu.", title="Exit", style="bold yellow"))
                break

            tables = {
                '1': "ASeries",
                '2': "NSeries",
                '3': "AMovies",
                '4': "NMovies"

            }
            table = tables.get(choice)
            if not table:
                console.print(Panel.fit("Invalid choice. Please try again.", title="Error", style="bold red"))
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

            if table == "ASeries" or table == "NSeries":
                episodes = Prompt.ask("Enter number of episodes")
                cursor.execute(f"INSERT INTO {table} (title, status, episodes) VALUES (%s, %s, %s)", (title, status, episodes))
            else:
                cursor.execute(f"INSERT INTO {table} (title, status) VALUES (%s, %s)", (title, status))

            myConnection.commit()
            console.print(Panel.fit(f"Record added to {table} successfully!", title="Success"))
    except ms.Error as e:
        console.print(Panel.fit(f"Failed to add record: {e}", title="Error", style="bold red"))
    finally:
        cursor.close()  # Ensure the cursor is closed

def viewAllRecords():
    try:
        cursor = myConnection.cursor()  # Create the cursor
        console.print(Panel.fit("Viewing all records:", title="View All Records"))

        # Create a table to display all records
        all_records_table = Table(title="All Records")

        # Add columns for ASeries
        all_records_table.add_column("Type", justify="left")
        all_records_table.add_column("ID", justify="left")
        all_records_table.add_column("Title", justify="left")
        all_records_table.add_column("Status", justify="left")
        all_records_table.add_column("Episodes", justify="right")

        # Fetch and add records from ASeries
        cursor.execute("SELECT 'ASeries' AS Type, id, title, status, episodes FROM ASeries")
        a_series_records = cursor.fetchall()
        for record in a_series_records:
            all_records_table.add_row(*map(str, record))

        # Fetch and add records from NSeries
        cursor.execute("SELECT 'NSeries' AS Type, id, title, status, episodes FROM NSeries")
        n_series_records = cursor.fetchall()
        for record in n_series_records:
            all_records_table.add_row(*map(str, record))
        # Fetch and add records from AMovies
        cursor.execute("SELECT 'AMovies' AS Type, id, title, status, NULL AS episodes FROM AMovies")
        a_movies_records = cursor.fetchall()
        for record in a_movies_records:
            all_records_table.add_row(*map(str, record))

        # Fetch and add records from NMovies
        cursor.execute("SELECT 'NMovies' AS Type, id, title, status, NULL AS episodes FROM NMovies")
        n_movies_records = cursor.fetchall()
        for record in n_movies_records:
            all_records_table.add_row(*map(str, record))



        # Print the table with all records
        console.print(all_records_table)

    except ms.Error as e:
        console.print(Panel.fit(f"Failed to view records: {e}", title="Error", style="bold red"))
    finally:
        cursor.close()  # Ensure the cursor is closed

def deleteRecord():
    try:
        cursor = myConnection.cursor()  # Create the cursor
        console.print(Panel.fit("Select the category to delete a record:", title="Delete Record"))
        options = (
            "[0] Exit",
            "[1] ASeries",
            "[2] NSeries",
            "[3] AMovies",
            "[4] NMovies"

        )
        console.print("\n".join(options))
        choice = input("Enter your choice: ")

        if choice == '0':
            console.print(Panel.fit("Exiting the delete record menu.", title="Exit", style="bold yellow"))
            return

        tables = {
            '1': "ASeries",
            '2': "NSeries",
            '3': "AMovies",
            '4': "NMovies",

        }
        table = tables.get(choice)
        if not table:
            console.print(Panel.fit("Invalid choice. Please try again.", title="Error", style="bold red"))
            return

        record_id = Prompt.ask("Enter the ID of the record to delete")
        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (record_id,))
        myConnection.commit()
        console.print(Panel.fit(f"Record with ID {record_id} deleted from {table} successfully!", title="Success", style="bold green"))
    except ms.Error as e:
        console.print(Panel.fit(f"Failed to delete record: {e}", title="Error", style="bold red"))
    finally:
        cursor.close()  # Ensure the cursor is closed

def updateRecord():
    try:
        cursor = myConnection.cursor()  # Create the cursor
        console.print(Panel.fit("Select the category to update a record:", title="Update Record"))
        options = (
            "[0] Exit",
            "[1] ASeries",
            "[2] NSeries",
            "[3] AMovies",
            "[4] NMovies",

        )
        console.print("\n".join(options))
        choice = input("Enter your choice: ")

        if choice == '0':
            console.print(Panel.fit("Exiting the update record menu.", title="Exit", style="bold yellow"))
            return

        tables = {
            '1': "ASeries",
            '2': "NSeries",
            '3': "AMovies",
            '4': "NMovies",

        }
        table = tables.get(choice)
        if not table:
            console.print(Panel.fit("Invalid choice. Please try again.", title="Error", style="bold red"))
            return

        record_id = Prompt.ask("Enter the ID of the record to update")
        new_title = Prompt.ask("Enter the new title")
        status_dict = getStatusChoices(table)

        console.print(Panel.fit("Select the new status:", title="Status"))
        for k, v in status_dict.items():
            console.print(f"[{k}] {v}")
        status_choice = input("Enter your choice for status: ")
        status = status_dict.get(status_choice, 'Invalid')

        if status == 'Invalid':
            console.print(Panel.fit("Invalid status choice. Please try again.", title="Error", style="bold red"))
            return

        if table == "ASeries" or table == "NSeries":
            new_episodes = Prompt.ask("Enter the new number of episodes", default="0")
            cursor.execute(f"UPDATE {table} SET title = %s, status = %s, episodes = %s WHERE id = %s", (new_title, status, new_episodes, record_id))
        else:
            cursor.execute(f"UPDATE {table} SET title = %s, status = %s WHERE id = %s", (new_title, status, record_id))

        myConnection.commit()
        console.print(Panel.fit(f"Record with ID {record_id} updated in {table} successfully!", title="Success"))
    except ms.Error as e:
        console.print(Panel.fit(f"Failed to update record: {e}", title="Error", style="bold red"))
    finally:
        cursor.close()  # Ensure the cursor is closed

def searchRecord():
    try:
        cursor = myConnection.cursor()  # Create the cursor
        console.print(Panel.fit("Enter the title to search for:", title="Search Record"))
        search_term = Prompt.ask("Enter the title to search for")

        # Create a table to display search results
        search_results_table = Table(title="Search Results")

        # Add columns for the search results
        search_results_table.add_column("Type", justify="left")
        search_results_table.add_column("Title", justify="left")
        search_results_table.add_column("Status", justify="left")
        search_results_table.add_column("Episodes", justify="right")
        # Search in ASeries
        cursor.execute("SELECT 'ASeries' AS Type, title, status, episodes FROM ASeries WHERE title LIKE %s", ('%' + search_term + '%',))
        a_series_records = cursor.fetchall()
        for record in a_series_records:
            search_results_table.add_row(*map(str, record))

        # Search in NSeries
        cursor.execute("SELECT 'NSeries' AS Type, title, status, episodes FROM NSeries WHERE title LIKE %s", ('%' + search_term + '%',))
        n_series_records = cursor.fetchall()
        for record in n_series_records:
            search_results_table.add_row(*map(str, record))

        # Search in AMovies
        cursor.execute("SELECT 'AMovies' AS Type, title, status, NULL AS episodes FROM AMovies WHERE title LIKE %s", ('%' + search_term + '%',))
        a_movies_records = cursor.fetchall()
        for record in a_movies_records:
            search_results_table.add_row(*map(str, record))

        # Search in NMovies
        cursor.execute("SELECT 'NMovies' AS Type, title, status, NULL AS episodes FROM NMovies WHERE title LIKE %s", ('%' + search_term + '%',))
        n_movies_records = cursor.fetchall()
        for record in n_movies_records:
            search_results_table.add_row(*map(str, record))



        # Print the table with search results
        if search_results_table.row_count > 0:
            console.print(search_results_table)
        else:
            console.print(Panel.fit(f"No records found matching '{search_term}'.", title="Info", style="bold yellow"))

    except ms.Error as e:
        console.print(Panel.fit(f"Failed to search records: {e}", title="Error", style="bold red"))
    finally:
        cursor.close()  # Ensure the cursor is closed

def getTotalData():
    try:
        cursor = myConnection.cursor()

        # Get totals for ASeries
        cursor.execute("SELECT SUM(episodes), COUNT(*) FROM ASeries")
        result_a = cursor.fetchone()
        total_episodes_a = result_a[0] if result_a[0] is not None else 0
        total_seasons_a = result_a[1] if result_a[1] is not None else 0

        # Get totals for NSeries
        cursor.execute("SELECT SUM(episodes), COUNT(*) FROM NSeries")
        result_n = cursor.fetchone()
        total_episodes_n = result_n[0] if result_n[0] is not None else 0
        total_seasons_n = result_n[1] if result_n[1] is not None else 0

        # Get total movies count
        cursor.execute("SELECT COUNT(*) FROM AMovies")
        total_movies_a = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM NMovies")
        total_movies_n = cursor.fetchone()[0] or 0

        # Return the totals, ensuring no NoneType errors occur
        return ((total_episodes_a, total_seasons_a),
                (total_episodes_n, total_seasons_n),
                (total_movies_a, total_movies_n))
    except ms.Error as e:
        console.print(Panel.fit(f"Failed to calculate totals: {e}", title="Error", style="bold red"))
        return ((0, 0), (0, 0), (0, 0))
    finally:
        cursor.close()



# Main function to run the application
def main():
    global myConnection
    MYSQLconnectionCheck()
    if myConnection:
        createTables()
        while True:
            # Get total episodes, seasons, and movies
            (total_episodes_a, total_seasons_a), (total_episodes_n, total_seasons_n), (total_movies_a, total_movies_n) = getTotalData()

            # Calculate combined totals
            combined_total_episodes = total_episodes_a + total_episodes_n
            combined_total_seasons = total_seasons_a + total_seasons_n
            combined_total_movies = total_movies_a + total_movies_n

            # Display all totals in a single box
            totals_message = (
                f"[bold green]Total Episodes in ASeries: {total_episodes_a}[/bold green]\n"
                f"[bold blue]Total Seasons in ASeries: {total_seasons_a}[/bold blue]\n"
                f"[bold green]Total Episodes in NSeries: {total_episodes_n}[/bold green]\n"
                f"[bold blue]Total Seasons in NSeries: {total_seasons_n}[/bold blue]\n"
                f"[bold magenta]Combined Total Episodes: {combined_total_episodes}[/bold magenta]\n"
                f"[bold magenta]Combined Total Seasons: {combined_total_seasons}[/bold magenta]\n"
                f"[bold yellow]Total Movies in AMovies: {total_movies_a}[/bold yellow]\n"  # Assuming total_movies is the sum of both
                f"[bold yellow]Total Movies in NMovies: {total_movies_n}[/bold yellow]\n"  # Assuming total_movies is the sum of both
                f"[bold red]Combined Total Movies: {combined_total_movies}[/bold red]"
            )

            console.print(Panel.fit(totals_message, title="Totals Summary"))

            console.print(Panel.fit("Select an option:", title="Main Menu"))
            options = (
                "[0] Exit",
                "[1] Add Record",
                "[2] View All Records",
                "[3] Delete Record",
                "[4] Update Record",
                "[5] Search Record"
            )
            console.print("\n".join(options))
            choice = input("Enter your choice: ")

            if choice == '0':
                console.print(Panel.fit("Exiting the application.", title="Exit", style="bold yellow"))
                break
            elif choice == '1':
                addRecord()
            elif choice == '2':
                viewAllRecords()
            elif choice == '3':
                deleteRecord()
            elif choice == '4':
                updateRecord()
            elif choice == '5':
                searchRecord()
            else:
                console.print(Panel.fit("Invalid choice. Please try again.", title="Error", style="bold red"))
        myConnection.close()

if __name__ == "__main__":
    main()

















































#Anime-October20,2020Parasyte
#COde-January21,2024
