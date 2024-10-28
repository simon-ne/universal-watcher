from tinydb import TinyDB, Query
from tinydb.table import Document
from typing import List
from pathlib import Path
from pydantic import BaseModel
from json import loads
from enum import Enum
import threading
import os

from ..decorators.injector import DependencyInjector as Injector


class DbTable(str, Enum):
    WATCHERS = "watchers"
    WATCHER_DATA = "watcher_data"
    DATA_SOURCES = "data_sources"
    NOTIFICATION_PLATFORMS = "notification_platforms"


@Injector.inject_as_singleton
class CoreDbService:
    def __init__(self):
        """
        Initialize the CoreDbService with the database path and threading lock.
        """
        env_db_path = Path(os.getenv("DB_PATH", "db.json"))
        db_path = (
            env_db_path
            if os.path.isabs(env_db_path)
            else Path(os.getcwd()) / env_db_path
        )
        self._db = TinyDB(db_path)
        self._lock = threading.Lock()

    def get_watcher_data(self, watcher_name: str) -> List[Document]:
        """
        Retrieve watcher data by watcher name.

        Args:
            watcher_name (str): The name of the watcher.

        Returns:
            List[Document]: The watcher data document.

        Raises:
            ValueError: If watcher is not found or names are not unique.
        """
        with self._lock:
            watcher_data = self._db.table(DbTable.WATCHERS).search(
                Query().name == watcher_name
            )

        if not watcher_data:
            raise ValueError(f"Watcher {watcher_name} not found.")

        if len(watcher_data) > 1:
            raise ValueError(
                f"Watchers must have unique names. Found {len(watcher_data)} watchers named {watcher_name}."
            )

        return watcher_data[0]

    def get_watcher_items(self, watcher: str) -> List[Document]:
        """
        Get items associated with a specific watcher.

        Args:
            watcher (str): The name of the watcher.

        Returns:
            List[Document]: List of watcher items.
        """
        with self._lock:
            items = self._db.table(DbTable.WATCHER_DATA).search(
                Query().name == watcher
            )

        if not items:
            return []

        return items[0]["data"]

    def set_watcher_items(self, watcher: str, data: list[BaseModel]) -> None:
        """
        Update or create watcher items in the database.

        Args:
            watcher (str): Name of the watcher.
            data (list[BaseModel]): List of Pydantic model objects to store.
        """
        dict_data = [loads(item.model_dump_json()) for item in data]
        with self._lock:
            self._db.table(DbTable.WATCHER_DATA).upsert(
                {"name": watcher, "data": dict_data}, Query().name == watcher
            )

    def get_data_source_data(self, data_source_name: str) -> dict:
        """
        Retrieve data for a specific data source.

        Args:
            data_source_name (str): The name of the data source.

        Returns:
            dict: The data source data.

        Raises:
            ValueError: If the data source is not found.
        """
        with self._lock:
            data_source = self._db.table(DbTable.DATA_SOURCES).search(
                Query().name == data_source_name
            )

        if not data_source:
            raise ValueError(f"Data source {data_source_name} not found.")

        return data_source[0]

    def get_notification_platform_data(
        self, notification_platform_name: str
    ) -> dict:
        """
        Retrieve data for a specific notification platform.

        Args:
            notification_platform_name (str): The name of the notification platform.

        Returns:
            dict: The notification platform data.

        Raises:
            ValueError: If the notification platform is not found.
        """
        with self._lock:
            data_source = self._db.table(
                DbTable.NOTIFICATION_PLATFORMS
            ).search(Query().name == notification_platform_name)

        if not data_source:
            raise ValueError(
                f"Data source {notification_platform_name} not found."
            )

        return data_source[0]
