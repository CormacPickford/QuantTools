
import numpy as np

class EnsembleOptimiser():

    def __init__(self,records,weights):
        self.records = records
        self.weights = weights
        self.alphas = len(self.records)
        self.days = len(records[0])
        self.report = self.calc_ensemble_report()
        self.sharpe, self.ret, self.std = self.calculate_daily_sharpe()
        self.learning_rate = 0.001

    def calculate_daily_sharpe(self):
        days = len(self.report)
        np_record = np.array(self.report)
        aggregate_return = np.sum(np_record)
        daily_return = aggregate_return / days
        square_of_mean = daily_return ** 2
        sum_squares = np.sum(np_record ** 2)
        mean_of_squares = sum_squares / days
        variance = mean_of_squares - square_of_mean
        std = (variance ** 0.5) / days ** 0.5
        sharpe = (aggregate_return / days) / std
        return sharpe,aggregate_return,std

    def sigma_prime(self):

        days = len(self.records[0])
        alphas = len(self.records)
        sigma_prime = np.zeros(alphas)
        av_agg_return = self.ret / days


        for day in range(days):
            ensemble_form = self.report[day] - av_agg_return
            individual_forms = [self.records[i][day] - (np.sum(self.records[i]))/days for i in range(alphas) ]
            sigma_prime += np.array(individual_forms) * np.array(ensemble_form)
        return sigma_prime

    def generate_naiive_grad(self):
        sigma = self.std * self.days ** 0.5
        lr_sharpe = self.sharpe * self.days ** 0.5
        alphas = len(self.records)
        individual_returns = [np.sum(self.records[i]) for i in range(alphas)]
        sig_prime = self.sigma_prime()
        naiive_grad = sigma * np.array(individual_returns) - (lr_sharpe * sig_prime)
        return naiive_grad

    def calc_gradient(self):
        naiive_grad = self.generate_naiive_grad()
        gradient_vector = naiive_grad - np.mean(naiive_grad)
        return gradient_vector

    def update_weights(self):
        self.weights -= self.learning_rate * self.calc_gradient()
        self.report = self.calc_ensemble_report()
        self.sharpe, self.ret, self.std = self.calculate_daily_sharpe()

    def calc_ensemble_report(self):
        weighted_records = [self.weights[i] * np.array(self.records[i]) for i in range(self.alphas)]
        report = np.zeros(self.days)
        for day in range(self.days):
            report[day] = np.sum(np.array(weighted_records)[:,day])
        return report




