#!/bin/usr/python3
import logging.config
from typing import Optional
from fastapi import FastAPI

import app.library.person
from app.library import health
from app.rest.person import PersonIn, PersonOut

fastapi = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@fastapi.get("/health")
def get_health():
    logger.debug("Received GET request on /health")
    return health.get_health()


@fastapi.get("/health_async")
async def get_health_async():
    logger.debug("Received GET request on /health_async")
    return await health.get_health_async()


@fastapi.get("/")
def read_root():
    return {"Hello": "World"}


@fastapi.get("/greetings/{greeting_id}")
async def read_item(greeting_id: int, language: Optional[str] = None):
    return {"greeting_id": greeting_id, "language": language, "greeting": f"Say Hello to ID {greeting_id} in {language}"}

@fastapi.post("/persons/", response_model=PersonOut)
async def post_person(input_person: PersonIn):
    person: app.library.person.Person = await app.library.person.create_person(input_person.name)
    return PersonOut(name=person.name, created_on=person.created_on)

@fastapi.get("/persons/{name}", response_model=PersonOut)
async def get_person(name: str):
    person: app.library.person.Person = await app.library.person.get_person(name)
    return PersonOut(name=person.name, created_on=person.created_on)

# def main():
#     logger.info("Starting...")
#
#     # sleeptime = int(os.environ['SLEEP_INTERVAL'])
#
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--some-host", help="some host", type=str, default="localhost")
#     parser.add_argument("--some-port", help="some port", type=int, default=8080)
#     args = parser.parse_args()
#     # args.some_port
#     # args.some_host
#
#     uvicorn.run(fastapi, host="0.0.0.0", port=8080)
#
#
#
# def main():
#     import uvicorn
#     import yaml
#     logging.config.dictConfig(yaml.load(open("app/logging-config.yaml", 'r')))  # configured via cmdline
#     logger.info("Starting via main()...")
#     uvicorn.run(fastapi, host="0.0.0.0", port=8080)
#
# # This only runs if the script is called instead of uvicorn; should probably not be used.
# if __name__ == "__main__":
#     main()
