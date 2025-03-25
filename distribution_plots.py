import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, binom, norm, geom

def plot_poisson_distribution(ax, lambda_value, max_k=20):
    k = np.arange(0, max_k + 1)
    probabilities = poisson.pmf(k, lambda_value)
    
    ax.bar(k, probabilities, alpha=0.8, color='skyblue', edgecolor='navy')
    ax.plot(k, probabilities, 'ro-', linewidth=2, markersize=4, alpha=0.7)
    
    ax.set_title(f'Poisson Distribution (λ = {lambda_value})', fontsize=10)
    ax.set_xlabel('Number of Events (k)', fontsize=8)
    ax.set_ylabel('Probability', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(k[::2])
    
    ax.text(0.95, 0.95, f'λ = {lambda_value}\nMean = {lambda_value}\nVariance = {lambda_value}', 
             transform=ax.transAxes, verticalalignment='top', 
             horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             fontsize=8)

def plot_binomial_distribution(ax, n, p, max_k=None):
    if max_k is None:
        max_k = n
    k = np.arange(0, max_k + 1)
    probabilities = binom.pmf(k, n, p)
    
    ax.bar(k, probabilities, alpha=0.8, color='lightgreen', edgecolor='darkgreen')
    ax.plot(k, probabilities, 'bo-', linewidth=2, markersize=4, alpha=0.7)
    
    ax.set_title(f'Binomial Distribution (n = {n}, p = {p:.2f})', fontsize=10)
    ax.set_xlabel('Number of Successes (k)', fontsize=8)
    ax.set_ylabel('Probability', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(k[::2])
    
    mean = n * p
    variance = n * p * (1 - p)
    ax.text(0.95, 0.95, f'n = {n}, p = {p:.2f}\nMean = {mean:.2f}\nVariance = {variance:.2f}', 
             transform=ax.transAxes, verticalalignment='top', 
             horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             fontsize=8)

def plot_normal_distribution(ax, mu, sigma):
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    y = norm.pdf(x, mu, sigma)
    
    ax.plot(x, y, 'g-', linewidth=2)
    ax.fill_between(x, y, alpha=0.3, color='lightgreen')
    
    ax.set_title(f'Normal Distribution (μ = {mu}, σ = {sigma})', fontsize=10)
    ax.set_xlabel('Value', fontsize=8)
    ax.set_ylabel('Probability Density', fontsize=8)
    ax.grid(True, alpha=0.3)
    
    ax.text(0.95, 0.95, f'μ = {mu}\nσ = {sigma}\nMean = {mu}\nVariance = {sigma**2}', 
             transform=ax.transAxes, verticalalignment='top', 
             horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             fontsize=8)

def plot_geometric_distribution(ax, p, max_k=20):
    k = np.arange(1, max_k + 1)
    probabilities = geom.pmf(k, p)
    
    ax.bar(k, probabilities, alpha=0.8, color='lightsalmon', edgecolor='red')
    ax.plot(k, probabilities, 'ro-', linewidth=2, markersize=4, alpha=0.7)
    
    ax.set_title(f'Geometric Distribution (p = {p:.2f})', fontsize=10)
    ax.set_xlabel('Number of Trials Until First Success (k)', fontsize=8)
    ax.set_ylabel('Probability', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(k[::2])
    
    mean = 1 / p
    variance = (1 - p) / (p ** 2)
    ax.text(0.95, 0.95, f'p = {p:.2f}\nMean = {mean:.2f}\nVariance = {variance:.2f}', 
             transform=ax.transAxes, verticalalignment='top', 
             horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             fontsize=8)

def plot_distributions(lambda_value, n, p, mu, sigma, geo_p, max_k=20):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    plot_poisson_distribution(ax1, lambda_value, max_k)
    plot_binomial_distribution(ax2, n, p, max_k)
    plot_normal_distribution(ax3, mu, sigma)
    plot_geometric_distribution(ax4, geo_p, max_k)
    
    plt.tight_layout()
    plt.show()

# Example usage
lambda_value = 10  # Poisson lambda
n = 20  # Binomial number of trials
p = 0.5  # Binomial probability of success
mu = 0  # Normal distribution mean
sigma = 1  # Normal distribution standard deviation
geo_p = 0.3  # Geometric distribution probability of success
max_k = 20  # Maximum number of events/successes to plot

plot_distributions(lambda_value, n, p, mu, sigma, geo_p, max_k)