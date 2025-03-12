from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.containers.app import App
from src.services import PasswordService

PasswordServiceAnnotated = Annotated[PasswordService, Depends(Provide[App.services.password])]
