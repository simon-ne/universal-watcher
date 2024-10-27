from pydantic import BaseModel, Field

from core.classes.notification_platform.notification_platform_input import (
    NotificationPlatformInput,
)


class EmailInput(BaseModel, NotificationPlatformInput):
    subject: str
    body: str
    content_type: str
