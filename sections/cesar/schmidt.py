"""
Schmidt Rank Calculator - Mathematical Functions
Calculates Schmidt rank and decomposition for bipartite quantum states
"""

import numpy as np
from scipy.linalg import svd


def calculate_schmidt_rank(state_vector, dim_a, dim_b):
    """
    Calculate Schmidt rank and decomposition.
    
    Args:
        state_vector: numpy array of state vector
        dim_a: dimension of subsystem A
        dim_b: dimension of subsystem B
    
    Returns:
        dict with schmidt_rank, coefficients, entropy, is_entangled
    """
    # Reshape to matrix
    state_matrix = state_vector.reshape(dim_a, dim_b)
    
    # Singular Value Decomposition
    U, singular_values, Vh = svd(state_matrix, full_matrices=False)
    
    # Schmidt coefficients = singular values
    schmidt_coeffs = singular_values
    
    # Count non-zero coefficients (Schmidt rank)
    tolerance = 1e-10
    schmidt_rank = np.sum(schmidt_coeffs > tolerance)
    
    # Entanglement check
    is_entangled = schmidt_rank > 1
    
    # Von Neumann entropy
    nonzero_coeffs = schmidt_coeffs[schmidt_coeffs > tolerance]
    probs = nonzero_coeffs ** 2
    entropy = -np.sum(probs * np.log2(probs + 1e-15))
    
    return {
        'schmidt_rank': int(schmidt_rank),
        'coefficients': schmidt_coeffs.tolist(),
        'is_entangled': bool(is_entangled),
        'entropy': float(entropy)
    }


def normalize_state(state_vector):
    """Normalize quantum state vector"""
    norm = np.linalg.norm(state_vector)
    if norm < 1e-10:
        raise ValueError("State vector has zero norm")
    return state_vector / norm


def parse_state_input(input_string):
    """
    Parse state vector from string.
    Supports: "1, 0, 0, 1" or "[1, 0, 0, 1]"
    """
    cleaned = input_string.strip().strip('[]')
    
    if ',' in cleaned:
        parts = cleaned.split(',')
    else:
        parts = cleaned.split()
    
    try:
        state_vector = np.array([complex(p.strip()) for p in parts])
    except ValueError as e:
        raise ValueError(f"Invalid state vector format: {e}")
    
    return state_vector


def get_predefined_states():
    """Get dictionary of common quantum states"""
    sqrt2 = np.sqrt(2)
    
    return {
        'bell_phi_plus': {
            'name': 'Bell State |Φ+⟩ = (|00⟩ + |11⟩)/√2',
            'vector': np.array([1/sqrt2, 0, 0, 1/sqrt2]),
            'dims': [2, 2]
        },
        'bell_phi_minus': {
            'name': 'Bell State |Φ-⟩ = (|00⟩ - |11⟩)/√2',
            'vector': np.array([1/sqrt2, 0, 0, -1/sqrt2]),
            'dims': [2, 2]
        },
        'bell_psi_plus': {
            'name': 'Bell State |Ψ+⟩ = (|01⟩ + |10⟩)/√2',
            'vector': np.array([0, 1/sqrt2, 1/sqrt2, 0]),
            'dims': [2, 2]
        },
        'product_00': {
            'name': 'Product State |0⟩⊗|0⟩ = |00⟩',
            'vector': np.array([1, 0, 0, 0]),
            'dims': [2, 2]
        },
        'product_plus': {
            'name': 'Product State |+⟩⊗|+⟩',
            'vector': np.array([0.5, 0.5, 0.5, 0.5]),
            'dims': [2, 2]
        },
        'partial': {
            'name': 'Partial Entangled: 0.8|00⟩ + 0.6|11⟩',
            'vector': np.array([0.8, 0, 0, 0.6]),
            'dims': [2, 2]
        },
    }
