# LogDB Backend

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Database Schema](#database-schema)
5. [API Endpoints](#api-endpoints)
6. [Development Environment Setup](#development-environment-setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Database Setup](#database-setup)
    - [Configuration](#configuration)
    - [Running the Development Server](#running-the-development-server)
7. [Usage](#usage)
8. [Contributing](#contributing)
9. [License](#license)
10. [Contact](#contact)

---

## Project Overview

**LogDB** is a centralized project log management system designed to aggregate, store, and manage logs from various subprojects and users within large-scale projects. The system enhances project oversight, streamlines log storage, and ensures secure access to log data based on user roles. This backend is developed using Django, adhering strictly to raw SQL interactions as per academic requirements.

---

## Features

- **User Management**
  - **Register New User:** Create new user accounts with roles.
  - **User Login:** Authenticate users and issue JWT tokens for secure access.

- **Project Management**
  - **Create Project:** Allow authenticated users to create new projects.

- **Log Management**
  - **View Logs:** Retrieve and view logs based on various filters.
  - **Submit Log:** Endpoint to submit logs using REST API with Bearer Authentication.

- **Audit Management**
  - **View Audit Logs:** Access audit logs recording user activities within the system.

---

## Technologies Used

- **Backend:**
  - [Django](https://www.djangoproject.com/) - Web framework for Python
  - [PyMySQL](https://pypi.org/project/PyMySQL/) - MySQL client for Python
  - [PyJWT](https://pypi.org/project/PyJWT/) - JSON Web Tokens for authentication

- **Database:**
  - [MySQL](https://www.mysql.com/) - Relational Database Management System

- **Others:**
  - [Git](https://git-scm.com/) - Version control
  - [Conda](https://docs.conda.io/en/latest/) - Environment management

---

## Database Schema

The database schema is designed to support user management, project management, log storage, and audit logging. Below are the primary tables:

- **Users**
- **Roles**
- **Projects**
- **UserProjects**
- **Logs**
- **AuditLogs**

*Refer to the [Database Schema](#database-schema) section for detailed table structures.*

---

## API Endpoints

The API follows RESTful principles and uses JSON for request and response bodies. Authentication is handled via JWT tokens passed in the `Authorization` header.

### Authentication

- **Register User**
  - **Endpoint:** `/api/auth/register/`
  - **Method:** `POST`
  - **Description:** Register a new user.

- **User Login**
  - **Endpoint:** `/api/auth/login/`
  - **Method:** `POST`
  - **Description:** Authenticate user and receive a JWT token.

### Project Management

- **Create Project**
  - **Endpoint:** `/api/projects/`
  - **Method:** `POST`
  - **Description:** Create a new project.

### Log Management

- **View Logs**
  - **Endpoint:** `/api/logs/`
  - **Method:** `GET`
  - **Description:** Retrieve logs with optional filtering.

- **Submit Log**
  - **Endpoint:** `/api/logs/submit/`
  - **Method:** `POST`
  - **Description:** Submit a new log entry via REST API.

### Audit Management

- **View Audit Logs**
  - **Endpoint:** `/api/audit-logs/`
  - **Method:** `GET`
  - **Description:** Retrieve audit logs for authorized users.

*For detailed API documentation, refer to the [API Documentation](#api-endpoints) section.*

---

## Development Environment Setup

Follow the steps below to set up the development environment for the LogDB backend.

### Prerequisites

Ensure you have the following installed on your machine:

- **Conda:** [Install Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- **Python 3.8+**
- **MySQL Server**
- **Git**
- **pip** (Python package installer, comes with Python)

### Installation

1. **Clone the Repository**

   Navigate to your desired directory and clone the repository:

   ```bash
   git clone https://github.com/yourusername/logdb_project.git
   cd logdb_project/backend
   ```

2. **Create a Conda Environment**

   Create and activate a new Conda environment named `logdb_env` with Python 3.8:

   ```bash
   conda create -n logdb_env python=3.8
   conda activate logdb_env
   ```

3. **Install Dependencies**

   Since some packages are not available via Conda, we'll install them using `pip`. Here's how to handle both:

   - **Install Conda Packages:**

     Install packages available through Conda first:

     ```bash
     conda install django pymysql
     ```

   - **Install Pip Packages:**

     Install packages that are not available via Conda using `pip`:

     ```bash
     pip install PyJWT
     ```

   **Note:** If you need to install additional packages, repeat the above steps accordingly.

### Database Setup

1. **Create the Database**

   Log into your MySQL server and create the `logdb` database:

   ```sql
   CREATE DATABASE logdb;
   ```

2. **Create Tables**

   Use the provided SQL script to create the necessary tables.

   - **Navigate to the SQL Script Directory**

     Assuming you have your SQL scripts in a directory named `sql_scripts`:

     ```bash
     cd sql_scripts
     ```

   - **Run the SQL Script**

     Execute the SQL script to create tables:

     ```bash
     mysql -u your_username -p logdb < create_tables.sql
     ```

     *Replace `your_username` with your actual MySQL username. You'll be prompted for your password.*

### Configuration

1. **Set Up Django Settings**

   Open `logdb_project/settings.py` and configure the database settings:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'logdb',
           'USER': 'your_mysql_username',
           'PASSWORD': 'your_mysql_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }

   ```

   **Security Tip:** For better security, store `SECRET_KEY` and other sensitive information in environment variables or a separate configuration file not tracked by version control.

### Running the Development Server

1. **Apply Migrations (Optional)**

   Since we're using raw SQL and not Django's ORM, migrations are not strictly necessary. However, to set up any Django-specific tables (like for admin), you can run:

   ```bash
   python manage.py migrate
   ```

2. **Start the Django Development Server**

   ```bash
   python manage.py runserver
   ```

3. **Access the Application**

   Open your browser and navigate to `http://localhost:8000/` to access the API endpoints.

---

## Usage

### Register a New User

- **Endpoint:** `/api/auth/register/`
- **Method:** `POST`
- **Payload:**

  ```json
  {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "SecurePassword123!"
  }
  ```

- **Response:**

  ```json
  {
    "message": "User registered successfully"
  }
  ```

### User Login

- **Endpoint:** `/api/auth/login/`
- **Method:** `POST`
- **Payload:**

  ```json
  {
    "email": "johndoe@example.com",
    "password": "SecurePassword123!"
  }
  ```

- **Response:**

  ```json
  {
    "token": "your_jwt_token_here"
  }
  ```

### Create a New Project

- **Endpoint:** `/api/projects/`
- **Method:** `POST`
- **Headers:**
  - `Authorization: Bearer your_jwt_token_here`
- **Payload:**

  ```json
  {
    "projectName": "Project Alpha",
    "description": "A new project for the Alpha release.",
    "status": "Planning",
    "startDate": "2024-01-01",
    "endDate": "2024-06-30"
  }
  ```

- **Response:**

  ```json
  {
    "message": "Project created successfully"
  }
  ```

### View Logs

- **Endpoint:** `/api/logs/`
- **Method:** `GET`
- **Headers:**
  - `Authorization: Bearer your_jwt_token_here`
- **Query Parameters (Optional):**
  - `projectId`: Filter by project ID.
  - `logLevel`: Filter by log level (`INFO`, `WARNING`, `ERROR`, `DEBUG`, `CRITICAL`).

- **Response:**

  ```json
  {
    "logs": [
      {
        "Log_ID": 1,
        "Project_ID": 1,
        "User_ID": 1,
        "Log_Level": "ERROR",
        "Module": "Authentication",
        "Log_Message": "Failed login attempt.",
        "AdditionalData": {},
        "Created_At": "2024-01-15T12:34:56Z"
      },
      // ... more logs ...
    ]
  }
  ```

### View Audit Logs

- **Endpoint:** `/api/audit-logs/`
- **Method:** `GET`
- **Headers:**
  - `Authorization: Bearer your_jwt_token_here`

- **Response:**

  ```json
  {
    "auditLogs": [
      {
        "Audit_ID": 1,
        "User_ID": 1,
        "Action_Type": "Login",
        "Action_Details": "User logged in successfully.",
        "Timestamp": "2024-01-15T12:35:00Z",
        "IP_Address": "192.168.1.10"
      },
      // ... more audit logs ...
    ]
  }
  ```

### Submit Log via REST API

- **Endpoint:** `/api/logs/submit/`
- **Method:** `POST`
- **Headers:**
  - `Authorization: Bearer your_jwt_token_here`
- **Payload:**

  ```json
  {
    "projectId": 1,
    "logLevel": "ERROR",
    "message": "An error occurred while processing the request.",
    "module": "Authentication",
    "timestamp": "2024-01-15T12:45:00Z",
    "additionalData": {
      "errorCode": "AUTH_FAIL",
      "details": "Invalid credentials provided."
    }
  }
  ```

- **Response:**

  ```json
  {
    "message": "Log submitted successfully"
  }
  ```

---

## Contributing

Contributions are welcome! Please follow these steps to contribute to the project:

1. **Fork the Repository**

   Click the "Fork" button at the top-right corner of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/yourusername/logdb_project.git
   cd logdb_project/backend
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**

5. **Commit Your Changes**

   ```bash
   git commit -m "Add feature: YourFeatureName"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request**

   Navigate to the original repository and create a pull request from your fork.

---

## License

This project is licensed under the [Unlicense](../LICENSE).

---

## Contact

For any questions or suggestions, please create a issue.

---
