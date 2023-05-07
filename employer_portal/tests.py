from django.test import TestCase
from django.contrib.auth.models import User
from job_applications.models import JobApplication
from job_postings.models import JobPosting
from django.contrib.messages import get_messages

# Create your tests here.
TEST_COMPANY = 'Test Company'
TEST_WEBSITE = 'https://www.example.com'
TEST_CONTACT_INFO = 'Test Contact Info'
TEST_JOB = 'Test Job'
TEST_REQUIREMENTS = 'Test Requirements'
TEST_LOCATION = 'Test Location'
TEST_SALARY = 'Test Salary'
TEST_DESCRIPTION = 'Test Description'


class AddJobPostingTestCase(TestCase):
    def test_add_job_posting(self):
        # create a test user and log them in
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # call the view function that adds a job posting
        response = self.client.post('/create-job-posting/', {
            'title': TEST_JOB,
            'company_name': TEST_COMPANY,
            'website': TEST_WEBSITE,
            'job_type': 'Full-time',
            'job_category': 'Technology',
            'location': TEST_LOCATION,
            'salary': TEST_SALARY,
            'description': TEST_DESCRIPTION,
            'requirements': TEST_REQUIREMENTS,
            'application_deadline': '2023-04-01',
            'contact_info': TEST_CONTACT_INFO,
        })

        # assert that the job posting was created successfully
        self.assertEqual(response.status_code, 302)
        self.assertEqual(JobPosting.objects.count(), 1)
        job_posting = JobPosting.objects.first()
        self.assertEqual(job_posting.title, TEST_JOB)
        self.assertEqual(job_posting.employer, user)
        self.assertEqual(job_posting.website, TEST_WEBSITE)


class UpdateJobPostingTestCase(TestCase):
    def setUp(self):
        # create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # create a test job posting
        self.job_posting = JobPosting.objects.create(
            title=TEST_JOB,
            employer=self.user,
            company_name=TEST_COMPANY,
            website=TEST_WEBSITE,
            job_type='Full-time',
            job_category='Technology',
            location=TEST_LOCATION,
            salary=TEST_SALARY,
            description=TEST_DESCRIPTION,
            requirements=TEST_REQUIREMENTS,
            application_deadline='2023-04-01',
            contact_info=TEST_CONTACT_INFO,
        )

    def test_update_job_posting(self):
        # call the view function that updates the job posting
        response = self.client.post('/update-job-posting/', {
            'job_id': self.job_posting.pk,
            'title': 'Updated Test Job',
            'company_name': 'Updated Test Company',
            'website': 'https://www.updated-example.com',
            'job_type': 'Part-time',
            'job_category': 'Business',
            'location': 'Updated Test Location',
            'salary': 'Updated Test Salary',
            'description': 'Updated Test Description',
            'requirements': 'Updated Test Requirements',
            'application_deadline': '2023-04-02',
            'contact_info': 'Updated Test Contact Info',
        })

        # assert that the job posting was updated successfully
        self.assertEqual(response.status_code, 302)
        self.job_posting.refresh_from_db()
        self.assertEqual(self.job_posting.title, 'Updated Test Job')
        self.assertEqual(self.job_posting.company_name, 'Updated Test Company')
        self.assertEqual(self.job_posting.website, 'https://www.updated-example.com')
        self.assertEqual(self.job_posting.job_type, 'Part-time')
        self.assertEqual(self.job_posting.job_category, 'Business')
        self.assertEqual(self.job_posting.location, 'Updated Test Location')
        self.assertEqual(self.job_posting.salary, 'Updated Test Salary')
        self.assertEqual(self.job_posting.description, 'Updated Test Description')
        self.assertEqual(self.job_posting.requirements, 'Updated Test Requirements')
        self.assertEqual(str(self.job_posting.application_deadline), '2023-04-02')
        self.assertEqual(self.job_posting.contact_info, 'Updated Test Contact Info')


class DeleteJobPostingTestCase(TestCase):
    def setUp(self):
        # create a test user and a test job posting
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.job_posting = JobPosting.objects.create(
            title=TEST_JOB,
            employer=self.user,
            company_name=TEST_COMPANY,
            website=TEST_WEBSITE,
            job_type='Full-time',
            job_category='Technology',
            location=TEST_LOCATION,
            salary=TEST_SALARY,
            description=TEST_DESCRIPTION,
            requirements=TEST_REQUIREMENTS,
            application_deadline='2023-04-01',
            contact_info=TEST_CONTACT_INFO,
        )

    def test_delete_job_posting(self):
        # log in as the test user and delete the test job posting
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(f'/delete-job-posting/{self.job_posting.pk}/')

        # assert that the job posting was deleted successfully
        self.assertEqual(response.status_code, 302)
        self.assertEqual(JobPosting.objects.count(), 0)


class SelectCandidateTestCase(TestCase):
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # create a job posting
        self.job_posting = JobPosting.objects.create(
            title=TEST_JOB,
            employer=self.user,
            company_name=TEST_COMPANY,
            website=TEST_WEBSITE,
            job_type='Full-time',
            job_category='Technology',
            location=TEST_LOCATION,
            salary=TEST_SALARY,
            description=TEST_DESCRIPTION,
            requirements=TEST_REQUIREMENTS,
            application_deadline='2023-04-01',
            contact_info=TEST_CONTACT_INFO,
        )

        # create a job application
        self.job_application = JobApplication.objects.create(
            student_username=self.user.profile,
            job_id=self.job_posting,
        )

    def test_select_candidate(self):
        # log in as the employer
        self.client.login(username='testuser', password='testpass')

        # call the view function that selects a candidate
        response = self.client.get(f'/select-candidate/{self.job_application.id}/', {
            'subject': 'Test Subject',
            'body': 'Test Body',
            'email': 'test@example.com',
        })

        # assert that the candidate was selected successfully
        self.assertEqual(response.status_code, 302)
        job_application = JobApplication.objects.get(id=self.job_application.id)
        self.assertEqual(job_application.status, 'Selected')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Notification successfully sent to candidate.')
