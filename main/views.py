# main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import ContactForm
from blog.models import BlogPost,Category as BlogCategory
from .models import About, Education,Award,SocialLink,Experience, Contact,Skill,Category,Project,Certificate,ChatSession, ChatMessage
from django.contrib import messages
from django.urls import reverse 
from django.db.models import Prefetch
from django.core.serializers.json import DjangoJSONEncoder
import json


def portfolio_view(request):
    contact_form = ContactForm()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            try:
                # Find the user and assign it to the contact form
                cajit_user = User.objects.get(username='cajit')
                contact.user = cajit_user
                contact.save()
                messages.success(request, 'Your message has been sent successfully!')
                # Redirect to prevent resubmission on refresh
                return redirect('{}#contact'.format(reverse('portfolio_view')))
            except User.DoesNotExist:
                # Handle the case where the user doesn't exist
                # You might want to log this error
                pass
    
    # Fetch data for the portfolio sections
    try:
        user_instance = User.objects.get(username='cajit')
        about_data = About.objects.filter(user=user_instance)
        education = Education.objects.filter(user=user_instance)
        project = Project.objects.filter(user=user_instance)
        certificate = Certificate.objects.filter(user=user_instance)
        experience = Experience.objects.filter(user=user_instance)
        socialLinkz = SocialLink.objects.filter(user=user_instance)
        award = Award.objects.filter(user=user_instance)
        posts = BlogPost.objects.all().order_by('-date')


        about_info = about_data.first() if about_data.exists() else None
        categories = Category.objects.all().prefetch_related(
            Prefetch(
                'skills',
                # Filter skills only for the target user
                queryset=Skill.objects.filter(user=user_instance), 
                to_attr='user_skills'
            )
        )

        highcharts_series = []
        color_palette = {
    # New Categories Added
    'Programing language': '#64B5F6',      # Muted Sky Blue
    'visualization': '#9CCC65',             # Light Lime Green
    'Data Analysis': '#A1887F',             # Light Brown/Taupe
    
    # Existing Categories
    'Backend': '#FB8C00',                   # Deep Amber/Orange (Primary Accent)
    'FrontEnd': '#FFC107',                  # Bright Amber/Yellow (Secondary Accent)
    'Machine Learning Library': '#4DB6AC',  # Muted Teal/Cyan (Contrasting Cool Color)
    'System/DevOps': '#7986CB',             # Muted Indigo/Purple (Utility)
    'Databases': '#D84315',                 # Dark Terracotta/Red-Brown (Warm Contrast)
    
    # Fallback for any other category:
    'Other': '#78909C'                      # Blue-Gray (Slate Muted)
}
        category = BlogCategory.objects.all()

        for category in categories:
            if not category.user_skills:
                continue
                
            series_data = {
                'name': category.name, 
                'color': color_palette.get(category.name, '#9E9E9E'), # Use predefined color or default gray
                'data': []
            }
            
            for skill in category.user_skills:
                series_data['data'].append({
                    'name': skill.skill_name,
                    # Highcharts uses 'value' for bubble size
                    'value': skill.proficiency 
                })
                
            highcharts_series.append(series_data)
        
        # 3. Convert Python list to safe JSON string
        json_series_data = json.dumps(highcharts_series, cls=DjangoJSONEncoder)
        
    except User.DoesNotExist:
        all_skills = []  
        about_data = []
        education = []
        project = []
        certificate = []
        experience = []
        socialLinkz = []
        award = []
        json_series_data = "[]"
        about_info = None
        
        
    # Create the context dictionary
    context = {
        'about_data': about_data,
        'about_info': about_info,
        'education': education,
        'contact_form': contact_form,
        'project':project,
        'certificate':certificate,
        'experience':experience,
        'socialLinkz':socialLinkz,
        'award':award,
        # 'all_skills':all_skills,
        'highcharts_series_json': json_series_data,
        'posts': posts,
        'category_list':category,    
    }
    
    # Render the template
    return render(request, 'try4.html', context)


def custom_404(request):
    return render(request, '404.html', {}, status=404)

