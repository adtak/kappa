import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DataBaseConnection(object):
    def __init__(self, db_url=None):
        self.db_url = db_url or os.environ["DATABASE_URL"]
        self.engine = create_engine(self.db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
