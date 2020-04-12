import os

COUNTIES = 'counties'
COVID_19_NYT = 'covid_19_nyt'
HOSPIAL_ATLAS = 'hospital_atlas_2017'

# Order matters! List these datasets in the order you'd like them to be processed
DATASETS = [
    COUNTIES,
    COVID_19_NYT,
    HOSPIAL_ATLAS
]

DATA_PREFIX = 'data/datasets/'
FILE_EXT = '.csv'

RAW_DATASETS = [
    COUNTIES,
    COVID_19_NYT
]
RAW_DATA_PREFIX = 'data/raw_datasets/'
RAW_FILE_EXT = '.csv'

RAW_DATASETS_TO_SOURCES = {
    COVID_19_NYT: 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
    COUNTIES: 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv'
}


def init_file_names(file_dict, data_prefix, datasets, file_ext):
    for dataset in datasets:
        file_dict[dataset] = '{}{}{}'.format(
            data_prefix, dataset, file_ext)
    return file_dict


files = init_file_names({}, DATA_PREFIX, DATASETS, FILE_EXT)
raw_files = init_file_names({}, RAW_DATA_PREFIX, RAW_DATASETS, RAW_FILE_EXT)


def get_dataset(dataset):
    return files[dataset]


def get_raw_dataset(raw_dataset):
    return raw_files[raw_dataset]


def dataset_exists(dataset):
    dataset_file = get_dataset(dataset)
    return file_exists(dataset_file)


def raw_dataset_exists(raw_dataset):
    raw_dataset_file = get_raw_dataset(raw_dataset)
    return file_exists(raw_dataset_file)


def file_exists(fname):
    cwd = os.getcwd()
    full_path = os.path.join(cwd, fname)
    return os.path.exists(full_path)
