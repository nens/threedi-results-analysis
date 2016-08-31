"""
This code was basically copied from python-flow with modifications to make
it work with our own data sources.
"""
import numpy as np
import inspect

from ..datasource.netcdf import NetcdfDataSource, normalized_object_type


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
        'q_max', 'q_cumulative_duration', 'q_end', 'tot_vol_positive',
        'tot_vol_negative', 'time_q_max']
    AVAILABLE_MANHOLE_PARAMETERS = ['s1_max', 'wos_duration']

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
            self.datasource = NetcdfDataSource(netcdf_file_path)
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

    def get_value_from_parameter(
            self, structure_type, obj_id, parameter_name, **kwargs):
        """Select the method from parameter name and call the method.

        Additional kwargs can be passed on.
        """
        method = getattr(self, parameter_name)
        return tailored_args(method,
                             structure_type=structure_type,
                             obj_id=obj_id,
                             **kwargs)

    def close(self):
        # TODO: is this used? also law of demeter
        self.datasource.ds.close()


class NcStatsAgg(NcStats):
    """A version of NcStats that works with the so called 'aggregation'
    version of the 3Di netCDF files."""

    # Update these lists if you add a new method
    AVAILABLE_STRUCTURE_PARAMETERS = ['q_cum', 'q_max', 'q_min']
    AVAILABLE_MANHOLE_PARAMETERS = ['s1_max']

    def __init__(self, *args, **kwargs):
        super(NcStatsAgg, self).__init__(*args, **kwargs)
        self.ds_agg = self.datasource.ds_aggregation

        # Construct a dict with thing we actually have in the loaded netcdf,
        # and store netcdf arrays in memory.
        self.variables = dict()
        for p in (self.AVAILABLE_MANHOLE_PARAMETERS +
                  self.AVAILABLE_STRUCTURE_PARAMETERS):
            try:
                copied_array = self.ds_agg.variables[p][:]
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
        if 'pump' in structure_type:
            # TODO: fix this
            raise NotImplementedError(
                "Some things don't work for pumps yet using the "
                "aggregated netCDF")
        norm_object_type = normalized_object_type(structure_type)
        netcdf_id = self.datasource.obj_to_netcdf_id(obj_id, norm_object_type)
        try:
            variable = self.variables[parameter_name]
            return variable[netcdf_id]
        except KeyError:
            print("This aggregation variable has no stats (%s), attempting "
                  "lookup in regular NcStats." % parameter_name)
            # The variable was not found in aggregation netCDF. We will look
            # further down in the regular netCDF.
            variable = super(NcStatsAgg, self).get_value_from_parameter(
                structure_type, obj_id, parameter_name, **kwargs)
            return variable
