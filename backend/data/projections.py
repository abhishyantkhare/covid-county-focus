import numpy as np
from scipy.integrate import odeint
import data.utils as utils


DAY_MS = 86400000


class Projections:

    def __init__(self, data):
        self.data = data
        self.gamma = 1.0 / 14
        self.end_ms = 1596265200000
        self.create_projections()

    def create_projections(self):
        self.state_county_beta = {}
        self.state_county_case_projections = {}
        self.state_county_healthy_projections = {}
        self.state_county_recovered_projections = {}

        for s in self.data.states:
            counties = self.data.state_to_counties[s]
            for c in counties:
                s_c = (s, c)
                self.state_county_case_projections[s_c] = []
                self.state_county_healthy_projections[s_c] = []
                self.state_county_recovered_projections[s_c] = []
                cases = self.data.state_county_cases[s_c]
                if len(cases) == 0:
                    continue
                last_case = cases.values[-1]
                beta = self.calc_beta_regression(cases)
                self.state_county_beta[s_c] = beta
                pop = self.data.state_county_pop[s_c]
                start_ms = self.data.state_county_last_epoch_ms[s_c]
                # utils.beta_est(cases, pop, start_ms)
                S_epochs_ms, I_epochs_ms, R_epochs_ms = self.sir_projections(
                    pop, beta, last_case, start_ms)
                self.state_county_case_projections[s_c] = I_epochs_ms
                self.state_county_healthy_projections[s_c] = S_epochs_ms
                self.state_county_recovered_projections[s_c] = R_epochs_ms

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

    def sir_projections(self, N, beta, last_case, start_ms):
        num_days = int((self.end_ms - start_ms) / DAY_MS)
        t = np.linspace(0, num_days, num_days)
        I0 = last_case
        R0 = 0
        S0 = N - I0 - R0
        y0 = S0, I0, R0
        sol = odeint(self.sir_diff_eq, y0, t, args=(N, beta))
        S, I, R = sol.T
        epochs_ms = np.linspace(start_ms, self.end_ms, num_days)
        S_epochs_ms = utils.data_list_epoch_ms_dict(
            S, 'projected_healthy', epochs_ms)
        I_epochs_ms = utils.data_list_epoch_ms_dict(
            I*.05, 'projected_cases', epochs_ms)
        R_epochs_ms = utils.data_list_epoch_ms_dict(
            R, 'projected_recovered', epochs_ms)
        return S_epochs_ms, I_epochs_ms, R_epochs_ms

    def sir_diff_eq(self, y, t, N, beta):
        S, I, _ = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - self.gamma * I
        dRdt = self.gamma * I
        return dSdt, dIdt, dRdt
