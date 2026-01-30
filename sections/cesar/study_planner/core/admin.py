from django.contrib import admin
from django.utils.html import format_html
from .models import Program, Course, Enrollment, Assignment, Grade


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    Admin interface for Program model.
    Displays programs with color coding and progress tracking.
    """
    list_display = ['name', 'university', 'degree_type', 'total_ects_required', 
                   'colored_badge', 'is_active', 'created_at']
    list_filter = ['degree_type', 'is_active', 'university']
    search_fields = ['name', 'university', 'faculty']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'university', 'faculty', 'degree_type')
        }),
        ('Requirements', {
            'fields': ('total_ects_required', 'is_active')
        }),
        ('Appearance', {
            'fields': ('color',)
        }),
        ('Details', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def colored_badge(self, obj):
        """Display color as a visual badge"""
        return format_html(
            '<span style="background-color: {}; padding: 5px 15px; '
            'border-radius: 3px; color: white;">{}</span>',
            obj.color,
            obj.color
        )
    colored_badge.short_description = 'Color'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin interface for Course model.
    Displays courses organized by program and semester.
    """
    list_display = ['code', 'name_short', 'program', 'semester', 'ects', 
                   'course_type', 'instructor']
    list_filter = ['program', 'semester_type', 'course_type', 'year']
    search_fields = ['code', 'name', 'instructor']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('program', 'code', 'name')
        }),
        ('Semester & Credits', {
            'fields': ('semester', 'year', 'semester_type', 'ects', 'course_type')
        }),
        ('Course Details', {
            'fields': ('description', 'instructor', 'hours_per_week', 'schedule')
        }),
        ('Resources', {
            'fields': ('syllabus_url',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def name_short(self, obj):
        """Display shortened course name"""
        return obj.get_short_name()
    name_short.short_description = 'Course Name'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin interface for Enrollment model.
    Tracks student enrollments in courses.
    """
    list_display = ['user', 'course_code', 'course_name', 'status', 
                   'is_passed', 'final_grade', 'enrolled_date']
    list_filter = ['status', 'is_passed', 'course__program', 'enrolled_date']
    search_fields = ['user__username', 'user__email', 'course__code', 'course__name']
    readonly_fields = ['created_at', 'updated_at', 'final_grade']
    date_hierarchy = 'enrolled_date'
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('user', 'course', 'status', 'enrolled_date')
        }),
        ('Status', {
            'fields': ('is_passed', 'final_grade')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def course_code(self, obj):
        """Display course code"""
        return obj.course.code
    course_code.short_description = 'Course Code'
    
    def course_name(self, obj):
        """Display course name"""
        return obj.course.get_short_name()
    course_name.short_description = 'Course Name'
    
    def final_grade(self, obj):
        """Display calculated final grade"""
        grade = obj.calculate_final_grade()
        if grade:
            return f"{grade:.2f}"
        return "No grades yet"
    final_grade.short_description = 'Final Grade'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Admin interface for Assignment model.
    Manages course assignments, projects, and exams.
    """
    list_display = ['title', 'course_code', 'assignment_type', 'due_date', 
                   'priority_badge', 'max_points', 'status_badge', 'days_left']
    list_filter = ['assignment_type', 'priority', 'is_completed', 
                  'course__program', 'due_date']
    search_fields = ['title', 'description', 'course__code', 'course__name']
    readonly_fields = ['created_at', 'updated_at', 'days_left']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Assignment Information', {
            'fields': ('course', 'title', 'description', 'assignment_type')
        }),
        ('Due Date & Priority', {
            'fields': ('due_date', 'priority', 'max_points')
        }),
        ('Completion Status', {
            'fields': ('is_completed', 'completed_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'days_left'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_incomplete']
    
    def course_code(self, obj):
        """Display course code"""
        return obj.course.code
    course_code.short_description = 'Course'
    
    def priority_badge(self, obj):
        """Display priority with color coding"""
        colors = {
            'low': '#10B981',      # Green
            'medium': '#F59E0B',   # Orange
            'high': '#EF4444',     # Red
        }
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; '
            'border-radius: 3px; color: white; font-weight: bold;">{}</span>',
            colors.get(obj.priority, '#6B7280'),
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    def status_badge(self, obj):
        """Display completion status with color"""
        if obj.is_completed:
            return format_html(
                '<span style="color: #10B981; font-weight: bold;">✓ Completed</span>'
            )
        elif obj.is_overdue():
            return format_html(
                '<span style="color: #EF4444; font-weight: bold;">⚠ Overdue</span>'
            )
        return format_html(
            '<span style="color: #F59E0B; font-weight: bold;">○ Pending</span>'
        )
    status_badge.short_description = 'Status'
    
    def days_left(self, obj):
        """Show days until due or overdue"""
        if obj.is_completed:
            return "Completed"
        days = obj.days_until_due()
        if days is None:
            return "-"
        if days < 0:
            return format_html(
                '<span style="color: #EF4444; font-weight: bold;">{} days overdue</span>',
                abs(days)
            )
        elif days == 0:
            return format_html(
                '<span style="color: #F59E0B; font-weight: bold;">Due today!</span>'
            )
        elif days <= 3:
            return format_html(
                '<span style="color: #F59E0B;">{} days left</span>',
                days
            )
        return f"{days} days left"
    days_left.short_description = 'Time Left'
    
    def mark_as_completed(self, request, queryset):
        """Bulk action to mark assignments as completed"""
        for assignment in queryset:
            assignment.mark_completed()
        self.message_user(request, f"{queryset.count()} assignments marked as completed.")
    mark_as_completed.short_description = "Mark selected as completed"
    
    def mark_as_incomplete(self, request, queryset):
        """Bulk action to mark assignments as incomplete"""
        queryset.update(is_completed=False, completed_date=None)
        self.message_user(request, f"{queryset.count()} assignments marked as incomplete.")
    mark_as_incomplete.short_description = "Mark selected as incomplete"


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """
    Admin interface for Grade model.
    Manages grades for assignments and courses.
    """
    list_display = ['enrollment_info', 'assignment_title', 'grade', 
                   'points_display', 'weight', 'date']
    list_filter = ['enrollment__course__program', 'date', 'grade']
    search_fields = ['enrollment__user__username', 'enrollment__course__code', 
                    'assignment__title']
    readonly_fields = ['created_at', 'updated_at', 'percentage_display']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Grade Information', {
            'fields': ('enrollment', 'assignment', 'grade', 'weight')
        }),
        ('Points', {
            'fields': ('points', 'max_points', 'percentage_display')
        }),
        ('Details', {
            'fields': ('date', 'comment')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def enrollment_info(self, obj):
        """Display enrollment information"""
        return f"{obj.enrollment.user.username} - {obj.enrollment.course.code}"
    enrollment_info.short_description = 'Student - Course'
    
    def assignment_title(self, obj):
        """Display assignment title or 'Final Grade'"""
        if obj.assignment:
            return obj.assignment.title
        return "Final Grade"
    assignment_title.short_description = 'Assignment'
    
    def points_display(self, obj):
        """Display points as fraction"""
        if obj.points is not None and obj.max_points:
            percentage = obj.get_percentage()
            return f"{obj.points}/{obj.max_points} ({percentage}%)"
        return "-"
    points_display.short_description = 'Points'
    
    def percentage_display(self, obj):
        """Display percentage score"""
        percentage = obj.get_percentage()
        if percentage is not None:
            return f"{percentage}%"
        return "N/A"
    percentage_display.short_description = 'Percentage Score'


# Customize admin site
admin.site.site_header = "Study Planner Administration"
admin.site.site_title = "Study Planner Admin"
admin.site.index_title = "Manage Your Academic Data"
