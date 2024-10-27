from abc import ABC, abstractmethod

from core.classes.notification_platform.notification_platform_input import NotificationPlatformInput

class NotificationPlatform(ABC):
    # @abstractmethod
    # def possible_params(self):
    #     """Possible parameters of the notification platform"""
    #     pass

    @abstractmethod
    def params(self):
        """Parameters for the data source"""
        pass

    @abstractmethod
    def set_params(self):
        """Setup the data source parameters"""
        pass

    @abstractmethod
    def notify(self, input_data: NotificationPlatformInput) -> None:
        """Notify the user about new items"""
        pass
