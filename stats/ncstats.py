"""
This code was basically copied from python-flow with modifications to make
it work with our own data sources.
"""
import numpy as np
import inspect

from ..datasource.netcdf import NetcdfDataSource, normalized_object_type
from ..utils.user_messages import log


def tailored_args(f, **kwargs):
    """Filter and apply relevant kwargs to function."""
    relevant_args = {k: v for (k, v) in kwargs.items() if k
                     in inspect.getargspec(f).args}
    return f(**relevant_args)


class NcStats(object):
    """Get basic stats about subgrid netCDF files"""

    # TODO: there are possible issues when you have arrays with shapes or
    # lengths of 2. I.e. a q slice array has a shape of (2,), and when
    # the last element is truncated you will get an array of shape (1,)
    # which can be broadcasted together with everything. In practise there
    # should probably be no issues since the time and q arrays are of the
    # same length, but you never know. Might need some investigation.

    # Update these lists if you add a new method
    AVAILABLE_STRUCTURE_PARAMETERS = [
        'q_cumulative_duration', 'q_end', 'tot_vol_positive',
        'tot_vol_negative', 'time_q_max']
    AVAILABLE_MANHOLE_PARAMETERS = ['s1_end', 'wos_duration']
    AVAILABLE_PUMP_PARAMETERS = ['tot_vol_pump', 'pump_duration']

    def __init__(self, netcdf_file_path=None, ds=None, datasource=None):
        """
        NOTE: ds arg is not supported at this time!!!

        Args:
            netcdf_file_path: path to netcdf
            ds: netcdf dataset
            datasource: NetcdfDataSource object
        """
        if datasource:
            self.datasource = datasource
        elif not ds and netcdf_file_path:
            raise NotImplementedError('DEPRECATED')
        elif ds:
            # TODO: needs fixing
            raise NotImplementedError('TODO')
        else:
            raise ValueError("No netCDF source")

    @property
    def timesteps(self):
        return self.datasource.timesteps

    @property
    def timestamps(self):
        return self.datasource.timestamps

    def tot_vol_positive(self, structure_type, obj_id):
        """Total volume through structure, counting only positive q's."""
        q_slice = self.datasource.get_values_by_id(
            'q', structure_type, object_id=obj_id)
        # mask negative values
        ma_q_slice = np.ma.masked_where(q_slice < 0, q_slice)
        # calc total vol thru structure
        vols = self.timesteps * ma_q_slice[0:-1]
        return vols.sum()

    def tot_vol_negative(self, structure_type, obj_id):
        """Total volume through structure, counting only negative q's."""
        q_slice = self.datasource.get_values_by_id(
            'q', structure_type, object_id=obj_id)
        # mask positive values
        ma_q_slice = np.ma.masked_where(q_slice > 0, q_slice)
        # calc total vol thru structure
        vols = self.timesteps * ma_q_slice[0:-1]
        return vols.sum()

    def tot_vol_pump(self, structure_type, obj_id):
        """Total volume through a pump calculated using integration.

        Note: for pumps we know that q_pump is always positive.
        """
        q_slice = self.datasource.get_values_by_id(
            'q_pump', structure_type, object_id=obj_id)
        # calc total vol thru structure
        vols = self.timesteps * q_slice[0:-1]
        return vols.sum()

    def pump_duration(self, structure_type, obj_id, capacity_L_per_sec=None):
        vol_pump = self.tot_vol_pump(structure_type, obj_id)
        duration_secs = 1000 * vol_pump / capacity_L_per_sec
        return duration_secs

    def q_max(self, structure_type, obj_id):
        """Maximum value of a q timeseries; can be negative.
        """
        q_slice = self.datasource.get_values_by_id(
            'q', structure_type, object_id=obj_id)
        _min = q_slice.min()
        _max = q_slice.max()
        # return highest absolute value, while retaining the sign of the number
        return max(_min, _max, key=abs)

    def time_q_max(self, structure_type, obj_id):
        """The time at maximum value of a q timeseries
        """
        q_slice = self.datasource.get_values_by_id(
            'q', structure_type, object_id=obj_id)
        _min = q_slice.min()
        _max = q_slice.max()
        # return highest absolute value, while retaining the sign of the number
        largest = max(_min, _max, key=abs)
        (rows,) = np.where(q_slice == largest)
        return self.timestamps[rows[0]]

    def s1_max(self, structure_type, obj_id):
        """Maximum value of a s1 timeseries."""
        s1_slice = self.datasource.get_values_by_id(
            's1', structure_type, object_id=obj_id)
        return s1_slice.max()

    def s1_end(self, structure_type, obj_id):
        """Last value of a s1 timeseries."""
        s1_slice = self.datasource.get_values_by_id(
            's1', structure_type, object_id=obj_id)
        return s1_slice[-1]

    def q_cumulative_duration(self, structure_type, obj_id, threshold=None):
        """Cumulative duration of all nonzero occurences of q.
        """
        if threshold:
            # TODO: q values can be vary small, maybe add a threshold??
            raise NotImplementedError()
        q_slice = self.datasource.get_values_by_id(
            'q', structure_type, object_id=obj_id)

        # normalize nonzero qs to 1, so it becomes a binary representation
        # of q, which we can simply multiply with the timesteps
        q_slice = np.absolute(q_slice)
        q_slice[q_slice > 0] = 1.
        cum_duration = self.timesteps * q_slice[0:-1]
        return cum_duration.sum()

    def wos_duration(self, structure_type, obj_id, surface_level=None):
        """Cumulative duration of s1 when there is 'water op straat'.

        This means, count the timesteps where s1 - surface level > 0.
        """
        s1_slice = self.datasource.get_values_by_id(
            's1', structure_type, object_id=obj_id)

        water_op_straat = s1_slice - surface_level

        # Normalize >0 to 1, and <0 to 0, so that we have a binary
        # representation of values we can multiply with the time steps.
        water_op_straat[water_op_straat > 0] = 1.
        water_op_straat[water_op_straat < 0] = 0
        cum_duration = self.timesteps * water_op_straat[0:-1]
        return cum_duration.sum()

    def q_end(self, structure_type, obj_id):
        """q at last timeSTAMP (!= timestep)
        """
        q_slice = self.datasource.get_values_by_id(
            'q', structure_type, object_id=obj_id)
        return q_slice[-1]

    def _get_value_from_parameter(
            self, structure_type, obj_id, parameter_name, **kwargs):
        """Select the method from parameter name and call the method.

        Additional kwargs can be passed on.
        """
        method = getattr(self, parameter_name)
        return tailored_args(method,
                             structure_type=structure_type,
                             obj_id=obj_id,
                             **kwargs)

    # Make NcStats have the same interface as NcStatsAgg
    get_value_from_parameter = _get_value_from_parameter

    def close(self):
        # TODO: is this used? also law of demeter
        self.datasource.ds.close()


class NcStatsAgg(NcStats):
    """A version of NcStats that works with the so called 'aggregation'
    version of the 3Di netCDF files."""

    # Update these lists if you add a new method
    AVAILABLE_STRUCTURE_PARAMETERS = ['q_cum', 'q_max', 'q_min'] + \
        NcStats.AVAILABLE_STRUCTURE_PARAMETERS
    AVAILABLE_MANHOLE_PARAMETERS = NcStats.AVAILABLE_MANHOLE_PARAMETERS + \
        ['wos_height', 's1_max', 'water_depth']
    AVAILABLE_PUMP_PARAMETERS = ['q_pump_cum'] \
        + NcStats.AVAILABLE_PUMP_PARAMETERS

    def __init__(self, *args, **kwargs):
        super(NcStatsAgg, self).__init__(*args, **kwargs)

        if (not isinstance(self.datasource, NetcdfDataSource) or
                self.datasource.ds_aggregation is None):
            raise ValueError("No aggration netcdf available in data source.")

        # Construct a dict with thing we actually have in the loaded netcdf,
        # and store netcdf arrays in memory.
        self.variables = dict()
        for p in (self.AVAILABLE_MANHOLE_PARAMETERS +
                  self.AVAILABLE_STRUCTURE_PARAMETERS +
                  self.AVAILABLE_PUMP_PARAMETERS):
            try:
                copied_array = self.datasource.ds_aggregation.variables[p][:]
                self.variables[p] = copied_array
            except KeyError:
                continue

        # Generate result statistics a priori
        for k, v in self.variables.items():
            if k.endswith('_cum'):
                # We can sum without integration because parameter is already
                # an integrated variable.
                calcd_array = v.sum(0)
            elif k.endswith('_min'):
                calcd_array = v.min(0)
            elif k.endswith('_max'):
                calcd_array = v.max(0)
            else:
                raise ValueError("Unknown variable")
            self.variables[k] = calcd_array
        self.variable_keys = self.variables.keys()

    def get_value_from_parameter(self, structure_type, obj_id,
                                 parameter_name, **kwargs):
        """Select array and get the value.

        Args:
            structure_type: raw layer name; structure type normalization,
                is delegated to the NetcdfDataSource
            obj_id: layer feature id?? -------------> TODO: needs checking!!!
            parameter_name: the netcdf variable name
            kwargs: unused, but needed to be compatible with NcStats
        """
        norm_object_type = normalized_object_type(structure_type)
        netcdf_id = self.datasource.obj_to_netcdf_id(obj_id, norm_object_type)
        if parameter_name in self.variable_keys:
            variable = self.variables[parameter_name]
            return variable[netcdf_id]
        else:
            log("This aggregation variable has no stats (%s), attempting "
                "lookup in regular NcStats." % parameter_name)
            # The variable was not found in aggregation netCDF. We will look
            # further down in the regular netCDF.
            variable = self._get_value_from_parameter(
                structure_type, obj_id, parameter_name, **kwargs)
            return variable

    def wos_height(self, structure_type, obj_id, surface_level=None):
        s1_max = self.get_value_from_parameter(
            structure_type, obj_id, 's1_max')
        return s1_max - surface_level

    def water_depth(self, structure_type, obj_id, bottom_level=None):
        s1_max = self.get_value_from_parameter(
            structure_type, obj_id, 's1_max')
        return s1_max - bottom_level
