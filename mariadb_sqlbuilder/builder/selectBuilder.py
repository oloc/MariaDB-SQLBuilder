from typing import Union

from ..execution import executeFunctions
from .baseBuilder import ConditionsBuilder, _getTCN
from .joinBuilder import _JoinBuilder, BaseJoinExtension


class SelectBuilder(ConditionsBuilder, BaseJoinExtension):

    def __init__(self, tb, column):
        super().__init__(tb)
        self.column = [_getTCN(self.tb.table, c) for c in column.replace(", ", ",").split(",")]

    def joinSelect(self, joinTable: str, column: str):
        column = column.replace(", ", ",").split(",")
        columns = []
        [columns.append(_getTCN(joinTable, c)) for c in column]
        self.column += columns
        return self

    def columnSelect(self, column: str):
        column = column.replace(", ", ",").split(",")
        columns = []
        [columns.append(_getTCN(self.tb.table, c)) for c in column]
        self.column += columns
        return self

    def fetchone(self):
        cursor = self.tb.connect.getAvailableCursor()
        result = executeFunctions.executeOne(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def fetchall(self):
        cursor = self.tb.connect.getAvailableCursor()
        result = executeFunctions.executeAll(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        return f"SELECT {', '.join(self.column)} FROM {self.tb.table} " \
               f"{' '.join(self.__joins) if self.__joins else ''} " \
            f"{'WHERE ' + ' AND '.join(self._where_conditions) if self._where_conditions else ''}"
