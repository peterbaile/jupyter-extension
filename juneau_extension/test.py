from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.types import DateTime
from sqlalchemy.sql.expression import select, func


class as_utc(GenericFunction):
    type = DateTime


print(select([func.as_utc()]))
