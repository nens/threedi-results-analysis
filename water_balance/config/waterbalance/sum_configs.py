
# Qt linestyles, linecolors etc
# http://pyqt.sourceforge.net/Docs/PyQt4/qpen.html

# QColor constructed from the given CMYK color values:
# c (cyan), m (magenta), y (yellow), k (black), and a (alpha-channel,
# i.e. transparency (0=totally transparant)).
# all numbers are integers between 0-256

fill_transp = ',' + str(150)
pen_transp = ',' + str(180)
fill_transp_vol_change = ',' + str(0)

serie_settings = [
    {
        'name': 'everything',
        'remnant_fill_color': '50,50,255' + fill_transp,
        'remnant_method': 'gross',
        'items': [{
            'name': '2d flow',
            'default_method': 'gross',
            'order': 1,
            'def_fill_color': '63,81,181' + fill_transp,
            'def_pen_color': '63,81,181' + pen_transp,
            'series': ['2d_in', '2d_out'],
        }, {
            'name': '2d boundaries',
            'default_method': 'gross',
            'order': 2,
            'def_fill_color': '156,39,176' + fill_transp,
            'def_pen_color': '156,39,176' + pen_transp,
            'series': ['2d_bound_in', '2d_bound_out'],
        }, {
            'name': '1d flow',
            'default_method': 'gross',
            'order': 3,
            'def_fill_color': '0,188,212' + fill_transp,
            'def_pen_color': '0,188,212' + pen_transp,
            'series': ['1d_in', '1d_out', ],
        }, {
            'name': '1d boundaries',
            'default_method': 'gross',
            'order': 4,
            'def_fill_color': '156,39,176' + fill_transp,
            'def_pen_color': '156,39,176' + pen_transp,
            'series': ['1d_bound_in', '1d_bound_out'],
        }, {
            'name': '1d-2d exchange (2d to 1d)',
            'default_method': 'gross',
            'order': 5,
            'def_fill_color': '240,210,50' + fill_transp,
            'def_pen_color': '240,210,50' + pen_transp,
            'series': ['1d__1d_2d_exch_in', '1d__1d_2d_exch_out'],
         },  {
            'name': '1d-2d flow (2d to 1d)',
            'default_method': 'gross',
            'order': 5,
            'def_fill_color': '100,220,5' + fill_transp,
            'def_pen_color': '100,220,5' + pen_transp,
            'series': ['1d__1d_2d_flow_in', '1d__1d_2d_flow_out',
                       '2d__1d_2d_flow_in', '2d__1d_2d_flow_out'],
        },  {
            'name': 'pumps',
            'default_method': 'gross',
            'order': 6,
            'def_fill_color': '255,235,59' + fill_transp,
            'def_pen_color': '255,235,59' + pen_transp,
            'series': ['pump_in', 'pump_out'],
        }, {
            'name': 'rain',
            'default_method': 'net',
            'order': 7,
            'def_fill_color': '0,150,136' + fill_transp,
            'def_pen_color': '0,150,136' + pen_transp,
            'series': ['rain'],
        }, {
            'name': 'lateral 1d',
            'default_method': 'net',
            'order': 8,
            'def_fill_color': '76,175,80' + fill_transp,
            'def_pen_color': '76,175,80' + pen_transp,
            'series': ['lat_1d'],
        }, {
            'name': 'lateral 2d',
            'default_method': 'net',
            'order': 9,
            'def_fill_color': '176,175,80' + fill_transp,
            'def_pen_color': '176,175,80' + pen_transp,
            'series': ['lat_2d'],
        }, {
            'name': 'infiltration',
            'default_method': 'net',
            'order': 10,
            'def_fill_color': '121,85,72' + fill_transp,
            'def_pen_color': '121,85,72' + pen_transp,
            'series': ['infiltration_rate_simple'],
        }, {
            'name': 'volume change 2d',
            'default_method': 'net',
            'order': 11,
            'def_fill_color': '244,67,54' + fill_transp_vol_change,
            'def_pen_color': '244,67,54' + pen_transp,
            'series': ['d_2d_vol'],
        }, {
            'name': 'volume change 1d',
            'default_method': 'net',
            'order': 12,
            'def_fill_color': '255,152,0' + fill_transp_vol_change,
            'def_pen_color': '255,152,0' + pen_transp,
            'series': ['d_1d_vol'],
        }, {
            'name': '2d groundwater flow',
            'default_method': 'gross',
            'order': 2.5,
            'def_fill_color': '0,0,128' + fill_transp,
            'def_pen_color': '0,0,128' + pen_transp,
            'series': ['2d_groundwater_in', '2d_groundwater_out'],
        }, {
            'name': 'volume change 2d groundwater',
            'default_method': 'net',
            'order': 11.5,
            'def_fill_color': '100,149,237' + fill_transp_vol_change,
            'def_pen_color': '100,149,237' + pen_transp,
            'series': ['d_2d_groundwater_vol'],
        }, {
            'name': 'leakage',
            'default_method': 'net',
            'order': 10.5,
            'def_fill_color': '221,160,221' + fill_transp,
            'def_pen_color': '221,160,221' + pen_transp,
            'series': ['leak'],
        }, {
            'name': 'inflow 1d from rain',
            'default_method': 'net',
            'order': 7.1,
            'def_fill_color': '50,130,136' + fill_transp,
            'def_pen_color': '50,130,136' + pen_transp,
            'series': ['inflow'],
        }]
    }, {
        'name': 'main flows',
        'remnant_fill_color': '50,50,255' + fill_transp,
        'remnant_method': 'net',
        'items': [{
            'name': '2d flow',
            'default_method': 'gross',
            'order': 1,
            'def_fill_color': '63,81,181' + fill_transp,
            'def_pen_color': '63,81,181' + pen_transp,
            'series': ['2d_in', '2d_out', '2d_bound_in', '2d_bound_out',
                       '2d__1d_2d_flow_in', '2d__1d_2d_flow_out'],
        }, {
            'name': '1d flow',
            'default_method': 'gross',
            'order': 2,
            'def_fill_color': '0,188,212' + fill_transp,
            'def_pen_color': '0,188,212' + pen_transp,
            'series': ['1d_in', '1d_out', 'pump_in', 'pump_out', '1d_bound_in',
                       '1d_bound_out', '1d__1d_2d_flow_in', '1d__1d_2d_flow_out'],
        }, {
            'name': 'external (rain and laterals)',
            'default_method': 'net',
            'order': 3,
            'def_fill_color': '0,150,136' + fill_transp,
            'def_pen_color': '0,150,136' + pen_transp,
            'series': ['rain', 'lat_1d', 'lat_2d', 'inflow'],
            # TODO: Add leakage?
        }, {
            'name': 'infiltration',
            'default_method': 'net',
            'order': 3,
            'def_fill_color': '50,150,136' + fill_transp,
            'def_pen_color': '50,150,136' + pen_transp,
            'series': ['infiltration_rate_simple'],
        }, {
            'name': '1d-2d exchange (2d to 1d)',
            'default_method': 'gross',
            'order': 5,
            'def_fill_color': '240,210,50' + fill_transp,
            'def_pen_color': '240,210,50' + pen_transp,
            'series': ['1d__1d_2d_exch_in', '1d__1d_2d_exch_out'],
        }, {
            'name': '1d-2d flow (2d to 1d)',
            'default_method': 'gross',
            'order': 5,
            'def_fill_color': '100,220,5' + fill_transp,
            'def_pen_color': '100,220,5' + pen_transp,
            'series': ['1d__1d_2d_flow_in', '1d__1d_2d_flow_out',
                       '2d__1d_2d_flow_in', '2d__1d_2d_flow_out'],
        }, {
            'name': 'volume change',
            'default_method': 'net',
            'order': 5,
            'def_fill_color': '255,152,0' + fill_transp_vol_change,
            'def_pen_color': '255,152,0' + pen_transp,
            'series': ['d_2d_vol', 'd_1d_vol', 'd_2d_groundwater_vol'],
        }, {
            'name': '2d groundwater flow',
            'default_method': 'gross',
            'order': 1.5,
            'def_fill_color': '0,0,128' + fill_transp,
            'def_pen_color': '0,0,128' + pen_transp,
            'series': ['2d_groundwater_in', '2d_groundwater_out'],
        }, {
            'name': 'leakage',
            'default_method': 'net',
            'order': 3.5,
            'def_fill_color': '221,160,221' + fill_transp,
            'def_pen_color': '221,160,221' + pen_transp,
            'series': ['leak'],
        }]
    }
]
