import sys
import os

sys.path.append(os.getcwd())

from sqlalchemy import create_mock_engine
from app.database.base import Base

import app.models

def dump(sql, *multiparams, **params):
    print(str(sql.compile(dialect=engine.dialect)).strip() + ";")

engine = create_mock_engine("postgresql://", dump)

Base.metadata.create_all(engine, checkfirst=False)
