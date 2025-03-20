import pandas as pd
from collections import OrderedDict
import os,json
from encodings.utf_8 import encode


path = "/home/revil/Documents/Shiks/Docs/Data/"
county_dict = OrderedDict()
crime_data = {
    "Counties": [
        "Nairobi", "Kiambu", "Meru", "Nakuru", "Machakos", "Murang'a", "Bungoma", "Kisii", "Mombasa", "Kitui",
        "Trans Nzoia", "Nyeri", "Kisumu", "Kilifi", "Uasin Gishu", "Makueni", "Kajiado", "Kakamega", "Migori", "Embu",
        "Kirinyaga", "Homa Bay", "Kericho", "Nyandarua", "Bomet", "Busia", "Narok", "Vihiga", "Nyamira", "Siaya",
        "Nandi", "Tharaka Nithi", "Laikipia", "Taita-Taveta", "Kwale", "Turkana", "Baringo", "Isiolo", "Elgeyo Marakwet",
        "Garissa", "West Pokot", "Marsabit", "Tana River", "Samburu", "Lamu", "Wajir", "Mandera"
    ],
    "ReportedCrimes2023": [
        11108, 9532, 6037, 5072, 4780, 3660, 3419, 3133, 2671, 2598,
        2412, 2400, 2380, 2342, 2325, 2316, 2240, 2223, 1938, 1935,
        1884, 1870, 1856, 1720, 1719, 1653, 1483, 1444, 1431, 1375,
        1337, 1291, 1140, 1125, 1094, 1014, 1004, 829, 781,
        666, 660, 637, 511, 438, 433, 382, 329
    ],
    "ReportedCrimes2022": [
        8512, 7844, 5698, 4514, 3813, 2696, 2668, 2641, 2321, 2314,
        2412, 2400, 2380, 2342, 2325, 2316, 2240, 2223, 1938, 1935,
        1884, 1870, 1856, 1720, 1719, 1653, 1483, 1444, 1431, 1375,
        1337, 1291, 1140, 1125, 1094, 1014, 1004, 829, 781,
        666, 660, 637, 511, 438, 433, 382, 329
    ],
    "ReportedCrimes2021": [
        6686, 5715, 5032, 4281, 2691, 2451, 2385, 2147, 2118, 1940,
        1800, 1780, 1742, 1725, 1716, 1640, 1623, 1338, 1335, 1284,
        1270, 1256, 1120, 1119, 1050, 987, 932, 876, 823, 801,
        776, 723, 687, 663, 641, 597, 542, 496, 472,
        460, 421, 397, 362, 344, 310, 287, 250
    ],
    "ReportedCrimes2020": [
        5844, 4353, 4110, 3872, 3560, 2493, 2451, 2385, 2147, 2118,
        1940, 1800, 1780, 1742, 1725, 1716, 1640, 1623, 1338, 1335,
        1284, 1270, 1256, 1120, 1119, 1050, 987, 932, 876, 823,
        801, 776, 723, 687, 663, 641, 597, 542, 496,
        472, 460, 421, 397, 362, 344, 310, 287
    ],
    "ReportedCrimes2019": [
        6364, 5715, 5032, 4281, 2691, 2451, 2385, 2147, 2118, 1940,
        1800, 1780, 1742, 1725, 1716, 1640, 1623, 1338, 1335, 1284,
        1270, 1256, 1120, 1119, 1050, 987, 932, 876, 823, 801,
        776, 723, 687, 663, 641, 597, 542, 496, 472,
        460, 421, 397, 362, 344, 310, 287, 250
    ],
    "ReportedCrimes2018": [
        7434, 5603, 5151, 4313, 2691, 2382, 2147, 2118, 1940, 1800,
        1780, 1742, 1725, 1716, 1640, 1623, 1338, 1335, 1284, 1270,
        1256, 1120, 1119, 1050, 987, 932, 876, 823, 801, 776,
        723, 687, 663, 641, 597, 542, 496, 472, 460,
        421, 397, 362, 344, 310, 287, 250, 200
    ],

    "Population2023": [
        4750056, 2652880, 1625982, 2347849, 1487758, 1112288, 1786973, 1344907, 1311860, 1229790,
        1069039, 835408, 1248474, 1577335, 1257330, 1042300, 1268261, 2002435, 1234082, 648425,
        653112, 1231659, 954896, 695531, 939761, 968763, 1284204, 625765, 657502, 1059458,
        951460, 416383, 561223, 363990, 944464, 1022773, 733333, 315937, 495239,
        927031, 676326, 515292, 352549, 348298, 167332, 870636, 959236
    ],
    "Population2019": [
        4397073, 2417735, 2162202, 1867579, 1670570, 1545714, 1453787, 1421932, 1266860, 1208333,
        993183, 1157873, 1155474, 1131950, 1116436, 1136187, 1163186, 1056640, 759164, 1117840,
        987653, 608599, 990341, 875689, 901777, 893681, 885711, 605576, 610411, 590013,
        926976, 621241, 841353, 518560, 666763, 810246, 867457, 393177, 454480,
        340671, 866820, 459785, 310327, 315943, 143920, 268002
    ]
}

def rename_d_files(path):
    for file in os.listdir(path):
        name, ext  = os.path.splitext(os.path.join(path, file))
        fname = name.split(' ')[0]
        nfile_name = f"{fname}{ext}"
        try:
            os.rename(os.path.join(path, file), nfile_name)
            print(nfile_name, "OK ")
        except Exception as exc:
            print(exc)

def get_all_county_info(path, county_dict):
    for file in os.listdir(path):
        fname = os.path.splitext(file)[0]
        if fname in crime_data['Counties']:
            data = pd.read_excel(os.path.join(path, file))
            county_data = {"crimes": list(data[data.columns[1]]),
                           "national_percent": list(data[data.columns[2]]),
                           "county_percent": list(data[data.columns[3]])
                           }
            county_dict[f'{fname}'] = county_data
            # if fname == "Nairobi":
            #     print(county_data)
        else:
            muranga = pd.read_excel(os.path.join(path,file))
            muranga_county_data = {"crimes": list(muranga[muranga.columns[1]]),
                           "national_percent": list(muranga[muranga.columns[2]]),
                           "county_percent": list(muranga[muranga.columns[3]])
                           }
            county_dict["Murang'a"]= muranga_county_data
    return county_dict

# crime_data['CountiesData'] = get_all_county_info(path, county_dict)

# with open("CrimeData.json", "w") as json_fp:
#     json.dump(crime_data, json_fp)
#     print("[+] dumpjson()")
