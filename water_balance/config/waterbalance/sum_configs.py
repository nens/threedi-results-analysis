

serie_settings = [
    {
        'name': 'alles',
        'remnant_def_color': '50,50,255',
        'remnant_method': 'gross',
        'items': [{
            'name': '2d flow',
            'default_method': 'gross',
            'order': 1,
            'def_color': '63,81,181',
            'series': ['2d_in', '2d_out'],
        }, {
            'name': '2d boundaries',
            'default_method': 'gross',
            'order': 2,
            'def_color': '156,39,176',
            'series': ['2d_bound_in', '2d_bound_out'],
        }, {
            'name': '1d flow',
            'default_method': 'gross',
            'order': 3,
            'def_color': '0,188,212',
            'series': ['1d_in', '1d_out', ],
        }, {
            'name': '1d boundaries',
            'default_method': 'gross',
            'order': 4,
            'def_color': '156,39,176',
            'series': ['1d_bound_in', '1d_bound_out'],
        }, {
            'name': '1d-2d uitwisseling',
            'default_method': 'gross',
            'order': 5,
            'def_color': '205,220,5',
            'series': ['2d_to_1d_pos', '2d_to_1d_neg'],
        },  {
            'name': '1d-2d flow',
            'default_method': 'gross',
            'order': 5,
            'def_color': '205,220,55',
            'series': ['1d_2d_out', '1d_2d_in'],
        }, {
            'name': 'pompen',
            'default_method': 'gross',
            'order': 6,
            'def_color': '255,235,59',
            'series': ['pump_in', 'pump_out'],
        }, {
            'name': 'neerslag',
            'default_method': 'net',
            'order': 7,
            'def_color': '0,150,136',
            'series': ['rain'],
        }, {
            'name': 'lateraal 1d',
            'default_method': 'net',
            'order': 8,
            'def_color': '76,175,80',
            'series': ['lat_1d'],
        }, {
            'name': 'lateraal 2d',
            'default_method': 'net',
            'order': 9,
            'def_color': '76,175,80',
            'series': ['lat_2d'],
        }, {
            'name': 'infiltratie',
            'default_method': 'net',
            'order': 10,
            'def_color': '121,85,72',
            'series': ['infiltration_rate_simple'],
        }, {
            'name': 'volumeverandering 2d',
            'default_method': 'net',
            'order': 11,
            'def_color': '244,67,54',
            'series': ['d_2d_vol'],
        }, {
            'name': 'volumeverandering 1d',
            'default_method': 'net',
            'order': 12,
            'def_color': '255,152,0',
            'series': ['d_1d_vol'],
        }, {
            'name': 'error',
            'default_method': 'net',
            'order': 13,
            'def_color': '62,69,81',
            'series': ['error_1d_2d', 'error_1d', 'error_2d'],
        }, {
            'name': '2d groundwater flow',
            'default_method': 'gross',
            'order': 2.5,
            'def_color': '0,0,128',
            'series': ['2d_groundwater_in', '2d_groundwater_out'],
        }, {
            'name': 'volumeverandering 2d grondwater',
            'default_method': 'net',
            'order': 11.5,
            'def_color': '100,149,237',
            'series': ['d_2d_groundwater_vol'],
        }, {
            'name': 'leakage',
            'default_method': 'net',
            'order': 10.5,
            'def_color': '221,160,221',
            'series': ['leak'],
        }, {
            'name': 'inflow 1d from rain',
            'default_method': 'net',
            'order': 7.1,
            'def_color': '0,130,136',
            'series': ['inflow'],
        }]
    }, {
        'name': 'hoofdstromen',
        'remnant_def_color': '50,50,255',
        'remnant_method': 'net',
        'items': [{
            'name': '2d flow',
            'default_method': 'gross',
            'order': 1,
            'def_color': '63,81,181',
            'series': ['2d_in', '2d_out', '2d_bound_in', '2d_bound_out', '1d_2d_out'],
        }, {
            'name': '1d flow',
            'default_method': 'gross',
            'order': 2,
            'def_color': '0,188,212',
            'series': ['1d_in', '1d_out', 'pump_in', 'pump_out', '1d_bound_in', '1d_bound_out', '1d_2d_in'],
        }, {
            'name': 'belasting (regen en lateralen)',
            'default_method': 'net',
            'order': 3,
            'def_color': '0,150,136',
            'series': ['rain', 'lat_1d', 'lat_2d', 'inflow'],  # TODO: Add leakage?
        }, {
            'name': 'infiltratie',
            'default_method': 'net',
            'order': 3,
            'def_color': '50,150,136',
            'series': ['infiltration_rate_simple'],
        }, {
            'name': '1d-2d uitwisseling',
            'default_method': 'net',
            'order': 4,
            'def_color': '205,220,57',
            'series': ['2d_to_1d_pos', '2d_to_1d_neg'],
        }, {
            'name': 'volumeverandering',
            'default_method': 'net',
            'order': 5,
            'def_color': '255,152,0',
            'series': ['d_2d_vol', 'd_1d_vol', 'd_2d_groundwater_vol'],
        }, {
            'name': 'error',
            'default_method': 'net',
            'order': 6,
            'def_color': '62,69,81',
            'series': ['error_1d_2d', 'error_1d', 'error_2d'],
        }, {
            'name': '2d groundwater flow',
            'default_method': 'gross',
            'order': 1.5,
            'def_color': '0,0,128',
            'series': ['2d_groundwater_in', '2d_groundwater_out'],
        }, {
            'name': 'leakage',
            'default_method': 'net',
            'order': 3.5,
            'def_color': '221,160,221',
            'series': ['leak'],
        }]
    }
]
