import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def dp_function(gpm, Cv):
    return (gpm / Cv)**2 * 0.9982

def detect_outliers(gpm, dp, Cv, threshold=2.5):
    dp_expected = dp_function(gpm, Cv)
    residuals = dp - dp_expected
    z_scores = np.abs((residuals - np.mean(residuals)) / np.std(residuals))
    return z_scores > threshold

def iterative_fit_and_remove_outliers(gpm, dp, max_iterations=5, threshold=2.5):
    mask = np.ones(len(gpm), dtype=bool)
    for iteration in range(max_iterations):
        popt, _ = curve_fit(dp_function, gpm[mask], dp[mask])
        Cv = popt[0]
        new_outliers = detect_outliers(gpm[mask], dp[mask], Cv, threshold)
        if not np.any(new_outliers):
            break
        mask[mask] = ~new_outliers
    return Cv, mask, iteration + 1

# Read data from the CSV file
data = pd.read_csv('dataset.csv')  # Replace with your actual file name

gpm_data = data.iloc[:, 0].values
num_datasets = data.shape[1] - 1

colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

plt.figure(figsize=(12, 8))

threshold = 2.0;  # Set the threshold for outlier detection

for i in range(num_datasets):
    column_name = data.columns[i+1]
    dp_data = data.iloc[:, i+1].values
    
    # Perform iterative fitting and outlier removal
    Cv_best, mask, iterations = iterative_fit_and_remove_outliers(gpm_data, dp_data, max_iterations=5, threshold=threshold)
    
    gpm_fit = np.linspace(min(gpm_data), max(gpm_data), 100)
    dp_fit = dp_function(gpm_fit, Cv_best)
    
    # Plot data points, marking outliers differently
    plt.scatter(gpm_data[mask], dp_data[mask], color=colors[i % len(colors)], label=f'{column_name} (Data)')
    plt.scatter(gpm_data[~mask], dp_data[~mask], color=colors[i % len(colors)], marker='x', s=100, label=f'{column_name} (Outliers)')
    plt.plot(gpm_fit, dp_fit, color=colors[i % len(colors)], linestyle='--', label=f'{column_name} (Fit)')
    
    # Display information on the plot
    plt.text(0.05, 0.95 - 0.12 * i,  # Adjusted spacing factor to give more room between text blocks
        f'{column_name}:\n'
        f'Cv = {Cv_best:.4f}\n'
        f'Iterations = {iterations}\n'
        f'Threshold = {threshold} std dev\n\n\n\n',  # Added extra empty lines for spacing
        transform=plt.gca().transAxes,
        verticalalignment='top', 
        color=colors[i % len(colors)],
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'), 
        fontsize=12
    )

    
    print(f"Results for {column_name}:")
    print(f"  Best-fit Cv: {Cv_best:.4f}")
    print(f"  Iterations: {iterations}")
    print(f"  Outliers detected: {np.sum(~mask)}")
    if np.any(~mask):
        print(f"  Outlier GPM values: {gpm_data[~mask]}")
    print()

plt.xlabel('Flow Rate, gpm')
plt.ylabel('Pressure Drop, psi')
plt.title(f'Flow Rate vs Pressure Drop - Iterative Curve Fitting for {num_datasets} Datasets')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
