import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import FinancialData

class Command(BaseCommand):
    help = 'Load data from data.json into the FinancialData model'

    def handle(self, *args, **kwargs):
        # Path to the data.json file
        data_file_path = os.path.join(settings.BASE_DIR, 'data', 'data.json')

        # Load the JSON data
        with open(data_file_path, 'r') as file:
            data_list = json.load(file)

        # Iterate over the data and create FinancialData objects
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

        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
