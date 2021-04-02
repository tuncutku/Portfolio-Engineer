from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

from src.messanger.tasks.email import send_email


@dataclass
class AlertBase(ABC):
    @property
    @abstractmethod
    def recipients(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def subject(self) -> str:
        pass

    @property
    @abstractmethod
    def email_template(self):
        pass

    @abstractmethod
    def condition(self) -> bool:
        pass

    @abstractmethod
    def generate_email_content(self) -> dict:
        pass

    def send_async_email(self) -> None:
        contents = self.generate_email_content()
        send_email.apply_async(
            subject=self.subject,
            recipients=self.recipients,
            html=render_template(self.email_template, **contents),
        )