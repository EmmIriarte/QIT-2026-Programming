import numpy as np


def parse_state_input(state_str):
    values = [complex(x.strip()) for x in state_str.split(',')]
    return np.array(values)


def normalize_state(state_vector):
    norm = np.linalg.norm(state_vector)
    if norm == 0:
        raise ValueError("State vector cannot be zero.")
    return state_vector / norm


def validate_dimensions(state_vector, dim_a, dim_b):
    expected = dim_a * dim_b
    if len(state_vector) != expected:
        raise ValueError(
            f"State vector length {len(state_vector)} does not match "
            f"dimensions {dim_a}x{dim_b}={expected}."
        )


def calculate_schmidt_decomposition(state_vector, dim_a, dim_b):
    matrix = state_vector.reshape(dim_a, dim_b)
    U, s, Vh = np.linalg.svd(matrix, full_matrices=False)
    threshold = 1e-10
    schmidt_coefficients = s[s > threshold].tolist()
    schmidt_rank = len(schmidt_coefficients)
    is_entangled = schmidt_rank > 1
    entropy = -sum(c**2 * np.log2(c**2) for c in schmidt_coefficients if c > 0)
    return {
        'schmidt_rank': schmidt_rank,
        'schmidt_coefficients': schmidt_coefficients,
        'is_entangled': is_entangled,
        'entropy': float(entropy),
    }


def get_predefined_states():
    return {
        'bell_phi_plus': {
            'name': 'Bell State |Phi+>',
            'vector': np.array([1, 0, 0, 1]) / np.sqrt(2),
            'dimensions': (2, 2),
        },
        'bell_phi_minus': {
            'name': 'Bell State |Phi->',
            'vector': np.array([1, 0, 0, -1]) / np.sqrt(2),
            'dimensions': (2, 2),
        },
        'product_00': {
            'name': 'Product State |00>',
            'vector': np.array([1, 0, 0, 0], dtype=complex),
            'dimensions': (2, 2),
        },
    }


def generate_random_state(dim_a, dim_b, rank=None):
    size = dim_a * dim_b
    if rank is None:
        rank = min(dim_a, dim_b)
    rank = min(rank, dim_a, dim_b)
    state = np.zeros(size, dtype=complex)
    for i in range(rank):
        a = np.random.randn(dim_a) + 1j * np.random.randn(dim_a)
        b = np.random.randn(dim_b) + 1j * np.random.randn(dim_b)
        state += np.kron(a, b)
    return normalize_state(state)
