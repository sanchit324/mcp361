import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, explained_variance_score

# Linear Regression Model
class LinearRegressionModel:
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
        #   x - A range of integers from 1 to n (inclusive), representing the independent variable
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
        # The split is performed with 20% of the data used for testing and the remaining 80% for training
        return train_test_split(x, y, test_size=0.2, random_state=0)

    def train_model(self, x_train, y_train):
        # A Linear Regression model is trained:
        #   x_train - Training data for the independent variable, reshaped to 2D for compatibility with the model
        #   y_train - Training data for the dependent variable
        # The model is fit to the training data, and the trained model is returned
        model = LinearRegression()
        model.fit(x_train.reshape(-1, 1), y_train)
        return model

    def plot_data(self, x, y, model):
        # A plot is created to visualize:
        #   The original data points (x, y) are displayed as a scatter plot in blue
        #   The fitted regression line is plotted in red using the model's intercept and coefficient
        #   The x-axis is labeled 'x' and the y-axis is labeled 'y'
        #   The title of the plot is 'Data and Fitted Regression Line'
        plt.scatter(x, y, color='blue')
        plt.plot(x, model.intercept_ + model.coef_[0]*x, color='red')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Data and Fitted Regression Line')
        plt.show()

    def plot_bar(self, x_test, y_test, y_pred):
        # A bar chart is plotted to compare:
        #   The true values (y_test) and predicted values (y_pred) for the test set
        #   x_test - The test data is sorted and used as the x-axis values
        #   True values and predicted values are shown side-by-side for comparison
        #   The chart includes labels, title, and a legend
        x_test_sorted = np.argsort(x_test)
        x_test_sorted_values = x_test[x_test_sorted]
        plt.bar(x_test_sorted_values, y_test[x_test_sorted], width=0.4, label='True y')
        plt.bar(x_test_sorted_values + 0.4, y_pred[x_test_sorted], width=0.4, label='Predicted y')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('True vs Predicted values')
        plt.legend()
        plt.show()

    def compute_metrics(self, y_test, y_pred):
        # Performance metrics are computed as follows:
        #   mae - Mean Absolute Error, representing the average absolute difference between true and predicted values
        #   mse - Mean Squared Error, representing the average of the squares of the differences
        #   rmse - Root Mean Squared Error, the square root of mse, representing the standard deviation of prediction errors
        #   r2 - R-squared, representing the proportion of variance explained by the model
        #   evs - Explained Variance Score, representing the proportion of the variance in the dependent variable that is predictable
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        evs = explained_variance_score(y_test, y_pred)
        return mae, mse, rmse, r2, evs

def main():
    # The random seed is set for reproducibility of the random data generation
    np.random.seed(0)
    
    # An instance of LinearRegressionModel is created with specific parameters:
    #   Intercept (a) = 0.2
    #   Slope (b) = 0.3
    #   Number of data points (n) = 50
    #   Standard deviation of error (error_std) = 0.5
    model = LinearRegressionModel(a=0.2, b=0.3, n=50, error_std=0.5)
    
    # Data is generated using the model's generate_data method
    x, y = model.generate_data()
    
    # The generated data is split into training and testing sets
    #   x_train, y_train - Training data
    #   x_test, y_test - Testing data
    x_train, x_test, y_train, y_test = model.split_data(x, y)
    
    # The model is trained using the training data
    #   x_train - Training data for the independent variable
    #   y_train - Training data for the dependent variable
    trained_model = model.train_model(x_train, y_train)
    
    # The model's slope (b) and intercept (a) are printed
    print(f"Slope (b): {trained_model.coef_[0]}")
    print(f"Intercept (a): {trained_model.intercept_}")
    
    # The data and the fitted regression line are plotted using the plot_data method
    model.plot_data(x, y, trained_model)
    
    # Predictions are made on the test data using the trained model
    #   x_test - Testing data for the independent variable, reshaped to 2D
    y_pred = trained_model.predict(x_test.reshape(-1, 1))
    
    # A bar chart comparing the true values and predicted values for the test set is plotted
    model.plot_bar(x_test, y_test, y_pred)
    
    # Performance metrics are computed for the model's predictions
    #   y_test - True values for the test set
    #   y_pred - Predicted values for the test set
    mae, mse, rmse, r2, evs = model.compute_metrics(y_test, y_pred)
    
    # The computed metrics are printed
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error: {rmse}")
    print(f"Coefficient of Determination: {r2}")
    print(f"Explained Variance Score: {evs}")

if __name__ == "__main__":
    main()
