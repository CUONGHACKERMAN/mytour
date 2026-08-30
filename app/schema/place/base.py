from core import DomainBaseModel
from sqlalchemy.ext.declarative import declared_attr

class PlaceBase(DomainBaseModel):
    __abstract__ = True
    @declared_attr
    def __table_args__(cls):
        return {"schema": "place"}
