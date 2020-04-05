import pandas as pd
import utils

# file names
data_prefix = './data/'
cases_csv = data_prefix + 'covid_19_data_nyt.csv'
hospital_suffix = "_hospital_data.csv"
hospital_atlas_csv = data_prefix + "hosp17_atlas.csv"
county_csv = data_prefix + "county_result.csv"


# load csvs
# County Data
county_df = pd.read_csv(county_csv)
states_formatted = county_df['State Formatted'].unique().tolist()
states = county_df['State'].unique().tolist()

# COVID-19 cases
cases_df = pd.read_csv(cases_csv)
cases_df['county'] = cases_df['county'].map(utils.nyc_to_ny)
cases_df['county'] = cases_df['county'].str.upper()
cases_df['county'] = cases_df['county'].str.replace(" ", "")
cases_df['state'] = cases_df['state'].str.upper()
cases_df['state'] = cases_df['state'].str.replace(" ", "")
cases_df = cases_df.assign(
    epoch_ms=cases_df['date'].map(utils.date_string_to_epoch_ms))
cases_df = cases_df.assign(cases_epoch_ms=cases_df.apply(
    lambda x: utils.data_epoch_ms_dict(x['cases'], 'cases', x['epoch_ms']), axis=1))
cases_df = cases_df.assign(deaths_epoch_ms=cases_df.apply(
    lambda x: utils.data_epoch_ms_dict(
        x['deaths'], 'deaths', x['epoch_ms']), axis=1
))


# Hospital Bed Data
atlas_df = pd.read_csv(hospital_atlas_csv)
atlas_df = atlas_df.assign(COUNTY=atlas_df['FCNTYNAME'].map(
    utils.county_from_atlas_fcntyname))
atlas_df = atlas_df.assign(TOTAL_BEDS=atlas_df.apply(
    lambda x: utils.atlas_total_beds(x['AHAbeds'], x['POSbeds']), axis=1))
atlas_df = atlas_df.assign(
    STATE=atlas_df['PSTATE'].map(utils.pstate_to_state))


# We cache the relevant data for the api dictionaries so we have fast lookup


# init county maps
state_to_counties = {}
state_to_counties_formatted = {}

# load counties
for s in states:
    state_counties = county_df.loc[county_df['State'] == s]
    state_to_counties[s] = state_counties['County'].tolist()
    state_to_counties_formatted[s] = state_counties['County Formatted'].tolist(
    )


# init case maps
state_county_dates = {}
state_county_cases = {}
state_county_deaths = {}
state_county_epochs_ms = {}
state_county_cases_epochs_ms = {}
state_county_deaths_epochs_ms = {}

# load case data
for s in states:
    counties = state_to_counties[s]
    state_df = cases_df.loc[cases_df['state'] == s]
    for c in counties:
        county_df = state_df.loc[state_df['county'] == c]
        s_c = (s, c)
        state_county_dates[s_c] = county_df['date']
        state_county_epochs_ms[s_c] = county_df['epoch_ms']
        state_county_cases[s_c] = county_df['cases']
        state_county_deaths[s_c] = county_df['deaths']
        state_county_cases_epochs_ms[s_c] = county_df['cases_epoch_ms'].tolist(
        )
        state_county_deaths_epochs_ms[s_c] = county_df['deaths_epoch_ms'].tolist(
        )

# init hospital maps
state_county_bed_data = {}

for s in states:
    counties = state_to_counties[s]
    state_hospitals_df = atlas_df.loc[atlas_df['STATE'] == s]
    for c in counties:
        county_beds_total = state_hospitals_df.loc[state_hospitals_df['COUNTY'] == c]['TOTAL_BEDS'].sum(
        )
        s_c_t = (s, c, 'total')
        state_county_bed_data[s_c_t] = county_beds_total

        # load hospital bed data
        # for s in states:
        #     if s in states_atlas:
        #         state_to_counties[s] = counties
        #         for c in counties:
        #             s_c = (s, c)
        #             county_df = state_df.loc[state_df['COUNTY_NAME'] == c]
        #             state_county_bed_data[(s, c, 'total')] = county_df.BED_CAPACITY.sum()
        #             bed_types = state_county_bed_types[s_c] = county_df.BED_CAPACITY_TYPE.unique(
        #             )
        #             state_county_bed_types[s_c] = bed_types
        #             for b in bed_types:
        #                 s_c_b = (s, c, b)
        #                 bed_df = county_df.loc[county_df['BED_CAPACITY_TYPE'] == b]
        #                 state_county_bed_data[s_c_b] = bed_df['BED_CAPACITY']

        # state_csv = data_prefix + s + hospital_suffix
        #     state_df_raw = pd.read_csv(state_csv)
        #     state_df_raw['COUNTY_NAME'] = state_df_raw['COUNTY_NAME'].str.replace(
        #         " ", "")
        #     state_df = state_df_raw.groupby(['COUNTY_NAME', 'BED_CAPACITY_TYPE'])[
        #         ['BED_CAPACITY']].agg('sum').reset_index()
        #     counties = state_df.COUNTY_NAME.unique()
