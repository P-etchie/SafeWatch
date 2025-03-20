from Model.base_model import BaseScreenModel


COUNTY_DATA = [
        {"name": "Nairobi", "lat": -1.286389, "lon": 36.817223},
        {"name": "Mombasa", "lat": -4.043477, "lon": 39.668206},
        {"name": "Kisumu", "lat": -0.091702, "lon": 34.767956},
        {"name": "Nakuru", "lat": -0.303099, "lon": 36.080026},
        {"name": "Kiambu", "lat": -1.171526, "lon": 36.835472},
        {"name": "Uasin Gishu", "lat": 0.524136, "lon": 35.269779},
        {"name": "Machakos", "lat": -1.5177, "lon": 37.2634},
        {"name": "Kajiado", "lat": -1.8521, "lon": 36.7767},
        {"name": "Kericho", "lat": -0.1827, "lon": 35.4781},
        {"name": "Nyeri", "lat": -0.4162, "lon": 36.9515},
        {"name": "Kakamega", "lat": 0.2833, "lon": 34.7500},
        {"name": "Bungoma", "lat": 0.5636, "lon": 34.5609},
        {"name": "Homa Bay", "lat": -0.6226, "lon": 34.4504},
        {"name": "Turkana", "lat": 3.3133, "lon": 35.5656},
        {"name": "Narok", "lat": -1.1041, "lon": 35.8770},
        {"name": "Embu", "lat": -0.5383, "lon": 37.4503},
        {"name": "Meru", "lat": 0.3557, "lon": 37.7986},
        {"name": "Kitui", "lat": -1.3664, "lon": 38.0106},
        {"name": "Garissa", "lat": -0.4524, "lon": 39.6460},
        {"name": "Wajir", "lat": 1.7500, "lon": 40.0500},
        {"name": "Mandera", "lat": 3.9383, "lon": 41.8553},
        {"name": "Taita Taveta", "lat": -3.3166, "lon": 38.3666},
        {"name": "Laikipia", "lat": 0.3903, "lon": 36.8609},
        {"name": "Bomet", "lat": -0.7833, "lon": 35.3333},
        {"name": "Busia", "lat": 0.4601, "lon": 34.1115},
        {"name": "Migori", "lat": -1.0635, "lon": 34.4730},
        {"name": "Siaya", "lat": -0.0617, "lon": 34.2422},
        {"name": "Trans Nzoia", "lat": 1.0142, "lon": 34.9504},
        {"name": "Nyandarua", "lat": -0.1833, "lon": 36.6666},
        {"name": "Marsabit", "lat": 2.3333, "lon": 37.9833},
        {"name": "Isiolo", "lat": 0.3546, "lon": 37.5822},
        {"name": "Samburu", "lat": 1.2166, "lon": 36.9166},
        {"name": "West Pokot", "lat": 1.5000, "lon": 35.2833},
        {"name": "Kilifi", "lat": -3.6305, "lon": 39.8499},
        {"name": "Kwale", "lat": -4.1738, "lon": 39.4521},
        {"name": "Tana River", "lat": -1.8155, "lon": 40.1614},
        {"name": "Lamu", "lat": -2.2694, "lon": 40.9006},
        {"name": "Vihiga", "lat": 0.1252, "lon": 34.7519},
        {"name": "Elgeyo Marakwet", "lat": 1.0504, "lon": 35.4781},
        {"name": "Tharaka Nithi", "lat": -0.3016, "lon": 37.5955},
        {"name": "Makueni", "lat": -1.8039, "lon": 37.6200},
        {"name": "Murang'a", "lat": -0.7839, "lon": 37.0400},
        {"name": "Nyamira", "lat": -0.5616, "lon": 34.9345},
        {"name": "Nandi", "lat": 0.1446, "lon": 35.1102},
        {"name": "Baringo", "lat": 0.4651, "lon": 36.0935}
    ]

class MapScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.map_screen.MapScreen.MapScreenView` class.
    """