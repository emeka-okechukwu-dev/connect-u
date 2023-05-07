from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth.decorators import login_required

from job_postings.models import JobPosting
from django.db.models import Q

from datetime import date

from job_applications.models import JobApplication
from .models import Profile


def home(request):
    return render(request, 'student_portal/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'student_portal/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='student_portal-login')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


@login_required
def profile(request):
    return render(request, 'student_portal/profile.html')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='student_portal-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'student_portal/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def job_postings(request):
    search_query = request.GET.get('search')
    job_type_filter = request.GET.get('job_type')
    today = date.today()

    if search_query:
        available_jobs = JobPosting.objects.filter(Q(title__icontains=search_query))
    elif job_type_filter:
        available_jobs = JobPosting.objects.filter(job_type=job_type_filter)
    else:
        available_jobs = JobPosting.objects.all()

    # Filter out job postings with application deadlines that have already passed
    available_jobs = available_jobs.filter(application_deadline__gte=today)

    # Sort by earliest deadline
    available_jobs = available_jobs.order_by('application_deadline')

    # Retrieve the job applications made by the logged-in student
    student_applications = JobApplication.objects.filter(student_username=request.user.profile)

    applied_job_ids = [app.job_id.job_id for app in student_applications]

    return render(request, 'student_portal/job_postings.html',
                  {'job_postings': available_jobs, 'applied_job_ids': applied_job_ids})


@login_required
def apply_for_job(request, job_id):
    job = JobPosting.objects.get(pk=job_id)
    student_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        JobApplication.objects.create(
            student_username=student_profile,
            job_id=job,
        )
        messages.success(request, 'You have successfully applied for this job.')
        return redirect('student_portal-view_job_applications')

    return render(request, 'student_portal/job_postings.html', {'job': job})


@login_required
def view_job_applications(request):
    search_query = request.GET.get('search')
    job_type_filter = request.GET.get('job_type')

    if search_query:
        searched_jobs = JobPosting.objects.filter(title__icontains=search_query)
        searched_job_ids = [job.job_id for job in searched_jobs]
        job_applications = JobApplication.objects.filter(student_username=request.user.profile,
                                                         job_id__in=searched_job_ids)
    elif job_type_filter:
        filtered_jobs = JobPosting.objects.filter(job_type=job_type_filter)
        filtered_job_ids = [job.job_id for job in filtered_jobs]
        job_applications = JobApplication.objects.filter(student_username=request.user.profile,
                                                         job_id__in=filtered_job_ids)
    else:
        job_applications = JobApplication.objects.filter(student_username=request.user.profile)

    # Create a list of job posting IDs for the current user's job applications
    applied_job_ids = [job_application.job_id_id for job_application in job_applications]

    # Filter the available jobs to only include the job postings that the current user has applied to
    available_jobs = JobPosting.objects.all().filter(job_id__in=applied_job_ids)

    return render(request, 'student_portal/view_job_applications.html',
                  {'job_postings': available_jobs, 'job_applications': job_applications})
