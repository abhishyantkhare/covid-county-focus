import data


class Controller:

    def __init__(self):
        self.states = data.states
        self.states_formatted = data.states_formatted
        self.state_to_counties = data.state_to_counties
        self.state_to_counties_formatted = data.state_to_counties_formatted
        self.state_county_bed_data = data.state_county_bed_data
        self.state_county_dates = data.state_county_dates
        self.state_county_cases = data.state_county_cases
        self.state_county_deaths = data.state_county_deaths
        self.state_county_epochs_ms = data.state_county_epochs_ms
        self.state_county_cases_epochs_ms = data.state_county_cases_epochs_ms
        self.state_county_deaths_epochs_ms = data.state_county_deaths_epochs_ms

    def check_state(self, state):
        return state in self.states

    def cases(self, state, county):
        s_c = (state, county)
        return self.state_county_cases_epochs_ms[s_c]

    def bed_capacity(self, state, county):
        s_c_t = (state, county, 'total')
        return {
            'total_bed_capacity': int(self.state_county_bed_data[s_c_t])
        }

    def counties(self, state):
        return self.state_to_counties_formatted[state]

    def get_states_formatted(self):
        return self.states_formatted

    def deaths(self, state, county):
        s_c = (state, county)
        return self.state_county_deaths_epochs_ms[s_c]
