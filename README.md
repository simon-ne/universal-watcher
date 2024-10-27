# Universal Watcher

**Universal Watcher** is a versatile and extensible Python package designed to monitor data sources and send notifications through various platforms. With a modular architecture and dependency injection, it allows seamless integration of new data sources and notification methods, making it ideal for a wide range of applications such as monitoring websites, APIs, or any data streams and notifying users via email, SMS, or other channels.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Adding New Data Sources](#adding-new-data-sources)
- [Adding New Notification Platforms](#adding-new-notification-platforms)
- [Dependency Injection](#dependency-injection)
- [Database](#database)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Modular Data Sources**: Easily add or remove data sources to monitor.
- **Flexible Notification Platforms**: Send notifications via email, SMS, or any other custom platform.
- **Dependency Injection**: Simplifies managing dependencies and enhances testability.
- **Persistent Storage**: Uses TinyDB for lightweight data storage.
- **Configurable Parameters**: Customize data source and notification parameters through configuration files.
- **Template-Based Formatting**: Utilize Jinja2 templates for crafting notification messages.
- **Singleton Services**: Ensures single instances of critical services for consistent behavior.

## Architecture

Universal Watcher follows a modular architecture with clear separations between data sources, notification platforms, services, and core functionalities. Here's an overview of the primary components:

- **Data Sources**: Implemented as subclasses of the `DataSource` abstract base class. Each data source fetches and processes data from a specific source.
- **Notification Platforms**: Implemented as subclasses of the `NotificationPlatform` abstract base class. Each platform handles sending notifications through different channels.
- **Services**: Singleton services manage registries for data sources and notification platforms, handle database interactions, and provide utility functions.
- **Dependency Injection**: Managed through a custom `DependencyInjector` decorator to handle dependencies and prevent circular references.

## Installation

### Prerequisites

- Python 3.8 or higher
- `pip` package manager

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/universal-watcher.git
   cd universal-watcher
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables

Set up the necessary environment variables for email notifications. Create a `.env` file or set them directly in your environment:

```env
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_ENCRYPTION=STARTTLS
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
SMTP_SENDER_EMAIL=sender@example.com
```

### Database

Universal Watcher uses TinyDB for data storage. The default database file is located at `package/core/db.json`. Ensure the application has read/write permissions to this file.

## Usage

### Setting Up Watchers

1. **Register Data Sources and Notification Platforms**

   The `core/setup.py` script registers available data sources and notification platforms. Ensure this script is executed when initializing the watcher.

2. **Initialize the Watcher**

   ```python
   import core.setup  # Registers data sources and notification platforms
   from core.watchers import Watcher

   watcher = Watcher()
   ```

3. **Configure Watcher Parameters**

   Configure your watcher by setting up data source parameters and notification platform parameters in the database (`db.json`).

4. **Run Checks**

   ```python
   watcher.check("watcher_name")
   ```

### Example

```python
from core.watchers import Watcher

# Initialize watcher
watcher = Watcher()

# Check a specific watcher by name
watcher.check("bazos_sk_watcher")
```

## Adding New Data Sources

To add a new data source:

1. **Create a Data Source Class**

   Subclass the `DataSource` abstract base class and implement all abstract methods.

   ```python
   from core.classes.data_source.data_source import DataSource
   from core.decorators.injector import DependencyInjector as Injector

   @Injector.inject_as_singleton
   @Injector.inject_dependencies
   class NewDataSource(DataSource):
       def __init__(self, *, data_service, db_service, formatter_service):
           # Initialize dependencies
           pass

       def params(self):
           # Return parameters
           pass

       def set_params(self, params: dict):
           # Set parameters
           pass

       def fetch_items(self):
           # Fetch new items
           pass

       def get_stored_items(self):
           # Get stored items
           pass

       def get_formatter(self, formatter_name: str):
           # Return formatter
           pass

       def format_items(self, formatter_name: str, items: list):
           # Format items
           pass
   ```

2. **Register the Data Source**

   In `core/setup.py`, register your new data source:

   ```python
   from data_sources.new_source.new_data_source import NewDataSource
   from data_sources.new_source.config import NEW_DATA_SOURCE_NAME

   data_sources_registry.register_data_source(
       NEW_DATA_SOURCE_NAME, NewDataSource
   )
   ```

3. **Define Parameters and Models**

   Create necessary parameter and item models using Pydantic.

4. **Implement Services**

   If your data source requires additional services (e.g., API clients), implement and inject them as needed.

## Adding New Notification Platforms

To add a new notification platform:

1. **Create a Notification Platform Class**

   Subclass the `NotificationPlatform` abstract base class and implement all abstract methods.

   ```python
   from core.classes.notification_platform.notification_platform import NotificationPlatform
   from core.decorators.injector import DependencyInjector as Injector

   @Injector.inject_as_singleton
   @Injector.inject_dependencies
   class NewNotificationPlatform(NotificationPlatform):
       def __init__(self, *, notification_service):
           # Initialize dependencies
           pass

       def params(self):
           # Return parameters
           pass

       def set_params(self, params: dict):
           # Set parameters
           pass

       def notify(self, input_data):
           # Send notification
           pass
   ```

2. **Register the Notification Platform**

   In `core/setup.py`, register your new notification platform:

   ```python
   from notification_platforms.new_platform.new_notification_platform import NewNotificationPlatform
   from notification_platforms.new_platform.config import NEW_NOTIFICATION_PLATFORM_NAME

   notification_platforms_registry.register_notification_platform(
       NEW_NOTIFICATION_PLATFORM_NAME, NewNotificationPlatform
   )
   ```

3. **Define Parameters and Models**

   Create necessary parameter and input models using Pydantic.

4. **Implement Services**

   Implement any required services (e.g., API clients) and inject them as needed.

## Dependency Injection

Universal Watcher utilizes a custom `DependencyInjector` for managing dependencies, promoting loose coupling and enhancing testability.

### How It Works

- **Singletons**: Classes can be marked as singletons using the `@inject_as_singleton` decorator, ensuring only one instance exists.
- **Dependency Injection**: Use the `@inject_dependencies` decorator on classes to automatically inject required dependencies based on type hints.
- **Circular Dependency Prevention**: The injector detects and prevents circular dependencies, raising a `CircularDependencyError` if detected.

### Example

```python
from core.decorators.injector import DependencyInjector as Injector

@Injector.inject_as_singleton
@Injector.inject_dependencies
class ExampleService:
    def __init__(self, *, dependency: AnotherService):
        self.dependency = dependency
```

## Database

Universal Watcher uses **TinyDB** for lightweight JSON-based data storage.

### Tables

- **watchers**: Stores watcher configurations.
- **watcher_data**: Stores fetched items for each watcher.
- **data_sources**: Stores registered data sources.
- **notification_platforms**: Stores registered notification platforms.

### CoreDbService

Provides methods to interact with the database, such as fetching and storing watcher data.

## Error Handling

Universal Watcher includes robust error handling to manage potential issues:

- **CircularDependencyError**: Raised when a circular dependency is detected during dependency injection.
- **ValueError**: Raised for invalid configurations, missing parameters, or failed operations.
- **Exception Handling**: Catch and handle exceptions during data fetching or notification sending to ensure reliability.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/new-feature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add new feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/new-feature
   ```

5. **Open a Pull Request**

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions, issues, or feature requests, please open an issue on the [GitHub repository](https://github.com/simon-ne/universal-watcher).

---

**Happy Watching!** 🚀