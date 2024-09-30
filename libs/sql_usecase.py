"""
Author: your name
Date: 2024-09-28 19:52:54
データベース系のユースケース(ビジネスロジック)を記述する.


"""

import logging
import traceback

# third-party packages
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

# user-defined packages
from .sql_handler import File, Page, Task


class DBUseCase:

    def __init__(self, database_url: str, is_health_check: bool = False):
        self.database_url = database_url
        self.is_open = False
        self.logger = logging.getLogger("DB")

        try:
            # SQLAlchemyエンジンの作成
            self.engine = create_engine(database_url, echo=True)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            self.is_open = True

            if is_health_check:
                self.health_check()
        except Exception:
            self.logger.error(f"Errror Occurred: {traceback.format_exc()}")
            self.close()

    def health_check_one(self, table_name: str) -> bool:
        if not self.is_open:
            raise ValueError("Session is not opened")

        try:
            self.logger.info(f'Checking if table "{table_name}" exists...')
            self.session.execute(f"SELECT 1 FROM {Task}")
            self.logger.info(f'Table "{table_name}" exists and is accessible.')
            return True
        except SQLAlchemyError as e:
            self.logger.error(f"Health check failed: {e}")
            raise e

    def health_check(self) -> bool:
        results = []
        for table_name in [Task.__tablename__, File.__tablename__, Page.__tablename__]:
            results.append(self.health_check_one(table_name))
        # 一つでもFalseの場合は、False
        return all(results)

    def close(self):
        if self.is_open:
            if hasattr(self, "session"):
                self.session.close()
                del self.session
            else:
                self.logger.warning("Session is not opened")

            if hasattr(self, "engine"):
                self.engine.dispose()
                del self.engine
            else:
                self.logger.warning("Engine is not opened")
            self.is_open = False
        else:
            self.logger.warning("Engine and Session are not opened.")

    def get_ready_tasks(self) -> list[Task]:
        return self.session.query(Task).filter(Task.status == "Ready").all()

    def register_page(self, page: Page):
        self.session.add(page)
        self.session.commit()


if __name__ == "__main__":
    pass
