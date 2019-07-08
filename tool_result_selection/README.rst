Result selection tool
=====================

In the result selection tool, you can do three things:

- Download results from Lizard.

- Select from among those results.

- Select model schematisation.

All three are handled by one single big dialog that is managed via
:py:class:`ThreeDiToolbox.tool_result_selection.result_selection.ThreeDiResultSelection`.

Throughout the whole plugin's code, you'll see ``self.ts_datasources``. That
is an instance of of
:py:class:`ThreeDiToolbox.tool_result_selection.models.TimeseriesDatasourceModel`,
which is a good starting point for investigating the result selection tool.

Also important is an attribute on abovementioned TimeSeriesDatasourceModel,
:py:attr:`ThreeDiToolbox.tool_result_selection.models.TimeseriesDatasourceModel.model_spatialite_filepath`,
which is the selected model schematisation.

A list of downloadable Lizard results is maintained in
:py:class:`ThreeDiToolbox.tool_result_selection.models.DownloadableResultModel`.
