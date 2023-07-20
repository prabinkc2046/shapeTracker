# ShapeTracker Web Application

ShapeTracker is a simple web application built with Flask that allows users to track their fitness progress by logging their waist size and weight over time. The data is stored in a MySQL database, and users can view their progress on graphs.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

To get started with ShapeTracker, follow these steps:

1. Clone this repository to your local machine:

```
   git clon <https://github.com/prabinkc2046/ShapeTracker.git>
```

2. Change into the project directory:

```
cd ShapeTracker
```

3. Build and run the Docker containers using Docker Compose:

```
docker-compose up
```

The application will be accessible at http://localhost:5000 in your web browser.

## Usage
Registration/Login: When you access the application, you will be prompted to either log in or register as a new user.

1. Log In: If you are an existing user, enter your username and password to log in.

2. Register: If you are a new user, choose the option to register and enter a new username and password.

3. Fitness Data Input: After logging in or registering, you will be redirected to the data input page. Enter your waist size and weight, and click submit.

4. View Progress: You will be asked if you want to view your progress. Choose "Yes" to see graphs of your waist size and weight progress over time.

5. Logout: To log out of the application, click the "Logout" button.

## Project Structure
The project structure is as follows:
```
.
├── docker-compose.yml
├── documentation
│   └── README.md
├── mysql
│   ├── create_table.sql
│   └── Dockerfile
├── README.md
└── shapeTracker
    ├── app.py
    ├── Dockerfile
    ├── requirements.txt
    ├── static
    │   └── styles.css
    └── templates
        ├── form.html
        ├── login.html
        └── result.html
```

- app.py: The main Flask application file.
- requirements.txt: Contains the required Python packages.
- static: Folder for static files (CSS, JS, etc.).
- templates: Folder for HTML templates used by Flask.
- mysql: Folder containing the Dockerfile and SQL script for MySQL.
- docker-compose.yml: Docker Compose configuration for the application.

## Contributing
If you'd like to contribute to ShapeTrack, please follow these steps:

- Fork this repository.
- Create a new branch for your feature/bug fix.
- Make your changes and commit them.
- Push the changes to your fork.
- Open a pull request in this repository.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to copy the content above and save it in a file named `README.md` in your project's root directory. Modify it according to your project's specific details and add any additional information or instructions you find relevant.
