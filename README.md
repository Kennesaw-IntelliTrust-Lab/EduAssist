# EduAssist Project

## Project Overview

EduAssist is a cloud-based app for teachers and professors that combines file organization with an AI assistant. It helps educators keep all their teaching materials in one place while providing AI support for common teaching tasks.
The app lets you create separate spaces for each course you teach, where you can store and organize assignments, rubrics, notes, and syllabi. This makes it easy to find what you need when you need it, without digging through scattered files or folders.
What makes EduAssist special is its AI assistant that helps with everyday teaching tasks like creating syllabi, generating questions for tests, creating rubric, etc.

EduAssist runs on Google Cloud and uses Groq's AI technology, making it fast and reliable. The app is designed to be straightforward to use, so you don't need to be tech-savvy to benefit from its AI features.


## Table of Contents

- [Prerequisites](#prerequisites)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
  - [Google Cloud Setup](#google-cloud-setup)
  - [Cloud Workstation Setup](#cloud-workstation-setup)
  - [Groq API Setup](#groq-api-setup)
  - [Environment Configuration](#environment-configuration)
  - [Local Development](#local-development)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Prerequisites

Before you begin, ensure you have the following:

- A Google Cloud Platform account: [Sign up here](https://cloud.google.com/free)
- A Groq Cloud account for AI API access: [Sign up here](https://console.groq.com/signup)
- Git for version control
- Basic familiarity with Django and PostgreSQL

## Architecture

EduAssist architecture consists of:

- **Backend**: Django application
- **Database**: PostgreSQL on Google Cloud
- **Storage**: Google Cloud Storage buckets
- **AI Services**: Groq Cloud API
- **Development Environment**: Google Cloud Workstation

## Setup Instructions

### Google Cloud Setup

1. **Create a new Google Cloud Project**:
   ```bash
   gcloud projects create [YOUR-PROJECT-ID] --name="EduAssist"
   gcloud config set project [YOUR-PROJECT-ID]
   ```

2. **Enable required APIs**:
   ```bash
   gcloud services enable storage.googleapis.com \
                          sqladmin.googleapis.com \
                          sql-component.googleapis.com \
                          workstations.googleapis.com
   ```

3. **Set up PostgreSQL on Google Cloud SQL**:
   ```bash
   gcloud sql instances create eduassist-postgres \
       --database-version=POSTGRES_13 \
       --cpu=1 \
       --memory=3840MB \
       --region=us-central1
   ```

4. **Create a database and user**:
   ```bash
   gcloud sql databases create eduassistdb --instance=eduassist-postgres
   gcloud sql users create eduassistadmin \
       --instance=eduassist-postgres \
       --password=[SECURE-PASSWORD]
   ```

5. **Create a Google Cloud Storage bucket**:
   ```bash
   gcloud storage buckets create gs://[YOUR-PROJECT-ID]-eduassist-files --location=us-central1
   ```

6. **Create a service account for application use**:
   ```bash
   gcloud iam service-accounts create eduassist-app
   gcloud projects add-iam-policy-binding [YOUR-PROJECT-ID] \
       --member="serviceAccount:eduassist-app@[YOUR-PROJECT-ID].iam.gserviceaccount.com" \
       --role="roles/cloudsql.client"
   gcloud projects add-iam-policy-binding [YOUR-PROJECT-ID] \
       --member="serviceAccount:eduassist-app@[YOUR-PROJECT-ID].iam.gserviceaccount.com" \
       --role="roles/storage.objectAdmin"
   ```

### Groq API Setup

1. Sign up for a Groq Cloud account at [console.groq.com](https://console.groq.com)
2. Navigate to API Keys section and create a new API key
3. Save the API key securely for later use in your environment configuration

### Environment Configuration

Within your Cloud Workstation (or local environment):

1. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```

2. Edit the `.env` file with your specific configuration:
   ```
   # Google Cloud Configuration
   GOOGLE_CLOUD_PROJECT=[YOUR-PROJECT-ID]
   GOOGLE_CLOUD_STORAGE_BUCKET=[YOUR-PROJECT-ID]-eduassist-files
   
   # Database Configuration
   DB_NAME=eduassistdb
   DB_USER=eduassistadmin
   DB_PASSWORD=[YOUR-DB-PASSWORD]
   DB_HOST=/cloudsql/[YOUR-PROJECT-ID]:us-central1:eduassist-postgres
   
   # Groq API Configuration
   GROQ_API_KEY=your-groq-api-key-here
   GROQ_MODEL=llama2-70b-4096
   
   # Django Configuration
   DJANGO_SECRET_KEY=[GENERATE-A-SECURE-KEY]
   DJANGO_DEBUG=True
   ```

3. Update the Django settings to use these environment variables:

   Look for `settings.py` in your project and ensure it has the proper configuration to read from environment variables.

  

### Cloud Workstation Setup

Cloud Workstation is the recommended development environment for this project:

1. **Enable the Cloud Workstations API**:
   ```bash
   gcloud services enable workstations.googleapis.com
   ```

2. **Create a workstation configuration**:
   ```bash
   gcloud workstations configs create eduassist-config \
       --machine-type=e2-standard-4 \
       --region=us-central1 \
       --service-account=eduassist-app@[YOUR-PROJECT-ID].iam.gserviceaccount.com
   ```

3. **Create a new workstation**:
   ```bash
   gcloud workstations create eduassist-dev \
       --config=eduassist-config \
       --region=us-central1
   ```

4. **Start and access your workstation**:
   Navigate to [Google Cloud Console → Cloud Workstations](https://console.cloud.google.com/workstations) and click on your workstation to launch it. When the workstation is ready, click "Start" and then "Open".

5. **Setup within the workstation**:
   Once connected to your workstation, open a terminal and:
   ```bash
   # Clone the repository
   git clone https://github.com/[username]/eduassist.git
   cd eduassist
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Authenticate with Google Cloud
   gcloud auth application-default login
   ```

### Local Development (Alternative)

If you prefer to develop locally without Cloud Workstation:

1. Install the [Cloud SQL Proxy](https://cloud.google.com/sql/docs/postgres/connect-admin-proxy)
2. Start the proxy to connect to your database:
   ```bash
   ./cloud-sql-proxy [YOUR-PROJECT-ID]:us-central1:eduassist-postgres
   ```
3. Configure your local environment variables to connect to the proxied database
4. Activate your Python virtual environment and install dependencies
5. Run the development server

## Running the Application

1. **Authenticate with Google Cloud** (if not already done):
   ```bash
   gcloud auth application-default login
   ```

2. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser** (first time only):
   ```bash
   python manage.py createsuperuser
   ```

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   - In Cloud Workstation: Access the forwarded port through the workstation interface
   - Local setup: Visit `http://localhost:8000`

6. **Verify service connections**:
   ```bash
   python scripts/verify_services.py
   ```

   Use this script to verify all your cloud services are properly authenticated:

```# From project root directory
python scripts/verify_services.py
```
The key part of the script that makes this work is:

```python
# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
```
Make sure to adjust `core.settings` if your Django settings module has a different name. - `project-name.settings`



## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Ensure you're logged in with `gcloud auth application-default login`
   - Verify your service account has necessary permissions
   - Check IAM roles and permissions in Google Cloud Console

2. **Database Connection Issues**:
   - Check if the PostgreSQL instance is running
   - Verify connection string and credentials
   - For Cloud SQL: Ensure the proxy is working or the connection is properly set up
   - Common error: `could not connect to server: No such file or directory`
     - Solution: Make sure DB_HOST path is correct for Cloud SQL connections

3. **Cloud Workstation Issues**:
   - If the workstation doesn't start: Check resource quota limits
   - If you can't connect: Check firewall rules
   - Port forwarding issues: Use the Cloud Workstation interface port forwarding feature

4. **Django Migration Errors**:
   - If you get migration errors: `python manage.py migrate --fake-initial`
   - Conflicting migrations: `python manage.py showmigrations` to see the state

5. **Storage Access Problems**:
   - Verify bucket permissions
   - Ensure service account has `storage.objects.*` permissions

6. **Groq API Issues**:
   - Validate your API key is active
   - Check for rate limiting or quota issues
   - Verify the model name is correct

For more detailed troubleshooting, see the [Google Cloud SQL documentation](https://cloud.google.com/sql/docs/postgres/connect-instance-cloud-workstations) and [Django documentation](https://docs.djangoproject.com/)

## Contributing

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Commit your changes
4. Push to your branch
5. Create a Pull Request