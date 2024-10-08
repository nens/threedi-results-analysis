# -*- coding: utf-8 -*-

"""
/***************************************************************************
 DWFCalculator
                                 A QGIS plugin
 Calculate DWF
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-01-27
        copyright            : (C) 2021 by Nelen en Schuurmans
        email                : emile.debadts@nelen-schuurmans.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = "Nelen en Schuurmans"
__date__ = "2021-01-27"
__copyright__ = "(C) 2021 by Nelen en Schuurmans"

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = "$Format:%H$"

from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingException
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterProviderConnection
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProviderConnectionException
from qgis.core import QgsProviderRegistry
from qgis.PyQt.QtCore import QCoreApplication

import csv
import datetime
import logging
import sqlite3
from typing import List

# Default values
DWF_FACTORS = [
    [0, 0.03],
    [1, 0.015],
    [2, 0.01],
    [3, 0.01],
    [4, 0.005],
    [5, 0.005],
    [6, 0.025],
    [7, 0.080],
    [8, 0.075],
    [9, 0.06],
    [10, 0.055],
    [11, 0.05],
    [12, 0.045],
    [13, 0.04],
    [14, 0.04],
    [15, 0.035],
    [16, 0.035],
    [17, 0.04],
    [18, 0.055],
    [19, 0.08],
    [20, 0.07],
    [21, 0.055],
    [22, 0.045],
    [23, 0.04],
]
INFLOW_0D_NONE = 0
INFLOW_0D_IMPERVIOUS_SURFACE = 1
INFLOW_0D_SURFACE = 2
INFLOW_TABLE_NAME_BASES = {
    INFLOW_0D_IMPERVIOUS_SURFACE: "impervious_surface",
    INFLOW_0D_SURFACE: "surface",
}


def get_dwf_factors_from_file(file_path):
    dwf_factors = []
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for row in reader:
            print(row)
            dwf_factors += [[int(row[0]), float(row[1])]]

    return dwf_factors


def start_time_and_duration_to_dwf_factors(start_time: str, duration: int, dwf_factors: List[List]) -> List[List]:
    """
    Get list of [timestep, dwf_factor] pairs for given timeframe

    :param start_time: time in the format HH:MM:SS
    :param duration: length of the resulting time series in s
    :param dwf_factors: list of 24 [hour, factor] pairs. sum of factors must be 1
    :return: list of [timestep, dwf_factor] pairs. one value per hour. timestep in s since start_time
    """
    starting_time = datetime.datetime.strptime(start_time, "%H:%M:%S")

    # First timestep at 0 seconds
    current_hour = starting_time.hour
    dwf_factor_per_timestep = [[0, dwf_factors[starting_time.hour % 24][1]]]

    for second in range(1, duration + 1):
        time = starting_time + datetime.timedelta(seconds=second)
        if time.hour != current_hour:
            dwf_factor_per_timestep.append([second, dwf_factors[time.hour % 24][1]])
        elif second == duration:
            dwf_factor_per_timestep.append([second, dwf_factors[time.hour % 24][1]])

        current_hour = time.hour

    return dwf_factor_per_timestep


def read_inflow_type(spatialite_connection):
    c = spatialite_connection.cursor()

    sql = """SELECT use_0d_inflow FROM v2_global_settings;"""
    c.execute(sql)
    use_0d_inflow = int(c.fetchone()[0])
    return use_0d_inflow


def read_dwf_per_node(spatialite_path):
    """
    Obtains the total dry weather flow in m3/d per connection node from a 3Di model sqlite-file.
    Returns None if use_0d_inflow = 0
    """
    conn = sqlite3.connect(spatialite_path)
    use_0d_inflow = read_inflow_type(conn)
    if use_0d_inflow == INFLOW_0D_NONE:
        return None
    else:
        basename = INFLOW_TABLE_NAME_BASES[use_0d_inflow]
        sql = f"""
                SELECT 	map.connection_node_id,
                        sum(surf.dry_weather_flow * surf.nr_of_inhabitants * map.percentage/100)/1000 AS dwf
                FROM 	v2_{basename} AS surf
                JOIN 	v2_{basename}_map AS map
                ON 		surf.id = map.{basename}_id
                WHERE 	surf.dry_weather_flow IS NOT NULL
                        and surf.nr_of_inhabitants != 0
                        and surf.nr_of_inhabitants IS NOT NULL
                        and map.percentage IS NOT NULL
                GROUP BY map.connection_node_id
                ;
        """
        c = conn.cursor()
        dwf = [row for row in c.execute(sql)]
        conn.close()

        return dwf


def generate_dwf_lateral_json(spatialite_filepath, start_time, duration, dwf_factors):
    dwf_list = []
    dwf_on_each_node = read_dwf_per_node(spatialite_filepath)
    if not dwf_on_each_node:
        return dwf_list
    dwf_factor_per_timestep = start_time_and_duration_to_dwf_factors(
        start_time=start_time, duration=duration, dwf_factors=dwf_factors
    )

    # Generate JSON for each connection node
    for connection_node_id, dwf_m3_d in dwf_on_each_node:
        values_list = []
        for timestep, dwf_factor in dwf_factor_per_timestep:
            dwf_m3_s = dwf_m3_d * dwf_factor / 3600
            values_list.append(f"{timestep},{dwf_m3_s}")
        values_str = "\n".join(values_list)
        dwf_list.append(
            {
                "offset": 0,
                "interpolate": 0,
                "values": values_str,
                "units": "m3/s",
                "connection_node": connection_node_id,
            }
        )

    return dwf_list


def dwf_json_to_csv(dwf_list, output_csv_file):
    with open(output_csv_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["id", "connection_node_id", "timeseries"])
        for i, row in enumerate(dwf_list):
            lat_id = i
            connection_node_id = row["connection_node"]
            timeseries = row["values"]
            writer.writerow([str(lat_id), str(connection_node_id), timeseries])


class DWFCalculatorAlgorithm(QgsProcessingAlgorithm):

    OUTPUT = "OUTPUT"
    INPUT = "INPUT"

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterProviderConnection(
                name=self.INPUT,
                description=self.tr("Input spatialite (.sqlite)"),
                provider="spatialite",
            )
        )

        self.addParameter(
            QgsProcessingParameterString("start_time", self.tr("Start time of day (HH:MM:SS)"), "00:00:00")
        )

        self.addParameter(QgsProcessingParameterString("duration", self.tr("Simulation duration (hours)")))

        self.addParameter(
            QgsProcessingParameterFile(
                "dwf_progress_file",
                self.tr("DWF progress file (.csv)"),
                extension="csv",
                defaultValue=None,
                optional=True,
            )
        )

        self.addParameter(QgsProcessingParameterFileDestination(self.OUTPUT, self.tr("Output CSV"), "csv(*.csv)"))

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        start_time = self.parameterAsString(parameters, "start_time", context)
        duration = self.parameterAsInt(parameters, "duration", context)
        connection_name = self.parameterAsConnectionName(parameters, self.INPUT, context)
        output_csv = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        dwf_factor_input = self.parameterAsFile(parameters, "dwf_progress_file", context)

        try:
            md = QgsProviderRegistry.instance().providerMetadata("spatialite")
            conn = md.createConnection(connection_name)
        except QgsProviderConnectionException:
            logging.exception("Error setting up connection to spatialite")
            raise QgsProcessingException(
                self.tr("Could not retrieve connection details for {}").format(connection_name)
            )

        spatialite_filename = conn.uri()[8:-1]

        if dwf_factor_input:
            dwf_factors = get_dwf_factors_from_file(dwf_factor_input)
        else:
            dwf_factors = DWF_FACTORS

        dwf_list = generate_dwf_lateral_json(
            spatialite_filepath=spatialite_filename,
            start_time=start_time,
            duration=int(duration * 3600),
            dwf_factors=dwf_factors,
        )

        dwf_json_to_csv(dwf_list=dwf_list, output_csv_file=output_csv)

        return {self.OUTPUT: output_csv}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DWFCalculator"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("DWF Calculator")

    def group(self):
        return "Pre-process simulation inputs"

    def groupId(self):
        return "pre_process_sim_inputs"

    def shortHelpString(self):

        help_string = """
        Calculate dry weather flow on connection nodes for a given model schematisation and simulation settings. Produces a formatted csv that can be used as a 1d lateral in the 3Di API Client.
        Input spatialite: valid spatialite containing the schematisation of a 3Di model. \n
        Start time of day: at which hour of the day the simulation is started (HH:MM:SS). \n
        Simulation duration: amount of time the simulation is run (hours). \n
        DWF progress file:  timeseries that contains the fraction of the maximum dry weather flow at each hour of the day. Formatted as follows:\n
        '0, 0.03'\n
        '1, 0.015'\n
        ...
        '23, 0.04'\n
        Defaults to a pattern specified by Rioned.
        Output CSV: csv file to which the output 1d laterals are saved. This will be the input used by the API Client.
        """

        return self.tr(help_string)

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return DWFCalculatorAlgorithm()
