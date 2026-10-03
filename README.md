# FastAPI Task API

A small FastAPI backend for managing student records. The project uses  MySQL as
the intended database.

## Features

- List all students
- Retrieve a student by ID
- Create a student
- Update a student
- Delete a student

## Project structure

```text
FastAPI-Task/
├── auth.py          
├── crud.py          
├── database.py      
├── main.py          
├── models.py        
├── schemas.py       
├── requirements.txt 
└── .env             
```


## Installation

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/Onkar2104/FastAPI-Task.git
   cd FastAPI-Task
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\Activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root. The application reads these values
when it starts:

```env
DATABASE_URL=mysql+mysqlconnector://<username>:<password>@localhost:3306/<database_name>
ALLOW_ORIGINS=http://localhost:5173
```

## Running the API


```bash
uvicorn main:app --reload
```

The API is available at:

- Base URL: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>


## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Health check |
| `GET` | `/students` | Return all students |
| `GET` | `/students/{student_id}` | Return one student |
| `POST` | `/students` | Create a student |
| `PUT` | `/students/{student_id}` | Replace a student |
| `DELETE` | `/students/{student_id}` | Delete a student |

