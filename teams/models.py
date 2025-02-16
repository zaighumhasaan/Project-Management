from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project  # Importing the Project model

User = get_user_model()

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Many-to-Many Relationship: A team can have multiple members (users)
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    
    # Many-to-Many Relationship: A team can be assigned to multiple projects
    projects = models.ManyToManyField(Project, related_name='teams', blank=True)

    def __str__(self):
        return self.name
