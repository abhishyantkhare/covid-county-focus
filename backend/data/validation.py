UNKNOWN = "UNKNOWN"


def validate_county_names(states, cases_df, county_df):
    invalid_county_names = set()
    for s in states:
        cases_state_df = cases_df[cases_df['state'] == s]
        county_state_df = county_df[county_df['State'] == s]
        invalid_counties = cases_state_df[~cases_state_df['county'].isin(
            county_state_df['County'])]['county'].unique().tolist()
        for c in invalid_counties:
            if c != UNKNOWN:
                invalid_county_names.add((s, c))
    try:
        assert(len(invalid_county_names) == 0)
    except AssertionError as e:
        for i_c in invalid_county_names:
            e.args += ("Invalid County: ",
                       ("State: {}, County: {}\n".format(i_c[0], i_c[1])))
        raise
