<a name="readme-top"></a>

# Connect-U

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#introduction">Introduction</a></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


## About The Project

### Introduction

Connect-U is a career service platform designed to connect students with potential employers. Using this web application, students can find suitable job opportunities and employers can find qualified candidates for their job openings.

<p>Check out the deployment of the project <a href="https://connect-u-portal.vercel.app" target="_blank">here</a>.</p>

### Features

#### Student

- Create and manage student profile
- Browse available job postings
- Apply to job postings
- View the status of their job application including email updates

#### Employers

- Create and manage employer profile
- Add and manage job postings
- Review candidate applications and resumes
- Notify candidate that they have been selected for an interview

#### Administrators

- Moderate system users
- Moderate job postings

### Built With

- Python (Django)
- HTML
- CSS
- Bootstrap
- Font Awesome

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

### Prerequisites

- Python 3.8 or higher installed on your system
- PyCharm (highly recommended for development). Download [here](https://www.jetbrains.com/pycharm/download).

### Installation

1. Clone the repo

Clone the repository by running the following command in your terminal:

```sh
git clone https://github.com/emeka-okechukwu-dev/connect-u.git
```

2. Set up a Python virtual environment (Mac users)

Create a new Python virtual environment by running the following command:

```sh
python3 -m venv env
```

Activate the virtual environment by running:

```sh
source env/bin/activate
```

3. Install requirements, apply migrations, create superuser, and run server:

Navigate to the project directory and run the following command to install the required packages, apply the database migrations, create a superuser account, and start the development server:

```sh
pip install -r requirements.txt
```

```sh
python manage.py migrate
```

```sh
python manage.py createsuperuser
```

```sh
python manage.py runserver
```

4. Create a .env file in the project root directory with the following format:

```sh
SECRET_KEY = your_secret_key
EMAIL_HOST_USER = your_smtp_username
EMAIL_HOST_PASSWORD = your_smtp_password
```

5. Access the application

Open a web browser and navigate to the following URL:

```sh
http://localhost:8000/
```

You should now be able to access the application locally.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contributing

Every contribution is appreciated. If you have an idea for improving the project, please fork the repository and create a pull request or open an issue with the tag "enhancement" to share your suggestion.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

Emeka Okechukwu - chuks.egkedu@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>
