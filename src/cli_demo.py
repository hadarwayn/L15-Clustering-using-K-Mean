# File: src/cli_demo.py
"""
Command-Line Demo script to verify Phase 1 functionality.
This script will be replaced by main.py and k_means_app.py in Phase 2.
"""

import numpy as np
import matplotlib.pyplot as plt
from data_model import initialize_groups
from k_means_logic import run_kmeans, generate_explanation

def main():
    print("--- 🚀 Phase 1: K-Means CLI Demo ---")
    
    # 1. Initialize Groups
    print("\n[1/4] Initializing 3 Gaussian groups...")
    groups = initialize_groups()
    
    # 2. Collect Data
    # Stack all points into one big array (600, 2)
    all_points = np.vstack([g.points for g in groups])
    
    # Create "ground truth" labels (0, 0, ..., 1, 1, ..., 2, 2, ...)
    original_labels = np.concatenate([
        [i] * g.n_points for i, g in enumerate(groups)
    ])
    
    print(f"Total points generated: {len(all_points)}")

    # 3. Run K-Means
    print("\n[2/4] Running K-Means (K=3)...")
    kmeans_results = run_kmeans(all_points, n_clusters=3)
    
    # 4. Generate Explanation
    print("\n[3/4] Generating statistical explanation...")
    explanation = generate_explanation(groups, kmeans_results, original_labels)
    print(explanation)
    
    # 5. Show Plot
    print("\n[4/4] Displaying plot...")
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plot Ground Truth (Original Groups)
    for i, group in enumerate(groups):
        ax.scatter(
            group.points[:, 0], group.points[:, 1],
            c=group.color,
            label=f"Ground Truth: {group.label}",
            alpha=0.5,
            edgecolor='none'
        )
        # Plot True Mean
        ax.scatter(
            group.mean[0], group.mean[1],
            c=group.color,
            marker='X', s=200, alpha=0.7,
            edgecolor='black',
            label=f"{group.label} True Mean"
        )
        
    # Plot K-Means Results
    cluster_colors = ['#E69F00', '#56B4E9', '#009E73'] # Orange, Blue, Green
    kmeans_labels = kmeans_results['labels']
    
    # Plot K-Means Centroids
    ax.scatter(
        kmeans_results['centroids'][:, 0], kmeans_results['centroids'][:, 1],
        c='black',
        marker='X', s=250,
        edgecolor='white',
        linewidth=2,
        label="K-Means Centroid"
    )
    
    # Add K-Means cluster assignment as an edge color
    for i in range(len(all_points)):
        ax.scatter(
            all_points[i, 0], all_points[i, 1],
            facecolor='none',
            edgecolor=cluster_colors[kmeans_labels[i]],
            linewidth=0.5,
            alpha=0.8
        )

    ax.set_title("K-Means CLI Demo (Phase 1)", fontsize=16)
    ax.set_xlabel("Dimension 1 (X-axis)")
    ax.set_ylabel("Dimension 2 (Y-axis)")
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)
    ax.set_aspect('equal', 'box')
    plt.tight_layout()
    
    print("\n--- ✅ Demo Complete ---")
    print("Close the plot window to exit.")
    plt.show()

if __name__ == "__main__":
    main()