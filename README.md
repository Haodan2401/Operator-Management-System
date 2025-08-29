# Operator-Management-System
Built on Django and Flask, this full-stack operator management system delivers secure user authentication, seamless CRUD operations for data management, and robust file/image upload capabilities. It offers an efficient backend solution for comprehensive operator administration.

## Features

*   **User Authentication:** Secure login and session management.
*   **CRUD Operations:** Full Create, Read, Update, and Delete functionality for operator data.
*   **File & Image Handling:** Robust upload, storage, and display of files and images.
*   **Admin Dashboard:** A comprehensive interface for managing system entities.

## Tech Stack

*   **Backend:** Django, Flask, Python
*   **Frontend:** HTML, CSS, JavaScript 
*   **Database:** MySQL
*   **File Storage:** Local filesystem

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Haodan2401/Operator-Management-System.git
    cd  Operator-Management-System
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django
    pip install flask
    pip install openpyxl
    
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py makemiragtions
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6.  **Access the application** at `http://localhost:8000`.

