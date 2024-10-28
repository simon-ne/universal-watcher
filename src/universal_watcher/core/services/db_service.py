from tinydb import TinyDB, Query
from tinydb.table import Document
from typing import List
from pathlib import Path
from pydantic import BaseModel
from json import loads
from enum import Enum
import threading
import os

from universal_watcher.core.decorators.injector import (
    DependencyInjector as Injector,
)
from universal_watcher.core.models.watcher_model import WatcherModel


class DbTable(str, Enum):
    WATCHERS = "watchers"
    WATCHER_DATA = "watcher_data"
    DATA_SOURCES = "data_sources"
    NOTIFICATION_PLATFORMS = "notification_platforms"


@Injector.inject_as_singleton
class CoreDbService:
    def __init__(self):
        """
        Initialize the CoreDbService with the database path and a threading lock.
        """
        env_db_path = Path(os.getenv("DB_PATH", "db.json"))
        db_path = (
            env_db_path
            if os.path.isabs(env_db_path)
            else Path(os.getcwd()) / env_db_path
        )
        self._db = TinyDB(db_path)
        self._lock = threading.Lock()

    def does_watcher_exist(self, watcher_name: str) -> bool:
        """
        Check if a watcher exists in the database.

        Args:
            watcher_name (str): The name of the watcher.

        Returns:
            bool: True if the watcher exists, False otherwise.
        """
        with self._lock:
            watcher_data = self._db.table(DbTable.WATCHERS).search(
                Query().name == watcher_name
            )

        return bool(watcher_data)

    def is_watcher_unique(self, watcher_name: str) -> bool:
        """
        Check if a watcher name is unique in the database.

        Args:
            watcher_name (str): The name of the watcher.

        Returns:
            bool: True if the watcher name is unique, False otherwise.
        """
        with self._lock:
            watcher_data = self._db.table(DbTable.WATCHERS).search(
                Query().name == watcher_name
            )

        return len(watcher_data) == 1

    def get_all_watchers_names(self) -> List[str]:
        """
        Get all watcher names stored in the database.

        Returns:
            List[str]: List of watcher names.
        """
        with self._lock:
            watchers = self._db.table(DbTable.WATCHERS).all()

        return [watcher["name"] for watcher in watchers]

    def get_watcher_data(self, watcher_name: str) -> Document:
        """
        Retrieve watcher data by watcher name.

        Args:
            watcher_name (str): The name of the watcher.

        Returns:
            Document: The watcher data document.

        Raises:
            ValueError: If watcher is not found or names are not unique.
        """
        if not self.does_watcher_exist(watcher_name):
            raise ValueError(f"Watcher {watcher_name} not found.")

        if not self.is_watcher_unique(watcher_name):
            raise ValueError(
                "Watchers must have unique names.",
                f"Found multiple watchers named {watcher_name}.",
            )

        with self._lock:
            watcher_data = self._db.table(DbTable.WATCHERS).search(
                Query().name == watcher_name
            )

        return watcher_data[0]

    def get_watcher_items(self, watcher_name: str) -> List[Document]:
        """
        Get items associated with a specific watcher.

        Args:
            watcher_name (str): The name of the watcher.

        Returns:
            List[Document]: List of watcher items.
        """
        if not self.does_watcher_exist(watcher_name):
            raise ValueError(f"Watcher {watcher_name} not found.")

        if not self.is_watcher_unique(watcher_name):
            raise ValueError(
                "Watchers must have unique names.",
                f"Found multiple watchers named {watcher_name}.",
            )

        with self._lock:
            items = self._db.table(DbTable.WATCHER_DATA).search(
                Query().name == watcher_name
            )

        return items[0]["data"] if items else []

    def set_watcher_items(
        self, watcher_name: str, data: List[BaseModel]
    ) -> None:
        """
        Update or create watcher items in the database.

        Args:
            watcher_name (str): Name of the watcher.
            data (List[BaseModel]): List of Pydantic model objects to store.
        """
        if not self.does_watcher_exist(watcher_name):
            raise ValueError(f"Watcher {watcher_name} not found.")

        if not self.is_watcher_unique(watcher_name):
            raise ValueError(
                "Watchers must have unique names.",
                f"Found multiple watchers named {watcher_name}.",
            )

        dict_data = [loads(item.model_dump_json()) for item in data]
        with self._lock:
            self._db.table(DbTable.WATCHER_DATA).upsert(
                {"name": watcher_name, "data": dict_data},
                Query().name == watcher_name,
            )

    def create_watcher(self, watcher_data: WatcherModel) -> None:
        """
        Create a new watcher in the database.

        Args:
            watcher_data (WatcherModel): The watcher data to store.

        Raises:
            ValueError: If the watcher already exists.
        """
        if self.does_watcher_exist(watcher_data.name):
            raise ValueError(
                f"A watcher with the name '{watcher_data.name}' already exists."
            )

        with self._lock:
            self._db.table(DbTable.WATCHERS).insert(watcher_data.model_dump())
