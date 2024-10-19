# Expense Management System
This is an Expense management system with streamlit as Frontend , FastAPI as Backend and MySQL as Databaase.

## Project Structure

- **frontend/**: Contains the Streamlit application code.
- **backend/**: Contains the FastAPI backend server code.
- **tests/**: Contains the test cases for both frontend and backend.
- **requirements.txt**: Lists the required Python packages.
- **README.md**: Provides an overview and instructions for the project.
- **run_app.py** : For creating exe file for application


## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chirag-agrawal24/Expense-Tracking-System.git
   cd expense-management-system
   ```
2. **Install dependencies:**:   
   ```commandline
    pip install -r requirements.txt
    ```
3. **Setup MySQL and change [sql.json](backend/sql.json) file in as per your configuration**
### Method-1 for running app:
   
   1. **Run the FastAPI server:**:   
   ```commandline
    uvicorn server.server:app --reload
   ```
   2. **Run the Streamlit app:**:   
   ```commandline
    streamlit run frontend/app.py
   ```
### Method-2: ("No need to separately handle opening/closing app)
   1. **cd to project directory in command line**
   2. **Run this command**:
   ```commandline
    pyinstaller --onefile run_app.py
   ```

   3. **A new folder name dist will be created**
   1. **Go to dist -> Then double click the run_app.exe**
