import json
import os
import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from .models import FinancialData

def home(request):
    # URL of the API endpoint
    api_url = 'http://127.0.0.1:8000/api/load-data/'

    # Fetch data from the API
    try:
        response = requests.get(api_url)
        print(api_url)
        data_list = response.json()

        # Clear existing data to avoid duplication (if necessary)
        FinancialData.objects.all().delete()

        # Map the fetched data to the model and save to the database
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

    # Fetch the data from the database to bind to the UI
    financial_data = FinancialData.objects.all()
    return render(request, 'myapp/index.html', {'financial_data': financial_data})


def load_data(request):
    # Construct the full path to the data.json file
    data_file_path = os.path.join(settings.BASE_DIR, 'data', 'data.json')

    # Load the JSON data from the file
    try:
        with open(data_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return JsonResponse({'error': 'Data file not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error decoding JSON'}, status=400)

    # Return the loaded data as a JSON response
    return JsonResponse(data, safe=False)


