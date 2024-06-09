from typing import Any

from apps.driver.repositories.interfaces.driver import IDriverRepository

from ..interfaces.driver import (
    IDriverActivateService,
    IDriverCreateService,
    IDriverDeactivateService,
    IDriverDeleteService,
    IDriverUpdateService,
)


class DriverCreateService(IDriverCreateService):
    def __init__(self, repository: IDriverRepository):
        self._repository = repository

    def create(self, data: dict[str, Any]) -> Any:
        return self._repository.create(data)


class DriverUpdateService(IDriverUpdateService):
    def __init__(self, repository: IDriverRepository):
        self._repository = repository

    def update(self, driver: Any, data: dict[str, Any]) -> Any:
        return self._repository.update(driver, data)


class DriverDeleteService(IDriverDeleteService):
    def __init__(self, repository: IDriverRepository):
        self._repository = repository

    def delete(self, driver: Any) -> None:
        self._repository.delete(driver)


class DriverActivateService(IDriverActivateService):
    def activate(self, driver: Any) -> None:
        driver.activate()


class DriverDeactivateService(IDriverDeactivateService):

    def deactivate(self, driver: Any) -> None:
        driver.deactivate()
