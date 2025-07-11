# MTB Project

## Overview
MTB is a Django project designed to provide a robust framework for building web applications. This README file outlines the setup and usage instructions for the project.

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.x
- pip (Python package installer)
- Django

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd MTB
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Project
To run the development server, use the following command:
```
python manage.py runserver
```
You can then access the application at `http://127.0.0.1:8000/`.

## Project Structure
```
MTB
├── manage.py
├── MTB
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
└── README.md
```

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.