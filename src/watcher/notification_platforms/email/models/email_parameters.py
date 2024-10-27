from pydantic import BaseModel, Field

from core.classes.notification_platform.notification_platform_parameters import (
    NotificationPlatformParameters,
)


class EmailParameters(BaseModel, NotificationPlatformParameters):
    to: str = Field(..., description="Adresa príjemcu emailu.")
