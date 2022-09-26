# Project: yamdb_final
____
## Description

- The YaMDb project collects user reviews on works (Titles). The works are divided into categories: "Books", "Films", "Music". The list of categories can be expanded by the administrator (for example, you can add the category "Art").
- The works themselves are not stored in YaMDb, you cannot watch a movie or listen to music here.
- In each category there are works: books, movies or music. For example, in the category "Books" there may be works "Winnie the Pooh and All All All" and "Martian Chronicles", and in the category "Music" - the song "Just Now" by the group "Insects" and the second suite by Bach.
- A work can be assigned a genre from the preset list (for example, "Fairy Tale", "Rock" or "Arthouse"). Only the administrator can create new genres.
- Grateful or outraged users leave text reviews for the works and give the work a rating in the range from one to ten (an integer); an average rating of the work is formed from user ratings — a rating (an integer). The user can leave only one review for one work.
____

## Installation

clone the repository and go to it on the command line:
```sh
git clone https://github.com/BerdyshevEugene/yamdb_final.git
cd yamdb_final
```

create and activate virtual enviroment:
```sh
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
```

create and fullfill .env file in yamdb_final/infra:
```sh
DB_ENGINE=django.db.backends.postgresq
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
build images and run the project locally:
```sh
docker-compose up -d --build 
```
make migrations:
```sh
docker-compose exec web python manage.py migrate
```
create superuser:
```sh
docker-compose exec web python manage.py createsuperuser
```
collect static:
```sh
docker-compose exec web python manage.py collectstatic --no-input
```
dump fixtures.json:
```sh
python3 manage.py shell
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
python manage.py loaddata dump.json
```
you can go to the project by following the next link:
http://51.250.1.29/
____

## Author
Eugene Berdyshev
____
![Build Status](https://github.com/BerdyshevEugene/yamdb_final/workflows/yamdb_workflow/badge.svg)
![github](https://camo.githubusercontent.com/6b7f701cf0bea42833751b754688f1a27b6090fdf90bf2b226addff01be817f0/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f646f636b65722d2532333064623765642e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d646f636b6572266c6f676f436f6c6f723d7768697465) ![github](https://camo.githubusercontent.com/5473e0d3006bb7e662bdf754d830a026ce050be61f1cbbd4689783ae49950b93/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f646a616e676f2d2532333039324532302e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d646a616e676f266c6f676f436f6c6f723d7768697465) ![github](https://camo.githubusercontent.com/cbef21adebc167fac6552145a03c9e12ae03b8afd5e4f7de52379a98297de3fe/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f444a414e474f2d524553542d6666313730393f7374796c653d666f722d7468652d6261646765266c6f676f3d646a616e676f266c6f676f436f6c6f723d776869746526636f6c6f723d666631373039266c6162656c436f6c6f723d67726179)
