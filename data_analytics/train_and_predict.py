import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

def train_linear_regression(X, y):
    """
    This function trains a linear regression model
    :param X: input features 
    :param y: target variable
    :return model: Trained linear regression model
    """
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_linear_regression(model, X):
    """
    This function makes predictions using the trained linear regression model
    :param model: trained linear regression model
    :param X: input features for which to make predictions
    :return predictions: The predicted values (numpy array)
    """
    predictions = model.predict(X)
    return predictions

def perform_train_test_split(X, y):
    """
    This function splits the data into training and test datasets
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    return X_train, X_test, y_train, y_test

def plot_predictions(true_values, predicted_values):
    plt.figure(figsize=(10,10))
    plt.scatter(true_values, predicted_values, c='crimson')
    plt.yscale('log')
    plt.xscale('log')

    p1 = max(max(predicted_values), max(true_values))
    p2 = min(min(predicted_values), min(true_values))
    plt.plot([p1, p2], [p1, p2], 'b-')
    plt.xlabel('True Values', fontsize=15)
    plt.ylabel('Predictions', fontsize=15)
    plt.axis('equal')
    plt.show()

def train_and_predict_linear_regression(metrics_data):
    """
    This function calls the training and prediction functions
    """
    columns = metrics_data.columns
    feature_cols = [col for col in columns if col not in ["electricity_consumed", "co2_emissions"]]
    feature_cols = ["memory_usage", "cpu_usage"]
    X = metrics_data[feature_cols]
    y = metrics_data["co2_emissions"]

    X_train, X_test, y_train, y_test = perform_train_test_split(X, y)
    lm = train_linear_regression(X_train, y_train)
    predictions = list(predict_linear_regression(lm, X_test))
    plot_predictions(y_test.tolist(), predictions)
    # Create the dataframe that will contain our results
    results = X_test.copy()
    results["co2_emissions"] = y_test
    results["predicted_co2_emissions"] = predictions
    results["residuals"] = results["co2_emissions"] - results["predicted_co2_emissions"]
    return results

if __name__ == "__main__":
    cluster = "cluster1"
    file_path = r"C:\Users\upech\Documents\SA\sa_i2_project\data_processing\data\{0}\preprocessed_file_with_co2_emissions.csv".format(cluster)
    metrics_df = pd.read_csv(file_path)
    filtered_metrics_df = metrics_df[metrics_df["co2_emissions"]!=0]
    filtered_metrics_df.dropna(subset=["cpu_usage", "memory_usage"], inplace=True)
    print(len(filtered_metrics_df))
    train_and_predict_linear_regression(filtered_metrics_df)
