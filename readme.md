# Spree Ecommerce website

## Requirements

- virtualenv

## Setup

1. Clone the Repo

    ```bash
    git pull origin https://github.com/MuhammadHassan1998/spree_ecommerce.git
    cd spree_ecommerce
    ```

2. Install the project: `pip install -r requirements.txt`

4. populate `.env`:

    Add a `.env` file in the repo root.
    important values to run the project

    ```sh
    NAME: 'myproject',
    USER: 'root',
    PASSWORD: 'root',
    HOST: 'localhost',
    PORT: '',
    ```
5. Run `python manage.py makekigrations`

6. Run `python manage.py makemigrate`

7. Run `Python manage.py runserver`

_**Note:** You need to run the postgresql server first and create the db
the site will run on http://localhost:8000
