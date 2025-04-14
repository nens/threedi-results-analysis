from qgis.PyQt.QtGui import QStandardItemModel


class FractionModel(QStandardItemModel):

    def set_column_sizes_on_view(self, table_view):
        """Helper function for applying the column sizes on a view.

        :table_view: table view instance that uses this model
        """
        if table_view.model is None:
            raise RuntimeError("No model set on view.")

        for col_nr in range(0, self.columnCount()):
            width = self.columns[col_nr].column_width
            if width:
                table_view.setColumnWidth(col_nr, width)
            if not self.columns[col_nr].show:
                table_view.setColumnHidden(col_nr, True)