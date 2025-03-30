from collections.abc import AsyncGenerator
from typing import Any

import pytest
from dishka import Scope
from src.repositories import EventRepository
from src.transport.rest import FastAPIContainerized


@pytest.fixture()
async def event_repository(app: FastAPIContainerized) -> AsyncGenerator[EventRepository, Any]:
    async with app.state.dishka_container(scope=Scope.REQUEST) as request_container:
        yield await request_container.get(EventRepository)
