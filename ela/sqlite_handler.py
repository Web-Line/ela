import sqlite3
import logging
import time


class SQLiteHandler(logging.Handler):
    """
    Logging handler for SQLite.
    Based on Vinay Sajip"s DBHandler class (http://www.red-dove.com/python_logging.html)

    This version sacrifices performance for thread-safety:
    Instead of using a persistent cursor, we open/close connections for each entry.

    AFAIK this is necessary in multi-threaded applications,
    because SQLite doesn"t allow access to objects across threads.
    """

    initial_sql = """CREATE TABLE IF NOT EXISTS log(
                        Created text,
                        Name text,
                        LogLevel int,
                        LogLevelName text,
                        Message text,
                        Args text,
                        Module text,
                        FuncName text,
                        LineNo int,
                        Exception text,
                        Process int,
                        Thread text,
                        ThreadName text
                   )"""

    insertion_sql = """INSERT INTO log(
                        Created,
                        Name,
                        LogLevel,
                        LogLevelName,
                        Message,
                        Args,
                        Module,
                        FuncName,
                        LineNo,
                        Exception,
                        Process,
                        Thread,
                        ThreadName
                   )
                   VALUES (
                        "%(dbtime)s",
                        "%(name)s",
                        %(levelno)d,
                        "%(levelname)s",
                        "%(msg)s",
                        "%(args)s",
                        "%(module)s",
                        "%(funcName)s",
                        %(lineno)d,
                        "%(exc_text)s",
                        %(process)d,
                        "%(thread)s",
                        "%(threadName)s"
                   );
                   """

    def __init__(self):
        logging.Handler.__init__(self)

    def formatDBTime(self, record):
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(record.created))

    def emit(self, record):

        # Use default formatting:
        self.format(record)
        # Set the database time up:
        self.formatDBTime(record)
        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(
                record.exc_info)
        else:
            record.exc_text = ""
        # Insert log record:
        sql = SQLiteHandler.insertion_sql % record.__dict__
        # conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()

# mhg
# This is a django app, which it does not seem right to me to care for multi-
# threading. so i made the object global, to load once in the running wsgi
# process.

# Create table if needed:
conn = sqlite3.connect("debug.db")
conn.execute(SQLiteHandler.initial_sql)
conn.commit()
