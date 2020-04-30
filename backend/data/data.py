import pandas as pd
import data.utils as utils
import data.datasets as datasets
import unidecode


class Data:

    def __init__(self):
        self.dataset_fns = dict()
        self.init_dataset_fns()
        for dataset_name in datasets.DATASETS:
            for dataset_fn in self.dataset_fns[dataset_name]:
                dataset_fn()

    def init_counties_dataset(self):
        counties_dataset = datasets.get_dataset(datasets.COUNTIES)
        self.counties_df = pd.read_csv(counties_dataset)

    def init_covid_19_nyt_county_dataset(self):
        covid_19_nyt_county_dataset = datasets.get_dataset(
            datasets.COVID_19_NYT_COUNTY)
        self.covid_19_nyt_county_df = pd.read_csv(covid_19_nyt_county_dataset)
        self.covid_19_nyt_county_df = self.covid_19_nyt_county_df.assign(cases_epoch_ms=self.covid_19_nyt_county_df.apply(
            lambda x: utils.data_epoch_ms_dict(x['cases'], 'cases', x['epoch_ms']), axis=1))
        self.covid_19_nyt_county_df = self.covid_19_nyt_county_df.assign(deaths_epoch_ms=self.covid_19_nyt_county_df.apply(
            lambda x: utils.data_epoch_ms_dict(
                x['deaths'], 'deaths', x['epoch_ms']), axis=1
        ))

    def init_covid_19_nyt_state_dataset(self):
        covid_19_nyt_state_dataset = datasets.get_dataset(
            datasets.COVID_19_NYT_STATE)
        self.covid_19_nyt_state_df = pd.read_csv(covid_19_nyt_state_dataset)
        self.covid_19_nyt_state_df = self.covid_19_nyt_state_df.assign(cases_epoch_ms=self.covid_19_nyt_state_df.apply(
            lambda x: utils.data_epoch_ms_dict(x['cases'], 'cases', x['epoch_ms']), axis=1))
        self.covid_19_nyt_state_df = self.covid_19_nyt_state_df.assign(deaths_epoch_ms=self.covid_19_nyt_state_df.apply(
            lambda x: utils.data_epoch_ms_dict(
                x['deaths'], 'deaths', x['epoch_ms']), axis=1
        ))

    def init_hospital_atlas_dataset(self):
        hospital_atlas_dataset = datasets.get_dataset(datasets.HOSPIAL_ATLAS)
        self.hospital_atlas_df = pd.read_csv(hospital_atlas_dataset)

    def init_dataset_fns(self):
        self.dataset_fns[datasets.COUNTIES] = [
            self.init_counties_dataset,
            self.process_counties_dataset
        ]
        self.dataset_fns[datasets.COVID_19_NYT_COUNTY] = [
            self.init_covid_19_nyt_county_dataset,
            self.process_covid_19_nyt_county_dataset
        ]
        self.dataset_fns[datasets.COVID_19_NYT_STATE] = [
            self.init_covid_19_nyt_state_dataset,
            self.process_covid_19_nyt_state_dataset
        ]
        self.dataset_fns[datasets.HOSPIAL_ATLAS] = [
            self.init_hospital_atlas_dataset,
            self.process_hospital_atlas_dataset
        ]

    def process_counties_dataset(self):
        self.states_formatted = self.counties_df['State Formatted'].unique(
        ).tolist()
        self.states = self.counties_df['State'].unique().tolist()
        self.state_to_counties = {}
        self.state_to_counties_formatted = {}
        self.state_county_pop = {}
        for s in self.states:
            state_counties = self.counties_df.loc[self.counties_df['State'] == s]
            self.state_to_counties[s] = state_counties['County']
            self.state_to_counties_formatted[s] = state_counties['County Formatted']
            for c in self.state_to_counties[s]:
                s_c = (s, c)
                self.state_county_pop[s_c] = state_counties.loc[state_counties['County']
                                                                == c]['Population'].values[0]

    def process_covid_19_nyt_county_dataset(self):
        self.state_county_dates = {}
        self.state_county_cases = {}
        self.state_county_deaths = {}
        self.state_county_epochs_ms = {}
        self.state_county_cases_epochs_ms = {}
        self.state_county_deaths_epochs_ms = {}
        self.state_county_last_epoch_ms = {}
        for s in self.states:
            counties = self.state_to_counties[s]
            state_df = self.covid_19_nyt_county_df.loc[self.covid_19_nyt_county_df['state'] == s]
            for c in counties:
                county_df = state_df.loc[state_df['county'] == c]
                s_c = (s, c)
                self.state_county_dates[s_c] = county_df['date']
                self.state_county_epochs_ms[s_c] = county_df['epoch_ms']
                self.state_county_last_epoch_ms[s_c] = utils.calc_last_epoch_ms(
                    county_df['epoch_ms'])
                cases = county_df['cases']
                deaths = county_df['deaths']
                self.state_county_cases[s_c] = cases
                self.state_county_deaths[s_c] = deaths
                self.state_county_cases_epochs_ms[s_c] = county_df['cases_epoch_ms']
                self.state_county_deaths_epochs_ms[s_c] = county_df['deaths_epoch_ms']

    def process_covid_19_nyt_state_dataset(self):
        self.state_dates = {}
        self.state_cases = {}
        self.state_deaths = {}
        self.state_epochs_ms = {}
        self.state_cases_epochs_ms = {}
        self.state_deaths_epochs_ms = {}
        self.state_last_epoch_ms = {}
        for s in self.states:
            state_df = self.covid_19_nyt_state_df.loc[self.covid_19_nyt_state_df['state'] == s]
            self.state_dates[s] = state_df['date']
            self.state_epochs_ms[s] = state_df['epoch_ms']
            self.state_last_epoch_ms[s] = utils.calc_last_epoch_ms(
                state_df['epoch_ms'])
            cases = state_df['cases']
            deaths = state_df['deaths']
            self.state_cases[s] = cases
            self.state_deaths[s] = deaths
            self.state_cases_epochs_ms[s] = state_df['cases_epoch_ms']
            self.state_deaths_epochs_ms[s] = state_df['deaths_epoch_ms']

    def process_hospital_atlas_dataset(self):
        self.state_county_bed_data = {}
        for s in self.states:
            counties = self.state_to_counties[s]
            state_hospitals_df = self.hospital_atlas_df.loc[self.hospital_atlas_df['STATE'] == s]
            for c in counties:
                county_beds_total = state_hospitals_df.loc[state_hospitals_df['COUNTY'] == c]['TOTAL_BEDS'].sum(
                )
                s_c_t = (s, c, 'total')
                self.state_county_bed_data[s_c_t] = county_beds_total
