"""
This code was basically copied from python-flow with modifications to make
it work with our own data sources.
"""
import numpy as np

from ..datasource.netcdf import NetcdfDataSource


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
        'tot_vol', 'q_max', 'cumulative_duration', 'q_end', 'tot_vol_positive',
        'tot_vol_negative', 'time_q_max']
    AVAILABLE_MANHOLE_PARAMETERS = ['s1_max']

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

        self.timesteps = self.datasource.timesteps
        self.timestamps = self.datasource.get_timestamps()

    def tot_vol(self, structure_type, obj_id):
        """Total volume through a structure. Structures are: pipes, weirs,
        orifices. So no pumps

        Note that the last element in q_slice is skipped (skipping the first
        element is another option, but not implemented here). Also note that q
        can be negative, so the absolute values are used.
        """
        q_slice = self.datasource.get_timeseries_values(
            structure_type, obj_id, ['q'])
        q_slice = np.absolute(q_slice)
        # calc total vol thru structure
        vols = self.timesteps * q_slice[0:-1]
        return vols.sum()

    def tot_vol_positive(self, structure_type, obj_id):
        """Total volume through structure, counting only positive q's."""
        q_slice = self.datasource.get_timeseries_values(
            structure_type, obj_id, ['q'])
        # mask negative values
        ma_q_slice = np.ma.masked_where(q_slice < 0, q_slice)
        # calc total vol thru structure
        vols = self.timesteps * ma_q_slice[0:-1]
        return vols.sum()

    def tot_vol_negative(self, structure_type, obj_id):
        """Total volume through structure, counting only negative q's."""
        q_slice = self.datasource.get_timeseries_values(
            structure_type, obj_id, ['q'])
        # mask positive values
        ma_q_slice = np.ma.masked_where(q_slice > 0, q_slice)
        # calc total vol thru structure
        vols = self.timesteps * ma_q_slice[0:-1]
        return vols.sum()

    def q_max(self, structure_type, obj_id):
        """Maximum value of a q timeseries; can be negative.
        """
        q_slice = self.datasource.get_timeseries_values(
            structure_type, obj_id, ['q'])
        _min = q_slice.min()
        _max = q_slice.max()
        # return highest absolute value, while retaining the sign of the number
        return max(_min, _max, key=abs)

    def time_q_max(self, structure_type, obj_id):
        """The time at maximum value of a q timeseries
        """
        q_slice = self.datasource.get_timeseries_values(
            structure_type, obj_id, ['q'])
        _min = q_slice.min()
        _max = q_slice.max()
        # return highest absolute value, while retaining the sign of the number
        largest = max(_min, _max, key=abs)
        (rows,) = np.where(q_slice == largest)
        return self.timestamps[rows[0]]

    def s1_max(self, structure_type, obj_id):
        """Maximum value of a s1 timeseries."""
        slice = self.datasource.get_timeseries_values(
            structure_type, obj_id, ['s1'])
        return slice.max()

    def cumulative_duration(self, structure_type, obj_id, threshold=None):
        """Cumulative duration of all nonzero occurences of q.
        """
        if threshold:
            # TODO: q values can be vary small, maybe add a threshold??
            raise NotImplementedError()
        q_slice = self.datasource.get_timeseries_values(
            structure_type, obj_id, ['q'])

        # normalize nonzero qs to 1, so it becomes a binary representation
        # of q, which we can simply multiply with the timesteps
        q_slice = np.absolute(q_slice)
        q_slice[q_slice > 0] = 1.
        cum_duration = self.timesteps * q_slice[0:-1]
        return cum_duration.sum()

    def q_end(self, structure_type, obj_id):
        """q at last timeSTAMP (!= timestep)
        """
        q_slice = self.datasource.get_timeseries_values(
            structure_type, obj_id, ['q'])
        return q_slice[-1]

    def close(self):
        # TODO: is this used? also law of demeter
        self.datasource.ds.close()
