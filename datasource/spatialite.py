

def _get_spatialite_path(self):
    """Return the full path of the spatialite."""
    provider = self.layer.dataProvider()
    if not provider.name() == 'spatialite':
        return
    # uri is something like
    # ---------------------
    # u'dbname=\'/d/dev/models/sewerage/purmerend/purmerend_result.sqlite\'
    # table="sewerage_manhole" (the_geom) sql='
    # ---------------------
    uri = provider.dataSourceUri()
    dbname = uri.split("'")[1]
    return dbname
