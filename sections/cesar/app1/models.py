from django.db import models
import json


class Calculation(models.Model):
    state_vector = models.TextField()
    dimension_a = models.IntegerField()
    dimension_b = models.IntegerField()
    state_name = models.CharField(max_length=200, blank=True)
    schmidt_rank = models.IntegerField()
    schmidt_coefficients = models.TextField()
    is_entangled = models.BooleanField()
    entropy = models.FloatField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_state_vector_list(self):
        return json.loads(self.state_vector)

    def get_coefficients_list(self):
        return json.loads(self.schmidt_coefficients)
