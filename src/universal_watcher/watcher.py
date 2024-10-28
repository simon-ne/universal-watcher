from universal_watcher.core import (
    setup,
)  # Registers data sources and notification platforms

from universal_watcher.core.decorators.injector import (
    DependencyInjector as Injector,
)
from universal_watcher.core.services.data_source_registry_service import (
    DataSourcesRegistryService,
)
from universal_watcher.core.services.db_service import CoreDbService
from universal_watcher.core.services.notification_registry_service import (
    NotificationRegistryService,
)


@Injector.inject_dependencies
class Watcher:
    def __init__(
        self,
        *,
        db_service: CoreDbService,
        data_sources_registry_service: DataSourcesRegistryService,
        notification_registry_service: NotificationRegistryService,
    ):
        self._db_service = db_service
        self._data_sources_service = data_sources_registry_service
        self._notifications_service = notification_registry_service

    def create(self):
        # TODO: Implement API
        pass

    def check(self, watcher_name: str):
        watcher_data = self._db_service.get_watcher_data(watcher_name)

        data_source = self._data_sources_service.get_data_source(
            watcher_data["data_source"]["name"]
        )

        data_source.set_params(watcher_data["data_source"]["parameters"])

        items = data_source.fetch_items()
        self._db_service.get_watcher_items(watcher_name)
        current_items = data_source.get_stored_items(watcher_name)

        # Initial setup, do not notify about new items
        if not current_items:
            self._db_service.set_watcher_items(watcher_name, items)
            return

        new_items = [item for item in items if item not in current_items]

        if not new_items:
            return

        notif_platform = self._notifications_service.get_notification_platform(
            watcher_data["notification_platform"]["name"]
        )
        notif_platform.set_params(
            watcher_data["notification_platform"]["parameters"]
        )

        print("Found new items")
        print(len(new_items))

        formatter = data_source.get_formatter(
            watcher_data["data_source"]["formatter"]
        )
        notification_platform_input = data_source.format_items(
            formatter, new_items
        )
        notif_platform.notify(notification_platform_input)

        # Save the current items to the database after the notification is sent
        # self._db_service.set_watcher_items(watcher_name, items)

    def check_all(self):
        # TODO: Implement
        pass
