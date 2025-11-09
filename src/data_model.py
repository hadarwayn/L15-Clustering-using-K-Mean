# File: src/data_model.py
"""
Defines the GaussianGroup class for generating and manipulating data clusters.
Based on PRD FR1 and Task P1-T2.
"""

import numpy as np
from typing import List, Dict, Any

# Set a global random seed for reproducible results
np.random.seed(42)

class GaussianGroup:
    """
    Represents one Gaussian-distributed cluster of 2D points.
    
    Layman's Explanation:
    This class is a "blueprint" for a cloud of points. It knows:
    - Its center (mean)
    - Its shape/spread (covariance)
    - How many points to create (n_points)
    - Its "true" color and name
    """
    
    def __init__(self, mean: List[float], cov: List[List[float]], 
                 n_points: int, color: str, label: str):
        """
        Initializes the group.
        
        Parameters:
        - mean: 2D vector [μₓ, μᵧ] (the center of the cloud)
        - cov: 2x2 covariance matrix (the shape of the cloud)
        - n_points: Number of points in the cloud
        - color: Matplotlib color code (e.g., '#FF5733')
        - label: Group identifier ('A', 'B', 'C')
        """
        self.mean = np.array(mean)
        self.cov = np.array(cov)
        
        # --- Input Validation (Task P1-T2.6) ---
        if self.mean.shape != (2,):
            raise ValueError(f"Mean for {label} must be a 2D vector [x, y].")
        if self.cov.shape != (2, 2):
            raise ValueError(f"Covariance for {label} must be a 2x2 matrix.")
        if np.linalg.det(self.cov) <= 0:
            print(f"Warning: Covariance for {label} is not positive definite. Adding regularization.")
            self.cov += 1e-6 * np.eye(2) # Add small value to diagonal
            
        self.n_points = n_points
        self.color = color
        self.label = label
        
        # Generate the points when the object is created
        self.points = self.generate_points()

    def generate_points(self) -> np.ndarray:
        """
        Samples n_points from the N(μ, Σ) distribution.
        
        Layman's Explanation:
        This is the function that actually creates the cloud of points based
        on the group's center (mean) and shape (covariance).
        """
        return np.random.multivariate_normal(
            self.mean, self.cov, self.n_points
        )

    def move(self, new_mean: np.ndarray) -> None:
        """
        Updates the group's mean (center) and regenerates its points.
        This is for the "drag" functionality.
        """
        print(f"Moving {self.label} to {new_mean}")
        self.mean = np.array(new_mean)
        # We must regenerate the points to reflect the new mean
        self.points = self.generate_points()

    def explode(self, scale_factor: float = 2.0) -> None:
        """
        Increases the group's variance (spread) by scaling the covariance.
        This is for the "explode" functionality.
        """
        print(f"Exploding {self.label} by {scale_factor}x")
        # We multiply the *original* covariance to prevent runaway growth
        # This requires storing the original cov if we want to reset,
        # but for now, we'll just scale the current one.
        self.cov = self.cov * scale_factor
        # Regenerate points with the new, larger shape
        self.points = self.generate_points()

    def get_statistics(self) -> Dict[str, Any]:
        """
        Returns a dictionary of the group's key statistics.
        'Empirical' means what we *actually* measure from the generated points.
        """
        empirical_mean = np.mean(self.points, axis=0)
        empirical_cov = np.cov(self.points.T)
        
        return {
            'label': self.label,
            'color': self.color,
            'n_points': self.n_points,
            'target_mean': self.mean,
            'empirical_mean': empirical_mean,
            'target_cov': self.cov,
            'empirical_cov': empirical_cov
        }

# --- Initial Configuration (Task P1-T4) ---

# This dictionary defines the starting state of our three groups
INITIAL_GROUPS_CONFIG: Dict[str, Dict[str, Any]] = {
    'A': {
        'mean': [2, 3],
        'cov': [[1.0, 0.3], [0.3, 1.0]],
        'color': '#E69F00',  # Orange
        'label': 'Group A',
        'n_points': 200
    },
    'B': {
        'mean': [8, 4],
        'cov': [[1.2, -0.2], [-0.2, 0.8]],
        'color': '#56B4E9',  # Sky Blue
        'label': 'Group B',
        'n_points': 200
    },
    'C': {
        'mean': [5, 8],
        'cov': [[0.9, 0.1], [0.1, 1.1]],
        'color': '#009E73',  # Bluish Green
        'label': 'Group C',
        'n_points': 200
    }
}

def initialize_groups() -> List[GaussianGroup]:
    """
    Creates and returns a list of GaussianGroup objects based
    on the initial configuration.
    """
    groups = []
    for config in INITIAL_GROUPS_CONFIG.values():
        groups.append(
            GaussianGroup(
                mean=config['mean'],
                cov=config['cov'],
                n_points=config['n_points'],
                color=config['color'],
                label=config['label']
            )
        )
    return groups