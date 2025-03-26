import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

# Load the data from the CSV file
df = pd.read_csv('RegressionAnalysis.csv')

# Prepare the input features (X) and output variables (y)
X = df[['Drum Temperature [C]', 'Electrical Lower Temperature [C]', 'Line Velocity [m/h]']]
y_MaxT = df['MaxT [C]']
y_MinT = df['MinT [C]']

# Feature Scaling (important for comparing coefficients)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Add a constant to the input features to account for the intercept
X_scaled = sm.add_constant(X_scaled)

# Fit the OLS (Ordinary Least Squares) regression model for MaxT
model_MaxT = sm.OLS(y_MaxT, X_scaled).fit()

# Fit the OLS regression model for MinT
model_MinT = sm.OLS(y_MinT, X_scaled).fit()

# Print the regression results
print("Model for MaxT:")
print(model_MaxT.summary())

print("\nModel for MinT:")
print(model_MinT.summary())

# Extract the coefficients
coef_MaxT = model_MaxT.params
coef_MinT = model_MinT.params

# Extract the standardized coefficients (excluding the constant)
coef_MaxT_scaled = coef_MaxT[1:]
coef_MinT_scaled = coef_MinT[1:]

# Create a function to plot the coefficients
def plot_coefficients(coefficients, feature_names, title):
    """Plots the regression coefficients."""
    plt.figure(figsize=(10, 6))
    plt.barh(feature_names, coefficients)
    plt.xlabel('Standardized Coefficient Value')
    plt.title(title)
    plt.gca().invert_yaxis()  # Invert y-axis for better readability
    plt.show()

# Get feature names
feature_names = ['Drum Temperature [C]', 'Electrical Lower Temperature [C]', 'Line Velocity [m/h]']

# Plot the coefficients for MaxT
plot_coefficients(coef_MaxT_scaled, feature_names, 'Sensitivity Analysis - Impact on MaxT')

# Plot the coefficients for MinT
plot_coefficients(coef_MinT_scaled, feature_names, 'Sensitivity Analysis - Impact on MinT')


# Additional Visualization: Scatter plots of each input vs. each output
def plot_scatter(input_feature, output_feature, input_name, output_name):
    plt.figure(figsize=(8, 6))
    plt.scatter(df[input_feature], df[output_feature])
    plt.xlabel(input_name)
    plt.ylabel(output_name)
    plt.title(f'Scatter Plot of {input_name} vs {output_name}')
    plt.grid(True)
    plt.show()

# Create scatter plots
plot_scatter('Drum Temperature [C]', 'MaxT [C]', 'Drum Temperature [C]', 'MaxT [C]')
plot_scatter('Electrical Lower Temperature [C]', 'MaxT [C]', 'Electrical Lower Temperature [C]', 'MaxT [C]')
plot_scatter('Line Velocity [m/h]', 'MaxT [C]', 'Line Velocity [m/h]', 'MaxT [C]')

plot_scatter('Drum Temperature [C]', 'MinT [C]', 'Drum Temperature [C]', 'MinT [C]')
plot_scatter('Electrical Lower Temperature [C]', 'MinT [C]', 'Electrical Lower Temperature [C]', 'MinT [C]')
plot_scatter('Line Velocity [m/h]', 'MinT [C]', 'Line Velocity [m/h]', 'MinT [C]')
