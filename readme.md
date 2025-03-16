# FastAPI Project

## Setup

### Create a virtual environment
Open a terminal in Visual Studio Code and navigate to your project directory:

```bash
cd c:\ai_projects\api_tests
```

Create a virtual environment named venv:

```bash
python -m venv venv
```

Activate the virtual environment
On Windows, activate the virtual environment using:

```bash
.\venv\Scripts\activate
```

Install the required packages
Install the dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

Run the FastAPI application
Start the FastAPI server using Uvicorn:

```bash
uvicorn app:app --reload
```

This will start the FastAPI server, and you can access the API at http://127.0.0.1:8000