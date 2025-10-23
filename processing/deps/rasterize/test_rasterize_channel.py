import numpy as np
import shapely
from shapely.geometry import LineString, Point
from shapely import wkt, wkb
from shapely import __version__ as shapely_version, geos_version
import pytest

from rasterize_channel import (
    IndexedPoint,
    Triangle,
    Channel,
    CrossSectionLocation,
    SupportedShape,
    find_wedge_channels,
    # fill_wedges,
    parse_cross_section_table,
    triangulate_between, highest_valid_index_single_offset, highest_valid_index, is_valid_offset,
)

WALL_DISPLACEMENT = 0.01  # tops or bottoms of vertical segments are moved by this amount

if int(shapely_version.split(".")[0]) < 2:
    raise Exception(f"Required Shapely version >= 2.0.0. Installed Shapely version: {shapely_version}")
if not (geos_version[0] > 3 or (geos_version[0] == 3 and geos_version[1] >= 12)):
    raise Exception(f"Required GEOS version >= 3.12.0. Installed GEOS version: {geos_version}")


# Generate test data
def get_test_channel(nr: int = 0):
    """Channel 0 has no cross-section location; 1, 2, and 3 do have one in the middle."""

    if nr == 0:
        channel_geom = LineString([[0, 0], [1, 1], [2, 2]])
        channel = Channel(
            geometry=channel_geom,
            connection_node_id_start=1,
            connection_node_id_end=2,
            id=1,
        )
    elif nr == 1:
        channel = Channel(
            geometry=LineString([Point(20, -100), Point(0, -50), Point(0, 0)]),
            connection_node_id_start=1,
            connection_node_id_end=2,
            id=1,
        )
        xsec = get_test_cross_section_location()
        xsec.geometry = Point(0, -50)
        channel.add_cross_section_location(xsec)
    elif nr == 2:
        channel = Channel(
            geometry=LineString([Point(0, 0), Point(10, 50), Point(10, 100)]),
            connection_node_id_start=2,
            connection_node_id_end=3,
            id=2,
        )
        xsec = get_test_cross_section_location()
        xsec.geometry = Point(10, 50)
        channel.add_cross_section_location(xsec)
    elif nr == 3:
        channel = Channel(
            geometry=LineString([Point(0, 0), Point(50, 0), Point(100, 10)]),
            connection_node_id_start=2,
            connection_node_id_end=4,
            id=3,
        )
        xsec = get_test_cross_section_location()
        xsec.geometry = Point(50, 0)
        channel.add_cross_section_location(xsec)
    elif nr == 4:
        wkb_geometry = b"\x01\x02\x00\x00\x00\x03\x00\x00\x00\xc6\xd2w\xb3Vo\"@\x00\xcc)C\x13S\xa1?\x13\xc9nJ\x8c\x08" \
                       b">@\x00\xce_\xe3\x19\xa2\xb9?b\xd4\x90\x9d\xb6lI@\x00[\x95\x12UM\xc5?"
        channel = Channel(
            geometry=wkb.loads(wkb_geometry),
            connection_node_id_start=5,
            connection_node_id_end=6,
            id=4,
        )

    elif nr == 5:
        wkb_geometry = b"\x01\x02\x00\x00\x00\x03\x00\x00\x00b\xd4\x90\x9d\xb6lI@\x00[\x95\x12UM\xc5?\xc7\xf5" \
                       b"\x1a\\\xb9YN@\x15\xc0\xc1!}\x812@\x96\x8bR\r^\xa3Q@\xba*\xaf\xcc/lB@'"
        channel = Channel(
            geometry=wkb.loads(wkb_geometry),
            connection_node_id_start=6,
            connection_node_id_end=7,
            id=5,
        )
    elif nr == 6:
        channel = Channel(
            geometry=LineString([
                [0, 0], [10, 10], [10, 20], [0, 30], [0, 40], [10, 50], [20, 50], [30, 40], [30, 30], [20, 20],
                [20, 10], [30, 0], [37, 0], [38, 1], [38, 2], [37, 3], [37, 4], [38, 5], [39, 5], [40, 4], [40, 3],
                [39, 2], [39, 1], [40, 0]]
            ),
            connection_node_id_start=1,
            connection_node_id_end=2,
            id=6,
        )
    elif nr == 7:
        channel = Channel(
            geometry=LineString([[20, -100], [-50, -150]]),
            connection_node_id_start=1,
            connection_node_id_end=4,
            id=7,
        )
    else:
        raise ValueError(f"Invalid value for parameter 'nr': {nr}")
    return channel


def get_test_cross_section_location(nr: int = 0):
    if nr == 0:
        y, z = parse_cross_section_table(
            table="0, 0\n1.0, 2.0\n2.0, 4.0",
            cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
        )

        cross_section_loc = CrossSectionLocation(
            id=1,
            reference_level=10.0,
            bank_level=12.0,
            y_ordinates=y,
            z_ordinates=z,
            geometry=Point(1, 1),
        )
        return cross_section_loc

    elif nr == 4:
        y, z = parse_cross_section_table(
            table="0, 5\n"
                  "5, 0\n"
                  "7, 3",
            cross_section_shape=SupportedShape.YZ.value
        )

        cross_section_loc = CrossSectionLocation(
            id=4,
            reference_level=10.0,
            bank_level=12.0,
            y_ordinates=y,
            z_ordinates=z,
            geometry=Point(30.033391, 0.10013)
        )
        return cross_section_loc

    elif nr == 5:
        y, z = parse_cross_section_table(
            table="0, 5\n"
                  "1, 3\n"
                  "2, 0\n"
                  "3, 0.5\n"
                  "4, 1\n"
                  "5, 2.3\n"
                  "6, 4.8",
            cross_section_shape=SupportedShape.YZ.value
        )

        cross_section_loc = CrossSectionLocation(
            id=1,
            reference_level=10.0,
            bank_level=12.0,
            y_ordinates=y,
            z_ordinates=z,
            geometry=Point(30.033391, 0.10013)
        )
        return cross_section_loc


def get_wedge_channels():
    wedge_channels = find_wedge_channels(
        [get_test_channel(1), get_test_channel(2), get_test_channel(3)],
        connection_node_id=(2, 0)
    )
    return wedge_channels


def cross_section_locations_are_equal(reference: CrossSectionLocation, compare: CrossSectionLocation) -> bool:
    """Compares cross-section locations by properties, except parent and position"""
    assert reference.bank_level == compare.bank_level
    assert reference.geometry.wkt == compare.geometry.wkt
    assert reference.id == compare.id
    assert reference.max_width == compare.max_width
    assert np.array_equal(reference.offsets, compare.offsets)
    assert reference.reference_level == compare.reference_level
    assert reference.thalweg_y == compare.thalweg_y
    assert np.array_equal(reference.y_ordinates, compare.y_ordinates)
    assert np.array_equal(reference.z_ordinates, compare.z_ordinates)
    return True


# Tests
def test_parse_cross_section_table():
    # TABULATED RECTANGLE
    y, z = parse_cross_section_table(
        table="0, 2\n1, 4",
        cross_section_shape=SupportedShape.TABULATED_RECTANGLE.value,
        wall_displacement=WALL_DISPLACEMENT
    )
    assert np.all(y == np.array([0, 1, 1 + WALL_DISPLACEMENT, 3, 3 + WALL_DISPLACEMENT, 4]))
    assert np.all(z == np.array([1, 1, 0, 0, 1, 1]))

    # TABULATED TRAPEZIUM
    y, z = parse_cross_section_table(
        table="0, 2\n1, 4",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value,
        wall_displacement=WALL_DISPLACEMENT
    )
    assert np.all(y == np.array([0, 1, 3, 4]))
    assert np.all(z == np.array([1, 0, 0, 1]))

    # TABULATED TRAPEZIUM WITH THREE ROWS
    y, z = parse_cross_section_table(
        table="0, 10.0\n1.0, 20.0\n2.0, 40.0",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )
    assert np.all(y == np.array([0, 10, 15, 25, 30, 40]))
    assert np.all(z == np.array([2, 1, 0, 0, 1, 2]))

    # TABULATED TRAPEZIUM WITH LOWEST WIDTH = 0
    y, z = parse_cross_section_table(
        table="0, 0\n1, 4",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value,
        wall_displacement=WALL_DISPLACEMENT
    )
    assert np.all(y == np.array([0, 2, 4]))
    assert np.all(z == np.array([1, 0, 1]))

    # TABULATED TRAPEZIUM WITH VERTICAL WALL
    y, z = parse_cross_section_table(
        table="0, 0\n"
              "0.434, 6.823\n"
              "0.867, 8.975\n"
              "1.301, 9.995\n"
              "1.734, 11.273\n"
              "2.168, 11.644\n"
              "2.601, 11.644\n"
              "3.035, 42.656",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value,
        wall_displacement=WALL_DISPLACEMENT
    )
    assert np.allclose(
        y,
        [
            0., 15.506, 15.506 + WALL_DISPLACEMENT, 15.6915, 16.3305, 16.8405, 17.9165, 21.328, 24.7395, 25.8155,
            26.3255,
            26.9645, 27.15, 27.15 + WALL_DISPLACEMENT, 42.656
        ]
    )
    assert np.allclose(
        z, [3.035, 2.601, 2.168, 1.734, 1.301, 0.867, 0.434, 0., 0.434, 0.867, 1.301, 1.734, 2.168, 2.601, 3.035]
    )

    # TABULATED RECTANGLE which describes a rectangle
    y, z = parse_cross_section_table(
        table="0.0, 1.0\n0.5, 1.0",
        cross_section_shape=SupportedShape.TABULATED_RECTANGLE.value,
        wall_displacement=WALL_DISPLACEMENT
    )
    assert np.all(y == np.array([0, 0.01, 1, 1.01]))
    assert np.all(z == np.array([0.5, 0, 0, 0.5]))

    # TABULATED RECTANGLE: wall displacement "overtakes" next segment
    y, z = parse_cross_section_table(
        table="0.0, 0.0\n"
              "0.075, 1.309\n"
              "0.151, 1.737\n"
              "0.226, 2.096\n"
              "0.302, 2.343\n"
              "0.377, 2.59\n"
              "0.453, 3.039\n"
              "0.528, 3.255\n"
              "0.604, 3.475\n"
              "0.679, 3.694\n"
              "0.755, 3.914",
        cross_section_shape=SupportedShape.TABULATED_RECTANGLE.value,
        wall_displacement=0.25
    )
    assert np.allclose(y, np.array([
        0., 0.11, 0.36, 0.4695, 0.5795, 0.6875, 0.912, 1.0355, 1.159, 1.3385, 1.5525, 1.957, 2.207, 2.457, 2.6115,
        2.8615, 3.0755, 3.255, 3.3785, 3.502, 3.7265, 3.8345, 3.9445, 4.054
    ]))
    assert np.allclose(z, np.array([
        0.755, 0.755, 0.679, 0.604, 0.528, 0.453, 0.377, 0.302, 0.226, 0.151, 0.075, 0.075, 0., 0.075, 0.075, 0.151,
        0.226, 0.302, 0.377, 0.453, 0.528, 0.604, 0.679, 0.755
    ]))
    # plt.plot(y, z)
    # plt.show()

    # YZ
    y, z = parse_cross_section_table(
        table="0, 3\n2, 1\n4, 0\n8, 4",
        cross_section_shape=SupportedShape.YZ.value,
        wall_displacement=WALL_DISPLACEMENT
    )
    assert np.all(y == np.array([0, 2, 4, 8]))
    assert np.all(z == np.array([3, 1, 0, 4]))

    # Invalid shape
    with pytest.raises(ValueError):
        y, z = parse_cross_section_table(
            table="0, 3\n2, 1\n4, 0\n8, 4",
            cross_section_shape=1,
            wall_displacement=WALL_DISPLACEMENT
        )


def test_is_valid_offset():
    # VALID
    assert is_valid_offset(LineString([[0, 0], [0, 1], [0, 2], [0, 3], [1, 1]]), -.5) is True

    # EMPTY OFFSETS
    assert is_valid_offset(LineString([[-4, 4], [-4, 0], [0, 0], [0, 4]]), 2) is False
    assert is_valid_offset(LineString([[0, 0], [0, 1], [0, 2], [0, 3], [1, 1], [1, 0]]), -.5) is False

    # MULTILINESTRING
    line_coords = np.array(
        [[0, 0], [10, 10], [10, 20], [0, 30], [0, 40], [10, 50], [20, 50], [30, 40], [30, 30], [20, 20], [20, 10],
         [30, 0], [37, 0], [38, 1], [38, 2], [37, 3], [37, 4], [38, 5], [39, 5], [40, 4], [40, 3], [39, 2], [39, 1],
         [40, 0]]
    )
    line = LineString(line_coords)
    assert is_valid_offset(line, -0.5) is False
    assert is_valid_offset(line, -0.4) is True


def test_highest_valid_index_single_offset(plot: bool = False):
    line = LineString([[0, 0], [0, 1], [0, 2], [0, 3], [2, 3], [2, 2], [1, 1], [1, 0]])
    offset = -2
    if plot:
        import matplotlib.pyplot as plt
        offset_line = line.offset_curve(offset)
        plt.plot(line.xy[0], line.xy[1], 'b-')  # 'b-' for blue line
        if type(offset_line) == LineString:
            plt.plot(offset_line.xy[0], offset_line.xy[1], 'g-')
        else:  # Probably MultiLineString
            for offset_line_geom in offset_line.geoms:
                plt.plot(offset_line_geom.xy[0], offset_line_geom.xy[1], 'g-')
        hvi = highest_valid_index_single_offset(line, offset)
        point_x, point_y = line.coords[hvi]
        plt.plot(point_x, point_y, 'ro', label=f"HVI: {hvi}")
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.axis('equal')  # Set equal scaling
        plt.legend()
        plt.show()

    assert highest_valid_index_single_offset(line, -2) == 4

    line = LineString([[0, 0], [0, 1], [0, 2], [0, 3], [2, 3], [4, 3], [8, 3], [10, 3]])
    assert highest_valid_index_single_offset(line, -2) == 7


def test_highest_valid_index(plot: bool = False):
    line_coords = np.array(
        [[0, 0], [10, 10], [10, 20], [0, 30], [0, 40], [10, 50], [20, 50], [30, 40], [30, 30], [20, 20], [20, 10],
         [30, 0], [37, 0], [38, 1], [38, 2], [37, 3], [37, 4], [38, 5], [39, 5], [40, 4], [40, 3], [39, 2], [39, 1],
         [40, 0]]
    )
    line = LineString(line_coords)
    offset_small = -0.5
    offset_large = -5

    if plot:
        import matplotlib.pyplot as plt
        offset_line_0_5 = line.offset_curve(offset_small)
        offset_line_5 = line.offset_curve(offset_large)
        plt.plot(line.xy[0], line.xy[1], 'b-')  # 'b-' for blue line
        for offset_line_geom in offset_line_0_5.geoms:
            plt.plot(offset_line_geom.xy[0], offset_line_geom.xy[1], 'g-')
        for offset_line_geom in offset_line_5.geoms:
            plt.plot(offset_line_geom.xy[0], offset_line_geom.xy[1], 'r-')
        hvi_small_offset = highest_valid_index(line, [offset_small])
        point_x, point_y = line.coords[hvi_small_offset]
        plt.plot(point_x, point_y, 'ro', label=f"HVI for small offset: {hvi_small_offset}")
        hvi_large_offset = highest_valid_index(line, [offset_large])
        point_x, point_y = line.coords[hvi_large_offset]
        plt.plot(point_x, point_y, 'ko', label=f"HVI for large offset: {hvi_large_offset}")
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.axis('equal')  # Set equal scaling
        plt.legend()
        plt.show()

    assert highest_valid_index(line, [offset_small, offset_large]) == 9
    assert highest_valid_index(line, [offset_small, offset_large]) == highest_valid_index(line, [offset_large])
    assert highest_valid_index(line, [offset_small]) == 21


def test_channel_azimuth_at():
    assert get_test_channel(1).azimuth_at(connection_node_id=(2, 0)) == 180
    assert round(get_test_channel(2).azimuth_at(connection_node_id=(2, 0)), 2) == 11.31
    assert get_test_channel(3).azimuth_at(connection_node_id=(2, 0)) == 90


def test_cross_section_location_thalweg_y():
    y, z = parse_cross_section_table(
        table="0, 10.0\n1.0, 20.0\n2.0, 40.0",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )

    cross_section_loc = CrossSectionLocation(
        id=1,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(0, 0),
    )
    assert cross_section_loc.thalweg_y == 20.0


def test_cross_section_location_z_at():
    # Symmetrical Tabulated Trapezium
    xsec = get_test_cross_section_location()
    z = xsec.z_at(offset=0.0)
    assert xsec.z_at(offset=0.0) == 10
    assert xsec.z_at(offset=1.0) == 11
    assert xsec.z_at(offset=-1.0) == 11
    assert xsec.z_at(offset=1.5) == 11.5  # Interpolation
    assert xsec.z_at(offset=3.0) == 12  # Extrapolation

    # Asymmetrical YZ profile
    y, z = parse_cross_section_table(
        table="0, 3\n1.0, 2\n2.0, 0\n3.0, 3",
        cross_section_shape=SupportedShape.YZ.value
    )

    xsec = CrossSectionLocation(
        id=1,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(0, 0),
    )
    assert xsec.z_at(offset=0) == 10
    assert xsec.z_at(offset=1) == 12
    assert xsec.z_at(offset=-1) == 13
    assert xsec.z_at(offset=2) == 13
    assert xsec.z_at(offset=1.5) == 12.5  # interpolate
    assert xsec.z_at(offset=-5) == 13  # extrapolate


def test_channel_vertex_positions():
    channel = get_test_channel()
    vp = channel.vertex_positions
    assert np.all(vp == (np.array([0, 0.5, 1]) * channel.geometry.length))
    assert len(vp) == 3


def test_channel_properties():
    channel = get_test_channel()
    xsec = get_test_cross_section_location()
    channel.add_cross_section_location(xsec)

    y, z = parse_cross_section_table(
        table="0, 10.0\n1.0, 20.0\n2.0, 40.0",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )

    cross_section_loc = CrossSectionLocation(
        id=2,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(0, 0),
    )

    channel.add_cross_section_location(cross_section_loc)

    y, z = parse_cross_section_table(
        table="0, 0.1\n1.0, 0.2\n2.0, 0.4",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )

    cross_section_loc = CrossSectionLocation(
        id=3,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(2, 2),
    )

    channel.add_cross_section_location(cross_section_loc)

    assert np.all(channel.max_widths == np.array([40.0, 4.0, 0.4]))
    assert np.allclose(channel.unique_offsets, np.array(
        [-20.00, -10.00, -5.00, -2.00, -1.00, -0.20, -0.10, -0.05, 0.00, 0.05, 0.10, 0.20, 1.00, 2.00, 5.00, 10.00,
         20.00]
    )
                       )
    assert np.all(channel.cross_section_location_positions == np.array([0, 0.5, 1]) * channel.geometry.length)


def test_channel_outline(plot: bool = False):
    if plot:
        import matplotlib.pyplot as plt

        def plot_channel_and_sections(channel,
                                      cross_section_locations,
                                      title: str = "",
                                      channel_color='blue',
                                      outline_edge='black',
                                      outline_face='none',
                                      xs_color='red',
                                      xs_size=40):
            """
            Plot a Channel (with geometry and outline) and its CrossSectionLocations.

            Parameters
            ----------
            channel : object
                An object with:
                  - .geometry: shapely LineString (the channel centerline)
                  - .outline: shapely Polygon (the channel boundary)
            cross_section_locations : list
                List of objects with .geometry (shapely Points).
            channel_color : str
                Color of the channel LineString.
            outline_edge : str
                Edge color for the channel outline Polygon.
            outline_face : str
                Face color for the outline Polygon (default transparent).
            xs_color : str
                Color for the cross-section points.
            xs_size : int
                Size of cross-section markers.
            """

            fig, ax = plt.subplots(figsize=(8, 8))

            # --- Plot channel outline ---
            if channel.outline is not None:
                x, y = channel.outline.exterior.xy
                ax.fill(x, y, facecolor=outline_face, edgecolor=outline_edge, alpha=0.6, label='Channel outline')

            # --- Plot channel centerline ---
            if channel.geometry is not None:
                x, y = channel.geometry.xy
                ax.plot(x, y, color=channel_color, linewidth=2, label='Channel centerline')

            # --- Plot cross-section points ---
            if cross_section_locations:
                xs_x = [xs.geometry.x for xs in cross_section_locations]
                xs_y = [xs.geometry.y for xs in cross_section_locations]
                ax.scatter(xs_x, xs_y, color=xs_color, s=xs_size, label='Cross-section locations')

            ax.set_aspect('equal', adjustable='box')
            ax.legend()
            ax.set_title(title)
            plt.show()

    # Straight channel with 1 symmetrical cross-section
    channel = get_test_channel()
    xsec = get_test_cross_section_location()
    channel.add_cross_section_location(xsec)

    assert round(channel.outline.area, 10) == round(channel.geometry.buffer(2).area, 10)

    # Straight channel with 1 asymmetrical YZ.value cross-section
    channel = get_test_channel()
    y, z = parse_cross_section_table(
        table="0, 3\n1.0, 2\n2.0, 0\n3.0, 3",
        cross_section_shape=SupportedShape.YZ.value
    )

    cross_section_loc = CrossSectionLocation(
        id=1,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(0, 0),
    )

    channel.add_cross_section_location(cross_section_loc)
    if plot:
        plot_channel_and_sections(
            channel=channel,
            cross_section_locations=[cross_section_loc],
            title="Straight channel with 1 asymmetrical YZ.value cross-section"
        )
    expected_geometry_wkb = \
       b"\x01\x03\x00\x00\x00\x01\x00\x00\x00E\x00\x00\x00\xafo\x87v\xbe\x04\xe0\xbf\xe9\x0c=\xa1B:\xf2\xbf)<\xe7I" \
       b"\x94\xad\xe4\xbf\x91\xb6YB\xca\xe1\xf1\xbf(\xd5_\xd6S?\xe9\xbfq\xd3tgIO\xf1\xbf\xf0\x9cB0\xb9\xae\xed\xbf" \
       b"\x01\x1b\xc6A)\x84\xf0\xbfJk\xa2\x8ej\xf8\xf0\xbf\xa4~\x017\xbd\x04\xef\xbf\x88\x9d\xe2\x04\x94\xfd\xf2" \
       b"\xbf\x90TV\n\xca\x98\xec\xbfS\xa5f\xf5\xdd\xe1\xf4\xbf\xfe\x04`mq\xca\xe9\xbf\xcc;\x7ff\x9e\xa0\xf6\xbf" \
       b"\xce;\x7ff\x9e\xa0\xe6\xbfd\xa0\xef\xe9\x875\xf8\xbf\xdb\x0eN\x84\x1d#\xe3\xbf.\xc8j8\xb4\x9c\xf9\xbf\x8c" \
       b"\xfe\x8bF\x13\xb5\xde\xbf7]\xc0\xce\xad\xd2\xfa\xbf\x905\x8bmm\xa0\xd6\xbf\xe7\xb8\x05ux\xd4\xfb\xbf\x98" \
       b"\x84\r'k8\xcc\xbfWq\xb4\x9a\x98\x9f\xfc\xbf\xf4\xca\x04\x7f\xab\xf5\xb4\xbfwT\x99u\x192\xfd\xbf\xd8\xf9" \
       b"\x7f\xc9\xa10\xaf?\xcf\xaa|\xd4\x91\x8a\xfd\xbfk0\xdf\xbf\x7fo\xca?\xf3\xce\x9f\x99'\xa8\xfd\xbf\xc9;\x7ff" \
       b"\x9e\xa0\xd6?\xcf\xaa|\xd4\x91\x8a\xfd\xbf\xaeo\x87v\xbe\x04\xe0?wT\x99u\x192\xfd\xbf+<\xe7I\x94\xad\xe4?Wq" \
       b"\xb4\x9a\x98\x9f\xfc\xbf'\xd5_\xd6S?\xe9?\xe8\xb8\x05ux\xd4\xfb\xbf\xef\x9cB0\xb9\xae\xed?8]\xc0\xce\xad" \
       b"\xd2\xfa\xbfIk\xa2\x8ej\xf8\xf0?/\xc8j8\xb4\x9c\xf9\xbf\x88\x9d\xe2\x04\x94\xfd\xf2?e\xa0\xef\xe9\x875\xf8" \
       b"\xbfR\xa5f\xf5\xdd\xe1\xf4?\xcd;\x7ff\x9e\xa0\xf6\xbf\xcc;\x7ff\x9e\xa0\xf6?4\xef\xfc\x99y\x82\xda\xbf\xe6" \
       b"\x9d?3OP\x03@f\x88\x013\xc3\xbe\xe2?\xe6\x9d?3OP\x0b@S\xb52\x15D<\xe6?1\xd0\xf7\xf4\xc3\x1a\x0c@\xee\xc4:" \
       b"\xf6\xd7\x04\xea?\x17d5\x1cZ\xce\x0c@k)\xbb\xe2*\x0f\xee?\x9c.`\xe7Vi\r@\x84\xb1\xdeg\xa3(\xf1?t\xdc\x82:<" \
       b"\xea\r@j\x15\xd0\x14V`\xf3?\xac8ZM\xccO\x0e@\xe8a\x0c\xdb5\xa9\xf5?<\xaa\xcc\xba\x0c\x99\x0e@*H\xbc\xc4\xa0" \
       b"\xfd\xf7?hU>\xeaH\xc5\x0e@\x0c1`f\xd8W\xfa?z\xe7\xcf\xcc\x13\xd4\x0e@\xee\x19\x04\x08\x10\xb2\xfc?hU>\xeaH" \
       b"\xc5\x0e@/\x00\xb4\xf1z\x06\xff?<\xaa\xcc\xba\x0c\x99\x0e@V&\xf8[\xad\xa7\x00@\xac8ZM\xccO\x0e@J\xd8p\xb2" \
       b"\x86\xc3\x01@t\xdc\x82:<\xea\r@\xb2f\xb1\xad\r\xd4\x02@\x9c.`\xe7Vi\r@\xd0\x7f\xd1h\xa2\xd6\x03@\x18d5\x1cZ" \
       b"\xce\x0c@\xb7\x83\x13a\xc7\xc8\x04@2\xd0\xf7\xf4\xc3\x1a\x0c@\xf2\xce\x9f\x99'\xa8\x05@\xe7\x9d?3OP\x0b@>" \
       b"\x01X[\x9cr\x06@\xacR\xb3\xfa\xeep\n@$\x95\x95\x822&\x07@\xc5Nq\x02\xca~\t@\xa8_\xc0M/\xc1\x07@\xa65QG5|" \
       b"\x08@\x80\r\xe3\xa0\x14B\x08@>\xa7\x10L\xaek\x07@\xb8i\xba\xb3\xa4\xa7\x08@L\xf5\x97\xf5\xd4O\x06@H\xdb,!" \
       b"\xe5\xf0\x08@\x0c\xcfy\x12e+\x05@t\x86\x9eP!\x1d\t@\xec\xdb\xa1\x9d/\x01\x04@\x86\x1803\xec+\t@z\xe7\xcf" \
       b"\xcc\x13\xd4\x02@t\x86\x9eP!\x1d\t@\x08\xf3\xfd\xfb\xf7\xa6\x01@H\xdb,!\xe5\xf0\x08@\xe9\xff%\x87\xc2|" \
       b"\x00@\xb8i\xba\xb3\xa4\xa7\x08@R\xb3\x0fH\xa5\xb0\xfe?\x80\r\xe3\xa0\x14B\x08@oO\x1e\x9b\xf2x\xfc?\xa9_" \
       b"\xc0M/\xc1\x07@\x9e2\x9d\xa4\xe4W\xfa?$\x95\x95\x822&\x07@^\x00].\xbbR\xf8??\x01X[\x9cr\x06@\x94\xf8" \
       b"\xd8=qn\xf6?\xf4\xce\x9f\x99'\xa8\x05@\x1ab\xc0\xcc\xb0\xaf\xf4?\xe7\x9d?3OP\xfb?d\x88\x013\xc3\xbe\xd2?" \
       b"\xce;\x7ff\x9e\xa0\xe6?\xce;\x7ff\x9e\xa0\xe6\xbf\xdb\x0eN\x84\x1d#\xe3?\xfa\x04`mq\xca\xe9\xbf\x90\xfe" \
       b"\x8bF\x13\xb5\xde?\x8eTV\n\xca\x98\xec\xbf\x905\x8bmm\xa0\xd6?\xa2~\x017\xbd\x04\xef\xbf\x94\x84\r'k8\xcc?" \
       b"\x01\x1b\xc6A)\x84\xf0\xbf\xf0\xca\x04\x7f\xab\xf5\xb4?q\xd3tgIO\xf1\xbf\x10\xfa\x7f\xc9\xa10\xaf\xbf\x91" \
       b"\xb6YB\xca\xe1\xf1\xbfn0\xdf\xbf\x7fo\xca\xbf\xe9\x0c=\xa1B:\xf2\xbf\xca;\x7ff\x9e\xa0\xd6\xbf\r1`f\xd8W" \
       b"\xf2\xbf\xafo\x87v\xbe\x04\xe0\xbf\xe9\x0c=\xa1B:\xf2\xbf"

    expected_geometry = wkb.loads(expected_geometry_wkb)
    intersection = channel.outline.intersection(expected_geometry)
    assert abs(intersection.area - channel.outline.area) < 0.01

    # Straight channel with 2 YZ.value cross-sections that are assymetrical in opposite directions
    channel = get_test_channel()
    y, z = parse_cross_section_table(
        table="0, 3\n1.0, 2\n2.0, 0\n3.0, 3",
        cross_section_shape=SupportedShape.YZ.value
    )
    cross_section_locations = []
    cross_section_locations.append(
        CrossSectionLocation(
            id=1,
            reference_level=10.0,
            bank_level=12.0,
            y_ordinates=y,
            z_ordinates=z,
            geometry=Point(0, 0),
        )
    )

    y, z = parse_cross_section_table(
        table="0, 3\n1.0, 0\n2.0, 1.0\n3.0, 3",
        cross_section_shape=SupportedShape.YZ.value
    )

    cross_section_locations.append(
        CrossSectionLocation(
            id=2,
            reference_level=10.0,
            bank_level=12.0,
            y_ordinates=y,
            z_ordinates=z,
            geometry=Point(2, 2),
        )
    )
    for xsec in cross_section_locations:
        channel.add_cross_section_location(xsec)

    if plot:
        plot_channel_and_sections(
            channel, cross_section_locations,
            title="Straight channel with 2 YZ.value cross-sections that are assymetrical in opposite directions"
        )

    expected_geometry_wkb = \
       b"\x01\x03\x00\x00\x00\x01\x00\x00\x00E\x00\x00\x00\xafo\x87v\xbe\x04\xe0\xbf\xe9\x0c=\xa1B:\xf2\xbf" \
       b")<\xe7I\x94\xad\xe4\xbf\x91\xb6YB\xca\xe1\xf1\xbf(" \
       b"\xd5_\xd6S?\xe9\xbfq\xd3tgIO\xf1\xbf\xf0\x9cB0\xb9\xae\xed\xbf\x01\x1b\xc6A)\x84\xf0\xbfJk\xa2\x8ej\xf8" \
       b"\xf0\xbf\xa4~\x017\xbd\x04\xef\xbf\x88\x9d\xe2\x04\x94\xfd\xf2\xbf\x90TV\n\xca\x98\xec\xbfS\xa5f\xf5\xdd" \
       b"\xe1\xf4\xbf\xfe\x04`mq\xca\xe9\xbf\xcc;\x7ff\x9e\xa0\xf6\xbf\xce;\x7ff\x9e\xa0\xe6\xbfd\xa0\xef\xe9" \
       b"\x875\xf8\xbf\xdb\x0eN\x84\x1d#\xe3\xbf.\xc8j8\xb4\x9c\xf9\xbf\x8c\xfe\x8bF\x13\xb5\xde\xbf7]\xc0\xce" \
       b"\xad\xd2\xfa\xbf\x905\x8bmm\xa0\xd6\xbf\xe7\xb8\x05ux\xd4\xfb\xbf\x98\x84\r'k8\xcc\xbfWq\xb4\x9a\x98\x9f" \
       b"\xfc\xbf\xf4\xca\x04\x7f\xab\xf5\xb4\xbfwT\x99u\x192\xfd\xbf\xd8\xf9\x7f\xc9\xa10\xaf?\xcf\xaa|\xd4\x91" \
       b"\x8a\xfd\xbfk0\xdf\xbf\x7fo\xca?\xf3\xce\x9f\x99'\xa8\xfd\xbf\xc9;\x7ff\x9e\xa0\xd6?\xcf\xaa|\xd4\x91" \
       b"\x8a\xfd\xbf\xaeo\x87v\xbe\x04\xe0?wT\x99u\x192\xfd\xbf+<\xe7I\x94\xad\xe4?Wq\xb4\x9a\x98\x9f\xfc\xbf" \
       b"'\xd5_\xd6S?\xe9?\xe8\xb8\x05ux\xd4\xfb\xbf\xef\x9cB0\xb9\xae\xed?8]\xc0\xce\xad\xd2\xfa\xbfIk\xa2\x8ej" \
       b"\xf8\xf0?/\xc8j8\xb4\x9c\xf9\xbf\x88\x9d\xe2\x04\x94\xfd\xf2?e\xa0\xef\xe9\x875\xf8\xbfR\xa5f\xf5\xdd" \
       b"\xe1\xf4?\xcd;\x7ff\x9e\xa0\xf6\xbf\xcc;\x7ff\x9e\xa0\xf6?V\xa5f\xf5\xdd\xe1\xf4\xbfa\xa0\xef\xe9\x875" \
       b"\xf8?\x89\x9d\xe2\x04\x94\xfd\xf2\xbf-\xc8j8\xb4\x9c\xf9?Jk\xa2\x8ej\xf8\xf0\xbf7]\xc0\xce\xad\xd2\xfa" \
       b"?\xa2\x8e\xf5+\xf4\xbe\xd2?\"G\x90\x1aC\x95\x02@\x9c2\x9d\xa4\xe4W\xfa?\xa8_\xc0M/\xc1\x07@kO\x1e\x9b" \
       b"\xf2x\xfc?\x80\r\xe3\xa0\x14B\x08@R\xb3\x0fH\xa5\xb0\xfe?\xb8i\xba\xb3\xa4\xa7\x08@\xe8\xff%\x87\xc2" \
       b"|\x00@H\xdb,!\xe5\xf0\x08@\x08\xf3\xfd\xfb\xf7\xa6\x01@t\x86\x9eP!\x1d\t@y\xe7\xcf\xcc\x13\xd4\x02@\x86" \
       b"\x1803\xec+\t@\xea\xdb\xa1\x9d/\x01\x04@t\x86\x9eP!\x1d\t@\x0b\xcfy\x12e+\x05@H\xdb," \
       b"!\xe5\xf0\x08@J\xf5\x97\xf5\xd4O\x06@\xb8i\xba\xb3\xa4\xa7\x08@=\xa7\x10L\xaek\x07@\x80\r\xe3\xa0\x14B" \
       b"\x08@\xa55QG5|\x08@\xa9_\xc0M/\xc1\x07@\xc4Nq\x02\xca~\t@$\x95\x95\x822&\x07@\xaaR\xb3\xfa\xeep\n" \
       b"@>\x01X[\x9cr\x06@\xe6\x9d?3OP\x0b@\xf4\xce\x9f\x99'\xa8\x05@1\xd0\xf7\xf4\xc3\x1a\x0c@\xb8\x83\x13a\xc7" \
       b"\xc8\x04@\x17d5\x1cZ\xce\x0c@\xd2\x7f\xd1h\xa2\xd6\x03@\x9c.`\xe7Vi\r@\xb2f\xb1\xad\r\xd4\x02@t\xdc\x82" \
       b":<\xea\r@K\xd8p\xb2\x86\xc3\x01@\xac8ZM\xccO\x0e@X&\xf8[" \
       b"\xad\xa7\x00@<\xaa\xcc\xba\x0c\x99\x0e@2\x00\xb4\xf1z\x06\xff?hU>\xeaH\xc5\x0e@\xf0\x19\x04\x08\x10\xb2" \
       b"\xfc?z\xe7\xcf\xcc\x13\xd4\x0e@\r1`f\xd8W\xfa?hU>\xeaH\xc5\x0e@)H\xbc\xc4\xa0\xfd\xf7?<\xaa\xcc\xba\x0c" \
       b"\x99\x0e@\xeba\x0c\xdb5\xa9\xf5?\xac8ZM\xccO\x0e@k\x15\xd0\x14V`\xf3?t\xdc\x82:<\xea\r@\x88\xb1\xdeg" \
       b"\xa3(\xf1?\x9c.`\xe7Vi\r@n)\xbb\xe2*\x0f\xee?\x17d5\x1cZ\xce\x0c@\xee\xc4:\xf6\xd7\x04\xea?2\xd0\xf7\xf4" \
       b"\xc3\x1a\x0c@Y\xb52\x15D<\xe6?\xe7\x9d?3OP\x0b@f\x88\x013\xc3\xbe\xe2?\xaaR\xb3\xfa\xeep\n@t~AX\xe0)\xdf" \
       b"?\xc6Nq\x02\xca~\t@L\xdfT\x1e/\x8d\xd9?\xa65QG5|\x08@$\x8b\xfe\xc4H\xb5\xd4?W\x9c\x02\xf5BP\xfb?\x109" \
       b"\x82\xd4\x18\xaa\xd4\xbf\x905\x8bmm\xa0\xd6?\xa2~\x017\xbd\x04\xef\xbf\x94\x84\r'k8\xcc?\x01\x1b\xc6A" \
       b")\x84\xf0\xbf\xf0\xca\x04\x7f\xab\xf5\xb4?q\xd3tgIO\xf1\xbf\x10\xfa\x7f\xc9\xa10\xaf\xbf\x91\xb6YB\xca" \
       b"\xe1\xf1\xbfn0\xdf\xbf\x7fo\xca\xbf\xe9\x0c=\xa1B:\xf2\xbf\xca;\x7ff\x9e\xa0\xd6\xbf\r1`f\xd8W\xf2\xbf" \
       b"\xafo\x87v\xbe\x04\xe0\xbf\xe9\x0c=\xa1B:\xf2\xbf"

    expected_geometry = wkb.loads(expected_geometry_wkb)
    intersection = channel.outline.intersection(expected_geometry)
    assert abs(intersection.area - channel.outline.area) < 0.01

    # Curved channel with 2 cross-sections with different widths
    channel = get_test_channel(6)
    channel.geometry = LineString(channel.geometry.coords[:4])
    y, z = parse_cross_section_table(
        table="0.0, 3.0\n"
              "1.0, 2.0\n"
              "2.0, 0.0\n"
              "3.0, 3.0",
        cross_section_shape=SupportedShape.YZ.value
    )

    cross_section_locations = []

    cross_section_locations.append(
        CrossSectionLocation(
            id=1,
            reference_level=10.0,
            bank_level=12.0,
            y_ordinates=y,
            z_ordinates=z,
            geometry=Point(channel.geometry.coords[0]),
        )
    )

    y, z = parse_cross_section_table(
        table="0.0, 3.0\n"
              "2.0, 0.0\n"
              "4.0, 1.0\n"
              "6.0, 3.0",
        cross_section_shape=SupportedShape.YZ.value
    )

    cross_section_locations.append(
        CrossSectionLocation(
            id=2,
            reference_level=10.0,
            bank_level=12.0,
            y_ordinates=y,
            z_ordinates=z,
            geometry=Point(channel.geometry.coords[3]),
        )
    )
    for xsec in cross_section_locations:
        channel.add_cross_section_location(xsec)

    if plot:
        plot_channel_and_sections(
            channel, cross_section_locations,
            title="Curved channel with 2 cross-sections with different widths"
        )
    expected_geometry_wkb = (
        b'\x01\x03\x00\x00\x00\x01\x00\x00\x00W\x00\x00\x00\xafo\x87v\xbe\x04\xe0\xbf\xe9\x0c=\xa1B:\xf2\xbf)<\xe7I'
        b'\x94\xad\xe4\xbf\x91\xb6YB\xca\xe1\xf1\xbf('
        b'\xd5_\xd6S?\xe9\xbfq\xd3tgIO\xf1\xbf\xf0\x9cB0\xb9\xae\xed\xbf\x01\x1b\xc6A)\x84\xf0\xbfJk\xa2\x8ej\xf8'
        b'\xf0\xbf\xa4~\x017\xbd\x04\xef\xbf\x88\x9d\xe2\x04\x94\xfd\xf2\xbf\x90TV\n\xca\x98\xec\xbfS\xa5f\xf5\xdd'
        b'\xe1\xf4\xbf\xfe\x04`mq\xca\xe9\xbf\xcc;\x7ff\x9e\xa0\xf6\xbf\xce;\x7ff\x9e\xa0\xe6\xbfd\xa0\xef\xe9\x875'
        b'\xf8\xbf\xdb\x0eN\x84\x1d#\xe3\xbf.\xc8j8\xb4\x9c\xf9\xbf\x8c\xfe\x8bF\x13\xb5\xde\xbf7]\xc0\xce\xad\xd2'
        b'\xfa\xbf\x905\x8bmm\xa0\xd6\xbf\xe7\xb8\x05ux\xd4\xfb\xbf\x98\x84\r\'k8\xcc\xbfWq\xb4\x9a\x98\x9f\xfc\xbf'
        b'\xf4\xca\x04\x7f\xab\xf5\xb4\xbfwT\x99u\x192\xfd\xbf\xd8\xf9\x7f\xc9\xa10\xaf?\xcf\xaa|\xd4\x91\x8a\xfd'
        b'\xbfk0\xdf\xbf\x7fo\xca?\xf3\xce\x9f\x99\'\xa8\xfd\xbf\xc9;\x7ff\x9e\xa0\xd6?\xcf\xaa|\xd4\x91\x8a\xfd\xbf'
        b'\xaeo\x87v\xbe\x04\xe0?wT\x99u\x192\xfd\xbf+<\xe7I\x94\xad\xe4?Wq\xb4\x9a\x98\x9f\xfc\xbf\'\xd5_\xd6S?\xe9'
        b'?\xe8\xb8\x05ux\xd4\xfb\xbf\xef\x9cB0\xb9\xae\xed?8]\xc0\xce\xad\xd2\xfa\xbfIk\xa2\x8ej\xf8\xf0?/\xc8j8'
        b'\xb4\x9c\xf9\xbf\x88\x9d\xe2\x04\x94\xfd\xf2?e\xa0\xef\xe9\x875\xf8\xbfR\xa5f\xf5\xdd\xe1\xf4?\xcd;\x7ff'
        b'\x9e\xa0\xf6\xbf\xcc;\x7ff\x9e\xa0\xf6?\xa9\xd9g\x1a\xba\xf2\x1f@CFQX\x9b\xa1%@\xbdZ"\xfa\x93\xfd\x1f@\xd5'
        b'\xaaw\xb1\x89\x053@\xcc;\x7ff\x9e\xa0\xf6\xbfC\x0c\x98\x19\xf6\x95<@\xfc\x04`mq\xca\xf9\xbf\x12\x1f\xbb'
        b'\'\xce\xcd<@\x90TV\n\xca\x98\xfc\xbf\x0b\xa0\xcbeW\n=@\xa2~\x017\xbd\x04\xff\xbfS\xa6\x93\x94\xfcJ=@\x01'
        b'\x1b\xc6A)\x84\x00\xc0\xed\xc9cS\x1e\x8f=@q\xd3tgIO\x01\xc0j\xf6\x01\xa9\x14\xd6=@\x91\xb6YB\xca\xe1\x01'
        b'\xc0\xf9\x7f\xc9\xa10\x1f>@\xe9\x0c=\xa1B:\x02\xc0\xc1|\xff\xfe\xbdi>@\r1`f\xd8W\x02\xc0\xde\xf93\xf3\x04'
        b'\xb5>@\xe9\x0c=\xa1B:\x02\xc0\xfavh\xe7K\x00?@\x91\xb6YB\xca\xe1\x01\xc0\xc2s\x9eD\xd9J?@q\xd3tgIO\x01'
        b'\xc0R\xfde=\xf5\x93?@\x02\x1b\xc6A)\x84\x00\xc0\xcf)\x04\x93\xeb\xda?@\xa4~\x017\xbd\x04\xff\xbf\xb4&\xea'
        b'\xa8\x86\x0f@@\x92TV\n\xca\x98\xfc\xbf\xd8)N@\xd9/@@\xfe\x04`mq\xca\xf9\xbfUjV\xdf\x1dN@@\xce;\x7ff\x9e'
        b'\xa0\xf6\xbf\xbd\xf3g\xe6\tj@@\xe1\x0eN\x84\x1d#\xf3\xbf\x06\xfa\x9e~X\x83@@\x8c\xfe\x8bF\x13\xb5\xee\xbf'
        b'\x83\xac\x86C\xcb\x99@@\x925\x8bmm\xa0\xe6\xbf\xd3\x05\xec\xdc*\xad@@\xb0\x84\r\'k8\xdc\xbf\x8e['
        b'P\x87G\xbd@@\xf8\xca\x04\x7f\xab\xf5\xc4\xbf\x15G\xab\x89\xf9\xc9@@\xc8\xf9\x7f\xc9\xa10\xbf?G\x95Y\x97'
        b'!\xd3@@\x7f0\xdf\xbf\x7fo\xda?\xad\xcaG\x1d\xa9\xd8@@\xc7;\x7ff\x9e\xa0\xe6?\xef\xfc\x99y\x82\xda@@\xa7o'
        b'\x87v\xbe\x04\xf0?\xad\xcaG\x1d\xa9\xd8@@*<\xe7I\x94\xad\xf4?G\x95Y\x97!\xd3@@&\xd5_\xd6S?\xf9?\x15G\xab'
        b'\x89\xf9\xc9@@\xf3\x9cB0\xb9\xae\xfd?\x8e['
        b'P\x87G\xbd@@Ik\xa2\x8ej\xf8\x00@\xd3\x05\xec\xdc*\xad@@\x87\x9d\xe2\x04\x94\xfd\x02@\x83\xac\x86C\xcb\x99'
        b'@@T\xa5f\xf5\xdd\xe1\x04@\x06\xfa\x9e~X\x83@@\xcb;\x7ff\x9e\xa0\x06@\xbd\xf3g\xe6\tj@@a\xa0\xef\xe9\x875'
        b'\x08@UjV\xdf\x1dN@@\x85d\xeb\x9d\xcb\xab(@\x1e\x07\xfe\t\xd2\x925@|\xc0\xb2\x00\x01\xf5('
        b'@sZL\x1fwa5@DOQD/4)@\x8a\xe5\xba\x8e\xc2,5@\x8e\x99l\xa4\xbah)@\x929 '
        b'I6\xf54@\xcc\x94\xba\x95!\x92)@\xb8xmA['
        b'\xbb4@s\x12c\x05\xfe\xaf)@eR\x0b\x1b\xc0\x7f4@LA\xa7T\x06\xc2)@\xfc10\xca\xf7B4@\xc8\xd1b\x0e\x0e\xc8'
        b')@\x85\x9f\x92)\x98\x054@LA\xa7T\x06\xc2)@\x0e\r\xf5\x888\xc83@\\Wn\xa5!+('
        b'@\x9f\x85\xff\\V\x86#@\xd4E\x1d\xd1\xfc\x1b(@\x1a\xd0\x13\xe7> #@N\xee\xaf\xee\xe8\x02('
        b'@\x10\x80\x81I!\xbc"@bd\xdc\xd1#\xe0\'@O|\x0cX\xf4Z"@K\xac\x9d3\x03\xb4\'@pi\xd1\xa6\xa7\xfd!@/#\xdc\xde'
        b'\xf3~\'@k@\x9c;!\xa5!@:P5\xa4xA\'@\xd4\x16\xceV;R!@\x8ddx\x17)\xfc&@\x13>HY\xc2\x05!@\xcc\x8b\xf2\x19\xb0'
        b'\xaf&@gR\x8b\xccr\xc0 @\xdb\x0eN\x84\x1d#\xe3?\xfa\x04`mq\xca\xe9\xbf\x90\xfe\x8bF\x13\xb5\xde?\x8eTV\n'
        b'\xca\x98\xec\xbf\x905\x8bmm\xa0\xd6?\xa2~\x017\xbd\x04\xef\xbf\x94\x84\r\'k8\xcc?\x01\x1b\xc6A)\x84\xf0'
        b'\xbf\xf0\xca\x04\x7f\xab\xf5\xb4?q\xd3tgIO\xf1\xbf\x10\xfa\x7f\xc9\xa10\xaf\xbf\x91\xb6YB\xca\xe1\xf1'
        b'\xbfn0\xdf\xbf\x7fo\xca\xbf\xe9\x0c=\xa1B:\xf2\xbf\xca;\x7ff\x9e\xa0\xd6\xbf\r1`f\xd8W\xf2\xbf\xafo\x87v'
        b'\xbe\x04\xe0\xbf\xe9\x0c=\xa1B:\xf2\xbf'
    )
    expected_geometry = wkb.loads(expected_geometry_wkb)
    intersection = channel.outline.intersection(expected_geometry)
    assert abs(intersection.area - channel.outline.area) < 0.01


def test_channel_parallel_offsets():
    channel = get_test_channel()
    xsec = get_test_cross_section_location()
    channel.add_cross_section_location(xsec)
    channel.generate_parallel_offsets()
    assert len(channel.parallel_offsets) == 5
    offset_distances = [po.offset_distance for po in channel.parallel_offsets]
    assert offset_distances == [-2.0, -1.0, 0.0, 1.0, 2.0]
    assert (channel.unique_offsets == offset_distances).all()

    # Parallel offset 1 is 1 m to the right of the channel geometry
    po1 = channel.parallel_offsets[1]
    heights_at_vertices = po1.heights_at_vertices
    assert np.all(heights_at_vertices == np.array([11.0, 11.0]))
    # print([str(point.geom) for point in po1.points])
    assert [str(point.geom) for point in po1.points] == [
        'POINT Z (0.7071067811865475 -0.7071067811865475 11)',
        'POINT Z (2.7071067811865475 1.2928932188134525 11)'
    ]

    # Parallel offset 5 is 2 m to the right of the channel geometry
    po5 = channel.parallel_offsets[4]
    heights_at_vertices = po5.heights_at_vertices
    assert np.all(heights_at_vertices == np.array([12.0, 12.0]))
    points_str = [str(point.geom) for point in po5.points]
    assert points_str == [
        "POINT Z (-1.414213562373095 1.414213562373095 12)",
        "POINT Z (0.5857864376269051 3.414213562373095 12)",
    ]


def test_channel_split(plot: bool = False):
    if plot:
        import matplotlib.pyplot as plt

        def plot_it(channel: Channel, split_idx: int, title=""):
            """
            Plot a Channel (with .geometry as LineString),
            its cross-section locations (fractions along the length),
            and the split point defined by a vertex index.

            Parameters
            ----------
            channel : Channel
                An object with:
                  - .geometry : shapely LineString
                  - .cross_section_locations : list of floats in [0, 1]
            split_idx : int
                Index of the channel vertex to highlight as the split point.
            """
            channel_geom: LineString = channel.geometry

            # Validate index
            if split_idx < 0 or split_idx >= len(channel_geom.coords):
                raise IndexError(
                    f"split_idx {split_idx} out of range for channel with {len(channel_geom.coords)} vertices.")

            # Compute split point
            split_point = Point(channel_geom.coords[split_idx])

            # Compute cross section points
            cross_section_points = [
                channel_geom.interpolate(f, normalized=False)
                for f in channel.cross_section_location_positions
            ]

            # --- Plotting ---
            fig, ax = plt.subplots(figsize=(8, 4))

            # Plot channel
            x, y = channel_geom.xy
            ax.plot(x, y, color="blue", linewidth=2, label="Channel")

            # Plot cross-section points
            if cross_section_points:
                ax.scatter(
                    [p.x for p in cross_section_points],
                    [p.y for p in cross_section_points],
                    color="green", s=50, zorder=3, label="Cross Sections"
                )

            # Plot split point
            ax.scatter(
                split_point.x, split_point.y,
                color="red", s=80, zorder=3,
                label=f"Split Point (index {split_idx})"
            )

            # Decorations
            ax.legend()
            ax.set_aspect("equal", "box")
            ax.set_title(title)

            plt.show()

    # CASES

    # - Split point is at first vertex
    channel = get_test_channel(6)
    split_idx = 0
    split_channel = channel.split(split_idx)
    if plot:
        plot_it(channel, split_idx, title="Split point is at first vertex")
    assert split_channel == (None, channel)

    # Split point is at last vertex
    channel = get_test_channel(6)
    split_idx = len(channel.geometry.coords) - 1
    split_channel = channel.split(split_idx)
    if plot:
        plot_it(channel, split_idx, title="Split point is at last vertex")
    assert split_channel == (channel, None)

    # Split point is before the cross-section location
    channel = get_test_channel(6)
    xsec = get_test_cross_section_location()
    xsec.geometry = Point(channel.geometry.coords[15])
    channel.add_cross_section_location(xsec)
    split_idx = 10
    split_channel = channel.split(split_idx)
    if plot:
        plot_it(channel, split_idx, title="Split point is before the cross-section location")
    # - output types
    assert all([isinstance(part, Channel) for part in split_channel])

    # - geometry
    # print([len(part.geometry.coords) for part in split_channel])
    assert len(split_channel[0].geometry.coords) == split_idx + 1
    assert len(split_channel[1].geometry.coords) == len(channel.geometry.coords) - split_idx

    # - cross-section locations
    assert len(split_channel[0].cross_section_locations) == 1
    assert len(split_channel[1].cross_section_locations) == 1
    assert cross_section_locations_are_equal(split_channel[0].cross_section_locations[0], xsec)
    assert cross_section_locations_are_equal(split_channel[1].cross_section_locations[0], xsec)

    # - cross-section location positions
    assert np.array_equal(split_channel[0].cross_section_location_positions, channel.cross_section_location_positions)
    assert np.array_equal(
        split_channel[1].cross_section_location_positions,
        channel.cross_section_location_positions - split_channel[0].geometry.length
    )

    # - ID
    assert split_channel[0].id == channel.id
    assert split_channel[1].id == (channel.id[0], channel.id[1] + 1)

    # - connection_node id start and connection_node id end
    assert split_channel[0].connection_node_id_start == channel.connection_node_id_start
    assert split_channel[0].connection_node_id_end == (channel.connection_node_id_start[0],
                                                       channel.connection_node_id_start[1] + 1)
    assert split_channel[1].connection_node_id_start == split_channel[0].connection_node_id_end
    assert split_channel[1].connection_node_id_end == channel.connection_node_id_end

    # - Split point is after the cross-section location
    channel = get_test_channel(6)
    xsec = get_test_cross_section_location()
    xsec.geometry = Point(channel.geometry.coords[15])
    channel.add_cross_section_location(xsec)
    split_idx = 16
    split_channel = channel.split(split_idx)

    if plot:
        plot_it(channel, split_idx, title="Split point is after the cross-section location")

    # - output types
    assert all([isinstance(part, Channel) for part in split_channel])

    # - geometry
    assert len(split_channel[0].geometry.coords) == split_idx + 1
    assert len(split_channel[1].geometry.coords) == len(channel.geometry.coords) - split_idx

    # - cross-section locations
    assert len(split_channel[0].cross_section_locations) == 1
    assert len(split_channel[1].cross_section_locations) == 1
    assert cross_section_locations_are_equal(split_channel[0].cross_section_locations[0], xsec)
    assert cross_section_locations_are_equal(split_channel[1].cross_section_locations[0], xsec)

    # - cross-section location positions
    assert np.array_equal(split_channel[0].cross_section_location_positions, channel.cross_section_location_positions)
    assert np.array_equal(
        split_channel[1].cross_section_location_positions,
        channel.cross_section_location_positions - split_channel[0].geometry.length
    )

    # - ID
    assert split_channel[0].id == channel.id
    assert split_channel[1].id == (channel.id[0], channel.id[1] + 1)

    # - connection_node id start and connection_node id end
    assert split_channel[0].connection_node_id_start == channel.connection_node_id_start
    assert split_channel[0].connection_node_id_end == (channel.connection_node_id_start[0],
                                                       channel.connection_node_id_start[1] + 1)
    assert split_channel[1].connection_node_id_start == split_channel[0].connection_node_id_end
    assert split_channel[1].connection_node_id_end == channel.connection_node_id_end

    # Split point is in between two cross-section locations
    channel = get_test_channel(6)
    for i, idx in enumerate([5, 15]):
        xsec = get_test_cross_section_location()
        xsec.geometry = Point(channel.geometry.coords[idx])
        xsec.id = i
        channel.add_cross_section_location(xsec)
    split_idx = 10
    split_channel = channel.split(split_idx)

    if plot:
        plot_it(channel, split_idx, title="Split point is in between two cross-section locations")

    # - output types
    assert all([isinstance(part, Channel) for part in split_channel])

    # - geometry
    assert len(split_channel[0].geometry.coords) == split_idx + 1
    assert len(split_channel[1].geometry.coords) == len(channel.geometry.coords) - split_idx

    # - cross-section locations
    assert len(split_channel[0].cross_section_locations) == 2
    assert len(split_channel[1].cross_section_locations) == 2
    assert cross_section_locations_are_equal(split_channel[0].cross_section_locations[0],
                                             channel.cross_section_locations[0])
    assert cross_section_locations_are_equal(split_channel[0].cross_section_locations[1],
                                             channel.cross_section_locations[1])
    assert cross_section_locations_are_equal(split_channel[1].cross_section_locations[0],
                                             channel.cross_section_locations[0])
    assert cross_section_locations_are_equal(split_channel[1].cross_section_locations[1],
                                             channel.cross_section_locations[1])

    # - cross-section location positions
    assert np.allclose(split_channel[0].cross_section_location_positions, channel.cross_section_location_positions)
    assert np.allclose(
        split_channel[1].cross_section_location_positions,
        channel.cross_section_location_positions - split_channel[0].geometry.length
    )

    # - ID
    assert split_channel[0].id == channel.id
    assert split_channel[1].id == (channel.id[0], channel.id[1] + 1)

    # - connection_node id start and connection_node id end
    assert split_channel[0].connection_node_id_start == channel.connection_node_id_start
    assert split_channel[0].connection_node_id_end == (channel.connection_node_id_start[0],
                                                       channel.connection_node_id_start[1] + 1)
    assert split_channel[1].connection_node_id_start == split_channel[0].connection_node_id_end
    assert split_channel[1].connection_node_id_end == channel.connection_node_id_end

    # Two cross-section locations after the split point
    channel = get_test_channel(6)
    for i, idx in enumerate([5, 15]):
        xsec = get_test_cross_section_location()
        xsec.geometry = Point(channel.geometry.coords[idx])
        xsec.id = i
        channel.add_cross_section_location(xsec)
    split_idx = 3
    split_channel = channel.split(split_idx)

    if plot:
        plot_it(channel, split_idx, title="Two cross-section locations after the split point")

    # - output types
    assert all([isinstance(part, Channel) for part in split_channel])

    # - geometry
    assert len(split_channel[0].geometry.coords) == split_idx + 1
    assert len(split_channel[1].geometry.coords) == len(channel.geometry.coords) - split_idx

    # - cross-section locations
    assert len(split_channel[0].cross_section_locations) == 1
    assert len(split_channel[1].cross_section_locations) == 2
    assert cross_section_locations_are_equal(split_channel[0].cross_section_locations[0],
                                             channel.cross_section_locations[0])
    assert cross_section_locations_are_equal(split_channel[1].cross_section_locations[0],
                                             channel.cross_section_locations[0])
    assert cross_section_locations_are_equal(split_channel[1].cross_section_locations[1],
                                             channel.cross_section_locations[1])

    # - cross-section location positions
    assert np.allclose(split_channel[0].cross_section_location_positions, channel.cross_section_location_positions[0])
    assert np.allclose(
        split_channel[1].cross_section_location_positions,
        channel.cross_section_location_positions - split_channel[0].geometry.length
    )

    # - ID
    assert split_channel[0].id == channel.id
    assert split_channel[1].id == (channel.id[0], channel.id[1] + 1)

    # - connection_node id start and connection_node id end
    assert split_channel[0].connection_node_id_start == channel.connection_node_id_start
    assert split_channel[0].connection_node_id_end == (channel.connection_node_id_start[0],
                                                       channel.connection_node_id_start[1] + 1)
    assert split_channel[1].connection_node_id_start == split_channel[0].connection_node_id_end
    assert split_channel[1].connection_node_id_end == channel.connection_node_id_end

    # Two cross-section locations before the split point
    channel = get_test_channel(6)
    for i, idx in enumerate([5, 15]):
        xsec = get_test_cross_section_location()
        xsec.geometry = Point(channel.geometry.coords[idx])
        xsec.id = i
        channel.add_cross_section_location(xsec)
    split_idx = 20
    split_channel = channel.split(split_idx)

    if plot:
        plot_it(channel, split_idx, title="Two cross-section locations before the split point")

    # - output types
    assert all([isinstance(part, Channel) for part in split_channel])

    # - geometry
    assert len(split_channel[0].geometry.coords) == split_idx + 1
    assert len(split_channel[1].geometry.coords) == len(channel.geometry.coords) - split_idx

    # - cross-section locations
    assert len(split_channel[0].cross_section_locations) == 2
    assert len(split_channel[1].cross_section_locations) == 1
    assert cross_section_locations_are_equal(split_channel[0].cross_section_locations[0],
                                             channel.cross_section_locations[0])
    assert cross_section_locations_are_equal(split_channel[0].cross_section_locations[1],
                                             channel.cross_section_locations[1])
    assert cross_section_locations_are_equal(split_channel[1].cross_section_locations[0],
                                             channel.cross_section_locations[1])

    # - cross-section location positions
    assert np.allclose(split_channel[0].cross_section_location_positions, channel.cross_section_location_positions)
    assert np.allclose(
        split_channel[1].cross_section_location_positions,
        channel.cross_section_location_positions[1] - split_channel[0].geometry.length
    )

    # - ID
    assert split_channel[0].id == channel.id
    assert split_channel[1].id == (channel.id[0], channel.id[1] + 1)

    # - connection_node id start and connection_node id end
    assert split_channel[0].connection_node_id_start == channel.connection_node_id_start
    assert split_channel[0].connection_node_id_end == (channel.connection_node_id_start[0],
                                                       channel.connection_node_id_start[1] + 1)
    assert split_channel[1].connection_node_id_start == split_channel[0].connection_node_id_end
    assert split_channel[1].connection_node_id_end == channel.connection_node_id_end


def test_two_vertex_channel():
    """Test the edge case where all parallel offsets are only two vertices long"""
    wkt_geometry = "LineString (0 0, 10 10)"
    channel_geom = wkt.loads(wkt_geometry)
    channel = Channel(
        geometry=channel_geom,
        connection_node_id_start=1,
        connection_node_id_end=2,
        id=1,
    )

    y, z = parse_cross_section_table(
        table="0, 1.2\n0.53, 2.1",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )

    cross_section_loc = CrossSectionLocation(
        id=1,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(5, 5),
    )

    channel.add_cross_section_location(cross_section_loc)
    channel.generate_parallel_offsets()
    channel.fill_parallel_offsets()
    # print([tri.geometry.wkt for tri in channel.triangles])
    assert [tri.geometry.wkt for tri in channel.triangles] == [
        'POLYGON Z ((0.7424621202458749 -0.7424621202458749 10.53, 0.4242640687119285 -0.4242640687119285 10, '
        '10.424264068711928 9.575735931288072 10, 0.7424621202458749 -0.7424621202458749 10.53))',
        'POLYGON Z ((0.7424621202458749 -0.7424621202458749 10.53, 10.424264068711928 9.575735931288072 10, '
        '10.742462120245875 9.257537879754125 10.53, 0.7424621202458749 -0.7424621202458749 10.53))',
        'POLYGON Z ((0.4242640687119285 -0.4242640687119285 10, 9.575735931288072 10.424264068711928 10, '
        '10.424264068711928 9.575735931288072 10, 0.4242640687119285 -0.4242640687119285 10))',
        'POLYGON Z ((0.4242640687119285 -0.4242640687119285 10, -0.4242640687119285 0.4242640687119285 10, '
        '9.575735931288072 10.424264068711928 10, 0.4242640687119285 -0.4242640687119285 10))',
        'POLYGON Z ((-0.4242640687119285 0.4242640687119285 10, 9.257537879754125 10.742462120245875 10.53, '
        '9.575735931288072 10.424264068711928 10, -0.4242640687119285 0.4242640687119285 10))',
        'POLYGON Z ((-0.4242640687119285 0.4242640687119285 10, -0.7424621202458749 0.7424621202458749 10.53, '
        '9.257537879754125 10.742462120245875 10.53, -0.4242640687119285 0.4242640687119285 10))'
    ]


def test_cross_section_starting_at_0_0():
    """"Just to check if this does not give an error"""
    wkt_geometry = "LineString (94066.74041438 441349.75156281, 94060.74041445 441355.7515628, 94064.24041445 " \
                   "441359.75156275, 94074.24041445 441372.25156263)"
    channel_geom = wkt.loads(wkt_geometry)
    channel = Channel(
        geometry=channel_geom,
        connection_node_id_start=1,
        connection_node_id_end=2,
        id=1,
    )

    y, z = parse_cross_section_table(
        table="0, 0\n0.53, 15.13\n1.060, 16.666\n1.590, 17.413\n2.120, 24.984\n2.65, 32.00",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )

    cross_section_loc = CrossSectionLocation(
        id=1,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(0, 1),
    )
    channel.add_cross_section_location(cross_section_loc)
    channel.generate_parallel_offsets()


def test_channel_max_width_at():
    channel_geom = LineString([[0, 0], [0, 1], [0, 2], [0, 3]])
    channel = Channel(
        geometry=channel_geom,
        connection_node_id_start=1,
        connection_node_id_end=2,
        id=1,
    )

    y, z = parse_cross_section_table(
        table="0, 0\n1.0, 2.0\n2.0, 4.0",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )

    cross_section_loc = CrossSectionLocation(
        id=1,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(0, 1),
    )

    channel.add_cross_section_location(cross_section_loc)

    y, z = parse_cross_section_table(
        table="0, 0\n1.0, 2.0\n2.0, 8.0",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )

    cross_section_loc = CrossSectionLocation(
        id=2,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(0, 2),
    )
    channel.add_cross_section_location(cross_section_loc)

    assert channel.max_width_at(0.2) == 4.0
    assert channel.max_width_at(0 * channel.geometry.length) == 4.0
    assert channel.max_width_at(0.25 * channel.geometry.length) == 4.0
    assert channel.max_width_at(0.5 * channel.geometry.length) == 6.0
    assert channel.max_width_at(0.75 * channel.geometry.length) == 8.0
    assert channel.max_width_at(1 * channel.geometry.length) == 8.0


def test_parallel_offset_heights_at_vertices():
    """Test method heights_at_vertices of ParallelOffset"""
    channel_geom = LineString([[0, 0], [5, 1], [7, 1], [18, 2], [20, 2], [35, 3]])
    channel = Channel(
        geometry=channel_geom,
        connection_node_id_start=1,
        connection_node_id_end=2,
        id=1,
    )

    y, z = parse_cross_section_table(
        table="0, 0\n1.0, 2.0\n2.0, 4.0",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )
    cross_section_loc = CrossSectionLocation(
        id=1,
        reference_level=2.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(5, 1),
    )
    channel.add_cross_section_location(cross_section_loc)

    y, z = parse_cross_section_table(
        table="0, 0\n1.0, 2.0\n2.0, 8.0",
        cross_section_shape=SupportedShape.TABULATED_TRAPEZIUM.value
    )

    cross_section_loc = CrossSectionLocation(
        id=2,
        reference_level=4.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(20, 2),
    )
    channel.add_cross_section_location(cross_section_loc)
    channel.generate_parallel_offsets()
    po = channel.parallel_offset_at(1.0)
    assert np.allclose(po.heights_at_vertices,
                       np.array([3., 3., 3., 3.00655041, 3.26610821, 4.72680547, 4.73884013, 5., 5.])
                       )


def test_find_wedge_channels():
    wedge_channels = get_wedge_channels()
    assert wedge_channels[0].connection_node_id_start == (2, 0)
    assert wedge_channels[1].connection_node_id_end == (2, 0)


def test_fill_wedge(plot: bool = False):
    if plot:
        import matplotlib.pyplot as plt

        def plot_channel_triangles(channels, ax=None, show=True, title="", highlight: Channel = None):
            """
            Plot triangles for one or more Channels, distinguishing between
            parallel offset and wedge fill triangles.

            Parameters
            ----------
            channels : Channel or list[Channel]
                A single Channel object or a list of Channel objects.
            ax : matplotlib.axes.Axes, optional
                Existing matplotlib Axes to draw on. If None, a new figure is created.
            show : bool, default True
                Whether to call plt.show() after plotting.
            colors : tuple[str, str], default ("lightblue", "salmon")
                Colors to use for (parallel offset triangles, wedge fill triangles).
            """
            if not isinstance(channels, (list, tuple)):
                channels = [channels]

            if ax is None:
                fig, ax = plt.subplots(figsize=(8, 8))

            for channel in channels:
                if channel == highlight:
                    color = "blue"
                    edgecolor = "black"
                    facecolor = "lightblue"
                else:
                    color = "darkgrey"
                    edgecolor = "grey"
                    facecolor = "lightgrey"
                # Parallel offset triangles
                for tri in channel._parallel_offset_triangles:
                    poly = tri.geometry
                    x, y = poly.exterior.xy
                    ax.fill(x, y, alpha=0.5, edgecolor=edgecolor, facecolor=facecolor,
                            label="Parallel offset")

                # Wedge fill triangles
                for tri in channel._wedge_fill_triangles:
                    poly = tri.geometry
                    x, y = poly.exterior.xy
                    ax.fill(x, y, alpha=0.5, edgecolor="red", facecolor="salmon",
                            label="Wedge fill")

                # Plot channel centerline geometry
                line = channel.geometry  # shapely LineString
                x, y = line.xy
                ax.plot(x, y, color=color, linewidth=2.5, label="Channel centerline")

                # Add an arrow at the end
                plt.arrow(
                    x[-2], y[-2],  # start from the second-to-last point
                    x[-1] - x[-2], y[-1] - y[-2],  # direction vector
                    shape="full", lw=0, length_includes_head=True, head_width=2.5, color=color
                )

            ax.set_aspect("equal")
            ax.set_title(title)

            # Avoid duplicate legend entries
            handles, labels = ax.get_legend_handles_labels()
            unique = dict(zip(labels, handles))
            ax.legend(unique.values(), unique.keys())

            if show:
                plt.show()

    # Channels with same, symmetrical cross-section,
    # tail of channel 1 is connected to head of channel 2 | <--<--
    # wedge at left side
    channel_1, channel_2 = get_wedge_channels()
    channel_1.generate_parallel_offsets()
    channel_1.fill_parallel_offsets()
    channel_2.generate_parallel_offsets()
    channel_2.fill_parallel_offsets()

    channel_1.fill_wedge(channel_2)
    if plot:
        plot_channel_triangles(
            channels=[
                channel_1,
                channel_2
            ],
            title="Channels with same, symmetrical cross-section\n"
                  "tail of channel 1 is connected to head of channel 2 | <--<--\n"
                  "wedge at left side",
            highlight=channel_2
        )

    assert len(channel_1._wedge_fill_triangles) == 0
    assert len(channel_2._wedge_fill_triangles) == 3
    assert [tri.geometry.wkt for tri in channel_2._wedge_fill_triangles] == [
        'POLYGON Z ((0 0 10, -0.9805806756909201 0.196116135138184 11, -1 0 11, 0 0 10))',
        'POLYGON Z ((-1 0 11, -0.9805806756909201 0.196116135138184 11, -1.9611613513818402 0.3922322702763681 12, '
        '-1 0 11))',
        'POLYGON Z ((-1 0 11, -1.9611613513818402 0.3922322702763681 12, -2 0 12, -1 0 11))'
    ]

    # Channels with same, asymmetrical cross-section, connected head-to-tail (-->-->), wedge at left side
    channel_1, channel_2 = get_wedge_channels()

    y, z = parse_cross_section_table(
        table="0, 3\n2, 1\n4, 0\n5, 4",
        cross_section_shape=SupportedShape.YZ.value,
        wall_displacement=WALL_DISPLACEMENT
    )
    cross_section_loc = CrossSectionLocation(
        id=1,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(-50, 0),
    )
    channel_1.cross_section_locations = []
    channel_1.parallel_offsets = []
    channel_1._wedge_fill_points = []
    channel_1._wedge_fill_triangles = []
    channel_1._extra_outline = []
    channel_1.add_cross_section_location(cross_section_loc)

    channel_1.generate_parallel_offsets()
    channel_1.fill_parallel_offsets()
    channel_2.generate_parallel_offsets()
    channel_2.fill_parallel_offsets()

    channel_1.fill_wedge(channel_2)

    if plot:
        plot_channel_triangles(
            channels=[channel_1, channel_2],
            title = "Channels with same, asymmetrical cross-section\n"
                    "connected head-to-tail (-->-->)\n"
                    "wedge at left side",
            highlight=channel_2
        )

    assert len(channel_1._wedge_fill_triangles) == 0
    assert len(channel_2._wedge_fill_triangles) == 3
    # print([tri.geometry.wkt for tri in channel_2._wedge_fill_triangles])
    assert [tri.geometry.wkt for tri in channel_2._wedge_fill_triangles] == [
        'POLYGON Z ((0 0 10, -1.9611613513818402 0.3922322702763681 11, -1 0 11, 0 0 10))',
        'POLYGON Z ((-1 0 11, -1.9611613513818402 0.3922322702763681 11, -2 0 12, -1 0 11))',
        'POLYGON Z ((-2 0 12, -1.9611613513818402 0.3922322702763681 11, -3.9223227027636804 0.7844645405527362 13, '
        '-2 0 12))'
    ]

    # Channel has a wedge at both sides
    channel_1, channel_2 = get_wedge_channels()
    channel_3 = get_test_channel(7)

    y, z = parse_cross_section_table(
        table="0, 3\n2, 1\n4, 0\n5, 4",
        cross_section_shape=SupportedShape.YZ.value,
        wall_displacement=WALL_DISPLACEMENT
    )
    cross_section_loc = CrossSectionLocation(
        id=1,
        reference_level=10.0,
        bank_level=12.0,
        y_ordinates=y,
        z_ordinates=z,
        geometry=Point(-50, 0),
    )
    channel_1.cross_section_locations = []
    channel_1.parallel_offsets = []
    channel_1._wedge_fill_points = []
    channel_1._wedge_fill_triangles = []
    channel_1._extra_outline = []
    channel_1.add_cross_section_location(cross_section_loc)
    cross_section_loc_channel_3 = CrossSectionLocation.clone(cross_section_loc)
    cross_section_loc_channel_3.geometry = Point(channel_3.geometry.coords[1])  # put it in the middle
    channel_3.add_cross_section_location(cross_section_loc_channel_3)

    channel_1.generate_parallel_offsets()
    channel_1.fill_parallel_offsets()
    channel_2.generate_parallel_offsets()
    channel_2.fill_parallel_offsets()
    channel_3.generate_parallel_offsets()
    channel_3.fill_parallel_offsets()

    channel_1.fill_wedge(channel_2)
    channel_2.fill_wedge(channel_3)

    if plot:
        plot_channel_triangles(
            channels=[channel_1, channel_2, channel_3],
            title="Channel has a wedge at both sides",
            highlight=channel_2
        )

    assert len(channel_1._wedge_fill_triangles) == 0
    assert len(channel_2._wedge_fill_triangles) == 6
    assert len(channel_3._wedge_fill_triangles) == 0
    # print([tri.geometry.wkt for tri in channel_2._wedge_fill_triangles])
    assert [tri.geometry.wkt for tri in channel_2._wedge_fill_triangles] == [
        'POLYGON Z ((0 0 10, -1.9611613513818402 0.3922322702763681 11, -1 0 11, 0 0 10))',
        'POLYGON Z ((-1 0 11, -1.9611613513818402 0.3922322702763681 11, -2 0 12, -1 0 11))',
        'POLYGON Z ((-2 0 12, -1.9611613513818402 0.3922322702763681 11, -3.9223227027636804 0.7844645405527362 13, '
        '-2 0 12))',
        'POLYGON Z ((20 -100 10, 21.162476387438193 -101.62746694241346 11, 20.928476690885258 -99.62860932364589 11, '
        '20 -100 10))',
        'POLYGON Z ((20.928476690885258 -99.62860932364589 11, 21.162476387438193 -101.62746694241346 11, '
        '21.85695338177052 -99.2572186472918 12, 20.928476690885258 -99.62860932364589 11))',
        'POLYGON Z ((21.85695338177052 -99.2572186472918 12, 21.162476387438193 -101.62746694241346 11, '
        '22.324952774876387 -103.25493388482694 13, 21.85695338177052 -99.2572186472918 12))'
    ]


    # Case drawn in QGIS that lead to errors
    # Channel 1 head connects to channel 2 tail, wedge at right side
    channel_1 = get_test_channel(4)
    xsec = get_test_cross_section_location(4)
    channel_1.add_cross_section_location(xsec)
    channel_1.generate_parallel_offsets()
    channel_1.fill_parallel_offsets()

    channel_2 = get_test_channel(5)
    xsec = get_test_cross_section_location(4)
    channel_2.add_cross_section_location(xsec)
    channel_2.generate_parallel_offsets()
    channel_2.fill_parallel_offsets()

    channel_1.fill_wedge(channel_2)

    if plot:
        plot_channel_triangles(
            channels=[channel_1, channel_2],
            title="Channel 1 head connects to channel 2 tail, wedge at right side",
            highlight=channel_1
        )

    assert len(channel_1._wedge_fill_triangles) == 1
    assert len(channel_2._wedge_fill_triangles) == 0
    # print([tri.geometry.wkt for tri in channel_1._wedge_fill_triangles])
    assert [tri.geometry.wkt for tri in channel_1._wedge_fill_triangles] == [
        'POLYGON Z ((50.84932298251876 0.166422494958816 10, 52.611203192631464 -0.7800330640682285 13, '
        '50.85569237696996 -1.8335673627190487 13, 50.84932298251876 0.166422494958816 10))'
    ]


def test_indexed_point():
    point = IndexedPoint(3.4, 2.4, np.float64(48.3), index=3)
    assert point.index == 3
    assert point.x == 3.4
    assert point.y == 2.4
    assert point.z == 48.3


def test_triangle(plot: bool = False):
    if plot:
        import matplotlib.pyplot as plt

        def plot_triangle_with_lines(triangle, line1, line2, title=""):
            fig, ax = plt.subplots(figsize=(6, 6))
            poly = triangle.geometry
            x, y = poly.exterior.xy
            ax.fill(x, y, alpha=0.5, edgecolor="black", facecolor="lightgreen", label="Triangle")

            x, y = line1.xy
            ax.plot(x, y, color="blue", linewidth=2, label="Line 1")

            x, y = line2.xy
            ax.plot(x, y, color="red", linewidth=2, label="Line 2")

            ax.set_aspect("equal")
            ax.set_title(title)
            ax.legend()
            plt.show()

    # Base triangle
    point_coords = {0: (0, 0), 1: (1, 1), 2: (2, 0)}
    indexed_points = [IndexedPoint(val, index=key) for key, val in point_coords.items()]
    tri = Triangle(indexed_points)
    assert tri.geometry.wkt == "POLYGON ((0 0, 1 1, 2 0, 0 0))"

    # --- Case 0: one line is a Point ---
    line_1 = LineString([(-10, -10), (10, 10)])
    point_line = Point(5, 5)
    if plot:
        plot_triangle_with_lines(tri, line_1, LineString([point_line, point_line]), "Case 0: one line is a Point")
    assert tri.is_between(line_1, point_line)

    # --- Case 1: triangle side crosses one line ---
    line_1 = LineString([(-10, -10), (10, 10)])
    line_2 = LineString([(-9, -10), (11, 10)])
    if plot:
        plot_triangle_with_lines(tri, line_1, line_2, "Case 1: triangle side crosses one line")
    assert not tri.is_between(line_1, line_2)

    # --- Case 2.1: one side shared, needs touches ---
    line_1 = LineString([(-10, -10), (10, 10)])
    line_2 = LineString([(-8, -10), (12, 10)])
    if plot:
        plot_triangle_with_lines(tri, line_1, line_2, "Case 2.1: one side shared, opposite point touches other line")
    assert tri.is_between(line_1, line_2)

    # --- Case 2.1: one side shared, needs touches ---
    line_1 = LineString([(-10, -10), (10, 10)])
    line_2 = LineString([(-6, -10), (14, 10)])
    if plot:
        plot_triangle_with_lines(tri, line_1, line_2,
                                 "Case 2.1: one side shared, opposite point does not touch other line")
    assert not tri.is_between(line_1, line_2)

    # --- Case 2.2: two sides shared ---
    # Sharing both (0,0)-(1,1) and (1,1)-(2,0), leaving (0,0)-(2,0) as non-shared
    line_1 = LineString([(-10, -10), (1, 1)])
    line_2 = LineString([(1, 1), (12, -10)])
    if plot:
        plot_triangle_with_lines(tri, line_1, line_2, "Case 2.2: two sides shared")
    assert tri.is_between(line_1, line_2)

    # --- Lines not next to each other ---
    line_1 = LineString([(-10, -10), (10, 10)])
    line_2 = LineString([(15, 15), (35, 35)])
    if plot:
        plot_triangle_with_lines(tri, line_1, line_2, "Lines not next to each other")
    assert not tri.is_between(line_1, line_2)


def test_triangulate_between(plot: bool = False):
    if plot:
        from typing import List
        import matplotlib.pyplot as plt

        def plot_triangles_and_points(
                triangles: List[Triangle],
                points_a: List[IndexedPoint],
                points_b: List[IndexedPoint],
                title: str = "",
                color_a='blue',
                color_b='red',
                triangle_edge='black',
                triangle_face='none'
        ):
            """
            Plot triangles and two sets of points using matplotlib.

            Parameters
            ----------
            triangles : list of Triangle
                Each Triangle has a .geometry attribute (a shapely Polygon).
            points_a : list of shapely.geometry.Point
                First list of points to plot.
            points_b : list of shapely.geometry.Point
                Second list of points to plot.
            color_a : str, optional
                Color for first set of points.
            color_b : str, optional
                Color for second set of points.
            triangle_edge : str, optional
                Edge color for triangles.
            triangle_face : str, optional
                Face color for triangles (default: none = transparent).
            """

            fig, ax = plt.subplots(figsize=(8, 8))

            # Plot triangles
            for tri in triangles:
                geom = tri.geometry
                x, y = geom.exterior.xy
                ax.fill(x, y, facecolor=triangle_face, edgecolor=triangle_edge, alpha=0.8)

            # Plot first set of points
            if points_a:
                ax.scatter([p.geom.x for p in points_a], [p.geom.y for p in points_a],
                           color=color_a, s=40, label='Points A')

            # Plot second set of points
            if points_b:
                ax.scatter([p.geom.x for p in points_b], [p.geom.y for p in points_b],
                           color=color_b, s=40, marker='x', label='Points B')

            ax.set_aspect('equal', adjustable='box')
            ax.legend()
            ax.set_title(title)
            plt.show()

    # Base case: two parallel lines
    # TODO: add assertions to this case
    points_1 = [
        IndexedPoint(0, 0, 10, index=0),
        IndexedPoint(0, 2, 20, index=1),
        IndexedPoint(0, 4, 30, index=2),
        IndexedPoint(0, 8, 40, index=3),
    ]
    points_2 = [
        IndexedPoint(10, 3, 20, index=5),
        IndexedPoint(10, 6, 30, index=6),
        IndexedPoint(10, 9, 40, index=7),
    ]
    triangles = [triangle for triangle in triangulate_between(
        left_side_points=points_1,
        right_side_points=points_2,
    )]
    if plot:
        plot_triangles_and_points(triangles, points_1, points_2, title="Base case: two parallel lines")
    assert [tri.geometry.wkt for tri in triangles] == [
        'POLYGON Z ((0 0 10, 10 3 20, 0 2 20, 0 0 10))',
        'POLYGON Z ((0 2 20, 10 3 20, 0 4 30, 0 2 20))',
        'POLYGON Z ((0 4 30, 10 3 20, 10 6 30, 0 4 30))',
        'POLYGON Z ((0 4 30, 10 6 30, 0 8 40, 0 4 30))',
        'POLYGON Z ((0 8 40, 10 6 30, 10 9 40, 0 8 40))',
    ]

    # Typical wedge: Both sides have > 1 points, start from the same 0 point
    # TODO: add assertions to this case
    points_1 = [
        IndexedPoint(0, 0, 10, index=0),
        IndexedPoint(0, 2, 20, index=1),
        IndexedPoint(0, 4, 30, index=2),
        IndexedPoint(0, 8, 40, index=3),
    ]
    points_2 = [
        # IndexedPoint(0, 0, 10, index=4),
        IndexedPoint(2, 2, 20, index=5),
        IndexedPoint(4, 4, 30, index=6),
        IndexedPoint(8, 8, 40, index=7),
    ]
    points_2.reverse()
    triangles = [triangle for triangle in triangulate_between(
        left_side_points=points_1,
        right_side_points=points_2,
    )]
    if plot:
        plot_triangles_and_points(
            triangles,
            points_1,
            points_2,
            title="Typical wedge: Both sides have > 1 points, start from the same 0 point"
        )
    assert [tri.geometry.wkt for tri in triangles] == [
        'POLYGON Z ((0 0 10, 2 2 20, 0 2 20, 0 0 10))',
        'POLYGON Z ((0 2 20, 2 2 20, 0 4 30, 0 2 20))',
        'POLYGON Z ((0 4 30, 2 2 20, 4 4 30, 0 4 30))',
        'POLYGON Z ((0 4 30, 4 4 30, 0 8 40, 0 4 30))',
        'POLYGON Z ((0 8 40, 4 4 30, 8 8 40, 0 8 40))'
    ]

    # Side 1 has only 1 point (corner case)
    points_1 = [IndexedPoint(50, 5, 15, index=8)]
    points_2 = [
        IndexedPoint(50, 0, 10, index=5),
        IndexedPoint(45, 2.5, 15, index=9)
    ]
    triangles = [triangle for triangle in triangulate_between(
        left_side_points=points_1,
        right_side_points=points_2,
    )]
    if plot:
        plot_triangles_and_points(
            triangles,
            points_1,
            points_2,
            title="Side 1 has only 1 point (corner case)"
        )
    assert len(triangles) == 1
    assert triangles[0].geometry.wkt == "POLYGON Z ((50 5 15, 50 0 10, 45 2.5 15, 50 5 15))"


if __name__ == "__main__":
    test_parse_cross_section_table()
    test_is_valid_offset()
    test_highest_valid_index_single_offset()
    test_highest_valid_index()
    test_channel_azimuth_at()
    test_cross_section_location_thalweg_y()
    test_cross_section_location_z_at()
    test_channel_vertex_positions()
    test_channel_properties()
    test_channel_outline(True)
    test_channel_parallel_offsets()
    test_channel_split()
    test_two_vertex_channel()
    test_cross_section_starting_at_0_0()
    test_channel_max_width_at()
    test_parallel_offset_heights_at_vertices()
    test_find_wedge_channels()
    test_fill_wedge()
    test_indexed_point()
    test_triangle()
    test_triangulate_between()
