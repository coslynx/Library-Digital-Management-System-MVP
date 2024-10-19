<div class="hero-icon" align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>

<h1 align="center">
Library-Digital-Management-System-MVP
</h1>
<h4 align="center">A backend system for streamlined library operations</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Framework-FastAPI-blue" alt="Framework-FastAPI-blue">
  <img src="https://img.shields.io/badge/Language-Python-red" alt="Language-Python-red">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue" alt="Database-PostgreSQL-blue">
  <img src="https://img.shields.io/badge/LLMs-Custom,_Gemini,_OpenAI-black" alt="LLMs-Custom,_Gemini,_OpenAI-black">
</div>
<div class="badges" align="center">
  <img src="https://img.shields.io/github/last-commit/coslynx/Library-Digital-Management-System-MVP?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/coslynx/Library-Digital-Management-System-MVP?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/coslynx/Library-Digital-Management-System-MVP?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

## 📑 Table of Contents
- 📍 Overview
- 📦 Features
- 📂 Structure
- 💻 Installation
- 🏗️ Usage
- 🌐 Hosting
- 📄 License
- 👏 Authors

## 📍 Overview
This repository houses the backend for the Efficient Library Digital Management System MVP. This system streamlines library operations by providing a robust backend system for managing library resources, handling user authentication and authorization, processing borrowing requests, and tracking due dates. The tech stack includes FastAPI, Python, PostgreSQL, and leverages custom LLMs like Gemini and OpenAI.

## 📦 Features
|    | Feature            | Description                                                                                                        |
|----|--------------------|--------------------------------------------------------------------------------------------------------------------|
| ⚙️ | **Architecture**   | The system uses a modular architecture with separate modules for authentication, book management, and user management, ensuring ease of development and maintenance. |
| 📄 | **Documentation**  | This README file provides a detailed overview of the MVP, its dependencies, and instructions on how to set up and run the system. |
| 🔗 | **Dependencies**   | The project relies on external libraries such as FastAPI, SQLAlchemy, psycopg2, and Pydantic for efficient development and robust data handling. |
| 🔐 | **Security**       | The system implements security measures, including JWT authentication for secure access and data validation to prevent vulnerabilities. |
| ⚡️  | **Performance**    | The system optimizes performance by leveraging FastAPI's high-performance capabilities, efficient database queries, and appropriate data structures. |
| 📶 | **Scalability**    | The system is designed for scalability, utilizing a robust database like PostgreSQL and efficient architecture to handle increasing user load and data volume. |
| 🔌 | **Integrations**   | The system can integrate with external APIs like OCLC or Worldcat for retrieving bibliographic data and external authentication systems. |
| 🧪 | **Testing**        | Unit tests are included to verify the correctness and robustness of the authentication, book management, and user management logic. |
| 🔀 | **Version Control**| The project utilizes Git for version control and employs a robust CI/CD pipeline for automated builds and deployments. |

## 📂 Structure
```text
└── api
    └── routes
        └── auth_routes.py
        └── book_routes.py
        └── user_routes.py
    └── main.py
    └── dependencies.py
└── models
    └── book.py
    └── user.py
└── services
    └── auth_service.py
    └── book_service.py
    └── user_service.py
└── utils
    └── database.py
    └── config.py
    └── auth.py
    └── exceptions.py
    └── logger.py
    └── helpers.py
└── tests
    └── unit
        └── test_auth_service.py
        └── test_book_service.py
        └── test_user_service.py
└── .env
└── .gitignore
└── README.md
└── requirements.txt
└── startup.sh
└── commands.json
```

## 💻 Installation

### 🔧 Prerequisites
- Python 3.9+
- PostgreSQL 15+
- Docker (recommended)

### 🚀 Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/coslynx/Library-Digital-Management-System-MVP.git
   cd Library-Digital-Management-System-MVP
   ```
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Create a `.env` file in the project root directory.
   - Copy the `.env.example` file and replace the placeholder values with your actual configuration:
     ```text
     DATABASE_URL=postgres://user:password@host:port/database
     JWT_SECRET=your_secret_key
     HOST=0.0.0.0
     PORT=8000
     DB_HOST=localhost
     DB_PORT=5432
     DB_USER=user
     DB_PASSWORD=password
     DB_NAME=database
     ```

## 🏗️ Usage

### 🏃‍♂️ Running the MVP
1. Start the database (using Docker Compose):
   ```bash
   docker-compose up -d database
   ```
2. Start the backend server:
   ```bash
   uvicorn api.main:app --host $HOST --port $PORT --reload
   ```
3. Access the API:
   - The API is now accessible at `http://localhost:8000` (or the specified port in `.env`).

### ⚙️ Configuration
- **`.env` file:** This file contains environment variables for configuring the database connection, JWT secret key, server host and port, and other settings.  
- **Database Configuration:** 
  - Ensure that the database is running and configured correctly.
  - Update the `DATABASE_URL` environment variable with your database credentials.
- **JWT Secret Key:**
  - Create a strong secret key for JWT token generation and store it in the `JWT_SECRET` environment variable.

### 📚 Examples
- **Register a new user:** 
   ```bash
   curl -X POST http://localhost:8000/api/register \
   -H "Content-Type: application/json" \
   -d '{"username": "newuser", "email": "user@example.com", "password": "securepass123"}'
   ```
- **Login an existing user:**
   ```bash
   curl -X POST http://localhost:8000/api/login \
   -H "Content-Type: application/json" \
   -d '{"email": "user@example.com", "password": "securepass123"}'
   ```
- **Search for a book:**
   ```bash
   curl -X GET http://localhost:8000/api/books?title=The%20Hobbit
   ```

## 🌐 Hosting

### 🚀 Deployment Instructions

#### Docker Deployment
1. Build the Docker image:
   ```bash
   docker build -t library-backend .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 library-backend
   ```

#### Other Hosting Options
-  **AWS Elastic Beanstalk:**  Consider using Elastic Beanstalk for easy deployment to AWS.
- **Heroku:**  Heroku is a popular choice for deploying Python applications.

### 🔑 Environment Variables
- `DATABASE_URL`: Connection string for the PostgreSQL database.
  - Example: `postgresql://user:password@host:port/database`
- `JWT_SECRET`: Secret key for JWT token generation.
  - Example: `your-256-bit-secret`
- `HOST`: Server host.
  - Example: `0.0.0.0`
- `PORT`: Server port.
  - Example: `8000`
- `DB_HOST`: Database host.
  - Example: `localhost`
- `DB_PORT`: Database port.
  - Example: `5432`
- `DB_USER`: Database user.
  - Example: `user`
- `DB_PASSWORD`: Database password.
  - Example: `password`
- `DB_NAME`: Database name.
  - Example: `database`

## 📜 API Documentation

### 🔍 Endpoints

- **POST `/api/register`:** Register a new user.
   - Request Body: JSON object with `username`, `email`, and `password`.
   - Response: 201 (Created) if successful, 400 (Bad Request) if there are validation errors.
- **POST `/api/login`:** Logs in an existing user.
   - Request Body: JSON object with `email` and `password`.
   - Response: 200 (OK) with JWT token if successful, 401 (Unauthorized) if authentication fails.
- **GET `/api/books`:** Retrieves a list of all books.
   - Response: 200 (OK) with a JSON array of book objects.
- **GET `/api/books/{book_id}`:** Retrieves details for a specific book.
   - Response: 200 (OK) with a JSON object representing the book, 404 (Not Found) if the book doesn't exist.
- **POST `/api/books`:** Creates a new book record.
   - Request Body: JSON object with book details (e.g., `title`, `author`, `ISBN`, etc.).
   - Response: 201 (Created) if successful, 400 (Bad Request) if there are validation errors.
- **PUT `/api/books/{book_id}`:** Updates an existing book record.
   - Request Body: JSON object with updated book details.
   - Response: 200 (OK) if successful, 404 (Not Found) if the book doesn't exist.
- **DELETE `/api/books/{book_id}`:** Deletes a book record.
   - Response: 204 (No Content) if successful, 404 (Not Found) if the book doesn't exist.

### 🔒 Authentication
- The system utilizes JSON Web Tokens (JWT) for user authentication.
- Upon successful registration or login, a JWT token is issued.
- Include the JWT token in the `Authorization` header of subsequent requests using the format: `Authorization: Bearer YOUR_JWT_TOKEN`.

### 📝 Examples

```bash
# Register a new user
curl -X POST http://localhost:8000/api/register \
-H "Content-Type: application/json" \
-d '{"username": "newuser", "email": "user@example.com", "password": "securepass123"}'

# Login an existing user
curl -X POST http://localhost:8000/api/login \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "securepass123"}'

# Search for a book
curl -X GET http://localhost:8000/api/books?title=The%20Hobbit 

# Retrieve book details
curl -X GET http://localhost:8000/api/books/123

# Create a new book
curl -X POST http://localhost:8000/api/books \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-d '{"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "isbn": "0345391802"}'
```

## 📜 License & Attribution

### 📄 License
This Minimum Viable Product (MVP) is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) license.

### 🤖 AI-Generated MVP
This MVP was entirely generated using artificial intelligence through [CosLynx.com](https://coslynx.com).

No human was directly involved in the coding process of the repository: Library-Digital-Management-System-MVP

### 📞 Contact
For any questions or concerns regarding this AI-generated MVP, please contact CosLynx at:
- Website: [CosLynx.com](https://coslynx.com)
- Twitter: [@CosLynxAI](https://x.com/CosLynxAI)

<p align="center">
  <h1 align="center">🌐 CosLynx.com</h1>
</p>
<p align="center">
  <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
</p>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
  <img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
  <img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
  <img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
</div>