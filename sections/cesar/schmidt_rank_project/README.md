# Schmidt Rank Calculator

A Django web application for calculating Schmidt rank and decomposition of quantum states.

## Overview

This application allows you to:
- Calculate Schmidt rank of bipartite quantum states
- Compute Schmidt decomposition
- Visualize Schmidt coefficients
- Determine if a state is entangled
- Store and view calculation history

## What is Schmidt Rank?

The Schmidt rank is the number of non-zero Schmidt coefficients in the Schmidt decomposition of a bipartite quantum state. It measures the degree of entanglement:
- Schmidt rank = 1: Product state (not entangled)
- Schmidt rank > 1: Entangled state

## Features

- **Input Methods**:
  - Direct matrix input
  - Predefined quantum states (Bell states, etc.)
  - Random state generation

- **Calculations**:
  - Schmidt rank
  - Schmidt coefficients
  - Singular value decomposition
  - Entanglement entropy

- **Visualization**:
  - Bar chart of Schmidt coefficients
  - Matrix heatmap
  - Calculation history

## Technology Stack

- **Backend**: Django 5.0
- **Mathematics**: NumPy, SciPy
- **Visualization**: Matplotlib, Chart.js
- **Frontend**: Bootstrap 5
- **Database**: SQLite

## Installation

### Prerequisites
- Python 3.11+
- pip

### Setup

1. **Extract the project**
```bash
# Extract to your desired location
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Run server**
```bash
python manage.py runserver
```

7. **Access application**
- Main app: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Usage Examples

### Example 1: Bell State (Maximally Entangled)

```python
# |Φ+⟩ = (|00⟩ + |11⟩)/√2
State vector: [1/√2, 0, 0, 1/√2]
Schmidt rank: 2
Schmidt coefficients: [0.707, 0.707]
```

### Example 2: Product State (Not Entangled)

```python
# |0⟩ ⊗ |0⟩
State vector: [1, 0, 0, 0]
Schmidt rank: 1
Schmidt coefficients: [1.0]
```

### Example 3: Partially Entangled State

```python
# State vector: [0.8, 0.0, 0.0, 0.6]
Schmidt rank: 2
Schmidt coefficients: [0.8, 0.6]
```

## Mathematical Background

For a bipartite quantum state |ψ⟩ in Hilbert space H_A ⊗ H_B, the Schmidt decomposition is:

|ψ⟩ = Σᵢ λᵢ |iᴬ⟩ ⊗ |iᴮ⟩

Where:
- λᵢ are Schmidt coefficients (non-negative)
- |iᴬ⟩ and |iᴮ⟩ are orthonormal bases
- Schmidt rank = number of non-zero λᵢ

The application uses Singular Value Decomposition (SVD) to compute the Schmidt decomposition.

## Project Structure

```
schmidt_rank_project/
├── manage.py
├── requirements.txt
├── README.md
├── config/              # Django settings
├── calculator/          # Main application
│   ├── models.py       # Database models
│   ├── views.py        # View logic
│   ├── forms.py        # Input forms
│   ├── schmidt.py      # Schmidt rank calculations
│   ├── templates/      # HTML templates
│   └── static/         # CSS, JS
└── db.sqlite3          # Database
```

## API (Optional Future Enhancement)

The application can be extended with a REST API:

```python
POST /api/calculate/
{
    "state_vector": [0.707, 0, 0, 0.707],
    "dimensions": [2, 2]
}

Response:
{
    "schmidt_rank": 2,
    "schmidt_coefficients": [0.707, 0.707],
    "is_entangled": true,
    "entropy": 0.693
}
```

## Contributing

This is a project for QIT course at University of Gdańsk.

## Related Concepts

- Quantum Entanglement
- Singular Value Decomposition (SVD)
- Von Neumann Entropy
- Bipartite Systems
- Quantum Information Theory

## References

- Nielsen & Chuang, "Quantum Computation and Quantum Information"
- QIT Course Materials, University of Gdańsk

## License

MIT License

## Author

Created for Quantum Information Technology course
University of Gdańsk, 2026
