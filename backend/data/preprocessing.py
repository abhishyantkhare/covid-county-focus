import csv
import data.utils as utils
import data.datasets as datasets
import pandas as pd
import unidecode

CUSTOM_COUNTIES = [
    # Special case for Kansas City. Kansas city encompases several counties
    # so we're going to remove those and replace them with Kansas City
    ["Kansas City", "KANSASCITY", "Missouri", "MISSOURI", 1163157],
]


def preprocess_counties():
    if not datasets.raw_dataset_exists(datasets.COUNTIES):
        return
    raw_counties = datasets.get_raw_dataset(datasets.COUNTIES)
    counties = datasets.get_dataset(datasets.COUNTIES)
    with open(raw_counties, 'r', encoding="ISO-8859-1") as f:
        with open(counties, 'w',  encoding="utf-8") as resultcsv:
            county_writer = csv.writer(
                resultcsv, delimiter=',')
            county_writer.writerow(
                ["County Formatted", "County", "State Formatted", "State", "Population"])
            county_reader = csv.reader(f)
            # Skip headers
            next(county_reader, None)
            for row in county_reader:
                if row[5] == row[6]:
                    continue
                county_name_formatted = row[6]
                county_name_formatted = utils.remove_county_from_name(
                    county_name_formatted)
                county_name_formatted = utils.remove_parish_from_name(
                    county_name_formatted)
                county_name_formatted = utils.remove_municipality_from_name(
                    county_name_formatted)
                county_name = county_name_formatted.replace(
                    " ", "").upper()
                state_formatted = row[5]
                population = row[18]
                state = state_formatted.replace(" ", "").upper()
                county_writer.writerow(
                    [county_name_formatted, county_name, state_formatted, state, population])
            # Add custom counties
            for custom_county in CUSTOM_COUNTIES:
                county_writer.writerow(custom_county)


def preprocess_covid_19_nyt_county():
    if not datasets.raw_dataset_exists(datasets.COVID_19_NYT_COUNTY):
        return

    raw_covid_19_nyt_county = datasets.get_raw_dataset(
        datasets.COVID_19_NYT_COUNTY)
    raw_covid_19_nyt_county_df = pd.read_csv(raw_covid_19_nyt_county)
    raw_covid_19_nyt_county_df['county'] = raw_covid_19_nyt_county_df['county'].map(
        utils.nyc_to_ny)
    raw_covid_19_nyt_county_df['county'] = raw_covid_19_nyt_county_df['county'].str.upper(
    )
    raw_covid_19_nyt_county_df['county'] = raw_covid_19_nyt_county_df['county'].str.replace(
        " ", "")
    raw_covid_19_nyt_county_df['county'] = raw_covid_19_nyt_county_df['county'].map(
        unidecode.unidecode)
    raw_covid_19_nyt_county_df['state'] = raw_covid_19_nyt_county_df['state'].str.upper(
    )
    raw_covid_19_nyt_county_df['state'] = raw_covid_19_nyt_county_df['state'].str.replace(
        " ", "")
    raw_covid_19_nyt_county_df = raw_covid_19_nyt_county_df.assign(
        epoch_ms=raw_covid_19_nyt_county_df['date'].map(utils.date_string_to_epoch_ms))

    covid_19_nyt_county = datasets.get_dataset(datasets.COVID_19_NYT_COUNTY)
    raw_covid_19_nyt_county_df.to_csv(covid_19_nyt_county)


def preprocess_covid_19_nyt_state():
    if not datasets.raw_dataset_exists(datasets.COVID_19_NYT_STATE):
        return
    raw_covid_19_nyt_state = datasets.get_raw_dataset(
        datasets.COVID_19_NYT_STATE)

    raw_covid_19_nyt_state_df = pd.read_csv(raw_covid_19_nyt_state)
    raw_covid_19_nyt_state_df['state'] = raw_covid_19_nyt_state_df['state'].str.upper(
    )
    raw_covid_19_nyt_state_df['state'] = raw_covid_19_nyt_state_df['state'].str.replace(
        " ", "")
    raw_covid_19_nyt_state_df = raw_covid_19_nyt_state_df.assign(
        epoch_ms=raw_covid_19_nyt_state_df['date'].map(utils.date_string_to_epoch_ms))

    covid_19_nyt_state = datasets.get_dataset(datasets.COVID_19_NYT_STATE)
    raw_covid_19_nyt_state_df.to_csv(covid_19_nyt_state)


def preprocess_hospital_atlas():
    if not datasets.raw_dataset_exists(datasets.HOSPIAL_ATLAS):
        return
    raw_hospital_atlas = datasets.get_raw_dataset(datasets.HOSPIAL_ATLAS)
    hospital_atlas = datasets.get_dataset(datasets.HOSPIAL_ATLAS)
    raw_hospital_atlas_df = pd.read_csv(raw_hospital_atlas)
    raw_hospital_atlas_df = raw_hospital_atlas_df.assign(COUNTY=raw_hospital_atlas_df['FCNTYNAME'].map(
        utils.county_from_atlas_fcntyname))
    raw_hospital_atlas_df = raw_hospital_atlas_df.assign(TOTAL_BEDS=raw_hospital_atlas_df.apply(
        lambda x: utils.atlas_total_beds(x['AHAbeds'], x['POSbeds']), axis=1))
    raw_hospital_atlas_df = raw_hospital_atlas_df.assign(
        STATE=raw_hospital_atlas_df['PSTATE'].map(utils.pstate_to_state))
    raw_hospital_atlas_df.to_csv(hospital_atlas)


dataset_to_preprocessing = {
    datasets.COUNTIES: preprocess_counties,
    datasets.COVID_19_NYT_COUNTY: preprocess_covid_19_nyt_county,
    datasets.COVID_19_NYT_STATE: preprocess_covid_19_nyt_state,
    datasets.HOSPIAL_ATLAS: preprocess_hospital_atlas,
}
