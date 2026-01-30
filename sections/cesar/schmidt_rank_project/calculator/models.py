from django.db import models
from django.utils import timezone
import json


class Calculation(models.Model):
    """
    Stores Schmidt rank calculation results.
    """
    # Input data
    state_vector = models.TextField(
        help_text="JSON array of state vector components"
    )
    dimension_a = models.IntegerField(
        help_text="Dimension of subsystem A"
    )
    dimension_b = models.IntegerField(
        help_text="Dimension of subsystem B"
    )
    state_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional name for the state (e.g., 'Bell State')"
    )
    
    # Results
    schmidt_rank = models.IntegerField(
        help_text="Schmidt rank of the state"
    )
    schmidt_coefficients = models.TextField(
        help_text="JSON array of Schmidt coefficients"
    )
    is_entangled = models.BooleanField(
        help_text="Whether the state is entangled"
    )
    entropy = models.FloatField(
        help_text="Von Neumann entropy"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    notes = models.TextField(
        blank=True,
        help_text="Optional notes about the calculation"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Calculation'
        verbose_name_plural = 'Calculations'
    
    def __str__(self):
        if self.state_name:
            return f"{self.state_name} (Rank: {self.schmidt_rank})"
        return f"Calculation {self.id} (Rank: {self.schmidt_rank})"
    
    def get_state_vector_list(self):
        """Parse state vector JSON to list"""
        try:
            return json.loads(self.state_vector)
        except:
            return []
    
    def get_coefficients_list(self):
        """Parse Schmidt coefficients JSON to list"""
        try:
            return json.loads(self.schmidt_coefficients)
        except:
            return []
    
    def get_short_vector(self, max_length=50):
        """Get shortened version of state vector for display"""
        vector_str = self.state_vector
        if len(vector_str) > max_length:
            return vector_str[:max_length] + "..."
        return vector_str
    
    def get_entanglement_type(self):
        """Get human-readable entanglement type"""
        if not self.is_entangled:
            return "Product State (Not Entangled)"
        elif self.schmidt_rank == min(self.dimension_a, self.dimension_b):
            return "Maximally Entangled"
        else:
            return "Partially Entangled"
