# Universal Watcher

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

**Universal Watcher** is a versatile and extendable Python package designed to monitor various data sources and notify users about new data through multiple notification platforms. Easily add support for new data sources and notification methods without modifying the core package.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Creating a Watcher](#creating-a-watcher)
  - [Checking Watchers](#checking-watchers)
- [Extending Universal Watcher](#extending-universal-watcher)
  - [Adding a New Data Source](#adding-a-new-data-source)
  - [Adding a New Formatter](#adding-a-new-formatter)
  - [Adding a New Notification Platform](#adding-a-new-notification-platform)
- [Configuration](#configuration)
- [Development](#development)
  - [Running Tests](#running-tests)
  - [Building and Publishing](#building-and-publishing)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Extendable Data Sources**: Add custom data sources with multiple formatters.
- **Multiple Notification Platforms**: Integrate various notification methods like email, SMS, and more.
- **Dependency Injection**: Simplified management of dependencies using a custom injector.
- **Thread-Safe Database Operations**: Reliable storage with TinyDB.
- **Environment Variable Configuration**: Securely manage sensitive information.
- **Automated Releases**: CI/CD pipeline to build and publish packages to PyPI.

## Installation

Install via pip:

```bash
pip install universal_watcher
```

Or install from source:

```bash
git clone https://github.com/simon-ne/universal-watcher.git
cd universal-watcher
pip install .
```

## Usage

Universal Watcher provides methods to create new watchers, check existing watchers for new data, and check all watchers at once.

### Creating a Watcher

To create a new watcher, define the data source and notification platform parameters and register the watcher in the database. This setup allows you to monitor specific data sources and receive notifications through your chosen platforms.

```python
from universal_watcher import Watcher

watcher = Watcher()
watcher.create(
    watcher_name="my_watcher",
    data_source_data={
        "name": "bazos_sk",
        "formatter": "email_formatter",
        "parameters": {
            "category": "auto",
            "location": "12345",
            "search": "sedan",
            "min_price": 5000,
            "max_price": 20000,
            "radius": 50
        }
    },
    notification_platform_data={
        "name": "email",
        "parameters": {
            "to": "recipient@example.com"
        }
    }
)
```

### Checking Watchers

- **Check a Specific Watcher**: Looks for new data and notifies the user if any new items are found.

  ```python
  watcher.check("my_watcher")
  ```

- **Check All Watchers**: Iterates through all registered watchers, checking for new data and sending notifications as needed.

  ```python
  watcher.check_all()
  ```

## Extending Universal Watcher

Universal Watcher is designed to be easily extensible. You can add new data sources, formatters, and notification platforms without altering the core package.

### Adding a New Data Source

1. **Create the Data Source Class**: Inherit from `DataSource` and implement the required abstract methods.

2. **Add Formatters**: Each data source can have multiple formatters. Create formatter classes inheriting from `Formatter`.

3. **Register the Data Source**: Place your data source in the `data_sources` package and ensure it's discoverable via the `setup.py` script.

**Example Structure:**

```
universal_watcher/
  data_sources/
    your_data_source/
      __init__.py
      your_data_source.py
      formatters/
        your_formatter.py
      models/
        your_item.py
      services/
        your_service.py
```

### Adding a New Formatter

1. **Create Formatter Class**: Inherit from `Formatter` and implement the `format_items` method.

2. **Register Formatter**: Add the formatter to the data source's `config.py` under the `FORMATTERS` dictionary.

```python
# your_formatter.py
from universal_watcher.core.classes.formatter.formatter import Formatter

class YourFormatter(Formatter):
    def format_items(self, items):
        # Implement formatting logic
        pass
```

```python
# config.py
from .your_formatter import YourFormatter

FORMATTERS = {
    'your_formatter': YourFormatter
}
```

### Adding a New Notification Platform

1. **Create Notification Platform Class**: Inherit from `NotificationPlatform` and implement the required methods.

2. **Register the Notification Platform**: Place your platform in the `notification_platforms` package and ensure it's discoverable via the `setup.py` script.

**Example Structure:**

```
universal_watcher/
  notification_platforms/
    your_platform/
      __init__.py
      your_platform.py
      models/
        your_input.py
      services/
        your_service.py
```

## Configuration

Use environment variables to manage sensitive configurations such as SMTP credentials. This ensures that sensitive information is not hard-coded and can be easily managed across different environments.

**Example Environment Variables for Email Notification Platform:**

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_ENCRYPTION`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_SENDER_EMAIL`

You can set these variables in your environment or use a `.env` file. Ensure that your environment variables are loaded before running the application.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).