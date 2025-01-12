# A_N_DB - Personalized Showbox
![Screenshot 2025-01-12 215726](https://github.com/user-attachments/assets/db1cfad8-6561-4fb7-90a8-fa2fb8ce644d)
A Python-based command-line database management system for keeping track of series and movies using MySQL.

## Features
- Add, view, update, delete, and search records for:
  - Anime Series (ASeries)
  - Normal Series (NSeries)
  - Anime Movies (AMovies)
  - Normal Movies (NMovies)
- MySQL database integration
- Interactive CLI using `rich` for a better user experience
- Secure password handling with `dotenv`

## Technologies Used
- Python
- MySQL
- `rich` for CLI aesthetics
- `python-dotenv` for secure environment variable handling

## Prerequisites
- Python 3.x installed
- MySQL Server installed and running
- Required Python packages:
  ```bash
  pip install rich mysql-connector-python python-dotenv
  ```

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repo-link>
   ```
2. Navigate to the project directory:
   ```bash
   cd A_N_DB
   ```
3. Create a `.env` file in the project root and add your MySQL password:
   ```plaintext
   MYSQL_PASSWORD=yourpassword
   ```
4. Run the Python script:
   ```bash
   python main.py
   ```

## Database Schema
- `NMovies` (id, title, status)
- `ASeries` (id, title, status, episodes)
- `NSeries` (id, title, status, episodes)
- `AMovies` (id, title, status)


## Usage
1. **Main Menu**
   - Add Record
   - View All Records
   - Delete Record
   - Update Record
   - Search Record
2. Follow on-screen prompts for data entry and management.

## Security Note
- The password can be provided through the `.env` file for better security.

## Troubleshooting
- Ensure MySQL server is running.
- Verify your password in the `.env` file.
