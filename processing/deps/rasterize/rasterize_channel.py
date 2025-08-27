# TODO error when channels (in .fill_wedge()) or
#  cross-section locations (in .split() or .make_valid()) do not have id.

from enum import Enum
from typing import Iterator, List, Union, Set, Sequence, Tuple

import numpy as np
from shapely import wkt, set_precision, MultiPoint
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Point, Polygon
from shapely.ops import unary_union, linemerge, nearest_points, transform


# Shapely method "offset_curve" docs: The side is determined by the sign of the distance parameter
# (negative for right side offset, positive for left side offset). Left and right are determined by following
# the direction of the given geometric points of the LineString.
RIGHT = -1
LEFT = 1

LEFT_LEFT = 2
RIGHT_RIGHT = -2

VERTEX_LIMIT = 50000


class SupportedShape(Enum):
    TABULATED_RECTANGLE = 5
    TABULATED_TRAPEZIUM = 6
    YZ = 7


def index_of_vertex(line: LineString, vertex: Point, grid_size: float = 0.000001):
    for i, vertex_coords in enumerate(line.coords):
        line_vertex = set_precision(Point(vertex_coords), grid_size=grid_size)
        vertex = set_precision(vertex, grid_size=grid_size)
        if line_vertex.intersects(vertex):
            return i


def is_monotonically_increasing(a: np.array, equal_allowed=False):
    if equal_allowed:
        return np.all(a[1:] >= a[0:-1])
    return np.all(a[1:] > a[0:-1])


def is_left_of_line(point: Point, line: LineString) -> Union[bool, None]:
    """
    Is ``point`` to the left of ``line``?

    Returns None if ``point`` intersects ``line``

    Based on:
    https://stackoverflow.com/questions/1560492/how-to-tell-whether-a-point-is-to-the-right-or-left-side-of-a-line

    :param point: the Point to analyse
    :param line: LineString with 2 vertices
    """
    assert len(line.coords) == 2
    if point.intersects(line):
        return None
    start, end = [Point(coord) for coord in line.coords]
    return (
        (end.x - start.x) * (point.y - start.y)
        - (end.y - start.y) * (point.x - start.x)
    ) > 0


def parse_cross_section_table(
        table: str,
        cross_section_shape: int,
        wall_displacement: float = 0
) -> Tuple[np.array, np.array]:
    """
    Returns [y_ordinates], [z_ordinates]
    """
    if cross_section_shape in (SupportedShape.TABULATED_RECTANGLE.value, SupportedShape.TABULATED_TRAPEZIUM.value):
        heights = list()
        widths = list()
        for row in table.split("\n"):
            height, width = row.split(",")
            if len(heights) == 0:
                # first pass
                heights.append(float(height))
                widths.append(float(width))
            else:
                if float(width) < widths[-1]:
                    raise WidthsNotIncreasingError
                if cross_section_shape == SupportedShape.TABULATED_RECTANGLE.value:
                    # add extra height/width entry to convert tabulated rectangle to tabulated trapezium
                    # but only if width is different from previous width
                    if float(width) > widths[-1]:
                        heights.append(float(height))
                        widths.append(float(widths[-1]))
                heights.append(float(height))
                widths.append(float(width))
        # convert to YZ
        if widths[0] == 0:  # do not duplicate middle y value if it is 0
            y_ordinates = np.hstack([np.flip(widths)/-2, np.array(widths)[1:]/2])
            z_ordinates = np.hstack([np.flip(heights), np.array(heights)[1:]])
        else:
            y_ordinates = np.hstack([np.flip(widths)/-2, np.array(widths)/2])
            z_ordinates = np.hstack([np.flip(heights), heights])
        y_ordinates += np.max(widths)/2
    elif cross_section_shape == SupportedShape.YZ.value:
        y_list = list()
        z_list = list()
        for row in table.split("\n"):
            y, z = row.split(",")
            y_list.append(float(y))
            z_list.append(float(z))
        y_ordinates = np.array(y_list)
        z_ordinates = np.array(z_list)
        if not is_monotonically_increasing(y_ordinates, equal_allowed=True):
            # equal Y is allowed, will be fixed with wall displacement
            raise YNotIncreasingError

    else:
        raise ValueError(f"Unsupported cross_section_shape {cross_section_shape}")

    # apply wall displacement to vertical segments
    if wall_displacement > 0:
        while not is_monotonically_increasing(y_ordinates):
            y_ordinates[1:][y_ordinates[1:] == y_ordinates[:-1]] += wall_displacement
            # remove YZ coordinates that have been 'taken over' by the previous ones due to wall displacement
            valid_ordinates = y_ordinates[1:] >= y_ordinates[:-1]
            while np.sum(np.invert(valid_ordinates)) > 0:
                valid_ordinates = y_ordinates[1:] >= y_ordinates[:-1]
                valid_mask = np.hstack([np.array([True]), valid_ordinates])
                y_ordinates = y_ordinates[valid_mask]
                z_ordinates = z_ordinates[valid_mask]
    elif not is_monotonically_increasing(y_ordinates):
        raise YNotIncreasingError("Could not make this cross-section valid. Use a wall_displacement > 0")
    return y_ordinates, z_ordinates


def simplify(y_ordinates: np.array, z_ordinates: np.array, tolerance: float) -> Tuple[np.array, np.array]:
    """
    Simplify a YZ cross-section using shapely LineString.simplify()
    """
    linestring = LineString(np.stack([y_ordinates, z_ordinates], axis=1))
    simplified_linestring = linestring.simplify(tolerance)
    coord_array = simplified_linestring.coords.xy
    y_ordinates, z_ordinates = np.array(coord_array)
    return y_ordinates, z_ordinates


def offset_curve_fixed(line: LineString, distance: float):
    """
    Shapely offset_curve, but with a fix. With Shapely 2.0.2 and GEOS 3.12.0, some offset curves are
    MultiLineStrings even though they can be linemerged into a LineString
    """
    result = line if -0.001 < distance < 0.001 else line.offset_curve(distance=distance)
    result = linemerge(result) if isinstance(result, MultiLineString) else result
    return result


def reverse(geom):
    """
    Source: https://gis.stackexchange.com/questions/415864/how-do-you-flip-invert-reverse-the-order-of-the-
    coordinates-of-shapely-geometrie
    """

    def _reverse(x, y, z=None):
        if z:
            return x[::-1], y[::-1], z[::-1]
        return x[::-1], y[::-1]

    return transform(_reverse, geom)


def variable_buffer(linestring: LineString, radii: Sequence[float], shifts: Sequence[float] = None) -> Polygon:
    """
    Create a buffer around a Linestring, for which the buffer distance varies per vertex
    By default, the buffer is symmetrical. This can be varied by specifying the ``shifts``

    :param linestring: line to be buffered
    :param radii: buffer distance per vertex (must be >= 0
    :param shifts: shift of the center of the buffer. right = negative, left = positive
    """
    assert len(linestring.coords) == len(radii)
    assert np.all(np.array(radii) >= 0)
    vertices = [Point(coord) for coord in linestring.coords]
    if shifts is not None:
        # shift each vertex onto the offset_curve with given shift
        shifts = np.array(shifts)
        shifts[np.logical_and(-0.001 < shifts, shifts < 0.001)] = 0  # if shift is too close to 0, offset_curve()
                                                                     # produces a GEOSException in some cases
        vertices = [
            nearest_points(offset_curve_fixed(linestring, shifts[i]), vertices[i])[0]
            for i, coord in enumerate(linestring.coords)
        ]
    buffered_points = [
        v.buffer(radii[i]) for i, v in enumerate(vertices)
    ]
    convex_hulls = [
        MultiPolygon([buffered_points[i], buffered_points[i + 1]]).convex_hull
        for i in range(len(buffered_points) - 1)
    ]
    result = unary_union(convex_hulls)
    return result


def is_valid_offset(line, offset):
    po = offset_curve_fixed(line, offset)
    if po.is_empty:
        return False
    if type(po) != LineString:
        return False
    return True


def highest_valid_index_single_offset(line: LineString, offset: float) -> int:
    """
    Returns index of the vertex at which to split ``line`` in a (first) part for which a valid offset_curve can be made
    at given ``offset`` and a (second) part, i.e. the rest of ``line``
    """
    vertex_positions = [line.project(Point(vertex)) for vertex in line.coords]
    highest_valid_idx = 1
    lowest_invalid_idx = len(vertex_positions) - 1
    current_idx = len(vertex_positions) - 1
    while lowest_invalid_idx - highest_valid_idx > 1:
        test_line = LineString([(Point(vertex)) for vertex in line.coords[:current_idx + 1]])
        if is_valid_offset(test_line, offset):
            highest_valid_idx = current_idx
        else:
            lowest_invalid_idx = current_idx
        current_idx = int(highest_valid_idx + (lowest_invalid_idx-highest_valid_idx)/2)
    return highest_valid_idx


def highest_valid_index(line: LineString, offsets: Sequence[float]) -> int:
    """
    For some LineStrings, it is not possible to generate valid offsets at all required offset distances.
    If such a LineString is split into smaller parts, it becomes possible to generate valid offsets for all
    these parts.

    The segment of the line that runs from vertex 0 to vertex n is the longest segment for which it is
    possible to generate valid offsets at all required offset distances. ``n`` is the "highest valid index" as returned
    by this function.
    """
    offsets = list(offsets)  # allow numpy array as type of ``offsets``
    offsets.sort(key=lambda x: -1 * abs(x))  # largest offsets first, because will probably result in the lowest index
    minimum_idx = len(line.coords) - 1
    for offset in offsets:
        line = LineString([(Point(vertex)) for vertex in line.coords[:minimum_idx + 1]])
        minimum_idx = min(minimum_idx, highest_valid_index_single_offset(line, offset))
    return minimum_idx


class EmptyOffsetError(ValueError):
    """Raised when the parallel offset at given offset distance results in an empty geometry"""
    # TODO Remove


class InvalidOffsetError(ValueError):
    """Raised when the parallel offset at given offset distance results in a geometry that is not a LineString"""
    # TODO Remove


class WedgeFillPointsAlreadySetError(ValueError):
    """Raised when it is attempted to set a channel's _wedge_fill_points that have already been set"""


class WidthsNotIncreasingError(ValueError):
    """Raised when one a width of a tabular cross-section < than the previous width of that crosssection"""
    # TODO Check if this can be removed


class MinYNotZeroError(ValueError):
    """"Raised when a YZ cross-section's lowest value is not 0"""


class YNotIncreasingError(ValueError):
    """Raised when one a Y value of a YZ cross-section <= than the previous Y of that crosssection"""


class NoCrossSectionLocationsError(ValueError):
    """Raised when attempting to generate parallel offsets for a channel that has no cross-section locations"""


class IntersectingSidesError(ValueError):
    """"Raised when the two lines between which triangulate_between() tries to triangulate"""


class TriangulationError(ValueError):
    """
    Raised when triangulation fails

    The attribute ``locations`` is a list of points located at the last position where valid triangulation was still
    possible
    """
    def __init__(self, *args, locations: List['IndexedPoint']):
        super().__init__(*args)
        self.locations: List['IndexedPoint'] = locations


class IndexedPoint:
    def __init__(self, *args, index: int):
        self.geom: Point = Point(*args)  # since shapely 2.0, it is no longer possible to add any custom attributes
                                         # to a Point, so it is impossible to inherit all from Point and add index
        self.index = index

    @property
    def x(self):
        return self.geom.x

    @property
    def y(self):
        return self.geom.y

    @property
    def z(self):
        return self.geom.z


class Triangle:
    def __init__(self, points: List[IndexedPoint]):
        self.points: List[IndexedPoint] = points

    @property
    def vertex_indices(self) -> List[int]:
        return [point.index for point in self.points]

    @property
    def sides(self) -> Set[Tuple[int, ...]]:
        """Returns a set of tuples, where each tuple is a sorted pair of vertex indices describing a triangle's side"""
        idx = self.vertex_indices
        return {
            tuple(sorted(idx[0:2])),
            tuple(sorted(idx[1:3])),
            tuple(sorted([idx[2], idx[0]])),
        }

    @property
    def geometry(self) -> Polygon:
        return Polygon(LineString([point.geom for point in self.points]))

    def are_sides_shared(self, line: LineString) -> Tuple[List[LineString], List[LineString]]:
        """Return the sides of the Triangle that are within ``line``, and the sides that are not"""
        yes = []
        no = []
        coords = self.geometry.exterior.coords
        segments = [LineString([coords[i - 1], coords[i]]) for i in range(1, len(coords))]
        for segment in segments:
            if segment.within(line):
                yes.append(segment)
            else:
                no.append(segment)
        return yes, no

    def is_between(self, left_side_line: Union[Point, LineString], right_side_line: Union[Point, LineString]):
        # case 0: one or both of the lines are a Point
        if isinstance(left_side_line, Point) or isinstance(right_side_line, Point):
            return True

        # case 1: one side of the triangle crosses one of the sides
        for start, end in [(0, 1), (0, 2), (1, 2)]:
            line = LineString([self.points[start].geom, self.points[end].geom])
            if line.crosses(left_side_line) or line.crosses(right_side_line):
                return False

        # case 2: one or more sides of the triangle are shared with one of the side lines
        shared_sides_left, non_shared_sides_left = self.are_sides_shared(left_side_line)
        shared_sides_right, non_shared_sides_right = self.are_sides_shared(right_side_line)

        # case 2.1: one side of the triangle are within one of the sides
        # --- the point opposite the shared side has to touch the other line
        if len(shared_sides_left) + len(shared_sides_right) == 1:
            # note: crosses() and touches() are mutually exclusive
            if len(shared_sides_left) == 1:
                result = any(side.touches(right_side_line) for side in non_shared_sides_left)
                return result
            if len(shared_sides_right) == 1:
                result = any(side.touches(left_side_line) for side in non_shared_sides_right)
                return result

        # case 2.2: two sides of the triangle are within one of the sides
        if len(shared_sides_left) == 2:
            check_point = non_shared_sides_left[0].interpolate(distance=0.5, normalized=True)
            return is_left_of_line(check_point, shared_sides_left[0]) is False and \
                is_left_of_line(check_point, shared_sides_left[0]) is False

        elif len(shared_sides_right) == 2:
            check_point = non_shared_sides_right[0].interpolate(distance=0.5, normalized=True)
            return is_left_of_line(check_point, shared_sides_right[0]) and \
                is_left_of_line(check_point, shared_sides_right[0])


class CrossSectionLocation:
    def __init__(
        self,
        id: int,
        reference_level: float,
        bank_level: float,
        y_ordinates: np.array,
        z_ordinates: np.array,
        geometry: Point,
        parent=None,
    ):
        """
        Note: adds reference level to z_ordinates

        :param reference_level:
        :param bank_level:
        :param y_ordinates: Use ``parse_cross_section_table`` to convert tabulated to yz
        :param z_ordinates: Use ``parse_cross_section_table`` to convert tabulated to yz. Input has 0 as lowest z.
        :param geometry:
        :param parent:
        """
        if not np.min(y_ordinates) == 0:
            raise MinYNotZeroError
        if not is_monotonically_increasing(y_ordinates):
            raise YNotIncreasingError

        self.id = id
        self.reference_level = reference_level
        self.bank_level = bank_level
        self.y_ordinates = y_ordinates
        self.z_ordinates = z_ordinates + reference_level
        self.geometry = geometry
        self.parent = parent

    @classmethod
    def from_qgs_feature(cls, feature, wall_displacement: float, simplify_tolerance: float):
        """
        wall_displacement is used as simplify tolerance for the cross-section. remaining vertical segments are made
        diagonal by displacing the top or bottom by wall_displacement
        """
        qgs_geometry = feature.geometry()
        wkt_geometry = qgs_geometry.asWkt()
        shapely_geometry = wkt.loads(wkt_geometry)
        id = feature.attribute("id")
        cross_section_shape = feature.attribute("cross_section_shape")
        table = feature.attribute("cross_section_table")
        y, z = parse_cross_section_table(
            table=table,
            cross_section_shape=cross_section_shape,
            wall_displacement=wall_displacement
        )
        y, z = simplify(y, z, tolerance=simplify_tolerance)

        return cls(
            id=id,
            geometry=shapely_geometry,
            reference_level=feature.attribute("reference_level"),
            bank_level=feature.attribute("bank_level"),
            y_ordinates=y,
            z_ordinates=z,
        )

    @classmethod
    def clone(cls, source: 'CrossSectionLocation') -> 'CrossSectionLocation':
        clone = cls(
            id=source.id,
            reference_level=source.reference_level,
            bank_level=source.bank_level,
            y_ordinates=source.y_ordinates,
            z_ordinates=source.z_ordinates - source.reference_level,
            geometry=source.geometry,
            parent=source.parent,
        )
        clone._position_normalized = source._position_normalized
        return clone

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: 'Channel'):
        """
        Set the parent of this CrossSectionLocation
        Also calculates the normalized position of the CrossSectionLocation along the channel
        """
        self._parent = parent
        self._position_normalized = None if parent is None else \
            self.parent.geometry.project(self.geometry, normalized=True)

    @property
    def position(self):
        """
        Return the position along the parent Channel, in m from the start of the channel.

        This position is calculated from the normalized position on the parent Channel's original geometry, i.e. the
        geometry the Channel had when it was assigned as parent to this CrossSectionLocation.

        This allows a ``simplify()`` of the Channel's geometry without messing up the intersections with its
        CrossSectionLocations
        """
        return self._position_normalized * self.parent.geometry.length

    @property
    def max_width(self):
        return np.max(self.y_ordinates)

    @property
    def thalweg_y(self):
        """Returns distance between the start of the cross-section at the left bank and the lowest point of the
        cross-section. The thalweg is located at the average y index of all points with the minimum z value"""
        z0_indices = np.where(self.z_ordinates == np.min(self.z_ordinates))[0]
        average_z0_index = np.average(z0_indices)
        if int(average_z0_index) == average_z0_index:
            return self.y_ordinates[int(average_z0_index)]
        else:
            # linear interpolation between y before and y after, only using y's where z=min(z)
            z0_index_before = z0_indices[z0_indices < average_z0_index][-1]
            z0_index_after = z0_indices[z0_indices > average_z0_index][0]
            y_before = self.y_ordinates[z0_index_before]
            y_after = self.y_ordinates[z0_index_after]
            return y_before + ((average_z0_index-z0_index_before)/(z0_index_after-z0_index_before))*(y_after-y_before)

    @property
    def offsets(self):
        """
        Return array of y_ordinates, but relative to the thalweg
        and using the shapely offset_curve logic of right = negative and left is positive
        """
        return self.thalweg_y - self.y_ordinates

    def z_at(self, offset: float) -> float:
        """Get interpolated z at given offset"""

        # offsets and z_ordinates are flipped ([::-1]) because offsets must be monotonically increasing, but is
        # monotonically decreasing due to the shapely offset_curve right = -1 and left = +1 logic
        return np.interp(offset, self.offsets[::-1], self.z_ordinates[::-1])


class Channel:
    """
    id is a tuple of two ints. The first int is the original channel id. The second int is the segment index. Some
    channels need to be cut into smaller segments in order to generate valid offset curves and triangulations for them.
    in such a case, these segments will have ids (23, 0), (23, 1), (23, 3) etc., where 23 is the original channel id

    The same system is applied to connection node ids
    """
    def __init__(
        self,
        id: Union[int, Tuple[int, int]],
        connection_node_id_start: Union[int, Tuple[int, int], None],
        connection_node_id_end: Union[int, Tuple[int, int], None],
        geometry: LineString,
    ):
        self.id = id if type(id) == tuple else (id, 0)
        self.connection_node_id_start = connection_node_id_start \
            if (type(connection_node_id_start) == tuple) \
            else (connection_node_id_start, 0)
        self.connection_node_id_end = connection_node_id_end \
            if (type(connection_node_id_end) == tuple) \
            else (connection_node_id_end, 0)
        self.cross_section_locations: List[CrossSectionLocation] = []
        self.geometry: LineString = geometry
        self.parallel_offsets: List[ParallelOffset] = []
        self._parallel_offset_triangles = []
        self._wedge_fill_points = []
        self._wedge_fill_triangles = []
        self._extra_outline = []

    @classmethod
    def from_qgs_feature(cls, feature):
        qgs_geometry = feature.geometry()
        wkt_geometry = qgs_geometry.asWkt()
        shapely_geometry = wkt.loads(wkt_geometry)
        start_id = feature.attribute("connection_node_id_start")
        end_id = feature.attribute("connection_node_id_end")
        id = feature.attribute("id")
        return cls(
            geometry=shapely_geometry,
            connection_node_id_start=start_id,
            connection_node_id_end=end_id,
            id=id,
        )

    @property
    def max_widths(self) -> np.array:
        """Array describing the max crosssectional width along the channel"""
        return np.array([x.max_width for x in self.cross_section_locations])

    @property
    def thalweg_ys(self) -> np.array:
        """Array of y ordinates of the thalweg of each cross-section location along the channel"""
        return np.array([x.thalweg_y for x in self.cross_section_locations])

    @property
    def unique_offsets(self) -> np.array:
        """
        Unique offsets for entire channel, see ``CrossSectionLocation.offsets`` documentation
        Offsets are rounded to mm before selecting unique values
        """
        if len(self.cross_section_locations) == 0:
            raise NoCrossSectionLocationsError("Channel has no cross-section locations")
        offsets_list = [xsec.offsets for xsec in self.cross_section_locations]
        all_offsets_array = np.hstack(offsets_list)
        result = np.unique((1000*np.round(all_offsets_array, 3)).astype(int))/1000
        return result

    @property
    def cross_section_location_positions(self) -> np.array:
        """Array of cross-section location positions along the channel"""
        return np.array([x.position for x in self.cross_section_locations])

    @property
    def vertex_positions(self) -> np.array:
        """Array of channel vertex positions along the channel"""
        result_list = [
            self.geometry.project(Point(vertex)) for vertex in self.geometry.coords
        ]
        result_array = np.array(result_list)
        return result_array

    @property
    def last_index(self) -> int:
        """
        Return the highest index of the channel's ``IndexedPoint``s
        """
        po_points_last_index = self.parallel_offsets[-1].vertex_indices[-1] if self.parallel_offsets else -1
        wedge_fill_points_last_index = self._wedge_fill_points[-1].index if self._wedge_fill_points else -1
        result = np.max([po_points_last_index, wedge_fill_points_last_index])
        return result


    @property
    def outline(self) -> Polygon:
        """
        Generate a polygon that describes the extent of the rasterized channel
        """
        radii = np.array([self.max_width_at(position) / 2 for position in self.vertex_positions])
        thalweg_ys = np.array([self.thalweg_y_at(position) for position in self.vertex_positions])
        shifts = (radii - thalweg_ys) * -1
        result = variable_buffer(linestring=self.geometry, radii=radii, shifts=shifts)

        # add extra outline generated by self.fill_wedge()
        for extra in self._extra_outline:
            result = result.union(extra)
        return result

    def add_cross_section_location(self, cross_section_location: CrossSectionLocation):
        """
        Become the parent of the cross-section location.
        Inserts ``cross_section_location`` in the list of the channel's cross-section locations ordered by their
        position
        """
        cross_section_location.parent = self
        self.cross_section_locations.append(cross_section_location)
        self.cross_section_locations.sort(key=lambda x: x.position)

    def cross_section_location_index(self, id: int):
        """
        Get the index of the CrossSectionLocation with given ``id``
        Returns None if no CrossSectionLocation with that id is found
        """
        for i, xsec in enumerate(self.cross_section_locations):
            if xsec.id == id:
                return i

    def max_width_at(self, position: float) -> float:
        """Interpolated max cross-sectional width at given position along the channel"""
        return np.interp(
            position, self.cross_section_location_positions, self.max_widths
        )

    def thalweg_y_at(self, position: float) -> float:
        """
        Interpolated y ordinate of thalweg at given position along the channel
        """
        return np.interp(
            position, self.cross_section_location_positions, self.thalweg_ys
        )

    def simplify(self, tolerance):
        """
        Simplify the Channel's geometry, without removing the vertices at cross-section locations
        """
        simplified_geometry = self.geometry.simplify(tolerance)
        vertices = [Point(x, y) for x, y in simplified_geometry.coords]
        positions = [simplified_geometry.project(vertex) for vertex in vertices]
        cross_section_points = [
            simplified_geometry.interpolate(xsec_pos) for xsec_pos in self.cross_section_location_positions
        ]
        pos_vertex_dict = dict(zip(positions, vertices))
        pos_cross_section_dict = dict(zip(self.cross_section_location_positions, cross_section_points))
        pos_vertex_dict.update(pos_cross_section_dict)
        self.geometry = LineString([vertex for pos, vertex in sorted(pos_vertex_dict.items())])

    def generate_parallel_offsets(self, offset_0: bool = False):
        """
        Generate a set of lines parallel to the input linestring, at both sides of the line
        Offsets are sorted from ``LEFT`` to ``RIGHT``

        :param offset_0: guarantee an offset at 0, even if this does not occur in the channel's ``unique_offsets``
        """
        self._parallel_offset_triangles = []
        self._wedge_fill_points = []
        self._wedge_fill_triangles = []
        self._extra_outline = []
        # offsets are sorted from left to right
        offsets = sorted(list(set(self.unique_offsets) | {0}), reverse=RIGHT == -1) if offset_0 else self.unique_offsets
        self.parallel_offsets = [ParallelOffset(parent=self, offset_distance=offset) for offset in offsets]

        last_vertex_index = -1
        # -1 so that we have 0-based indexing, because QgsMesh vertices have 0-based indices too
        for po in self.parallel_offsets:
            po.set_vertex_indices(first_vertex_index=last_vertex_index + 1)
            last_vertex_index = po.vertex_indices[-1]

    def parallel_offset_at(self, offset_distance):
        """
        Find the ParallelOffset at given ``offset_distance``
        """
        if offset_distance not in self.unique_offsets:
            raise ValueError(
                f"Parallel offset not found at offset distance {offset_distance}. "
                f"Channel between nodes {self.connection_node_id_start} and "
                f"{self.connection_node_id_end}. Available offset distances: {self.unique_offsets}"
            )
        for po in self.parallel_offsets:
            if po.offset_distance == offset_distance:
                return po
        raise ValueError(
            f"Parallel offset not found at offset distance {offset_distance}. "
            f"Channel between nodes {self.connection_node_id_start} and "
            f"{self.connection_node_id_end}. Available offset distances: {self.unique_offsets}"
        )

    @property
    def points(self):
        """
        Returns all points of all parallel offsets ordered by vertex index
        """
        all_points = []
        for po in self.parallel_offsets:
            all_points += po.points
        all_points += self._wedge_fill_points
        all_points.sort(key=lambda x: x.index)
        assert len(all_points) -1 == all_points[-1].index
        return all_points

    @staticmethod
    def add_to_triangle_sort(
        triangle: Triangle,
        processed_sides: Set[Tuple],
        sorted_triangles: List[Triangle],
    ) -> bool:
        """
        Adds the triangle to `sorted_triangles` if at least one of its sides is already present in `processed_sides`
        Returns True if adding was successful, False if not
        """
        if len(triangle.sides & processed_sides):
            # at least one of the sides of the new triangle has already been processed
            sorted_triangles.append(triangle)
            processed_sides.update(triangle.sides)
            return True
        else:
            return False

    @property
    def triangles(self) -> List[Triangle]:
        """
        Returns a list of Triangles, sorted in such a way that each triangle shares at least one side with a
        preceding triangle in the list. If this is not possible, the resulting list may contain several sections to
        which this requirement applies, but not between the sections.

        Will only return triangles if ``fill_parallel_offsets`` and/or ``fill_wedge()`` have been called first.
        """
        triangles = self._parallel_offset_triangles + self._wedge_fill_triangles

        if not len(triangles) > 0:
            raise RuntimeError("Call fill_parallel_offsets() or fill_wedge() before using triangles().")

        # sort
        processed_sides = triangles[0].sides
        sorted_triangles = [triangles[0]]

        while len(sorted_triangles) < len(triangles):
            failed_triangles = []
            for triangle in triangles[1:]:
                # handle next triangle from the original list
                if not self.add_to_triangle_sort(
                    triangle, processed_sides, sorted_triangles
                ):
                    failed_triangles.append(triangle)

                # handle failed triangles from previous run(s)
                triangle_added = True
                while triangle_added:
                    before_count = len(sorted_triangles)
                    failed_triangles = [
                        ft
                        for ft in failed_triangles
                        if not self.add_to_triangle_sort(
                            ft, processed_sides, sorted_triangles
                        )
                    ]
                    triangle_added = len(sorted_triangles) > before_count
            if failed_triangles:
                # force first failed triangle in the sorted list and continue while loop
                sorted_triangles.append(failed_triangles[0])
                processed_sides.update(failed_triangles[0].sides)
                triangles = failed_triangles[1:]

        return sorted_triangles

    def find_vertex(self, connection_node_id: int, n: int) -> Point:
        """
        Starting from the given connection node, find the nth vertex
        """
        if connection_node_id == self.connection_node_id_start:
            return Point(self.geometry.coords[n])
        elif connection_node_id == self.connection_node_id_end:
            return Point(self.geometry.coords[-(n + 1)])
        else:
            raise ValueError(
                f"connection_node_id {connection_node_id} is not a start or end connection node of this "
                f"channel"
            )

    def azimuth_at(self, connection_node_id: Tuple[int, int]) -> float:
        """
        Return the azimuth of the segment of the channel's geometry that links to given connection node
        """
        connection_node_geometry = self.find_vertex(connection_node_id, 0)
        second_point = self.find_vertex(connection_node_id, 1)
        return azimuth(connection_node_geometry, second_point)

    def fill_parallel_offsets(self):
        """
        Triangulate between all parallel offsets
        """
        self._parallel_offset_triangles = []
        for i in range(len(self.parallel_offsets) - 1):
            for tri in self.parallel_offsets[i].triangulate(self.parallel_offsets[i + 1]):
                self._parallel_offset_triangles.append(tri)

    def fill_wedge(self, other: 'Channel'):
        """
        Add points and triangles to fill the wedge-shaped gap between self and other. Also updates self.outline
        """

        # Find out if and how self and other_channel are connected
        # head of `self` connects to tail of `other` | -->-->
        # wedge is added to `self`
        if self.connection_node_id_end == other.connection_node_id_start:
            channel_to_update = self
            channel_to_update_idx = -1  # end
            if ccw_angle(self, other) > 180:
                channel_to_update_side = RIGHT
                wedge_fill_points_source_side = RIGHT
            else:
                channel_to_update_side = LEFT
                wedge_fill_points_source_side = LEFT
            wedge_fill_points_source = other
            wedge_fill_points_source_idx = 0  # start

        # head of `self` connects to head of `other` | --><--
        # wedge is added to `self`
        elif self.connection_node_id_end == other.connection_node_id_end:
            channel_to_update = self
            channel_to_update_idx = -1  # end
            if ccw_angle(self, other) > 180:
                channel_to_update_side = RIGHT
                wedge_fill_points_source_side = LEFT
            else:
                channel_to_update_side = LEFT
                wedge_fill_points_source_side = RIGHT
            wedge_fill_points_source = other
            wedge_fill_points_source_idx = -1  # end

        # tail of `self` connects to tail of `other` | <---->
        # wedge is added to `self`
        elif self.connection_node_id_start == other.connection_node_id_start:
            channel_to_update = self
            channel_to_update_idx = 0  # start
            if ccw_angle(self, other) > 180:
                channel_to_update_side = LEFT
                wedge_fill_points_source_side = RIGHT
            else:
                channel_to_update_side = RIGHT
                wedge_fill_points_source_side = LEFT
            wedge_fill_points_source = other
            wedge_fill_points_source_idx = 0  # start

        # tail of `self` is connected to head of `other` | <--<--
        # wedge is connected to `other`
        elif self.connection_node_id_start == other.connection_node_id_end:
            channel_to_update = other
            channel_to_update_idx = -1  # end
            wedge_fill_points_source = self
            wedge_fill_points_source_idx = 0  # start
            if ccw_angle(self, other) > 180:
                channel_to_update_side = LEFT
                wedge_fill_points_source_side = LEFT
            else:
                channel_to_update_side = RIGHT
                wedge_fill_points_source_side = RIGHT

        # channels are not connected | -->          -->
        else:
            raise ValueError("Channels are not connected")

        # Regenerate parallel offsets if offset 0 is not included
        if 0 not in channel_to_update.unique_offsets:
            channel_to_update.generate_parallel_offsets(offset_0=True)
            channel_to_update.fill_parallel_offsets()

        channel_to_update_offsets = []
        channel_to_update_points = []

        # add points from `channel_to_update`, including the 0 point
        # sort on abs(offset_distance) to make sure we always go from the middle to the outside
        for po in sorted(channel_to_update.parallel_offsets, key=lambda x: np.abs(x.offset_distance)):
            if po.offset_distance * channel_to_update_side >= 0:
                channel_to_update_offsets.append(po.offset_distance)
                channel_to_update_points.append(po.points[channel_to_update_idx])

        # Append start or end vertices of all other_channel's parallel offsets to self._wedge_fill_points
        # left is positive, right is negative

        # add points from the other channel (`wedge_fill_points_source`)
        wedge_fill_points = []
        wedge_fill_points_source_offsets = []
        last_index = channel_to_update.last_index
        # sort on abs(offset_distance) to make sure we always go from the middle to the outside
        for po in sorted(wedge_fill_points_source.parallel_offsets, key=lambda x: np.abs(x.offset_distance)):
            if po.offset_distance * wedge_fill_points_source_side > 0:
                wedge_fill_points_source_offsets.append(po.offset_distance)
                existing_point = po.points[wedge_fill_points_source_idx]
                wedge_fill_points.append(
                    IndexedPoint(
                        existing_point.geom, index=last_index + 1
                    )
                )
                last_index += 1

        # Generate triangles to connect the added points to the existing points
        for triangle in triangulate_between(
            left_side_points=channel_to_update_points,
            right_side_points=wedge_fill_points,
        ):
            channel_to_update._wedge_fill_triangles.append(triangle)

        # Add wedge fill points
        channel_to_update._wedge_fill_points += wedge_fill_points

        # test that point indices are unique
        point_indices = [point.index for point in channel_to_update.points]
        assert len(set(point_indices)) == len(point_indices)
        # Create extra outline buffer for the wedge
        extra_point = Point(
            wedge_fill_points_source.geometry.coords[wedge_fill_points_source_idx]
        )
        position = (
            0
            if wedge_fill_points_source_idx == 0
            else wedge_fill_points_source.geometry.length
        )
        width_at_extra_point = wedge_fill_points_source.max_width_at(position)
        thalweg_y_at_extra_point = wedge_fill_points_source.thalweg_y_at(position)
        shift = -1 * ((width_at_extra_point/2) - thalweg_y_at_extra_point)
        extra_point_shifted = nearest_points(
            offset_curve_fixed(wedge_fill_points_source.geometry, shift),
            extra_point
        )[0]
        channel_to_update._extra_outline.append(extra_point_shifted.buffer(width_at_extra_point / 2))

    def as_query(self) -> str:
        selects = []
        for i, tri in enumerate(self.triangles):
            selects.append(
                f"SELECT {i + 1} as id, geom_from_wkt('{str(tri.geometry.wkt)}') as geom /*:polygon:28992*/"
            )
        return "\nUNION\n".join(selects)

    def split(self, vertex_index: int) -> Union[Tuple['Channel', 'Channel'], Tuple['Channel', None]]:
        """
        Split this Channel in two Channels at given ``vertex_index``
        Both channels will include the first cross-section location beyond the split point

        The channel id tuple's first value will always be the original channel id; the second value will be incremented
        by 1 for the last half. So (23, 0) becomes ((23, 0), (23, 1)); (23, 1) becomes ((23, 1), (23, 2)), etc. The same
        logic applies to connection_node_id_start and connection_node_id_end.
        """
        if vertex_index == len(self.geometry.coords) - 1:
            # entire input channel is valid
            return self, None

        vertex = Point(self.geometry.coords[vertex_index])
        vertex_index_position = self.geometry.project(vertex)
        first_part = Channel(
            id=self.id,
            connection_node_id_start=self.connection_node_id_start,
            connection_node_id_end=(self.connection_node_id_start[0], self.connection_node_id_start[1] + 1),
            geometry=LineString([(Point(vertex)) for vertex in self.geometry.coords[:vertex_index + 1]])
        )
        for xsec in self.cross_section_locations:
            xsec_copy = CrossSectionLocation.clone(xsec)
            first_part.add_cross_section_location(xsec_copy)
            # A bit hacky but quick way to give cross-section location a "ghost" location on its new channel
            xsec_copy_idx = first_part.cross_section_location_index(xsec.id)

            first_part.cross_section_locations[xsec_copy_idx]._position_normalized = (
                xsec.position / first_part.geometry.length
            )
            if xsec.position >= vertex_index_position:
                # the first cross-section location beyond the end of the first part has been added, so we can stop
                break

        last_part = Channel(
            id=(self.id[0], self.id[1] + 1),
            connection_node_id_start=(self.connection_node_id_start[0], self.connection_node_id_start[1] + 1),
            connection_node_id_end=self.connection_node_id_end,
            geometry=LineString([(Point(vertex)) for vertex in self.geometry.coords[vertex_index:]])
        )
        for xsec in reversed(self.cross_section_locations):
            xsec_copy = CrossSectionLocation.clone(xsec)
            last_part.add_cross_section_location(xsec_copy)

            # A bit hacky but quick way to give this cross-section location a "ghost" location on its new channel
            xsec_copy_idx = last_part.cross_section_location_index(xsec.id)
            last_part.cross_section_locations[xsec_copy_idx]._position_normalized = (
                (xsec.position - first_part.geometry.length) / last_part.geometry.length
            )
            if xsec.position <= vertex_index_position:
                # the first cross-section location before the start of the last part has been added, so we can stop
                break

        return first_part, last_part

    def make_valid_parallel_offsets(self) -> List['Channel']:
        """
        Make Channel valid enough to generate parallel offsets (and generate them in the process)

        Return a list of Channels for which valid offsets can be generated. If needed, the input channel will be cut
        into parts. Always returns a list, even when the input channel is already valid

        If ``self`` has parallel offsets, these will be generated for the resulting channels as well
        """
        result = []
        possibly_invalid_channel = self
        while possibly_invalid_channel:
            hvi = highest_valid_index(line=possibly_invalid_channel.geometry, offsets=self.unique_offsets)
            hvi = 1 if hvi == 0 else hvi
            valid_part, possibly_invalid_channel = possibly_invalid_channel.split(vertex_index=hvi)
            result.append(valid_part)
        for channel in result:
            channel.generate_parallel_offsets()
        return result

    def make_valid_vertex_count(self):
        """
        Split channel in parts for which the total number of vertices in the parallel offsets does not exceed the
        ``VERTEX_LIMIT``

        Also runs ``make_valid_triangulate()`` on the output channels
        """
        result = []
        num_po_vertices = np.sum([len(po.geometry.coords) for po in self.parallel_offsets])
        if num_po_vertices > VERTEX_LIMIT:
            channel_vertex_limit = int(min(VERTEX_LIMIT / num_po_vertices, 1) * len(self.geometry.coords)) - 1
            possibly_invalid_channel = self
            while possibly_invalid_channel:
                vertex_index = min(len(possibly_invalid_channel.geometry.coords) - 1, channel_vertex_limit)
                valid_part, possibly_invalid_channel = possibly_invalid_channel.split(vertex_index=vertex_index)
                valid_part.generate_parallel_offsets()
                result.append(valid_part)
        else:
            result.append(self)
        return result

    def make_valid_triangulate(self):
        """
        Make Channel valid enough to generate fill parallel offsets (and do this in the process)
        """
        result = []
        possibly_invalid_channel = self
        first_iteration = True
        while possibly_invalid_channel:
            index = len(possibly_invalid_channel.geometry.coords) - 1
            valid_part_found = False
            while not valid_part_found:
                index = 1 if index == 0 else index
                first_part, last_part = possibly_invalid_channel.split(vertex_index=index)
                try:
                    first_part.generate_parallel_offsets()
                    first_part.fill_parallel_offsets()
                    result.append(first_part)
                    possibly_invalid_channel = last_part
                    valid_part_found = True
                except TriangulationError as first_part_error:
                    # let's see if last_part is valid, so we can get rid of that
                    if last_part:
                        try:
                            last_part.generate_parallel_offsets()
                            last_part.fill_parallel_offsets()
                        except TriangulationError as last_part_error:
                            pass
                        else:
                            result.append(last_part)
                            possibly_invalid_channel = first_part
                            valid_part_found = True
                            continue

                    if first_iteration:
                        # Make a first guess for the index
                        min_pos = 2
                        for point in first_part_error.locations:
                            channel_vertices = MultiPoint(
                                [Point(coord) for coord in possibly_invalid_channel.geometry.coords]
                            )
                            snapped_point = nearest_points(channel_vertices, point.geom)[0]
                            # Why not use shapely.snap() here, you ask?
                            # I tried, but it gave really weird results in some cases
                            pos = possibly_invalid_channel.geometry.project(snapped_point, normalized=True)
                            if pos < min_pos:
                                split_point = snapped_point
                                min_pos = pos
                        index = index_of_vertex(possibly_invalid_channel.geometry, split_point)
                        first_iteration = False
                    else:
                        index = int(np.ceil(index / 2))
                except EmptyOffsetError:
                    if first_iteration:
                        # Make a first guess for the index
                        index = int(np.ceil((len(possibly_invalid_channel.geometry.coords)) / 2))
                    else:
                        index -= 1
        return result

    def make_valid(self) -> List['Channel']:
        made_valid_po = self.make_valid_parallel_offsets()
        made_valid_vertex_count = []
        for channel in made_valid_po:
            made_valid_vertex_count += channel.make_valid_vertex_count()
        made_valid_triangulate = []
        for channel in made_valid_vertex_count:
            made_valid_triangulate += channel.make_valid_triangulate()
        return made_valid_triangulate


class ParallelOffset:
    def __init__(self, parent: Channel, offset_distance: float):
        """
        The side is determined by the sign of the distance parameter (negative for right side offset, positive for left
        side offset). Left and right are determined by following the direction of the given geometric points of the
        LineString.
        """
        self.parent = parent
        self.geometry = offset_curve_fixed(parent.geometry, offset_distance)
        if self.geometry.is_empty:
            raise EmptyOffsetError
        if type(self.geometry) != LineString:
            raise InvalidOffsetError
        self.offset_distance = offset_distance
        cross_section_location_positions = []
        for pos in self.parent.cross_section_location_positions:
            # handle normal case where CrossSectionLocation is located on the Channel
            if pos >= 0 and pos <= self.parent.geometry.length:
                location_xy = self.parent.geometry.interpolate(pos)
                cross_section_location_point = nearest_points(location_xy, self.geometry)[0]
                cross_section_location_positions.append(self.geometry.project(cross_section_location_point))

            # handle 'ghost' cross-section locations that belong to channels created by Channel.split()
            # it is implicitly assumed that the channel in the "ghost" section(s) is straight, i.e. the length of the
            # ParallelOffset equals the length of the Channel in those sections
            else:
                cross_section_location_positions.append(pos)

        z_ordinates_at_cross_sections = [
            xsec.z_at(self.offset_distance) for xsec in self.parent.cross_section_locations
        ]
        self.vertex_positions = [
            self.geometry.project(Point(vertex)) for vertex in self.geometry.coords
        ]
        self.heights_at_vertices = np.interp(
            self.vertex_positions,
            cross_section_location_positions,
            z_ordinates_at_cross_sections,
        )
        self.vertex_indices = None

    @property
    def points(self) -> List[IndexedPoint]:
        result = []
        for i, (x, y) in enumerate(self.geometry.coords):
            result.append(IndexedPoint(x, y, self.heights_at_vertices[i], index=self.vertex_indices[i]))
        return result

    def set_vertex_indices(self, first_vertex_index: int):
        self.vertex_indices = list(
            range(first_vertex_index, first_vertex_index + len(self.geometry.coords))
        )

    def triangle_is_valid(self, triangle_points: Sequence[Point], other_parallel_offset: 'ParallelOffset'):
        """
        Return True if none of the sides of the triangle crosses the parallel offsets that should enclose it
        """
        valid = True
        for start, end in [(0, 1), (0, 2), (1, 2)]:
            line = LineString([triangle_points[start], triangle_points[end]])
            if self.geometry.crosses(line) or other_parallel_offset.geometry.crosses(
                line
            ):
                valid = False
        return valid

    def triangulate(self, other: 'ParallelOffset'):
        return triangulate_between(
            left_side_points=self.points,
            right_side_points=other.points,
        )


def triangulate_between(
    left_side_points: List[IndexedPoint],
    right_side_points: List[IndexedPoint],
) -> Iterator[Triangle]:
    """
    Generate a set of triangles that fills the space between two lines. Left and right only matters for lines with odd,
    curvy shapes. It does not matter for lines that run nicely parallel to each other.

    :param left_side_points: list of points located along a line to the left of ``right_side_points``
    :param right_side_points: list of points located along a line to the right of ``left_side_points``
    """
    if len(left_side_points) == 0:
        raise ValueError("left_side_points is empty")

    if len(right_side_points) == 0:
        raise ValueError("right_side_points is empty")

    # flip points of one side if that makes the sides more parallel
    if left_side_points[0].geom.distance(right_side_points[0].geom) > \
            left_side_points[0].geom.distance(right_side_points[-1].geom):
        right_side_points.reverse()

    # make lines out of the IndexedPoint lists, and calculate distances of each point along that line
    left_side_line = LineString([point.geom for point in left_side_points]) \
        if len(left_side_points) > 1 \
        else left_side_points[0].geom

    right_side_line = LineString([point.geom for point in right_side_points]) \
        if len(right_side_points) > 1 \
        else right_side_points[0].geom

    # raise error if lines intersect
    if left_side_line.intersects(right_side_line):
        raise IntersectingSidesError(
            f"left side line: {left_side_line.wkt} \n"
            f"right side line: {right_side_line.wkt}"
        )

    left_side_idx = 0
    right_side_idx = 0
    left_side_last_idx = len(left_side_points) - 1
    right_side_last_idx = len(right_side_points) - 1

    while (left_side_idx < left_side_last_idx) or (right_side_idx < right_side_last_idx):
        triangle_points = [left_side_points[left_side_idx], right_side_points[right_side_idx]]
        # first we handle the case where the end of the line has been reached at one of the sides
        if left_side_idx == left_side_last_idx:
            right_side_idx += 1
            triangle_points.append(right_side_points[right_side_idx])
        elif right_side_idx == right_side_last_idx:
            left_side_idx += 1
            triangle_points.append(left_side_points[left_side_idx])

        # then we handle the 'normal' case when we are still halfway at both sides
        else:
            move_on_left_side_cross_line = LineString([
                left_side_points[left_side_idx + 1].geom,
                right_side_points[right_side_idx].geom
            ])
            move_on_right_side_cross_line = LineString([
                left_side_points[left_side_idx].geom,
                right_side_points[right_side_idx + 1].geom
            ])
            move = LEFT if move_on_left_side_cross_line.length < move_on_right_side_cross_line.length else RIGHT

            # switch move side if moving on that side results in invalid triangle
            test_triangle_move_left = Triangle(triangle_points + [left_side_points[left_side_idx + 1]])
            test_triangle_move_right = Triangle(triangle_points + [right_side_points[right_side_idx + 1]])
            if move == LEFT:
                if not test_triangle_move_left.is_between(left_side_line, right_side_line):
                    if test_triangle_move_right.is_between(left_side_line, right_side_line):
                        move = RIGHT
                    else:
                        # both 'default' options are invalid
                        move = 0
            elif move == RIGHT:
                if not test_triangle_move_right.is_between(left_side_line, right_side_line):
                    if test_triangle_move_left.is_between(left_side_line, right_side_line):
                        move = LEFT
                    else:
                        # both 'default' options are invalid
                        move = 0
            if move == LEFT:
                left_side_idx += 1
                triangle_points.append(left_side_points[left_side_idx])
            elif move == RIGHT:
                right_side_idx += 1
                triangle_points.append(right_side_points[right_side_idx])
            else:
                # handle the case where both moves result in invalid triangle
                # alternative LEFT_LEFT and RIGHT_RIGHT are triangles that consist of only left_side or only right_side
                # triangles. this is the valid option in rare cases where left_side_line or right_side_line are super
                # curvy
                solution_possible = True
                if left_side_idx + 1 < left_side_last_idx:
                    test_triangle_move_left_left = Triangle([left_side_points[left_side_idx + n] for n in [0, 1, 2]])
                else:
                    solution_possible = False
                if right_side_idx + 1 < right_side_last_idx:
                    test_triangle_move_right_right = Triangle([right_side_points[right_side_idx + n] for n in [0, 1, 2]])
                else:
                    solution_possible = False

                if solution_possible:
                    if test_triangle_move_left_left.geometry.area > 0 \
                            and test_triangle_move_left_left.is_between(left_side_line, right_side_line):
                        triangle_points = [left_side_points[left_side_idx + n] for n in [0, 1, 2]]
                        left_side_idx += 2
                    elif test_triangle_move_right_right.geometry.area > 0 \
                            and test_triangle_move_right_right.is_between(left_side_line, right_side_line):
                        triangle_points = [right_side_points[right_side_idx + n] for n in [0, 1, 2]]
                        right_side_idx += 2
                    else:
                        solution_possible = False
                if not solution_possible:
                    raise TriangulationError("No valid triangle found, cannot continue", locations=triangle_points)

        yield Triangle(points=triangle_points)


def unique_connection_node_ids(channels: List[Channel]) -> Set[int]:
    result = set([channel.connection_node_id_start for channel in channels])
    result |= set([channel.connection_node_id_end for channel in channels])
    return result


def get_channels_per_connection_node(channels: List[Channel]) -> dict:
    result = dict()
    connection_node_ids = unique_connection_node_ids(channels)
    for connection_node_id in connection_node_ids:
        current_node_channels = []
        for channel in channels:
            if connection_node_id in [
                channel.connection_node_id_start,
                channel.connection_node_id_end,
            ]:
                current_node_channels.append(channel)
        result[connection_node_id] = current_node_channels
    return result


def azimuth(point1, point2):
    """azimuth between 2 shapely points (interval 0 - 360)"""
    angle = np.arctan2(point2.x - point1.x, point2.y - point1.y)
    return np.degrees(angle) if angle >= 0 else np.degrees(angle) + 360


def ccw_angle(channel1: Channel, channel2: Channel) -> float:
    """Calculate the CCW angle in degrees between a line from `point1` to `reference`
    and a line between `point2` and `reference`"""
    connection_node_ids = unique_connection_node_ids([channel1, channel2])
    for connection_node_id in connection_node_ids:
        if connection_node_id in [
            channel1.connection_node_id_start,
            channel1.connection_node_id_end,
        ] and connection_node_id in [
            channel2.connection_node_id_start,
            channel2.connection_node_id_end,
        ]:
            break
    connection_node_geometry = channel1.find_vertex(connection_node_id, 0)
    channel1_point = channel1.find_vertex(connection_node_id, 1)
    channel2_point = channel2.find_vertex(connection_node_id, 1)
    azimuth1 = azimuth(connection_node_geometry, channel1_point)
    azimuth2 = azimuth(connection_node_geometry, channel2_point)
    if azimuth2 > azimuth1:
        return azimuth1 + (360 - azimuth2)
    else:
        return azimuth1 - azimuth2


def find_wedge_channels(
    channels: List[Channel], connection_node_id: Tuple[int, int]
) -> Union[Tuple[Channel, Channel], Tuple[None, None]]:
    """In a list of channels that connect to the same connection node, find a pair of channels that connect at
    a > 180 degree angle, so that there is a wedge-shaped gap between them"""
    azimuth_channel_dict = {}
    for channel in channels:
        key = round(channel.azimuth_at(connection_node_id), 6)
        azimuth_channel_dict[key] = channel
    sorted_azimuths = list(azimuth_channel_dict.keys())
    sorted_azimuths.sort(reverse=True)
    sorted_azimuths = [sorted_azimuths[-1]] + sorted_azimuths + [sorted_azimuths[0]]
    for i in range(len(sorted_azimuths) - 1):
        channel_1 = azimuth_channel_dict[sorted_azimuths[i]]
        channel_2 = azimuth_channel_dict[sorted_azimuths[i + 1]]
        angle = ccw_angle(channel_1, channel_2)
        if angle > 180:
            return channel_1, channel_2
    return None, None


def fill_wedges(channels: List[Channel], feedback=None):
    """
    In a list of Channels, find cases where a wedge needs to be filled and fill them, i.e. add wedge triangles to
    one of the two channels involved.

    We iterate over each junction (connection node), find the two channels in the junction between which a wedge needs
    to be filled (i.e. angle between them is > 180 degrees), and fill them once (i.e. we only call
    ``channel1.fill_wedge(channel2)`` and not ``channel2.fill_wedge(channel1)``
    """
    connection_node_channels_dict = get_channels_per_connection_node(channels)
    for connection_node_id, channels in connection_node_channels_dict.items():
        if feedback:
            if feedback.isCanceled():
                return
        channel1, channel2 = find_wedge_channels(
            channels=channels, connection_node_id=connection_node_id
        )
        if channel1 and channel2:
            try:
                channel1.fill_wedge(channel2)
            except (IntersectingSidesError, ValueError) as e:
                if feedback:
                    feedback.pushWarning(
                        f"Warning: Could not fill wedge-shaped gap between channel {channel1.id} and {channel2.id}."
                        f"Error: {repr(e)}"
                    )