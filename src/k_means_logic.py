# File: src/k_means_logic.py
"""
Implements the K-Means execution and metrics calculation.
Based on PRD FR3 and Task P1-T3.
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from typing import Dict, Any, List

def run_kmeans(data: np.ndarray, n_clusters: int = 3, 
               random_state: int = 42) -> Dict[str, Any]:
    """
    Executes K-Means clustering and computes all required metrics.
    
    Layman's Explanation:
    This is the "engine" that runs the K-Means algorithm.
    - 'init="k-means++"': A smart way to pick starting points, as
      [cite_start]your textbook mentions. [cite: 428]
    - 'n_init=10': Runs the whole algorithm 10 times with different
      starting points and picks the best result. This avoids bad
      [cite_start]"local minima". [cite: 359, 715]
    
    It returns a "report card" (a dictionary) with all the results.
    """
    
    # Handle edge case where data might be too small
    if len(np.unique(data, axis=0)) < n_clusters:
        print("Warning: Not enough unique points to form clusters.")
        return {
            'labels': np.zeros(len(data), dtype=int),
            'centroids': np.array([np.mean(data, axis=0)] * n_clusters),
            'inertia': 0.0,
            'silhouette': 0.0,
            'bcs': 0.0,
            'n_iter': 0
        }

    kmeans = KMeans(
        n_clusters=n_clusters,
        init='k-means++',  # Smart initialization (Arthur & Vassilvitskii, 2007)
        n_init=10,         # Run 10 times and pick the best one
        max_iter=300,
        random_state=random_state
    )
    
    labels = kmeans.fit_predict(data)
    
    # --- Calculate Metrics ---
    
    # 1. Inertia (WCSS) - Provided by scikit-learn
    # [cite_start]This is the J(C, μ) function from your textbook. [cite: 273]
    inertia = kmeans.inertia_
    
    # 2. Silhouette Score - Using scikit-learn
    # [cite_start]This measures how well-separated clusters are. [cite: 1005]
    # It needs at least 2 unique labels to calculate.
    if len(np.unique(labels)) < 2:
        silhouette = 0.0
    else:
        silhouette = silhouette_score(data, labels)
    
    # 3. Between-Cluster Scatter (BCS) - Manual Calculation
    # This measures how far apart the *centers* of the clusters are.
    # As your book proves (Appendix B), minimizing Inertia (WCSS)
    # [cite_start]is the same as maximizing BCS! [cite: 363, 1832]
    global_mean = np.mean(data, axis=0)
    bcs = 0.0
    for k in range(n_clusters):
        # Find points belonging to this cluster
        cluster_points = data[labels == k]
        if len(cluster_points) > 0:
            # |C_k|
            num_points_in_cluster = len(cluster_points)
            # ||μ_k - μ||²
            distance_sq = np.sum((kmeans.cluster_centers_[k] - global_mean)**2)
            # |C_k| * ||μ_k - μ||²
            bcs += num_points_in_cluster * distance_sq

    return {
        'labels': labels,
        'centroids': kmeans.cluster_centers_,
        'inertia': inertia,
        'silhouette': silhouette,
        'bcs': bcs,
        'n_iter': kmeans.n_iter_
    }

def generate_explanation(groups: List['GaussianGroup'], kmeans_results: Dict[str, Any], 
                        original_labels: np.ndarray) -> str:
    """
    Creates a layman-friendly, detailed, and educational interpretation of the K-Means results.
    This is the full implementation for Task P4.
    """
    silhouette = kmeans_results['silhouette']
    inertia = kmeans_results['inertia']
    bcs = kmeans_results['bcs']
    n_iter = kmeans_results['n_iter']
    centroids = kmeans_results['centroids']
    kmeans_labels = kmeans_results['labels']
    
    # --- Header ---
    explanation = f"""
╔══════════════════════════════════════════════════════╗
║           K-MEANS CLUSTERING ANALYSIS                ║
╠══════════════════════════════════════════════════════╣
║ Metric                  | Value                      ║
╟─────────────────────────|────────────────────────────╢
║ Convergence             | {n_iter} iterations                  
║ Inertia (WCSS)          | {inertia:,.2f}                       
║ Silhouette Score        | {silhouette:.3f}                  
║ Between-Cluster Scatter | {bcs:,.2f}                  
╚══════════════════════════════════════════════════════╝
"""
    
    # --- Main Interpretation based on Silhouette Score ---
    explanation += "\n--- Overall Clustering Quality ---\n"
    if silhouette > 0.7:
        explanation += (
            f"✅ EXCELLENT (Silhouette: {silhouette:.3f})\n"
            "   The clusters are tight and very well-separated. The high silhouette score\n"
            "   indicates that points are much closer to their own cluster's center than\n"
            "   to other clusters. K-Means has successfully identified the natural groups."
        )
    elif silhouette > 0.5:
        explanation += (
            f"⚠️ MODERATE (Silhouette: {silhouette:.3f})\n"
            "   The clusters are reasonable, but there is some overlap. This score suggests\n"
            "   that some points are close to the boundary between clusters. This is common\n"
            "   if you dragged groups close together or 'exploded' a group's variance."
        )
    else:
        explanation += (
            f"❌ POOR (Silhouette: {silhouette:.3f})\n"
            "   The clusters are highly overlapped or ill-defined. K-Means is struggling\n"
            "   to find a good fit. This often happens when the underlying groups are not\n"
            "   spherical, have widely different variances, or are very close together."
        )

    # --- Detailed Analysis: Misclassification and Group Purity ---
    explanation += "\n\n--- Group-by-Group Analysis ---\n"
    
    # We need to find the best mapping between original groups and K-Means clusters
    # This is a classic assignment problem, solvable with the Hungarian algorithm,
    # but for K=3, a simple greedy approach is usually sufficient.
    group_to_cluster_map = {}
    unassigned_clusters = list(range(len(groups)))
    
    for i, group in enumerate(groups):
        best_jaccard = -1
        best_cluster = -1
        group_points_mask = (original_labels == i)
        
        for cluster_idx in unassigned_clusters:
            cluster_points_mask = (kmeans_labels == cluster_idx)
            intersection = np.sum(group_points_mask & cluster_points_mask)
            union = np.sum(group_points_mask | cluster_points_mask)
            jaccard = intersection / union if union > 0 else 0
            
            if jaccard > best_jaccard:
                best_jaccard = jaccard
                best_cluster = cluster_idx
        
        if best_cluster != -1:
            group_to_cluster_map[i] = best_cluster
            unassigned_clusters.remove(best_cluster)

    # Handle any unmapped clusters (can happen with severe splits/merges)
    if unassigned_clusters:
        for i in range(len(groups)):
            if i not in group_to_cluster_map:
                group_to_cluster_map[i] = unassigned_clusters.pop(0)

    total_misclassified = 0
    for i, group in enumerate(groups):
        group_mask = (original_labels == i)
        assigned_cluster = group_to_cluster_map.get(i, -1)
        
        correctly_classified = np.sum(group_mask & (kmeans_labels == assigned_cluster))
        misclassified = group.n_points - correctly_classified
        total_misclassified += misclassified
        
        purity = (correctly_classified / group.n_points) * 100
        
        explanation += (
            f"\n▶️ {group.label} (True Color: {group.color}):\n"
            f"   - Purity: {purity:.1f}% of its points were correctly assigned to Cluster {assigned_cluster}.\n"
            f"   - Misclassified: {misclassified} points ({misclassified/group.n_points:.1%}) were assigned elsewhere.\n"
        )

    misclass_rate = total_misclassified / len(original_labels)
    explanation += f"\nOverall Misclassification Rate: {misclass_rate:.1%}"

    # --- Centroid Drift Analysis ---
    explanation += "\n\n--- Centroid Drift Analysis ---\n"
    explanation += "   'Drift' is the distance between a group's true center and the K-Means centroid.\n"
    explanation += "   Large drift indicates that the cluster's center was 'pulled' by other groups.\n"
    
    for i, group in enumerate(groups):
        assigned_cluster = group_to_cluster_map.get(i, -1)
        if assigned_cluster != -1:
            centroid = centroids[assigned_cluster]
            drift = np.linalg.norm(group.mean - centroid)
            
            drift_emoji = "✅" if drift < 0.5 else ("⚠️" if drift < 1.5 else "❌")
            
            explanation += (
                f"   {drift_emoji} {group.label} ↔ Cluster {assigned_cluster}: Drift of {drift:.2f} units.\n"
            )

    # --- Educational Insights ---
    explanation += "\n\n--- Educational Insights ---\n"
    if silhouette < 0.5 or misclass_rate > 0.25:
        explanation += (
            "   🧠 Why did K-Means perform poorly? K-Means makes three key assumptions:\n"
            "      1. Clusters are spherical (like circles).\n"
            "      2. Clusters have similar sizes and densities.\n"
            "      3. It uses distance-to-center to assign points.\n"
            "   Your current data likely violates one or more of these. For example, an\n"
            "   'exploded' group is no longer spherical, causing K-Means to split it.\n"
        )
    else:
        explanation += (
            "   🧠 Why did K-Means work well? The current data likely fits the assumptions\n"
            "      of K-Means: the groups are relatively spherical, well-separated, and have\n"
            "      similar density. This is the ideal scenario for this algorithm.\n"
        )
    
    explanation += (
        "\n   💡 Experiment Idea: Try dragging one group directly on top of another and\n"
        "      rerun K-Means. Observe how the centroids and assignments change. You will\n"
        "      likely see two groups merge into a single cluster."
    )

    return explanation