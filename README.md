# Radio Nova Website

[https://radionova.no/](https://radionova.no/) is a student-run online radio based in Oslo.
The idea of this repo is to revamp the CMS for the main radionova website.

## Deployment

The project is configured to deploy to Azure App Services using GitHub Actions. The deployment process automatically runs database migrations and is set up to use Azure Storage for media files.

### Database Migrations

Migrations are automatically run during deployment. To add new migrations, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Azure Storage Configuration

The project uses Azure Storage for media files in production. To configure this:

1. Create an Azure Storage account in the Azure Portal
2. Create a container (default name: 'media')
3. Add the following secrets to your GitHub repository:
   - AZURE_STORAGE_ACCOUNT_NAME
   - AZURE_STORAGE_ACCOUNT_KEY
   - AZURE_STORAGE_CONTAINER (optional, defaults to 'media')

4. Add the same variables to your Azure App Service configuration

### Local Development

For local development, the project will default to using local file storage. If you want to use Azure Storage locally, uncomment and fill in the Azure Storage variables in the `.env` file.

### Database Configuration

The project uses PostgreSQL. Make sure to configure the following environment variables:
- DBNAME
- DBHOST
- DBUSER
- DBPASS
- DBPORT
- SECRET_KEY
