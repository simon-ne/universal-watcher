import pkgutil
import importlib

from universal_watcher.core.classes.data_source.data_source import DataSource
from universal_watcher.core.classes.notification_platform.notification_platform import (
    NotificationPlatform,
)
from universal_watcher.core.services.data_source_registry_service import (
    DataSourcesRegistryService,
)
from universal_watcher.core.services.notification_registry_service import (
    NotificationRegistryService,
)


def discover_and_register(package, base_class, registry, name_attr="NAME"):
    package = importlib.import_module(package)
    for finder, name, ispkg in pkgutil.walk_packages(
        package.__path__, prefix=package.__name__ + "."
    ):
        module = importlib.import_module(name)
        for attr in dir(module):
            cls = getattr(module, attr)
            if (
                isinstance(cls, type)
                and issubclass(cls, base_class)
                and cls is not base_class
            ):
                cls_name = getattr(cls, name_attr, cls.__name__.lower())
                print(f"Registering {cls_name}")
                if isinstance(registry, DataSourcesRegistryService):
                    registry.register_data_source(name=cls_name, cls_type=cls)
                elif isinstance(registry, NotificationRegistryService):
                    registry.register_notification_platform(
                        name=cls_name, cls_type=cls
                    )


data_sources_registry = DataSourcesRegistryService()
notification_registry = NotificationRegistryService()

# Discover DataSources
discover_and_register(
    "universal_watcher.data_sources", DataSource, data_sources_registry
)

# Discover NotificationPlatforms
discover_and_register(
    "universal_watcher.notification_platforms",
    NotificationPlatform,
    notification_registry,
)