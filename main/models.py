from django.db import models
from django.contrib.auth.models import User

# Existing Models with a User field
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    project_photo = models.ImageField(upload_to='project_photos/', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)

    date = models.DateField()
    related_posts = models.ManyToManyField(
        'blog.BlogPost',  # Use app_label.ModelName if BlogPost is in another app
        related_name='related_projects', 
        blank=True, 
        help_text="Select any blog posts written about this project."
    )
    def __str__(self):
        return self.project_name

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    description = models.TextField()
    start_month = models.CharField(max_length=20, blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_month = models.CharField(max_length=20, blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    logo = models.ImageField(upload_to='education_logos/', blank=True, null=True)


    def __str__(self):
        return f"{self.degree} at {self.institute}"

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=200)
    institute = models.CharField(max_length=200)
    link = models.URLField()
    date = models.DateField()
    logo = models.ImageField(upload_to='certificate_logos/', blank=True, null=True)
    

    def __str__(self):
        return self.certificate_name



class About(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    resume_pdf = models.FileField(
        upload_to='resumes/',  # Directory inside MEDIA_ROOT where PDFs will be saved
        blank=True,           # The field is optional
        null=True,            # Allows null values in the database
        verbose_name='Resume (PDF)' # Friendly name for the Admin
    )
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    
    # Place the field here, inside the class
    submitted_on = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Message from {self.name}"

# New Models with a User field
from django.db import models
from django.contrib.auth.models import User # Assuming this is your user model

## 1. Define the Category Model
class Category(models.Model):
    """
    Model to store skill categories (e.g., 'Backend', 'Frontend', 'DevOps').
    """
    name = models.CharField(max_length=50, unique=True)
    # Optional: Add an icon or description for the category itself
    # description = models.TextField(blank=True) 

    class Meta:
        verbose_name_plural = "Categories" # Fixes the plural name in the admin

    def __str__(self):
        return self.name

## 2. Update the Skill Model
class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    
    # Replaced the CharField with a ForeignKey linking to the Category model
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, # If a Category is deleted, set this skill's category to NULL
        null=True,                # Allows the field to be NULL in the database
        blank=True,               # Allows the field to be optional in forms
        related_name='skills'     # Allows you to access all skills in a category: category.skills.all()
    )
    
    # NOTE: The value field for Highcharts should ideally be 1-100, 
    # but we'll stick to your 1-5 for now.
    proficiency = models.IntegerField(
        help_text="Enter a number from 1 to 100, where 100 is expert."
    )
    
    icon = models.ImageField(upload_to='skill_icons/', blank=True, null=True)

    def __str__(self):
        return f"{self.skill_name} ({self.proficiency}/5)"

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    start_month = models.CharField(max_length=20, blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_month = models.CharField(max_length=20, blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=50)
    url = models.URLField()
    logo = models.ImageField(upload_to='social_logos/', blank=True, null=True)
    ICON_MAP = {
        'github': 'github',
        'linkedin': 'linkedin',
        'twitter': 'twitter',
        'x': 'twitter',
        'youtube': 'youtube',
        'leetcode': 'code',
        'kaggle': 'activity', 
    }

    # 2. Add a property to dynamically return the icon name
    @property
    def icon_name(self):
        """Returns the appropriate Feather icon name based on the platform name."""
        platform_key = self.platform_name.lower()
        # Use .get() with a default of 'link' to handle unknown platforms
        return self.ICON_MAP.get(platform_key, 'link')

    def __str__(self):
        return self.platform_name

class Award(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    award_name = models.CharField(max_length=200)
    awarded_by = models.CharField(max_length=200)
    date_received = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.award_name
    
    
class ChatSession(models.Model):
    """Represents a single conversation thread for a user."""
    # Link to the user (if logged in)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Optional: Link to the post/page if the conversation is page-specific
    # If the bot is global, you might remove this.
    # post = models.ForeignKey('blog.BlogPost', on_delete=models.CASCADE, null=True, blank=True) 

    session_id = models.CharField(max_length=100, unique=True, db_index=True) # Used by JS/Frontend
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Session {self.session_id} ({self.user.username if self.user else 'Anonymous'})"


class ChatMessage(models.Model):
    """Stores individual messages within a session."""
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    
    # Role: 'user' or 'assistant'
    role = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.session.session_id}: {self.role} - {self.content[:50]}"