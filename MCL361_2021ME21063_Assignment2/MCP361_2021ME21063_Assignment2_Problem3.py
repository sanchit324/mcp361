import numpy as np
import statsmodels.api as sm

class OLSRegressionAnalysis:
    def __init__(self, a, b, n, error_std, iterations):
        # The model parameters are initialized:
        #   a - Intercept of the linear equation
        #   b - Slope of the linear equation
        #   n - Number of data points to be generated
        #   error_std - Standard deviation of the Gaussian noise to be added to the data
        #   iterations - Number of iterations for performing the regression analysis
        self.a = a
        self.b = b
        self.n = n
        self.error_std = error_std
        self.iterations = iterations

    def generate_data(self):
        # Data is generated as follows:
        #   x - Array of integers from 1 to n, representing the independent variable
        #   error - Gaussian noise with mean 0 and standard deviation error_std, added to the data
        #   y - Dependent variable calculated using the linear equation y = a + b*x + error
        x = np.arange(1, self.n + 1)
        error = np.random.normal(0, self.error_std, self.n)
        y = self.a + self.b * x + error
        return x, y

    def perform_regression(self, x, y):
        # An OLS regression model is fit to the data:
        #   x - Independent variable data with an added constant term (intercept) for the regression model
        #   y - Dependent variable data
        #   The model is fit using Ordinary Least Squares (OLS) and the fitted model is returned
        x = sm.add_constant(x)
        model = sm.OLS(y, x).fit()
        return model

    def run_analysis(self):
        # Analysis is performed over multiple iterations:
        #   within_one_se - Counter for the number of times the true slope b is within one standard error of the estimated slope
        #   within_two_se - Counter for the number of times the true slope b is within two standard errors of the estimated slope
        within_one_se = 0
        within_two_se = 0

        for _ in range(self.iterations):
            # Data is generated and the regression model is fitted
            x, y = self.generate_data()
            model = self.perform_regression(x, y)

            # Standard error of the estimated slope and the estimated slope are retrieved from the model
            se = model.bse[1]
            slope = model.params[1]

            # The fraction of times the true slope is within one and two standard errors of the estimated slope is calculated
            if self.b >= slope - se and self.b <= slope + se:
                within_one_se += 1

            if self.b >= slope - 2 * se and self.b <= slope + 2 * se:
                within_two_se += 1

        # The results of the analysis are printed:
        #   Fraction of iterations where the true slope is within one standard error of the estimated slope
        #   Fraction of iterations where the true slope is within two standard errors of the estimated slope
        print(f"Fraction within one SE: {within_one_se / self.iterations}")
        print(f"Fraction within two SE: {within_two_se / self.iterations}")

def main():
    # The random seed is set for reproducibility of the random data generation
    np.random.seed(0)
    
    # An instance of OLSRegressionAnalysis is created with specific parameters:
    #   Intercept (a) = 0.2
    #   Slope (b) = 0.3
    #   Number of data points (n) = 50
    #   Standard deviation of error (error_std) = 0.5
    #   Number of iterations (iterations) = 1000
    analysis = OLSRegressionAnalysis(a=0.2, b=0.3, n=50, error_std=0.5, iterations=1000)
    
    # The regression analysis is performed using the run_analysis method
    analysis.run_analysis()

if __name__ == "__main__":
    main()
