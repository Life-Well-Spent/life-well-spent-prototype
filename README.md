# Life Well Spent
![GitHub](https://img.shields.io/github/license/Life-Well-Spent/life-well-spent?style=flat-square)
![GitHub Repo stars](https://img.shields.io/github/stars/Life-Well-Spent/life-well-spent?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/Life-Well-Spent/life-well-spent?style=flat-square)
![GitHub contributors](https://img.shields.io/github/contributors/Life-Well-Spent/life-well-spent?style=flat-square)

## About
I love to plan in my goals on a yearly, quarterly and weekly basis. 
To do so I have always used Project Management software, these contain lots of features and I only use the bare minimum functionality. 
In order to make my own life a bit easier (and also to work on yet another side project) I decided to start this project.

## Running the project
After cloning do the following things:
1. Create a virtual environment: `python -m venv .venv`
2. Activate the virtual environment: `.venv\Scripts\activate`
3. Install the requirements: `pip install -r requirements.txt`
4. Start the docker services: `docker-compose up -d --build`
5. Execute the migrations: `docker-compose exec web python manage.py migrate`

## Contributing
If you want to contribute to this project feel free to check out the issues.
When you want to add your changes to the project:
1. Execute `black .` for code formatting
2. Execute `isort .` for import sorting
3. Create a PR to the dev branch
