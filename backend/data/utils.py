from datetime import datetime
import numpy as np
import time

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

KC_COUNTIES = {
    "Jackson",
    "Clay",
    "Platte",
    "Cass"
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
        'epoch_ms': int(epoch_ms)
    }


def remove_parish_from_name(county):
    return county.replace(" Parish", "")


def remove_county_from_name(county):
    return county.replace(" County", "")


def remove_municipality_from_name(county):
    return county.replace(" Municipality", "")


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


def is_kc_county(state, county):
    # Special case for Kansas City. Kansas city encompases several counties
    # so we're going to remove those and replace them with Kansas City to match
    # the NYT dataset
    return state == "Missouri" and county in KC_COUNTIES


def gradient_descent_beta(cases_s, pop):
    beta = 0
    gamma = GAMMA
    step_size = 1
    cases = cases_s.values
    I_t = cases[0]
    S_t = pop - I_t
    for i in range(0, 5):
        step_size = step_size / 100000
        for c in cases[1:]:
            I_hyp = I_t + beta*S_t*I_t - gamma*I_t

            print("I hypothesis: {}".format(I_hyp))
            I_data = c
            I_L = I_data - I_hyp
            I_grad_beta = 2*I_L*-1*S_t*I_t
            I_grad_gamma = 2*I_L*I_t
            beta = beta - step_size*I_grad_beta
            gamma = gamma - step_size*I_grad_gamma
            #S_t = S_t - beta*S_t*I_t
            I_t = c
    print("BETA: {}, GAMMA: {}".format(beta, gamma))


def beta_est(cases_s, pop, start_ms):
    cases = cases_s.values
    beta_ests = np.linspace(GAMMA/20, 7*GAMMA, 50)
    beta_est = GAMMA
    min_err = 10**20
    lim = min(7, len(cases))
    for b in beta_ests:
        err = 0
        I_t = cases[len(cases) - lim]
        S_t = pop - I_t
        for c in cases[-1*lim:]:
            I_est = I_t + b*S_t*I_t - GAMMA*I_t
            err = err + (c - I_est)**2
            I_t = c
            S_t = pop - I_t
        avg_err = err / len(cases[1:])
        if avg_err < min_err:
            min_err = avg_err
            beta_est = b
    print("BETA: {}, min eror: {}".format(beta_est, min_err))
# From https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/


def data_list_epoch_ms_dict(data_list, label, epochs_ms):
    assert(len(data_list) == len(epochs_ms))
    return [data_epoch_ms_dict(data_list[i], label, epochs_ms[i]) for i in range(len(data_list))]


def calc_last_epoch_ms(epochs_ms):
    if len(epochs_ms) == 0:
        return int(time.time())*1000
    return epochs_ms.iloc[-1]
