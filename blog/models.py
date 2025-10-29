from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse


# --- NEW MODEL: Category ---
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate slug from name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# The existing 'Blog' model seems redundant if BlogPost is your main content, 
# but it's kept here for completeness. You should consider deleting this 
# model if all content is inside BlogPost.
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=255)
    blog = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_name
# ---------------------------


class BlogPost(models.Model):
    # Link post back to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    # --- ADDED: Many-to-Many relationship with Category ---
    categories = models.ManyToManyField(
        Category, 
        related_name='posts', 
        blank=True,
        help_text="Select categories for this post (e.g., Project, Education)."
    )
    # -----------------------------------------------------

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250, blank=True)
    
    summary = models.TextField()
    description = CKEditor5Field('Text', default='Blogs', config_name='extends')
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    read_time = models.IntegerField(default=5) # Estimated read time in minutes

    def save(self, *args, **kwargs):
        # Only auto-generate the slug if it's new or hasn't been set manually
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            
            # Counter for uniqueness
            num = 1
            
            # Check for existing slugs in the database
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            
            self.slug = slug
            
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "BlogPosts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Assumes you have a URL pattern named 'blog_detail'
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    
class Comment(models.Model):
    # Link back to the specific blog post
    post = models.ForeignKey(
        'BlogPost', 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    
    # Store the user (if logged in) or allow anonymous comments
    # We'll use a simple name field for anonymous users for simplicity
    author_name = models.CharField(max_length=80) 
    author_email = models.EmailField(blank=True, null=True) # Optional for Gravatar/identity
    
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False) # For moderation

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.author_name} on {self.post.title}'