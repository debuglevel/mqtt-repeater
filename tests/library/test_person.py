import uuid

import pytest
import app.library.person

@pytest.mark.asyncio
async def test_create_person():
    person: app.library.person.Person = await app.library.person.create_person("Hans")
    assert person.name == "Hans"


@pytest.mark.asyncio
async def test_get_person():
    created_person: app.library.person.Person = await app.library.person.create_person("Hans")
    retrieved_person: app.library.person.Person = await app.library.person.get_person("Hans")
    assert retrieved_person.name == "Hans"
