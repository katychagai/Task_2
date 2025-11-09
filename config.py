from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    base_url: str


def get_settings():
    return Settings(
        base_url=os.getenv("BASE_URL", "https://stellarburgers.education-services.ru"),
    )

