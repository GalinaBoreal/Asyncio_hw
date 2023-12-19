# Домашнее задание к лекции «Asyncio»

Извлечение из API персонажей Start Wars и загрузка в базу данных.<br>
Документация по API находится здесь: [SWAPI](https://swapi.dev/documentation#people). <br>

Выгружаются cледующие поля:<br>
**id** - ID персонажа <br>
**birth_year** <br>
**eye_color** <br>
**films** - строка с названиями фильмов через запятую <br>
**gender** <br>
**hair_color** <br>
**height** <br>
**homeworld** <br>
**mass** <br>
**name** <br>
**skin_color** <br>
**species** - строка с названиями типов через запятую <br>
**starships** - строка с названиями кораблей через запятую <br>
**vehicles** - строка с названиями транспорта через запятую <br>


1) Создание контейнера, команда: docker-compose up
2) Скрипт загрузки данных из API в базу: async_swapi_my.py

