import pkgutil
import importlib
from core.classes.data_source.data_source import DataSource
from core.classes.notification_platform.notification_platform import (
    NotificationPlatform,
)
from core.services.data_source_registry_service import (
    DataSourcesRegistryService,
)
from core.services.notification_registry_service import (
    NotificationRegistryService,
)


def discover_and_register(package, base_class, registry, name_attr="NAME"):
    package = importlib.import_module(package)
    for finder, name, ispkg in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package.__name__}.{name}")
        for attr in dir(module):
            cls = getattr(module, attr)
            if (
                isinstance(cls, type)
                and issubclass(cls, base_class)
                and cls is not base_class
            ):
                name = getattr(cls, name_attr, cls.__name__.lower())
                registry.register(**{"name": name, "cls_type": cls})


data_sources_registry = DataSourcesRegistryService()
notification_registry = NotificationRegistryService()

# Discover DataSources
discover_and_register(
    "watcher.data_sources", DataSource, data_sources_registry
)

# Discover NotificationPlatforms
discover_and_register(
    "watcher.notification_platforms",
    NotificationPlatform,
    notification_registry,
)
