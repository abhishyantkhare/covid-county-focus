from datetime import datetime


states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


def date_string_to_epoch_ms(date_string):
    date_split = date_string.split('-')
    year = int(date_split[0])
    month = int(date_split[1])
    day = int(date_split[2])
    return int(datetime(year, month, day, 0, 0).timestamp())*1000


def data_epoch_ms_dict(data, label, epoch_ms):
    return {
        label: data,
        'epoch_ms': epoch_ms
    }


def remove_county_from_name(county):
    if county[-6:] == 'County':
        return county[:-7]  # Remove ' County' from the end
    return county


def county_from_atlas_fcntyname(fcntyname):
    split_fcntyname = fcntyname.split("-")
    county = remove_county_from_name(split_fcntyname[1])
    return county.replace(" ", "").upper()


def atlas_total_beds(aha_beds, pos_beds):
    return aha_beds + pos_beds


def state_abbr_to_state(abbr):
    return states[abbr]


def pstate_to_state(pstate):
    return state_abbr_to_state(pstate).replace(" ", "").upper()


def nyc_to_ny(county):
    # Special case for New York City. The NYT dataset refers to New York County as New York City, but
    # everywhere else refers to it as New York County
    if county != "New York City":
        return county
    return "New York"
