import data.data as data
import data.datasets as datasets
import data.preprocessing as preprocessing
from data.projections import Projections
from urllib.request import urlretrieve
from apscheduler.schedulers.background import BackgroundScheduler


class Controller:

    def __init__(self, logger):
        self.raw_dataset_fetch_fns = dict()
        self.init_raw_dataset_fetch_fns()
        self.init_scheduler()
        self.logger = logger
        self.set_data()

    def init_scheduler(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler.add_job(self.set_data, 'interval', minutes=30)

    def init_raw_dataset_fetch_fns(self):
        self.raw_dataset_fetch_fns[datasets.COUNTIES] = self.fetch_raw_counties
        self.raw_dataset_fetch_fns[datasets.COVID_19_NYT_COUNTY] = self.fetch_raw_covid_19_nyt_county
        self.raw_dataset_fetch_fns[datasets.COVID_19_NYT_STATE] = self.fetch_raw_covid_19_nyt_state

    def fetch_raw_covid_19_nyt_county(self):
        source = datasets.RAW_DATASETS_TO_SOURCES[datasets.COVID_19_NYT_COUNTY]
        dest = datasets.get_raw_dataset(datasets.COVID_19_NYT_COUNTY)
        urlretrieve(source, dest)

    def fetch_raw_covid_19_nyt_state(self):
        source = datasets.RAW_DATASETS_TO_SOURCES[datasets.COVID_19_NYT_STATE]
        dest = datasets.get_raw_dataset(datasets.COVID_19_NYT_STATE)
        urlretrieve(source, dest)

    def fetch_raw_counties(self):
        source = datasets.RAW_DATASETS_TO_SOURCES[datasets.COUNTIES]
        dest = datasets.get_raw_dataset(datasets.COUNTIES)
        urlretrieve(source, dest)

    def fetch_raw_datasets(self):
        for dataset in datasets.RAW_DATASETS:
            self.raw_dataset_fetch_fns[dataset]()

    def preprocess_raw_datasets(self):
        for dataset in datasets.RAW_DATASETS:
            preprocessing.dataset_to_preprocessing[dataset]()

    def set_data(self):
        self.logger.critical("SETTING DATA")
        self.fetch_raw_datasets()
        self.preprocess_raw_datasets()
        self.data = data.Data()
        #self.projections = Projections(self.data)

    def state_county_cases(self, state, county):
        s_c = (state, county)
        return self.data.state_county_cases_epochs_ms[s_c].tolist()

    def state_cases(self, state):
        return self.data.state_cases_epochs_ms[state].tolist()

    def state_county_bed_capacity(self, state, county):
        s_c_t = (state, county, 'total')
        return {
            'total_bed_capacity': int(self.data.state_county_bed_data[s_c_t])
        }

    def state_bed_capacity(self, state):
        return {
            'total_bed_capacity': int(self.data.state_bed_data[state])
        }

    def counties(self, state):
        return ['All'] + self.data.state_to_counties_formatted[state].tolist()

    def get_states_formatted(self):
        return self.data.states_formatted

    def state_county_deaths(self, state, county):
        s_c = (state, county)
        return self.data.state_county_deaths_epochs_ms[s_c].tolist()

    def state_deaths(self, state):
        return self.data.state_deaths_epochs_ms[state].tolist()

    def case_projections(self, state, county):
        s_c = (state, county)
        return self.projections.state_county_case_projections[s_c]
