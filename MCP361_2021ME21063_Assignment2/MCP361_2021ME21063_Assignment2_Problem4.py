import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

class QuadraticModelAnalysis:
    def __init__(self, a, b, c, n, error_std):
        # The model parameters are initialized:
        #   a - Intercept term for the quadratic equation
        #   b - Linear coefficient
        #   c - Quadratic coefficient
        #   n - Number of data points to be generated
        #   error_std - Standard deviation of the Gaussian noise to be added to the data
        self.a = a
        self.b = b
        self.c = c
        self.n = n
        self.error_std = error_std

    def generate_data(self):
        # Data is generated as follows:
        #   x - Random values uniformly distributed between 0 and 50, representing the independent variable
        #   error - Gaussian noise with mean 0 and standard deviation error_std, added to the data
        #   y - Dependent variable calculated using the quadratic equation y = a + b*x + c*x^2 + error
        x = np.random.uniform(0, 50, self.n)
        error = np.random.normal(0, self.error_std, self.n)
        y = self.a + self.b * x + self.c * x**2 + error
        return x, y

    def perform_linear_regression(self, x, y):
        # A linear regression model is fit to the data:
        #   x - Independent variable data
        #   y - Dependent variable data
        #   x_linear - The independent variable x is augmented with a constant term (intercept) for the regression model
        #   The model is fit using Ordinary Least Squares (OLS) and the fitted model is returned
        x_linear = sm.add_constant(x)
        model = sm.OLS(y, x_linear).fit()
        return model

    def perform_quadratic_regression(self, x, y):
        # A quadratic regression model is fit to the data:
        #   x - Independent variable data
        #   y - Dependent variable data
        #   x_quadratic - The independent variable x is augmented with its square term
        #   The data is augmented with a constant term for the regression model
        #   The model is fit using Ordinary Least Squares (OLS) and the fitted model is returned
        x_quadratic = np.column_stack((x, x**2))
        x_quadratic = sm.add_constant(x_quadratic)
        model = sm.OLS(y, x_quadratic).fit()
        return model

    def plot_data_and_fits(self, x, y, model_linear, model_quadratic):
        # The data and regression fits are plotted as follows:
        #   x_fit - A range of x values for plotting the fitted lines
        #   y_linear_fit - The linear fit values computed using the linear model's parameters
        #   y_quadratic_fit - The quadratic fit values computed using the quadratic model's parameters
        #   Scatter plot of the original data (x, y) is displayed in gray
        #   The linear fit is plotted in blue
        #   The quadratic fit is plotted in red
        #   The plot includes labels, title, and a legend for clarity
        x_fit = np.linspace(0, 50, 500)
        y_linear_fit = model_linear.params[0] + model_linear.params[1] * x_fit
        y_quadratic_fit = model_quadratic.params[0] + model_quadratic.params[1] * x_fit + model_quadratic.params[2] * x_fit**2

        plt.scatter(x, y, label='Data', color='gray', alpha=0.5)
        plt.plot(x_fit, y_linear_fit, label='Linear Fit', color='blue')
        plt.plot(x_fit, y_quadratic_fit, label='Quadratic Fit', color='red')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Linear vs Quadratic Regression')
        plt.legend()
        plt.show()

def main():
    # The random seed is set for reproducibility of the random data generation
    np.random.seed(0)
    
    # An instance of QuadraticModelAnalysis is created with specific parameters:
    #   Intercept (a) = 3
    #   Linear coefficient (b) = 8
    #   Quadratic coefficient (c) = 20
    #   Number of data points (n) = 100
    #   Standard deviation of error (error_std) = 3
    analysis = QuadraticModelAnalysis(a=3, b=8, c=20, n=100, error_std=3)
    
    # Data is generated using the analysis object's generate_data method
    x, y = analysis.generate_data()
    
    # Linear and quadratic regression models are fitted to the data
    #   model_linear - The linear model is fit using the perform_linear_regression method
    #   model_quadratic - The quadratic model is fit using the perform_quadratic_regression method
    model_linear = analysis.perform_linear_regression(x, y)
    model_quadratic = analysis.perform_quadratic_regression(x, y)
    
    # The Akaike Information Criterion (AIC) for both models is retrieved
    #   aic_linear - AIC for the linear model
    #   aic_quadratic - AIC for the quadratic model
    aic_linear = model_linear.aic
    aic_quadratic = model_quadratic.aic
    
    # The AIC values and the coefficients of the quadratic model are printed
    print(f"AIC for linear model: {aic_linear}")
    print(f"AIC for quadratic model: {aic_quadratic}")
    print(f"Coefficients of quadratic model: {model_quadratic.params}")

    # The data and the regression fits are plotted using the plot_data_and_fits method
    analysis.plot_data_and_fits(x, y, model_linear, model_quadratic)

if __name__ == "__main__":
    main()
