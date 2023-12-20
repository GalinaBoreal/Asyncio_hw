import asyncio
import datetime

import requests
import aiohttp
from more_itertools import chunked

from models import Session, SwapiPeople, close_db, init_db

CHUNK_SIZE = 10


async def get_person(person_id: int):
    session = aiohttp.ClientSession()
    response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    person = await response.json()
    await session.close()
    return person


async def get_names(urls: list):
    async with aiohttp.ClientSession() as session:
        if urls:
            requests = [await session.get(url) for url in urls]
            response = [await i.json() for i in requests]
            names_list = ", ".join([i.get("title") or i.get("name") for i in response])
            return names_list
        else:
            return None


async def insert_person(people_list: tuple):
    async with Session() as session:
        people_list = [SwapiPeople(
            **{
                "name": person.get("name"),
                "height": person.get("height"),
                "mass": person.get("mass"),
                "hair_color": person.get("hair_color"),
                "skin_color": person.get("skin_color"),
                "eye_color": person.get("eye_color"),
                "birth_year": person.get("birth_year"),
                "gender": person.get("gender"),
                "homeworld": person.get("homeworld"),
                "films": await get_names(person.get("films")),
                "species": await get_names(person.get("species")),
                "vehicles": await get_names(person.get("vehicles")),
                "starships": await get_names(person.get("starships"))
            }
        ) for person in people_list]
        session.add_all(people_list)
        await session.commit()


async def main(number: int):
    await init_db()

    for person_id_chunk in chunked(range(1, number), CHUNK_SIZE):
        coros = [get_person(person_id) for person_id in person_id_chunk]
        result = await asyncio.gather(*coros)
        # print(result)
        asyncio.create_task(insert_person(result))

    tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks)
    await close_db()


if __name__ == "__main__":
    start = datetime.datetime.now()
    count = requests.get("https://swapi.py4e.com/api/people")
    number = count.json()["count"] + 2  # потому что в swapi начинается с 0 и range до "число-1"
    asyncio.run(main(number))
    print(datetime.datetime.now() - start)
