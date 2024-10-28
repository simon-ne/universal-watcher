from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum

from ....core.classes.data_source.data_source_parameters import (
    DataSourceParameters,
)


class CategoryEnum(str, Enum):
    def __str__(self):
        return self.value

    NONE = ""
    ZVIERATA = "zvierata"
    DETI = "deti"
    REALITY = "reality"
    PRACA = "praca"
    AUTO = "auto"
    MOTOCYKLE = "motocykle"
    STROJE = "stroje"
    DOM_A_ZAHRADA = "dom_a_zahrada"
    PC = "pc"
    MOBILY = "mobily"
    FOTO = "foto"
    ELEKTRO = "elektro"
    SPORT = "sport"
    HUDBA = "hudba"
    VSTUPENKY = "vstupenky"
    KNIHY = "knihy"
    NABYTOK = "nabytok"
    OBLECENIE = "oblecenie"
    SLUZBY = "sluzby"
    OSTATNE = "ostatne"


class BazosSkParameters(BaseModel, DataSourceParameters):
    category: Optional[CategoryEnum] = Field(
        CategoryEnum.NONE,
        description="Kategória inzerátov na vyhľadávanie.",
        json_schema_extra={"uri_param_name": "rub"},
    )
    location: Optional[str] = Field(
        "",
        description="Mesto alebo obec, kde sa má vyhľadávať. (PSČ)",
        json_schema_extra={"uri_param_name": "hlokalita"},
    )
    search: Optional[str] = Field(
        "",
        description="Text na vyhľadávanie.",
        json_schema_extra={"uri_param_name": "hledat"},
    )
    min_price: Optional[int] = Field(
        0,
        ge=0,
        description="Cena od (eur)",
        json_schema_extra={"uri_param_name": "cenaod"},
    )
    max_price: Optional[int] = Field(
        0,
        ge=0,
        description="Cena do (eur)",
        json_schema_extra={"uri_param_name": "cenado"},
    )
    radius: Optional[int] = Field(
        25,
        ge=0,
        description="Vzdialenosť od lokality (km)",
        json_schema_extra={"uri_param_name": "humkreis"},
    )

    @field_validator("location")
    def validate_location(cls, value):
        if not value.isdigit() or len(value) != 5:
            raise ValueError(
                "Location must be in the form of a 5 digit number (12345)."
            )
        return value
