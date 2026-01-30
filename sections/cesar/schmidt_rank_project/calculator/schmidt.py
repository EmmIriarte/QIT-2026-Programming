"""
Schmidt Rank and Decomposition Calculations

This module contains functions for calculating Schmidt rank and decomposition
of bipartite quantum states.
"""

import numpy as np
from scipy.linalg import svd
from typing import Tuple, List, Dict


def calculate_schmidt_decomposition(state_vector: np.ndarray, 
                                    dim_a: int, 
                                    dim_b: int) -> Dict:
    """
    Calculate Schmidt decomposition of a bipartite quantum state.
    
    Args:
        state_vector: 1D numpy array representing the quantum state
        dim_a: Dimension of subsystem A
        dim_b: Dimension of subsystem B
    
    Returns:
        Dictionary containing:
        - schmidt_rank: Number of non-zero Schmidt coefficients
        - schmidt_coefficients: List of Schmidt coefficients
        - is_entangled: Boolean indicating if state is entangled
        - entropy: Von Neumann entropy
        - u_matrix: Unitary matrix for subsystem A
        - v_matrix: Unitary matrix for subsystem B
    """
    
    # Reshape state vector into matrix form
    state_matrix = state_vector.reshape(dim_a, dim_b)
    
    # Perform Singular Value Decomposition
    U, singular_values, Vh = svd(state_matrix, full_matrices=False)
    
    # Schmidt coefficients are the singular values
    schmidt_coefficients = singular_values
    
    # Calculate Schmidt rank (number of non-zero coefficients)
    tolerance = 1e-10
    schmidt_rank = np.sum(schmidt_coefficients > tolerance)
    
    # Determine if state is entangled
    is_entangled = schmidt_rank > 1
    
    # Calculate Von Neumann entropy
    # S = -Σ λᵢ² log₂(λᵢ²)
    nonzero_coeffs = schmidt_coefficients[schmidt_coefficients > tolerance]
    probabilities = nonzero_coeffs ** 2
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-15))
    
    return {
        'schmidt_rank': int(schmidt_rank),
        'schmidt_coefficients': schmidt_coefficients.tolist(),
        'is_entangled': bool(is_entangled),
        'entropy': float(entropy),
        'u_matrix': U.tolist(),
        'v_matrix': Vh.tolist(),
        'state_matrix': state_matrix.tolist()
    }


def normalize_state(state_vector: np.ndarray) -> np.ndarray:
    """
    Normalize a quantum state vector.
    
    Args:
        state_vector: Input state vector
    
    Returns:
        Normalized state vector
    """
    norm = np.linalg.norm(state_vector)
    if norm < 1e-10:
        raise ValueError("State vector has zero norm")
    return state_vector / norm


def get_predefined_states() -> Dict[str, Dict]:
    """
    Get dictionary of predefined quantum states for testing.
    
    Returns:
        Dictionary of state name -> state info
    """
    sqrt2 = np.sqrt(2)
    
    states = {
        'bell_phi_plus': {
            'name': 'Bell State |Φ+⟩',
            'description': 'Maximally entangled: (|00⟩ + |11⟩)/√2',
            'vector': np.array([1/sqrt2, 0, 0, 1/sqrt2]),
            'dimensions': [2, 2],
            'expected_rank': 2
        },
        'bell_phi_minus': {
            'name': 'Bell State |Φ-⟩',
            'description': 'Maximally entangled: (|00⟩ - |11⟩)/√2',
            'vector': np.array([1/sqrt2, 0, 0, -1/sqrt2]),
            'dimensions': [2, 2],
            'expected_rank': 2
        },
        'bell_psi_plus': {
            'name': 'Bell State |Ψ+⟩',
            'description': 'Maximally entangled: (|01⟩ + |10⟩)/√2',
            'vector': np.array([0, 1/sqrt2, 1/sqrt2, 0]),
            'dimensions': [2, 2],
            'expected_rank': 2
        },
        'bell_psi_minus': {
            'name': 'Bell State |Ψ-⟩',
            'description': 'Maximally entangled: (|01⟩ - |10⟩)/√2',
            'vector': np.array([0, 1/sqrt2, -1/sqrt2, 0]),
            'dimensions': [2, 2],
            'expected_rank': 2
        },
        'product_00': {
            'name': 'Product State |0⟩⊗|0⟩',
            'description': 'Not entangled: |00⟩',
            'vector': np.array([1, 0, 0, 0]),
            'dimensions': [2, 2],
            'expected_rank': 1
        },
        'product_01': {
            'name': 'Product State |0⟩⊗|1⟩',
            'description': 'Not entangled: |01⟩',
            'vector': np.array([0, 1, 0, 0]),
            'dimensions': [2, 2],
            'expected_rank': 1
        },
        'product_plus_plus': {
            'name': 'Product State |+⟩⊗|+⟩',
            'description': 'Not entangled: (|0⟩+|1⟩)⊗(|0⟩+|1⟩)/2',
            'vector': np.array([0.5, 0.5, 0.5, 0.5]),
            'dimensions': [2, 2],
            'expected_rank': 1
        },
        'partial_entangled': {
            'name': 'Partially Entangled State',
            'description': 'Partially entangled: 0.8|00⟩ + 0.6|11⟩',
            'vector': np.array([0.8, 0, 0, 0.6]),
            'dimensions': [2, 2],
            'expected_rank': 2
        },
        'w_state': {
            'name': 'W-like State (2×2)',
            'description': 'Symmetric entangled state',
            'vector': np.array([1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3), 0]),
            'dimensions': [2, 2],
            'expected_rank': 2
        },
    }
    
    return states


def parse_state_input(input_string: str) -> np.ndarray:
    """
    Parse state vector from string input.
    
    Supports formats:
    - "[1, 0, 0, 1]"
    - "1, 0, 0, 1"
    - "1 0 0 1"
    - Complex numbers: "1+2j, 0, 0, 1-j"
    
    Args:
        input_string: String representation of state vector
    
    Returns:
        numpy array of state vector
    """
    # Remove brackets and extra whitespace
    cleaned = input_string.strip().strip('[]')
    
    # Try to split by comma first, then by space
    if ',' in cleaned:
        parts = cleaned.split(',')
    else:
        parts = cleaned.split()
    
    # Convert to complex numbers (handles real numbers too)
    try:
        state_vector = np.array([complex(p.strip()) for p in parts])
    except ValueError as e:
        raise ValueError(f"Invalid state vector format: {e}")
    
    return state_vector


def generate_random_state(dim_a: int, dim_b: int, 
                         target_rank: int = None) -> np.ndarray:
    """
    Generate a random quantum state.
    
    Args:
        dim_a: Dimension of subsystem A
        dim_b: Dimension of subsystem B
        target_rank: Target Schmidt rank (None for random)
    
    Returns:
        Random normalized state vector
    """
    total_dim = dim_a * dim_b
    
    if target_rank is None:
        # Generate fully random state
        real_part = np.random.randn(total_dim)
        imag_part = np.random.randn(total_dim)
        state = real_part + 1j * imag_part
    else:
        # Generate state with specific rank
        if target_rank > min(dim_a, dim_b):
            target_rank = min(dim_a, dim_b)
        
        # Generate random orthonormal bases
        U = np.random.randn(dim_a, dim_a) + 1j * np.random.randn(dim_a, dim_a)
        U, _ = np.linalg.qr(U)
        
        V = np.random.randn(dim_b, dim_b) + 1j * np.random.randn(dim_b, dim_b)
        V, _ = np.linalg.qr(V)
        
        # Generate random Schmidt coefficients
        coeffs = np.random.rand(target_rank)
        coeffs = coeffs / np.linalg.norm(coeffs)
        coeffs = np.sort(coeffs)[::-1]  # Sort descending
        
        # Construct state
        state_matrix = np.zeros((dim_a, dim_b), dtype=complex)
        for i in range(target_rank):
            state_matrix += coeffs[i] * np.outer(U[:, i], V[:, i])
        
        state = state_matrix.flatten()
    
    # Normalize
    return normalize_state(state)


def validate_dimensions(state_vector: np.ndarray, 
                       dim_a: int, 
                       dim_b: int) -> bool:
    """
    Validate that state vector dimensions match specified subsystem dimensions.
    
    Args:
        state_vector: State vector
        dim_a: Dimension of subsystem A
        dim_b: Dimension of subsystem B
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    expected_size = dim_a * dim_b
    actual_size = len(state_vector)
    
    if actual_size != expected_size:
        raise ValueError(
            f"State vector size ({actual_size}) doesn't match "
            f"dimensions {dim_a}×{dim_b} = {expected_size}"
        )
    
    return True
