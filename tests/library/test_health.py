import pytest
import app.library.health


def test_health():
    health: app.Health = app.library.health.get_health()
    assert health.status == "up"


@pytest.mark.asyncio
async def test_health_async():
    health: app.Health = await app.library.health.get_health_async()
    assert health.status == "up"
