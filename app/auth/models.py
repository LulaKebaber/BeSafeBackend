from app.utils import AppModel


class Contact(AppModel):
    name: str
    phone: str
    gps: bool
