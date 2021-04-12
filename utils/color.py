from collections import namedtuple

ColorRampData = namedtuple("ColorRampData", ["name", "colors", "info"])

COLOR_RAMP_OCEAN_DEEP = ColorRampData(
    'Ocean Deep',
    [
        '#ffffcc',
        '#a1dab4',
        '#41b6c4',
        '#2c7fb8',
        '#253494',
        '#0d1336'
    ],
    {'source': 'Thyng, K.M., C.A. Greene, R.D. Hetland, H.M. Zimmerle, and S.F. DiMarco (2016). True colors of '
               'oceanography: Guidelines for effective and accurate colormap selection. Oceanography, 29(3):9-13, '
               'http://dx.doi.org/10.5670/oceanog.2016.66.'
     }
)

COLOR_RAMP_OCEAN_HALINE = ColorRampData(
    'Ocean Haline',
    [
        '#231067',
        '#2c1d90',
        '#19399f',
        '#0c5094',
        '#15628d',
        '#237289',
        '#308088',
        '#3a9187',
        '#45a383',
        '#53b47a',
        '#69c26e',
        '#8dd05f',
        '#b7da60',
        '#dce378',
        '#fdf2ae'
    ],
    {'source': 'Thyng, K.M., C.A. Greene, R.D. Hetland, H.M. Zimmerle, and S.F. DiMarco (2016). True colors of '
               'oceanography: Guidelines for effective and accurate colormap selection. Oceanography, 29(3):9-13, '
               'http://dx.doi.org/10.5670/oceanog.2016.66.'
     }
)

COLOR_RAMP_OCEAN_CURL = ColorRampData(
    'Ocean Curl',
    [
        '#0D163E',
        '#1B3E57',
        '#185F6A',
        '#1B8179',
        '#4B9F84',
        '#8FBA99',
        '#CBD5C1',
        '#FAF1EE',
        '#EAC5B4',
        '#DD9983',
        '#CC6C67',
        '#B24560',
        '#8D2560',
        '#611554',
        '#330C34'
    ],
    {'source': 'Thyng, K.M., C.A. Greene, R.D. Hetland, H.M. Zimmerle, and S.F. DiMarco (2016). True colors of '
               'oceanography: Guidelines for effective and accurate colormap selection. Oceanography, 29(3):9-13, '
               'http://dx.doi.org/10.5670/oceanog.2016.66.'
     }
)

COLOR_RAMPS = [
    COLOR_RAMP_OCEAN_DEEP,
    COLOR_RAMP_OCEAN_HALINE,
    COLOR_RAMP_OCEAN_CURL
]
