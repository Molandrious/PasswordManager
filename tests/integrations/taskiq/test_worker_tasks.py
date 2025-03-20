import pytest

from src.integrations.taskiq.worker_tasks import add_one_task, create_event_task


class TestWorkerTasks:
    @pytest.mark.require_db
    async def test_create_event_task(self) -> None:
        task = await create_event_task.kiq()
        await task.wait_result(timeout=2)

    async def test_simple_task(self) -> None:
        task = await add_one_task.kiq(value=10)
        await task.wait_result(timeout=2)
