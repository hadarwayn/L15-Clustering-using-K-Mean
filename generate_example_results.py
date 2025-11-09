"""
This script generates all 5 example experiments for the README,
plus a GUI overview screenshot and a summary CSV.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
import numpy as np
import matplotlib.pyplot as plt
from data_model import GaussianGroup, initialize_groups
from k_means_logic import run_kmeans, generate_explanation

# Ensure results directory exists
os.makedirs('results', exist_ok=True)

def save_plot_and_explanation(fig, explanation, name):
    """Helper to save plot and text file"""
    plot_path = f"results/{name}_plot.png"
    text_path = f"results/{name}_explanation.txt"
    
    fig.savefig(plot_path, dpi=150, bbox_inches='tight', facecolor='white')
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(explanation)
    print(f"✅ Saved: {plot_path} and {text_path}")

def plot_scenario(groups, kmeans_results, title):
    """Helper to plot a scenario"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('white')
    
    cluster_colors = ['#E69F00', '#56B4E9', '#009E73']
    
    if kmeans_results:
        all_points = np.vstack([g.points for g in groups])
        original_labels = np.concatenate([[i] * g.n_points for i, g in enumerate(groups)])
        kmeans_labels = kmeans_results['labels']
        
        for i in range(len(all_points)):
            orig_idx = original_labels[i]
            kmeans_idx = kmeans_labels[i]
            ax.scatter(all_points[i, 0], all_points[i, 1], c=groups[orig_idx].color, s=15, alpha=0.8, zorder=2)
            ax.scatter(all_points[i, 0], all_points[i, 1], facecolor='none', edgecolor=cluster_colors[kmeans_idx], s=80, linewidth=2, alpha=0.9, zorder=1)
            
        centroids = kmeans_results['centroids']
        ax.scatter(centroids[:, 0], centroids[:, 1], c='black', marker='X', s=350, edgecolor='white', linewidth=3, label="K-Means Centroid", zorder=10)
    else:
        for group in groups:
            ax.scatter(group.points[:, 0], group.points[:, 1], c=group.color, label=group.label, alpha=0.7, s=40)

    for group in groups:
        ax.scatter(group.mean[0], group.mean[1], c=group.color, marker='X', s=250, alpha=0.6, edgecolor='black', linewidth=2, label=f"{group.label} True Mean")

    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel("Dimension 1")
    ax.set_ylabel("Dimension 2")
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_aspect('equal', 'box')
    ax.legend()
    fig.tight_layout()
    return fig

def generate_all_experiments():
    """Generate and save all 5 experiments"""
    
    all_metrics = []

    # --- Experiment 1: Perfect Separation ---
    groups = initialize_groups()
    all_points = np.vstack([g.points for g in groups])
    original_labels = np.concatenate([[i] * g.n_points for i, g in enumerate(groups)])
    kmeans_results = run_kmeans(all_points)
    explanation = generate_explanation(groups, kmeans_results, original_labels)
    fig = plot_scenario(groups, kmeans_results, "Experiment 1: Perfect Separation (Baseline)")
    save_plot_and_explanation(fig, explanation, "experiment_1")
    all_metrics.append(['Experiment 1', 'Perfect Separation', kmeans_results['inertia'], kmeans_results['silhouette'], kmeans_results['bcs']])
    plt.close(fig)

    # --- Experiment 2: Moderate Overlap ---
    groups = initialize_groups()
    groups[0].move([5, 4]) # Move Group A closer to B
    all_points = np.vstack([g.points for g in groups])
    original_labels = np.concatenate([[i] * g.n_points for i, g in enumerate(groups)])
    kmeans_results = run_kmeans(all_points)
    explanation = generate_explanation(groups, kmeans_results, original_labels)
    fig = plot_scenario(groups, kmeans_results, "Experiment 2: Moderate Overlap")
    save_plot_and_explanation(fig, explanation, "experiment_2")
    all_metrics.append(['Experiment 2', 'Moderate Overlap', kmeans_results['inertia'], kmeans_results['silhouette'], kmeans_results['bcs']])
    plt.close(fig)

    # --- Experiment 3: Variance Explosion ---
    groups = initialize_groups()
    groups[2].explode(3.0) # Explode Group C
    all_points = np.vstack([g.points for g in groups])
    original_labels = np.concatenate([[i] * g.n_points for i, g in enumerate(groups)])
    kmeans_results = run_kmeans(all_points)
    explanation = generate_explanation(groups, kmeans_results, original_labels)
    fig = plot_scenario(groups, kmeans_results, "Experiment 3: Variance Explosion")
    save_plot_and_explanation(fig, explanation, "experiment_3")
    all_metrics.append(['Experiment 3', 'Variance Explosion', kmeans_results['inertia'], kmeans_results['silhouette'], kmeans_results['bcs']])
    plt.close(fig)

    # --- Experiment 4: Complete Merger ---
    groups = initialize_groups()
    groups[0].move(groups[1].mean) # Move A on top of B
    all_points = np.vstack([g.points for g in groups])
    original_labels = np.concatenate([[i] * g.n_points for i, g in enumerate(groups)])
    kmeans_results = run_kmeans(all_points)
    explanation = generate_explanation(groups, kmeans_results, original_labels)
    fig = plot_scenario(groups, kmeans_results, "Experiment 4: Complete Merger")
    save_plot_and_explanation(fig, explanation, "experiment_4")
    all_metrics.append(['Experiment 4', 'Complete Merger', kmeans_results['inertia'], kmeans_results['silhouette'], kmeans_results['bcs']])
    plt.close(fig)

    # --- Experiment 5: Extreme Explosion ---
    groups = initialize_groups()
    for group in groups:
        group.explode(5.0)
    all_points = np.vstack([g.points for g in groups])
    original_labels = np.concatenate([[i] * g.n_points for i, g in enumerate(groups)])
    kmeans_results = run_kmeans(all_points)
    explanation = generate_explanation(groups, kmeans_results, original_labels)
    fig = plot_scenario(groups, kmeans_results, "Experiment 5: Extreme Explosion (Chaos)")
    save_plot_and_explanation(fig, explanation, "experiment_5")
    all_metrics.append(['Experiment 5', 'Extreme Explosion', kmeans_results['inertia'], kmeans_results['silhouette'], kmeans_results['bcs']])
    plt.close(fig)

    # --- Save GUI Overview Screenshot ---
    # This is a placeholder. A real screenshot should be taken from the app.
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.text(0.5, 0.5, "Placeholder for GUI Screenshot\n\nRun the app and take a screenshot, \nsave it as 'results/gui_overview.png'", 
            ha='center', va='center', fontsize=18, color='gray')
    ax.set_xticks([])
    ax.set_yticks([])
    fig.savefig("results/gui_overview.png", dpi=100)
    print("✅ Saved: results/gui_overview.png (placeholder)")
    plt.close(fig)

    # --- Save Summary CSV ---
    summary_path = "results/experiments_summary.csv"
    header = "Experiment,Scenario,Inertia,Silhouette,BCS"
    np.savetxt(summary_path, all_metrics, delimiter=",", fmt='%s', header=header, comments='')
    print(f"✅ Saved: {summary_path}")

if __name__ == "__main__":
    print("🚀 Generating all experiment results for the README...")
    generate_all_experiments()
    print("\n🎉 All experiments generated successfully!")