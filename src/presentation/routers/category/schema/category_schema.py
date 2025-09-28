from pydantic import BaseModel


class CategorySchema(BaseModel):
    name: dict[str, str] = {
        "en": "Electronics",
        "ru": "Электроника",
        "uz": "Elektronika"
    }
    description: dict[str, str] = {
        "en": "Devices and gadgets",
        "ru": "Устройства и гаджеты",
        "uz": "Qurilmalar va gadjetlar"
    }
