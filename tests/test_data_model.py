# File: tests/test_data_model.py
import numpy as np
import pytest
from src.data_model import GaussianGroup

@pytest.fixture
def default_group():
    """Provides a standard GaussianGroup for testing."""
    return GaussianGroup(
        mean=[2, 3],
        cov=[[1, 0.3], [0.3, 1]],
        n_points=100,
        color='red',
        label='Test Group'
    )

def test_initialization(default_group):
    assert default_group.label == 'Test Group'
    assert default_group.n_points == 100
    assert default_group.points.shape == (100, 2)
    
    # Check empirical mean is close to target mean
    emp_mean = default_group.get_statistics()['empirical_mean']
    assert np.allclose(emp_mean, default_group.mean, atol=0.5)

def test_invalid_covariance():
    with pytest.raises(ValueError):
        # Not positive definite (determinant is 0)
        GaussianGroup([0, 0], [[1, 1], [1, 1]], 100, 'r', 'Bad')

def test_move(default_group):
    original_mean = default_group.mean.copy()
    new_mean = np.array([10, 10])
    default_group.move(new_mean)
    
    assert np.array_equal(default_group.mean, new_mean)
    assert not np.array_equal(default_group.mean, original_mean)
    
    # Check new points are centered around new mean
    emp_mean = default_group.get_statistics()['empirical_mean']
    assert np.allclose(emp_mean, new_mean, atol=0.5)

def test_explode(default_group):
    original_cov = default_group.cov.copy()
    scale_factor = 3.0
    default_group.explode(scale_factor)
    
    assert np.array_equal(default_group.cov, original_cov * scale_factor)
    
    # Check that empirical variance is larger
    original_stats = GaussianGroup([2, 3], [[1, 0.3], [0.3, 1]], 100, 'r', 'Base').get_statistics()
    exploded_stats = default_group.get_statistics()
    
    original_var = np.diag(original_stats['empirical_cov']).sum()
    exploded_var = np.diag(exploded_stats['empirical_cov']).sum()
    
    assert exploded_var > original_var * (scale_factor * 0.5) # Check it's significantly larger