import uuid
from django.db import models
from django.conf import settings
from apps.regions.models import District

# TODO: Add transition validators if using FSM library in the future
STATUS_TRANSITIONS = {
    'draft': ['submitted'],
    'submitted': ['under_review', 'rejected'],
    'under_review': ['approved', 'rejected'],
    'approved': ['resolved'],
    'rejected': [],
    'resolved': [],
}


class Report(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('pothole', 'Pothole'),
        ('road_damage', 'Road Damage'),
        ('drainage', 'Drainage'),
        ('landslide', 'Landslide'),
        ('bridge_damage', 'Bridge Damage'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('resolved', 'Resolved'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True, null=True)
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='low')
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # FK to District (apps.regions.District)
    region = models.ForeignKey(
        District, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reports'
    )
    
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_reports'
    )
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_reports'
    )

    rejection_reason = models.TextField(blank=True, null=True) # Set when report is rejected

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self):
        return self.title or f"Report {self.id}"

    def save(self, *args, **kwargs):
        # Auto-generate title if blank: issue_type + timestamp
        if not self.title:
            from django.utils import timezone
            now_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            self.title = f"{self.get_issue_type_display()} - {now_str}"
        super().save(*args, **kwargs)


class ReportImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='reports/images/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Report Image'
        verbose_name_plural = 'Report Images'

    def __str__(self):
        return f"Image for {self.report.title}"


class ReportCluster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    reports = models.ManyToManyField(Report, related_name='clusters', blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_clusters'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Report Cluster'
        verbose_name_plural = 'Report Clusters'

    def __str__(self):
        return self.name
