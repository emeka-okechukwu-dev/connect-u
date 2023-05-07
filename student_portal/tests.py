from django.test import TestCase
from django.contrib.auth.models import User
from job_applications.models import JobApplication
from job_postings.models import JobPosting


# Create your tests here.
class ApplyForJobTestCase(TestCase):
    def setUp(self):
        # create a test employer and job posting
        self.employer = User.objects.create_user(username='testemployer', password='testpass')
        self.job_posting = JobPosting.objects.create(
            title='Test Job',
            employer=self.employer,
            company_name='Test Company',
            website='https://www.example.com',
            job_type='Full-time',
            job_category='Technology',
            location='Test Location',
            salary='Test Salary',
            description='Test Description',
            requirements='Test Requirements',
            application_deadline='2023-04-01',
            contact_info='Test Contact Info',
        )

        # create a test student and log them in
        self.student = User.objects.create_user(username='teststudent', password='testpass')
        self.client.login(username='teststudent', password='testpass')

    def test_apply_for_job(self):
        # call the view function that applies for the job posting
        response = self.client.post(f'/apply-for-job/{self.job_posting.job_id}/')

        # assert that the application was created successfully
        self.assertEqual(response.status_code, 302)
        self.assertEqual(JobApplication.objects.count(), 1)
        job_application = JobApplication.objects.first()
        self.assertEqual(job_application.student_username.user.username, 'teststudent')
        self.assertEqual(job_application.job_id, self.job_posting)

    def test_apply_for_job_with_get_request(self):
        # call the view function with a GET request
        response = self.client.get(f'/apply-for-job/{self.job_posting.job_id}/')

        # assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # assert that the correct job posting is passed to the template
        self.assertEqual(response.context['job'], self.job_posting)
