from typing_extensions import Annotated

from sqlalchemy import func
from sqlalchemy import types

from sqlalchemy.orm import mapped_column

import datetime

str_256 = Annotated[str, mapped_column(types.String(256))]
text = Annotated[str, mapped_column(types.String(256))]
pk = Annotated[int, mapped_column(types.BIGINT, primary_key=True)]
timestamp = Annotated[datetime.datetime, mapped_column(server_default=func.current_timestamp())]
