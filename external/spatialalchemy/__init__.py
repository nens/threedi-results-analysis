from .types import (  # NOQA
    Geometry,
    Geography,
    Raster
    )

from .elements import (  # NOQA
    WKTElement,
    WKBElement,
    RasterElement
    )

from . import functions  # NOQA

from sqlalchemy import Table, event
from sqlalchemy.sql import select, func, expression


def _setup_ddl_event_listeners():
    @event.listens_for(Table, "before_create")
    def before_create(target, connection, **kw):
        dispatch("before-create", target, connection)

    @event.listens_for(Table, "after_create")
    def after_create(target, connection, **kw):
        dispatch("after-create", target, connection)

    @event.listens_for(Table, "before_drop")
    def before_drop(target, connection, **kw):
        dispatch("before-drop", target, connection)

    @event.listens_for(Table, "after_drop")
    def after_drop(target, connection, **kw):
        dispatch("after-drop", target, connection)

    def dispatch(event, table, bind):
        if event in ('before-create', 'before-drop'):
            # Filter Geometry columns from the table with management=True
            # Note: Geography and PostGIS >= 2.0 don't need this
            gis_cols = [c for c in table.c if
                        isinstance(c.type, Geometry) and
                        (c.type.management is True or bind.dialect.name == 'sqlite')]

            # Find all other columns that are not managed Geometries
            regular_cols = [x for x in table.c if x not in gis_cols]

            # Save original table column list for later
            table.info["_saved_columns"] = table.c

            # Temporarily patch a set of columns not including the
            # managed Geometry columns
            column_collection = expression.ColumnCollection()
            for col in regular_cols:
                column_collection.add(col)
            table.columns = column_collection

            if event == 'before-drop':
                # Drop the managed Geometry columns with DropGeometryColumn()
                if bind.dialect.name == 'sqlite':
                    for c in gis_cols:
                        if c.type.spatial_index:
                            bind.execute(select(
                                [func.DisableSpatialIndex(table.name, c.name)]).execution_options(
                                autocommit=True))
                            bind.execute("DROP TABLE idx_%s_%s" % (table.name, c.name))

                        bind.execute(select(
                            [func.DiscardGeometryColumn(table.name, c.name)]).execution_options(
                            autocommit=True))
                    return

                table_schema = table.schema or 'public'
                for c in gis_cols:
                    stmt = select([
                        func.DropGeometryColumn(
                            table_schema, table.name, c.name)])
                    stmt = stmt.execution_options(autocommit=True)
                    bind.execute(stmt)

        elif event == 'after-create':
            # Restore original column list including managed Geometry columns
            table.columns = table.info.pop('_saved_columns')

            if bind.dialect.name == 'sqlite':
                for c in table.c:
                    # Add the managed Geometry columns with AddGeometryColumn()
                    if isinstance(c.type, Geometry):
                        stmt = select([
                            func.AddGeometryColumn(
                                table.name,
                                c.name,
                                c.type.srid,
                                c.type.geometry_type,
                                c.type.dimension,
                                0 if c.nullable else 1
                            )])
                        stmt = stmt.execution_options(autocommit=True)
                        bind.execute(stmt)

                        if c.type.spatial_index:
                            bind.execute(
                                "SELECT CreateSpatialIndex('%s', '%s')" % (table.name, c.name))
                            bind.execute("VACUUM %s" % table.name)

                return
            # else postgis

            table_schema = table.schema or 'public'
            for c in table.c:
                # Add the managed Geometry columns with AddGeometryColumn()
                if isinstance(c.type, Geometry) and c.type.management is True:
                    stmt = select([
                        func.AddGeometryColumn(
                            table_schema,
                            table.name,
                            c.name,
                            c.type.srid,
                            c.type.geometry_type,
                            c.type.dimension
                        )])
                    stmt = stmt.execution_options(autocommit=True)
                    bind.execute(stmt)

                # Add spatial indices for the Geometry and Geography columns
                if isinstance(c.type, (Geometry, Geography)) and \
                        c.type.spatial_index is True:
                    bind.execute('CREATE INDEX "idx_%s_%s" ON "%s"."%s" '
                                 'USING GIST ("%s")' %
                                 (table.name, c.name, table_schema,
                                  table.name, c.name))

                # Add spatial indices for the Raster columns
                #
                # Note the use of ST_ConvexHull since most raster operators are
                # based on the convex hull of the rasters.
                if isinstance(c.type, Raster) and c.type.spatial_index is True:
                    bind.execute('CREATE INDEX "idx_%s_%s" ON "%s"."%s" '
                                 'USING GIST (ST_ConvexHull("%s"))' %
                                 (table.name, c.name, table_schema,
                                  table.name, c.name))

        elif event == 'after-drop':
            # Restore original column list including managed Geometry columns
            table.columns = table.info.pop('_saved_columns')
# todo: add check or warning to prevent double initialisation of listeners (happens when
# package is imported in different ways
_setup_ddl_event_listeners()
