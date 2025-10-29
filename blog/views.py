# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Category,Comment
from django.urls import reverse
from main.models import About, SocialLink,Project,Education,Experience
from .forms import CommentForm
from django.contrib.auth.models import User
from collections import defaultdict
from operator import attrgetter
# Note: You need to import 'itertools' at the top of your file
from itertools import groupby
from django.core.paginator import Paginator
from django.db.models import Q

# ----------------------------------------------------------------------
# 1. HELPER FUNCTION: Extracts common data fetching and processing
# ----------------------------------------------------------------------

def get_common_context(request,username='cajit'):
    """Fetches user-specific data (About, Social Links) and maps social icons."""
    
    # 1. Fetch User and Core Data
    search_query = request.GET.get('q')
    
    # 1. Fetch User and Core Data
    try:
        user_instance = User.objects.get(username=username)
        about_data = About.objects.filter(user=user_instance).first()
        socialLinkz = SocialLink.objects.filter(user=user_instance)
        # Note: The 'icon_name' property should be defined on the SocialLink model.
    except User.DoesNotExist:
        # Handle case where critical user data is missing
        return {
            'about': None,
            'socialLinkz': [],
            'q': search_query if search_query else '', # Pass query even if user fails
        }

    # 2. Return a dictionary of common context items
    return {
        'about': about_data,
        'socialLinkz': socialLinkz,
        'q': search_query if search_query else '', # Pass the query string here
    }
# ----------------------------------------------------------------------
# 2. REFACTORED VIEW FUNCTIONS
# ----------------------------------------------------------------------

def apply_search_filter(posts_queryset, query):
    """Applies search filter across title, summary, and categories."""
    if query:
        # Filter posts where query matches title, summary, OR category name
        posts_queryset = posts_queryset.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct() # Use distinct to prevent duplicate posts from category matches
    return posts_queryset




def handle_pagination(request, posts_list):
    """Handles pagination for a given queryset."""
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj





# --- FIXED blog_list_view ---
def blog_list_view(request):
    query = request.GET.get('q')
    
    # Start with all posts
    posts_list = BlogPost.objects.all().order_by('-date')
    
    # Apply search filter if query exists
    posts_list = apply_search_filter(posts_list, query)
    
    # Handle pagination
    page_obj = handle_pagination(request, posts_list)

    all_categories = Category.objects.all()

    context = get_common_context(request,username='cajit')
    context.update({
        'posts': page_obj, 
        'category_list': all_categories,
        # Pass the search query back to the template if it exists
        'q': query if query else '',
    })
    return render(request, 'blog.html', context) 






# --- FIXED category_filter_view ---
def category_filter_view(request, slug):
    all_categories = Category.objects.all()
    query = request.GET.get('q') # <--- Get search query here

    # 1. Determine the base queryset (posts_list)
    if slug.lower() == 'all':
        posts_list = BlogPost.objects.all().order_by('-date')
        active_slug_to_pass = 'all'
    else:
        active_category = get_object_or_404(Category, slug=slug)
        # Filter by category first
        posts_list = BlogPost.objects.filter(categories=active_category).order_by('-date')
        active_slug_to_pass = active_category.slug

    # 2. Apply search filter (AFTER category filter)
    posts_list = apply_search_filter(posts_list, query) # <--- Apply search filter
    
    # 3. Handle Pagination
    page_obj = handle_pagination(request, posts_list)
    
    # 4. Build Context
    context = get_common_context(request,username='cajit')
    context.update({
        'posts': page_obj, 
        'category_list': all_categories,
        'active_category_slug': active_slug_to_pass,
        'q': query if query else '', # <--- Pass the search query back
    })
    
    return render(request, 'blog.html', context)




def blog_detail_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # 1. Fetch active comments
    comments = post.comments.filter(active=True)
    
    # 2. Handle form submission
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.active = True
            new_comment.save()
            
            # Redirect to the same page (optionally to the comments section)
            return redirect(reverse('blog_detail', kwargs={'slug': slug}) + '#comments')
    else:
        comment_form = CommentForm()

    all_categories = Category.objects.all()

    context = get_common_context(request, username='cajit')
    context.update({
        'posts': post,
        'comments': comments,          # <--- NEW
        'comment_form': comment_form,  # <--- NEW
        'category_list': all_categories,
    })
    return render(request, 'blog_post_detail.html', context)



def archive(request):
    # 1. Fetch all posts and categories
    # Order by date descending is crucial for the archive display
    posts = BlogPost.objects.all().order_by('-date')
    all_categories = Category.objects.all()

    # 2. Group Posts by Year
    # The data must be sorted by the key you want to group by (ascending or descending)
    # Since the queryset is already ordered by date (descending), it's sorted by year too.
    
    posts_by_year = defaultdict(list)
    
    # We use attrgetter to get the year from the date object for grouping
    for post in posts:
        year = post.date.year
        posts_by_year[year].append(post)
    
    # Convert the dictionary to a list of (year, [posts]) tuples, sorted descending by year
    # This prepares the data exactly for the template loop
    archive_list = sorted(posts_by_year.items(), key=lambda item: item[0], reverse=True)


    context = get_common_context(request,username='cajit')
    context.update({
        'archive_list': archive_list, # This is the new grouped data
        'category_list': all_categories,
    })
    
    return render(request, 'archive.html', context)


def about(request):
    # 1. Fetch common context (which relies on the user)
    context = get_common_context(request,username='cajit')
    
    # 2. Re-fetch the user instance explicitly for filtering chronological models
    try:
        user_instance = User.objects.get(username='cajit')
    except User.DoesNotExist:
        user_instance = None
    
    # 3. Fetch chronological data only if the user exists
    if user_instance:
        experience_list = Experience.objects.filter(user=user_instance).order_by('-start_year', '-end_year')
        education_list = Education.objects.filter(user=user_instance).order_by('-start_year', '-end_year')
        
        # --- NEW: Fetch Projects, ordered by date descending ---
        project_list = Project.objects.filter(user=user_instance).order_by('-date')
        # -----------------------------------------------------
    else:
        experience_list = []
        education_list = []
        project_list = [] # <--- Initialize empty list
    
    # 4. Fetch the other necessary data
    post = BlogPost.objects.all()
    all_categories = Category.objects.all()

    # 5. Update context
    context.update({
        'posts': post,
        'category_list': all_categories,
        'experience_list': experience_list,
        'education_list': education_list,
        'project_list': project_list, # <--- Add project_list to context
    })
    return render(request, 'about.html', context)