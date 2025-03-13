from dishka import AsyncContainer
from fastapi import FastAPI
from starlette.datastructures import State


class ContainerizedState(State):
    dishka_container: AsyncContainer


class FastAPIContainerized(FastAPI):
    state: ContainerizedState
