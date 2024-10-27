from abc import ABC, abstractmethod

from core.classes.data_source.data_source_item import DataSourceItem
from core.classes.data_source.data_source_parameters import DataSourceParameters
from core.classes.notification_platform.notification_platform_input import (
    NotificationPlatformInput,
)
from core.classes.formatter.formatter import Formatter


class DataSource(ABC):
    # @abstractmethod
    # def possible_params(self) -> list[dict]:
    #     """Possible parameters of the data source"""
    #     pass

    @abstractmethod
    def params(self) -> DataSourceParameters:
        """Parameters for the data source"""
        pass

    @abstractmethod
    def set_params(self, params: dict) -> None:
        """Setup the data source parameters"""
        pass

    @abstractmethod
    def fetch_items(self) -> list[DataSourceItem]:
        """Get the new items"""
        pass

    @abstractmethod
    def get_stored_items(self) -> list[DataSourceItem]:
        """Get the stored items"""
        pass

    @abstractmethod
    def get_formatter(self, formatter_name: str) -> Formatter:
        """Get the formatter object"""
        pass

    @abstractmethod
    def format_items(
        self, formatter_name: str, items: list[DataSourceItem]
    ) -> NotificationPlatformInput:
        """Format the items"""
        pass
