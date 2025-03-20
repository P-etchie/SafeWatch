import os, json
from collections import OrderedDict, UserDict

new_dict = OrderedDict()

def clean_json(new_dict):
    with open('../CrimeData.json', 'r') as crime_fp:
        data = json.load(crime_fp)
        for county, countyVal  in data['CountiesData'].items():
            crimes = countyVal.get("crimes")
            new_crime_list = []
            for crime in crimes:
                new_crime_text = crime.split("(")[0]
                new_crime_list.append(new_crime_text)
                new_dict[county] = new_crime_list
            countyVal['crimes'] = new_dict
            data['CountiesData'] = countyVal
        with open("safewatch.json", 'w') as new_safe_fp:
            json.dump(data, new_safe_fp)
            print("[+] File Cleaned Successfully")

# clean_json(new_dict)