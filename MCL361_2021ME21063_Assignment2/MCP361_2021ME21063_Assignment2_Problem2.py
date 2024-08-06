import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class ResidualErrorAnalysis:
    def __init__(self, a, b, n, error_std):
        # The model parameters are initialized:
        #   a - Intercept of the linear equation
        #   b - Slope of the linear equation
        #   n - Number of data points to be generated
        #   error_std - Standard deviation of the Gaussian noise to be added to the data
        self.a = a
        self.b = b
        self.n = n
        self.error_std = error_std

    def generate_data(self):
        # Data is generated as follows:
        #   x - Array of integers from 1 to n, representing the independent variable
        #   error - Gaussian noise with mean 0 and standard deviation error_std, added to the data
        #   y - Dependent variable calculated using the linear equation y = a + b*x + error
        x = np.arange(1, self.n+1)
        error = np.random.normal(0, self.error_std, self.n)
        y = self.a + self.b * x + error
        return x, y

    def split_data(self, x, y):
        # The data is split into training and testing sets:
        #   x - Independent variable data
        #   y - Dependent variable data
        #   20% of the data is used as the test set, and the remaining 80% is used for training
        #   The split is performed with a fixed random seed for reproducibility
        return train_test_split(x, y, test_size=0.2, random_state=0)

    def train_model(self, x_train, y_train):
        # A linear regression model is trained using the training data:
        #   x_train - Training data for the independent variable, reshaped to 2D
        #   y_train - Training data for the dependent variable
        #   The model is fit using the LinearRegression class from sklearn
        model = LinearRegression()
        model.fit(x_train.reshape(-1, 1), y_train)
        return model

    def compute_residuals(self, y_test, y_pred):
        # Residuals are computed as the difference between the actual and predicted values:
        #   y_test - Actual values from the test set
        #   y_pred - Predicted values from the model
        #   Residuals represent the errors or discrepancies of the model's predictions
        return y_test - y_pred

    def plot_histogram(self, residuals):
        # A histogram of the residuals is plotted to visualize their distribution:
        #   mean_residuals - Mean value of the residuals
        #   std_residuals - Standard deviation of the residuals
        #   The histogram displays the distribution of residuals with a fitted Gaussian curve for comparison
        mean_residuals = np.mean(residuals)
        std_residuals = np.std(residuals)
        
        print(f"Mean of Residuals: {mean_residuals:.2f}")
        print(f"Standard Deviation of Residuals: {std_residuals:.2f}")

        plt.hist(residuals, bins=30, density=True, alpha=0.6, color='g')
        xmin, xmax = plt.xlim()
        x_vals = np.linspace(xmin, xmax, 100)
        p = np.exp(-0.5*((x_vals - mean_residuals) / std_residuals)**2) / (std_residuals * np.sqrt(2 * np.pi))
        plt.plot(x_vals, p, 'k', linewidth=2)
        plt.title(f"Histogram of Residuals with Mean = {mean_residuals:.2f} and STD = {std_residuals:.2f}")
        plt.show()

def main():
    # The random seed is set for reproducibility of the random data generation
    np.random.seed(0)
    
    # An instance of ResidualErrorAnalysis is created with specific parameters:
    #   Intercept (a) = 0.2
    #   Slope (b) = 0.3
    #   Number of data points (n) = 5000
    #   Standard deviation of error (error_std) = 0.5
    analysis = ResidualErrorAnalysis(a=0.2, b=0.3, n=5000, error_std=0.5)
    
    # Data is generated using the analysis object's generate_data method
    x, y = analysis.generate_data()
    
    # The data is split into training and testing sets
    #   x_train, y_train - Training data
    #   x_test, y_test - Testing data
    x_train, x_test, y_train, y_test = analysis.split_data(x, y)
    
    # The model is trained using the training data
    trained_model = analysis.train_model(x_train, y_train)
    
    # Predictions are made on the test data using the trained model
    #   x_test - Testing data for the independent variable, reshaped to 2D
    y_pred = trained_model.predict(x_test.reshape(-1, 1))
    
    # Residuals are computed as the difference between the actual and predicted values
    residuals = analysis.compute_residuals(y_test, y_pred)
    
    # A histogram of the residuals is plotted using the plot_histogram method
    analysis.plot_histogram(residuals)

if __name__ == "__main__":
    main()
