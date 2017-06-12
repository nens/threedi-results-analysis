# -*- coding: utf-8 -*-
""" function for adding fields ot tables based on sqlalchmy orm definitions. Copied from
stackoverflow: https://stackoverflow.com/questions/2103274/sqlalchemy-add-new-field-to-class-
and-create-corresponding-column-in-table"""

import logging
import re

import sqlalchemy
from sqlalchemy import MetaData, Table, exc

_new_sa_ddl = sqlalchemy.__version__.startswith('0.7')

log = logging.getLogger(__name__)


def create_and_upgrade(engine, metadata):
    """For each table in metadata, if it is not in the database then create it.
    If it is in the database then add any missing columns and warn about any columns
    whose spec has changed"""
    db_metadata = MetaData()
    db_metadata.bind = engine

    for model_table in metadata.sorted_tables:
        try:
            db_table = Table(model_table.name, db_metadata, autoload=True)
        except exc.NoSuchTableError:
            log.info('Creating table %s' % model_table.name)
            model_table.create(bind=engine)
        else:
            ddl_c = engine.dialect.ddl_compiler(engine.dialect, None)

            log.debug('Table %s already exists. Checking for '
                      'missing columns' % model_table.name)

            model_columns = _column_names(model_table)
            db_columns = _column_names(db_table)

            to_create = model_columns - db_columns
            to_remove = db_columns - model_columns
            to_check = db_columns.intersection(model_columns)

            for c in to_create:
                model_column = getattr(model_table.c, c)
                log.info('Adding column %s.%s' %
                         (model_table.name, model_column.name))
                assert not model_column.constraints, \
                    'I cannot automatically add columns with constraints to the database'\
                    'Please consider fixing me if you care!'
                model_col_spec = ddl_c.get_column_specification(model_column)
                sql = 'ALTER TABLE %s ADD %s' % (
                    model_table.name, model_col_spec)
                engine.execute(sql)

            # It's difficult to reliably determine if the model has changed
            # a column definition. E.g. the default precision of columns
            # is None, which means the database decides. Therefore when I look at the model
            # it may give the SQL for the column as INTEGER but when I look at the database
            # I have a definite precision, therefore the returned type is INTEGER(11)

            for c in to_check:
                model_column = model_table.c[c]
                db_column = db_table.c[c]
                x = model_column == db_column

                log.info('Checking column %s.%s' %
                         (model_table.name, model_column.name))
                try:
                    model_col_spec = ddl_c.get_column_specification(
                        model_column)
                    db_col_spec = ddl_c.get_column_specification(db_column)
                except exc.CompileError:
                    log.debug("error in compiling  %s.%s" %
                              (model_table.name, model_column.name))

                model_col_spec = re.sub('[(][\d ,]+[)]', '', model_col_spec)
                db_col_spec = re.sub('[(][\d ,]+[)]', '', db_col_spec)
                db_col_spec = db_col_spec.replace('DECIMAL', 'NUMERIC')
                db_col_spec = db_col_spec.replace('TINYINT', 'BOOL')

                if model_col_spec != db_col_spec:
                    log.warning('Column %s.%s has specification %r in the model '
                                'but %r in the database' %
                                (model_table.name, model_column.name,
                                 model_col_spec, db_col_spec))

                if model_column.constraints or db_column.constraints:
                    log.debug('Column constraints not checked.')

            for c in to_remove:
                model_column = getattr(db_table.c, c)
                log.warning('Column %s.%s in the database is not in '
                            'the model' % (model_table.name, model_column.name))


def _column_names(table):
    # Autoloaded columns return unicode column names - make sure we treat all are equal
    return set((unicode(i.name) for i in table.c))
