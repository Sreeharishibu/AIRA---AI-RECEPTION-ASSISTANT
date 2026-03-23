from django.db import models

class ChatbotQuery(models.Model):
    query = models.CharField(max_length=255, unique=True)
    response = models.TextField()

    def __str__(self):
        return self.query
    
def detail_image_upload_path(instance, filename):
    """
    Decide subfolder based on category.
    Result: media/announcements/xxx or media/placements/xxx
    """
    if instance.category == 'ANNOUNCEMENT':
        folder = 'announcements'
    elif instance.category == 'PLACEMENT':
        folder = 'placements'
    else:
        folder = 'others'
    return f"{folder}/{filename}"


class DetailImage(models.Model):
    CATEGORY_CHOICES = [
        ('ANNOUNCEMENT', 'Announcement'),
        ('PLACEMENT', 'Placement'),
    ]

    title = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to=detail_image_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.title or self.image.name}"
    
class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ("STATIONERY", "Stationery"),
        ("ELECTRONICS", "Electronics"),
        ("LAB", "Lab Equipment"),
        ("FURNITURE", "Furniture"),
        ("OTHER", "Other"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="OTHER"
    )
    quantity = models.PositiveIntegerField(default=0)
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Lab/room/store location (optional)",
    )
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
    
class PlacementSummary(models.Model):
    total_offers = models.PositiveIntegerField(default=0)
    highest_package = models.CharField(max_length=50)
    average_package = models.CharField(max_length=50)
    top_recruiters = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Placement Summary"