# File: tests/test_k_means_logic.py
import numpy as np
import pytest
from src.k_means_logic import run_kmeans

@pytest.fixture
def simple_data():
    """Three well-separated clusters."""
    g1 = np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]], 50)
    g2 = np.random.multivariate_normal([10, 0], [[1, 0], [0, 1]], 50)
    g3 = np.random.multivariate_normal([0, 10], [[1, 0], [0, 1]], 50)
    return np.vstack([g1, g2, g3])

def test_run_kmeans_output(simple_data):
    results = run_kmeans(simple_data, n_clusters=3)
    
    assert 'labels' in results
    assert 'centroids' in results
    assert 'inertia' in results
    assert 'silhouette' in results
    assert 'bcs' in results
    assert 'n_iter' in results
    
    assert len(results['labels']) == 150
    assert results['centroids'].shape == (3, 2)
    assert results['silhouette'] > 0.7 # Should be well-separated
    assert results['inertia'] > 0
    assert results['bcs'] > 0

def test_determinism(simple_data):
    results1 = run_kmeans(simple_data, n_clusters=3, random_state=42)
    results2 = run_kmeans(simple_data, n_clusters=3, random_state=42)
    
    assert np.array_equal(results1['labels'], results2['labels'])
    assert np.allclose(results1['centroids'], results2['centroids'])
    assert results1['inertia'] == results2['inertia']

def test_bcs_wcss_tss(simple_data):
    results = run_kmeans(simple_data, n_clusters=3)
    
    wcss = results['inertia'] # WCSS is Inertia
    bcs = results['bcs']
    
    # Calculate Total Sum of Squares (TSS)
    global_mean = np.mean(simple_data, axis=0)
    tss = np.sum(np.linalg.norm(simple_data - global_mean, axis=1)**2)
    
    # [cite_start]Check the identity: TSS = WCSS + BCS [cite: 369]
    assert np.isclose(tss, wcss + bcs)