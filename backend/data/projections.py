import numpy as np
from scipy.integrate import odeint
import data.utils as utils
import sys


DAY_MS = 86400000


class Projections:

    def __init__(self, data):
        self.data = data
        self.gamma = 1.0 / 7
        self.projection_end_ms = 1596265200000
        self.create_projections()

    def create_projections(self):
        self.state_county_beta = {}
        self.state_county_case_projections = {}
        self.state_county_healthy_projections = {}
        self.state_county_recovered_projections = {}
        print("CREATING PROJECTIONS...")
        count = 0
        for s in self.data.states:
            if s != "CALIFORNIA":
                continue
            counties = self.data.state_to_counties[s]
            county_count = 0
            for c in counties:
                if c != "SANFRANCISCO":
                    continue
                s_c = (s, c)
                self.state_county_case_projections[s_c] = []
                self.state_county_healthy_projections[s_c] = []
                self.state_county_recovered_projections[s_c] = []
                cases = self.data.state_county_cases[s_c]
                if len(cases) == 0:
                    continue
                first_case = cases.iloc[0]
                pop = self.data.state_county_pop[s_c]
                start_ms = self.data.state_county_epochs_ms[s_c].iloc[0]
                s_percent, beta, gamma = self.monte_carlo_sample_parameters(
                    pop, len(cases[-5:]), cases.iloc[-6], cases[-5:])
                S, I, R = self.sir_projections(
                    pop*s_percent, beta, gamma, first_case, start_ms=start_ms, end_ms=self.projection_end_ms)
                S_epochs_ms, I_epochs_ms, R_epochs_ms = self.projections_to_epochs_ms(
                    S, I, R, start_ms, self.projection_end_ms)
                self.state_county_case_projections[s_c] = I_epochs_ms
                self.state_county_healthy_projections[s_c] = S_epochs_ms
                self.state_county_recovered_projections[s_c] = R_epochs_ms
                if county_count % 10 == 0:
                    print("LOADED {} percent of counties for state {}".format(
                        county_count * 100 / len(counties), s))
                county_count = county_count + 1
            if count % 10 == 0:
                print("LOADED {} percent".format(count * 2))
            count = count + 1

    def calc_beta_regression(self, cases_s):
        cases = cases_s.tolist()
        lim = len(cases)
        x = np.array(list(range(1, lim+1)))
        log_y = np.log(cases[-1*lim:])
        ln_k = np.divide((lim*np.sum(np.multiply(x, log_y)) - np.sum(x)
                          * np.sum(log_y)), (lim*np.sum(np.square(x)) - np.square(np.sum(x))))
        k = np.exp(ln_k)
        g = np.power(2, np.divide(1, k)) - 1
        return .5*(g + self.gamma)

    def projections_to_epochs_ms(self, S, I, R, start_ms, end_ms):
        num_days = int((end_ms - start_ms) / DAY_MS)
        epochs_ms = np.linspace(start_ms, end_ms, num_days)
        S_epochs_ms = utils.data_list_epoch_ms_dict(
            S, 'projected_healthy', epochs_ms)
        I_epochs_ms = utils.data_list_epoch_ms_dict(
            I*.05, 'projected_cases', epochs_ms)
        R_epochs_ms = utils.data_list_epoch_ms_dict(
            R, 'projected_recovered', epochs_ms)
        return S_epochs_ms, I_epochs_ms, R_epochs_ms

    def sir_projections(self, N, beta, gamma, first_case, days=None, start_ms=None, end_ms=None):
        num_days = 0
        if days is not None:
            num_days = days
        elif start_ms is not None and end_ms is not None:
            num_days = (end_ms - start_ms) // DAY_MS
        t = np.linspace(0, num_days, num_days)
        I0 = first_case
        R0 = 0
        S0 = N - I0 - R0
        y0 = S0, I0, R0
        sol = odeint(self.sir_diff_eq, y0, t, args=(N, beta, gamma))
        S, I, R = sol.T
        return S, I, R

    def sir_diff_eq(self, y, t, N, beta, gamma):
        S, I, _ = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    def monte_carlo_sample_parameters(self, N, num_days, first_case, actual_cases):
        S_percent_samples = np.linspace(.01, .99, 50)
        beta_samples = np.linspace(.35, .6, 20)
        print(beta_samples)
        gamma_samples = [1.0 / 10.0]
        min_err = sys.maxsize * 2 + 1
        best_param = (0, 0, 0)
        for s_percent in S_percent_samples:
            for beta in beta_samples:
                for gamma in gamma_samples:
                    _, I_est, _ = self.sir_projections(
                        N*s_percent, beta, gamma, first_case, days=num_days)
                    # use MSE as error
                    err = np.sum(np.square(I_est - actual_cases))
                    if err < min_err:
                        min_err = err
                        best_param = (s_percent, beta, gamma)
        print(min_err)
        print(best_param)
        return best_param
