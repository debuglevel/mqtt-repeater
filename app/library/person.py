import logging
import uuid
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from tinydb import TinyDB, Query

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Person(BaseModel):
    name: str
    created_on: str


async def create_person(name: str) -> Person:
    logger.debug(f"Creating person '{name}'...")

    person = Person(name=name, created_on=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    logger.debug(f"Opening TinyDB...")
    database = TinyDB('database.json')

    logger.debug(f"Inserting...")
    document_id = database.insert(person.dict())

    logger.debug(f"Getting inserted...")
    retrieved_person_document = database.get(doc_id=document_id)
    logger.debug(f"Got inserted {retrieved_person_document}")

    logger.debug("Converting document to model...")
    retrieved_person = Person(**retrieved_person_document)
    logger.debug(f"Got inserted {retrieved_person}")

    return retrieved_person


async def get_person(name: str) -> Person:
    logger.debug(f"Getting person with id={id}...")

    logger.debug(f"Opening TinyDB...")
    database = TinyDB('database.json')

    person_query = Query()

    logger.debug(f"Getting document...")
    retrieved_person_document = database.get(person_query.name == name)
    logger.debug(f"Got {retrieved_person_document}")

    logger.debug("Converting document to model...")
    retrieved_person = Person(**retrieved_person_document)
    logger.debug(f"Got {retrieved_person}")

    return retrieved_person
