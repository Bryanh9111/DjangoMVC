# NYBRECON3 Project

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Creating the Django App and API](#creating-the-django-app-and-api)
4. [Loading and Mapping Data to the Model](#loading-and-mapping-data-to-the-model)
5. [Rendering Data in the UI](#rendering-data-in-the-ui)
6. [Running the Project](#running-the-project)
7. [Project Structure](#project-structure)
8. [Troubleshooting](#troubleshooting)
9. [Future Enhancements](#future-enhancements)

---

## Project Overview
NYBRECON3 is a Django-based web application that fetches data from an API, maps it to a Django model, saves it to the database, and then renders it on a front-end UI. The project demonstrates efficient data handling and dynamic rendering using Django's backend capabilities.

---

## Setup Instructions

### 1. Clone or Download the Project
Navigate to your desired directory and clone the repository (if applicable) or download the project.

### 2. Create and Activate a Virtual Environment
1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### 3. Install Dependencies
Make sure you have Django and `requests` installed:
```bash
pip install django requests
```

### 4. Create the Django Project
1. **Start a new Django project**:
   ```bash
   django-admin startproject NYBRECON3 .
   ```
2. **Create a new app** called `myapp`:
   ```bash
   python manage.py startapp myapp
   ```

### 5. Register the App in `settings.py`
- Open `NYBRECON3/settings.py` and add `'myapp'` to the `INSTALLED_APPS` list:
  ```python
  INSTALLED_APPS = [
      ...,
      'myapp',
  ]
  ```

---

## Creating the Django App and API

### 1. Create the `data.json` File
1. **Create a folder** named `data` in the root directory and add `data.json`:
   ```
   NYBRECON3/
       data/
           data.json
   ```
2. **Add sample data** to `data.json`:
   ```json
   [
       {
           "GL_AC_NO": 123456,
           "GL_AC_DESC": "Description 1",
           "Net_DR_CR": 1000.0,
           "Converted_PnL": 1200.0,
           "GL_RP_DT_PRE_TL": 1100.0,
           "GL_RP_DT_CUR_TL": 1150.0,
           "GL_RP_DIFF": 50.0,
           "FOX_CON_TL": 1180.0,
           "DIFF": 20.0,
           "Comments": "Comment 1",
           "UPSTREAM_REPORT_DATE": "2023-05-27T10:30:00Z",
           "VERSION_ID": "v1",
           "LOAD_TIME_STAMP": "2023-05-28T12:00:00Z"
       },
       {
           "GL_AC_NO": 789012,
           "GL_AC_DESC": "Description 2",
           "Net_DR_CR": 2000.0,
           "Converted_PnL": 2200.0,
           "GL_RP_DT_PRE_TL": 2100.0,
           "GL_RP_DT_CUR_TL": 2150.0,
           "GL_RP_DIFF": 50.0,
           "FOX_CON_TL": 2180.0,
           "DIFF": 20.0,
           "Comments": "Comment 2",
           "UPSTREAM_REPORT_DATE": "2023-05-28T11:30:00Z",
           "VERSION_ID": "v2",
           "LOAD_TIME_STAMP": "2023-05-29T13:00:00Z"
       }
   ]
   ```

### 2. Create an API Endpoint
1. **Open `myapp/views.py`** and create a view to serve the JSON data:
   ```python
   import json
   import os
   from django.http import JsonResponse
   from django.conf import settings

   def load_data(request):
       # Path to the data.json file
       data_file_path = os.path.join(settings.BASE_DIR, 'data', 'data.json')

       # Load the JSON data
       try:
           with open(data_file_path, 'r') as file:
               data = json.load(file)
       except FileNotFoundError:
           return JsonResponse({'error': 'Data file not found'}, status=404)
       except json.JSONDecodeError:
           return JsonResponse({'error': 'Error decoding JSON'}, status=400)

       # Return the data as a JSON response
       return JsonResponse(data, safe=False)
   ```

2. **Set up URL routing** for the API in `myapp/urls.py`:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('load-data/', views.load_data, name='load_data'),
   ]
   ```

3. **Include the app URLs** in `NYBRECON3/urls.py`:
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/', include('myapp.urls')),
   ]
   ```

---

## Loading and Mapping Data to the Model

### 1. Create the `FinancialData` Model
1. **Open `myapp/models.py`** and create a model to match the JSON structure:
   ```python
   from django.db import models

   class FinancialData(models.Model):
       GL_AC_NO = models.BigIntegerField()
       GL_AC_DESC = models.CharField(max_length=255)
       Net_DR_CR = models.FloatField()
       Converted_PnL = models.FloatField()
       GL_RP_DT_PRE_TL = models.FloatField()
       GL_RP_DT_CUR_TL = models.FloatField()
       GL_RP_DIFF = models.FloatField()
       FOX_CON_TL = models.FloatField()
       DIFF = models.FloatField()
       Comments = models.TextField()
       UPSTREAM_REPORT_DATE = models.DateTimeField()
       VERSION_ID = models.CharField(max_length=50)
       LOAD_TIME_STAMP = models.DateTimeField()

       def __str__(self):
           return f"{self.GL_AC_DESC} ({self.GL_AC_NO})"
   ```

### 2. Apply Migrations
1. **Generate the migration file**:
   ```bash
   python manage.py makemigrations
   ```
2. **Apply the migration**:
   ```bash
   python manage.py migrate
   ```

### 3. Fetch and Map Data in the Backend
1. **Update `myapp/views.py`** to fetch data from the API and map it to the model:
   ```python
   import json
   import requests
   from django.shortcuts import render
   from .models import FinancialData

   def home(request):
       # URL of the API endpoint
       api_url = 'http://127.0.0.1:8000/api/load-data/'

       # Fetch data from the API
       try:
           response = requests.get(api_url)
           data_list = response.json()

           # Clear existing data to avoid duplication
           FinancialData.objects.all().delete()

           # Map the data to the model and save to the database
           for item in data_list:
               FinancialData.objects.create(
                   GL_AC_NO=item['GL_AC_NO'],
                   GL_AC_DESC=item['GL_AC_DESC'],
                   Net_DR_CR=item['Net_DR_CR'],
                   Converted_PnL=item['Converted_PnL'],
                   GL_RP_DT_PRE_TL=item['GL_RP_DT_PRE_TL'],
                   GL_RP_DT_CUR_TL=item['GL_RP_DT_CUR_TL'],
                   GL_RP_DIFF=item['GL_RP_DIFF'],
                   FOX_CON_TL=item['FOX_CON_TL'],
                   DIFF=item['DIFF'],
                   Comments=item['Comments'],
                   UPSTREAM_REPORT_DATE=item['UPSTREAM_REPORT_DATE'],
                   VERSION_ID=item['VERSION_ID'],
                   LOAD_TIME_STAMP=item['LOAD_TIME_STAMP']
               )
       except Exception as e:
           print(f"Error fetching data: {e}")

       # Fetch data from the database to pass to the template
       financial_data = FinancialData.objects.all()
       return render(request, 'myapp/index.html', {'financial_data': financial_data})
   ```

---

## Rendering Data in the UI

### 1. Create `index.html` in `myapp/templates/myapp/`
1. **Structure your HTML to render the data**:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>Data Viewer</title>
   </head>
   <body>
       <h1>Data Viewer</h1>
       <div id="data-container">
           {% for item in financial_data %}
               <div>
                   <p><strong>GL_AC_NO:</strong> {{ item.GL_AC_NO }}</p>
                   <p><strong>GL_AC

_DESC:</strong> {{ item.GL_AC_DESC }}</p>
                   <p><strong>Net_DR_CR:</strong> {{ item.Net_DR_CR }}</p>
                   <p><strong>Converted_PnL:</strong> {{ item.Converted_PnL }}</p>
                   <p><strong>GL_RP_DT_PRE_TL:</strong> {{ item.GL_RP_DT_PRE_TL }}</p>
                   <p><strong>GL_RP_DT_CUR_TL:</strong> {{ item.GL_RP_DT_CUR_TL }}</p>
                   <p><strong>GL_RP_DIFF:</strong> {{ item.GL_RP_DIFF }}</p>
                   <p><strong>FOX_CON_TL:</strong> {{ item.FOX_CON_TL }}</p>
                   <p><strong>DIFF:</strong> {{ item.DIFF }}</p>
                   <p><strong>Comments:</strong> {{ item.Comments }}</p>
                   <p><strong>UPSTREAM_REPORT_DATE:</strong> {{ item.UPSTREAM_REPORT_DATE }}</p>
                   <p><strong>VERSION_ID:</strong> {{ item.VERSION_ID }}</p>
                   <p><strong>LOAD_TIME_STAMP:</strong> {{ item.LOAD_TIME_STAMP }}</p>
                   <hr>
               </div>
           {% endfor %}
       </div>
   </body>
   </html>
   ```

---

## Running the Project

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```
2. **Visit `http://127.0.0.1:8000`** to view the data rendered on the UI.

---

## Project Structure
```
NYBRECON3/
    manage.py
    NYBRECON3/
        __init__.py
        settings.py
        urls.py
        wsgi.py
        asgi.py
    myapp/
        __init__.py
        models.py
        views.py
        urls.py
        templates/
            myapp/
                index.html
    data/
        data.json
    venv/
```











## Updated Project Structure

NYBRECON3/
│
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── NYBRECON3/                  # Main project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── static/                 # Static files (e.g., CSS, JS)
│   ├── templates/              # Shared templates across the project
│
├── apps/                       # Directory for all your apps
│   ├── __init__.py
│   ├── core/                   # Core app for shared utilities
│   │   ├── __init__.py
│   │   ├── models.py           # Shared models (if any)
│   │   ├── views.py            # Shared views (if any)
│   │   ├── utils.py            # Utility functions
│   │   ├── serializers.py      # Shared serializers (if using DRF)
│   │   ├── urls.py
│   │
│   ├── financial_data/         # App for managing financial data
│   │   ├── __init__.py
│   │   ├── models.py           # Models for financial data
│   │   ├── views/              # Views split into modules
│   │   │   ├── __init__.py
│   │   │   ├── api_views.py    # API views for financial data
│   │   │   ├── ui_views.py     # Views for rendering the UI
│   │   │
│   │   ├── templates/          # Templates specific to this app
│   │   │   └── financial_data/
│   │   │       ├── index.html
│   │   │       ├── other_page.html
│   │   │
│   │   ├── static/             # Static files specific to this app
│   │   │   └── financial_data/
│   │   │       ├── css/
│   │   │       ├── js/
│   │   │       ├── images/
│   │   │
│   │   ├── urls.py             # URL routing for this app
│   │   ├── admin.py
│   │   ├── tests.py
│   │
│   └── another_app/            # You can add more apps similarly
│       ├── __init__.py
│       ├── models.py
│       ├── views/
│       ├── templates/
│       ├── static/
│       ├── urls.py
│       ├── admin.py
│       ├── tests.py
│
└── data/                       # Directory for JSON data files
    └── data.json
