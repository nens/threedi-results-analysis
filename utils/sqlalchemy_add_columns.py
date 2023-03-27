""" function for adding fields ot tables based on sqlalchmy orm definitions.
Copied from stackoverflow:
https://stackoverflow.com/questions/2103274/sqlalchemy-add-new-field-to-class-and-create-corresponding-column-in-table
"""

from sqlalchemy import exc
from sqlalchemy import text
from sqlalchemy import MetaData
from sqlalchemy import Table

import logging
import re
import sqlalchemy


_new_sa_ddl = sqlalchemy.__version__.startswith("0.7")

logger = logging.getLogger(__name__)


def create_and_upgrade(engine, metadata):
    """For each table in metadata, if it is not in the database then create it.
    If it is in the database then add any missing columns and warn about any
    columns whose spec has changed"""
    db_metadata = MetaData()
    db_metadata.bind = engine

    for model_table in metadata.sorted_tables:
        try:
            db_table = Table(
                model_table.name,
                db_metadata,
                autoload_with=engine,
            )
        except exc.NoSuchTableError:
            logger.info("Creating table %s" % model_table.name)
            model_table.create(bind=engine)
            continue

        logger.debug(
            "Table %s already exists. Checking for "
            "missing columns" % model_table.name
        )
        ddl_c = engine.dialect.ddl_compiler(engine.dialect, None)
        model_columns = _column_names(model_table)
        db_columns = _column_names(db_table)

        to_create = model_columns - db_columns
        to_remove = db_columns - model_columns
        to_check = db_columns.intersection(model_columns)

        for c in to_create:
            model_column = getattr(model_table.c, c)
            logger.info("Adding column %s.%s" % (model_table.name, model_column.name))
            assert not model_column.constraints, (
                "I cannot automatically add columns with constraints to "
                "the database. Please consider fixing me if you care!"
            )
            model_col_spec = ddl_c.get_column_specification(model_column)
            sql = "ALTER TABLE %s ADD %s" % (model_table.name, model_col_spec)
            with engine.connect() as connection:
                connection.execute(text(sql))

        # It's difficult to reliably determine if the model has changed
        # a column definition. E.g. the default precision of columns
        # is None, which means the database decides. Therefore when I look
        # at the model it may give the SQL for the column as INTEGER but
        # when I look at the database I have a definite precision,
        # therefore the returned type is INTEGER(11)

        for c in to_check:
            model_column = model_table.c[c]
            db_column = db_table.c[c]

            logger.info("Checking column %s.%s" % (model_table.name, model_column.name))
            try:
                model_col_spec = ddl_c.get_column_specification(model_column)
                db_col_spec = ddl_c.get_column_specification(db_column)
            except exc.CompileError:
                logger.exception(
                    "error in compiling %s.%s, continuing with the next column",
                    model_table.name,
                    model_column.name,
                )
                continue

            model_col_spec = re.sub(r"[(][\d ,]+[)]", "", model_col_spec)
            db_col_spec = re.sub(r"[(][\d ,]+[)]", "", db_col_spec)
            db_col_spec = db_col_spec.replace("DECIMAL", "NUMERIC")
            db_col_spec = db_col_spec.replace("TINYINT", "BOOL")

            if model_col_spec != db_col_spec:
                logger.warning(
                    "Column %s.%s has specification %r in the model "
                    "but %r in the database"
                    % (model_table.name, model_column.name, model_col_spec, db_col_spec)
                )

            if model_column.constraints or db_column.constraints:
                logger.debug("Column constraints not checked.")

        for c in to_remove:
            model_column = getattr(db_table.c, c)
            logger.warning(
                "Column %s.%s in the database is not in "
                "the model" % (model_table.name, model_column.name)
            )


def _column_names(table):
    # Autoloaded columns return unicode column names - make sure we treat all
    # are equal
    return set((str(i.name) for i in table.c))
