import pytest

from src.transport.taskiq.tasks import create_event_task, simple_task


@pytest.mark.require_db
class TestCreateEventTask:
    async def test_ok(self) -> None:
        task = await create_event_task.kiq()
        await task.wait_result(timeout=2, with_logs=True)


class TestSimpleTask:
    async def test_ok(self) -> None:
        await simple_task(10)
