# Initial Setup
1. Install the required libraries from requirements.txt.
2. Install wkhtmltopdf.
3. In `myshop/myshop/settings`, replace `WKHTMLTOPDF_CMD` with your wkhtmltopdf.exe path.

# Running the Application
Navigate to the `myshop` directory and execute:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver {YOUR_IP}:8000
```
and create superuser
```
python manage.py createsuperuser
```

# Working with the Application
The admin panel is accessible at:
```
{YOUR_IP}:8000/admin
```

SwaggerUI documentation is available at:
```
{YOUR_IP}:8000/api/docs/#
```

Endpoint to obtain the QR code:
```
{YOUR_IP}:8000/cach_machine
```

Endpoint to obtain the PDF:
```
{YOUR_IP}:8000/media/{file_name}
```