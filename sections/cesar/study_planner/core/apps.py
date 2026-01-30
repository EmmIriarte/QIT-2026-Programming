from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration for the core application.
    This app handles all main functionality: programs, courses, enrollments, grades.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Study Planner Core'
