import MySQLdb
import logging
import time
from django.conf import settings


class MySQLHandler(logging.Handler):
    """
    Logging handler for SQLite.
    Based on Vinay Sajip"s DBHandler class (http://www.red-dove.com/python_logging.html)

    This version sacrifices performance for thread-safety:
    Instead of using a persistent cursor, we open/close connections for each entry.

    AFAIK this is necessary in multi-threaded applications,
    because SQLite doesn"t allow access to objects across threads.
    """

    initial_sql = """
        CREATE TABLE IF NOT EXISTS log(
            Id int not null primary key auto_increment,
            Created date,
            Name varchar(32) not null,
            LogLevel int not null,
            LogLevelName varchar(16) not null,
            Message varchar(4096) not null,
            Args varchar(256) not null,
            Module varchar(256) not null,
            FuncName varchar(256) not null,
            LineNo int not null,
            Exception varchar(4096) not null,
            Process int not null,
            Thread varchar(128) not null,
            ThreadName varchar(128) not null
        )"""

    insertion_sql = """
        INSERT INTO log (
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
        record.dbtime = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(record.created)
        )

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
        sql = MySQLHandler.insertion_sql % record.__dict__
        # conn = sqlite3.connect(self.db)
        cursor.execute(sql)
        conn.commit()


# mhg
# This is a django app, which it does not seem right to me to care for multi-
# threading. so i made the object global, to load once in the running wsgi
# process.

conn = MySQLdb.connect(
    db=settings.DATABASES['default']['NAME'],
    user=settings.DATABASES['default']['USER'],
    host=settings.DATABASES['default']['HOST'],
    port=int(settings.DATABASES['default']['PORT']),
    passwd=settings.DATABASES['default']['PASSWORD'],
)

cursor = conn.cursor()
# Create table if needed:
cursor.execute(MySQLHandler.initial_sql)
conn.commit()
