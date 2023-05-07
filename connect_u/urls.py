"""connect_u URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from student_portal.views import home, RegisterView, apply_for_job, view_job_applications

from django.contrib.auth import views as auth_views
from student_portal.views import CustomLoginView, profile, job_postings
from student_portal.forms import LoginForm

from django.conf import settings
from django.conf.urls.static import static

from employer_portal.views import employer_home, EmployerRegisterView, EmployerCustomLoginView, manage_job_postings, \
    create_job_posting, update_job_posting, delete_job_posting, view_candidates, select_candidate, employer_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('student_portal.urls')),
    path('register/', RegisterView.as_view(), name='student_portal-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='student_portal/login.html',
                                           authentication_form=LoginForm), name='student_portal-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='student_portal/logout.html'),
         name='student_portal-logout'),
    path('profile/', profile, name='student_portal-profile'),
    path('job-postings/', job_postings, name='student_portal-job_postings'),
    path('apply-for-job/<int:job_id>/', apply_for_job, name='apply_for_job'),
    path('view-job-applications', view_job_applications, name='student_portal-view_job_applications'),

    path('employer-home/', employer_home, name='employer_portal-home'),
    path('employer-register/', EmployerRegisterView.as_view(), name='employer_portal-register'),
    path('employer-login/', EmployerCustomLoginView.as_view(redirect_authenticated_user=True, template_name='employer_portal/login.html',
                                           authentication_form=LoginForm), name='employer_portal-login'),
    path('employer-logout/', auth_views.LogoutView.as_view(template_name='employer_portal/logout.html'),
         name='employer_portal-logout'),
    path('manage-job-postings/', manage_job_postings, name='employer_portal-manage_job_postings'),
    path('create-job-posting/', create_job_posting, name='create_job_posting'),
    path('update-job-posting/', update_job_posting, name='update_job_posting'),
    path('delete-job-posting/<int:job_id>/', delete_job_posting, name='delete_job_posting'),
    path('job/<int:job_id>/candidates/', view_candidates, name='view_candidates'),
    path('select-candidate/<int:job_application_id>/', select_candidate, name='select_candidate'),
    path('employer-profile/', employer_profile, name='employer_portal-employer_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
