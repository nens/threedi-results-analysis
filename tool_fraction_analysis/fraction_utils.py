from threedi_results_analysis.threedi_plugin_model import ThreeDiResultItem


def has_wq_results(result_item: ThreeDiResultItem):
    return len(result_item.threedi_result.available_water_quality_vars) != 0
