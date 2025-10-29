from django.contrib import admin
from .models import Project, Education, Certificate, About, Contact, Skill, Experience, SocialLink, Award,Category,ChatSession,ChatMessage

admin.site.register(Project)
admin.site.register(Education)
admin.site.register(Certificate)
# admin.site.register(Blog)
admin.site.register(About)
admin.site.register(Contact)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(SocialLink)
admin.site.register(Category)

admin.site.register(Award)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)