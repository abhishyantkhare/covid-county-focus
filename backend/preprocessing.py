import csv
import utils


def preprocess_county_list(county_file):
    with open(county_file, 'r', encoding="ISO-8859-1") as f:
        with open('county_result.csv', 'w') as resultcsv:
            county_writer = csv.writer(resultcsv, delimiter=',')
            county_writer.writerow(
                ["County Formatted", "County", "State Formatted", "State"])
            for line in f:
                line = line.replace("\"", "")
                line = line.replace("\n", "")
                if line[0].isalnum():
                    line_comma_split = line.split(",")
                    county_name_formatted = utils.remove_county_from_name(
                        line_comma_split[0])
                    county_name = county_name_formatted.replace(
                        " ", "").upper()
                    state_formatted = utils.state_abbr_to_state(line_comma_split[1].split(
                        "\t")[0].lstrip())
                    state = state_formatted.replace(" ", "").upper()
                    county_writer.writerow(
                        [county_name_formatted, county_name, state_formatted, state])


preprocess_county_list('./data/county_adjacency.txt')
