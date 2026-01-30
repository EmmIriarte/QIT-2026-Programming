from django.contrib import admin
from django.utils.html import format_html
from .models import Calculation


@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ['id', 'state_name_display', 'schmidt_rank', 'entanglement_badge',
                   'dimensions_display', 'entropy_display', 'created_at']
    list_filter = ['is_entangled', 'schmidt_rank', 'created_at']
    search_fields = ['state_name', 'notes']
    readonly_fields = ['created_at', 'schmidt_rank', 'schmidt_coefficients', 
                      'is_entangled', 'entropy']
    
    fieldsets = (
        ('Input', {
            'fields': ('state_name', 'state_vector', 'dimension_a', 'dimension_b')
        }),
        ('Results', {
            'fields': ('schmidt_rank', 'schmidt_coefficients', 'is_entangled', 'entropy')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at')
        }),
    )
    
    def state_name_display(self, obj):
        if obj.state_name:
            return obj.state_name
        return f"Calculation {obj.id}"
    state_name_display.short_description = 'State Name'
    
    def dimensions_display(self, obj):
        return f"{obj.dimension_a} × {obj.dimension_b}"
    dimensions_display.short_description = 'Dimensions'
    
    def entropy_display(self, obj):
        return f"{obj.entropy:.4f}"
    entropy_display.short_description = 'Entropy'
    
    def entanglement_badge(self, obj):
        if obj.is_entangled:
            if obj.schmidt_rank == min(obj.dimension_a, obj.dimension_b):
                return format_html(
                    '<span style="background-color: #EF4444; padding: 3px 10px; '
                    'border-radius: 3px; color: white; font-weight: bold;">Max Entangled</span>'
                )
            else:
                return format_html(
                    '<span style="background-color: #F59E0B; padding: 3px 10px; '
                    'border-radius: 3px; color: white; font-weight: bold;">Entangled</span>'
                )
        return format_html(
            '<span style="background-color: #10B981; padding: 3px 10px; '
            'border-radius: 3px; color: white; font-weight: bold;">Product State</span>'
        )
    entanglement_badge.short_description = 'Entanglement'
