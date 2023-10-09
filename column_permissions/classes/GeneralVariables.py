from column_permissions.settings import MEDIA_URL_CLOUD, MEDIA_URL_LOCAL
from column_permissions.settings import NO_IMAGE_URL
PEDIAHOME_ICON = "Pediahome_icon"

ART_CATEGRY = "ArtCategory"
ART_GENRES = "ArtGenres"
ART = "Art"
ART_IMAGE = "ArtImage"
ART_VIDEO = "ArtVideo"
ART_MATERIAL = "ArtMaterial"
CHARACTER = "Character"

COUNTRY = "Country"
PROVINCE = "Province"
CITY = "City"
LANGUAGE = "Language"

DUBBI_PROFILE_IMG = "DubbiProfileImg"
DUBBI_PROFILE_INFO_ICON = "DubbiProfileInfoIcon"
DUBBI_TALENT_VOICE = "dubbi_talent_voice"
DUBBI_SPECIALIST_VOICE = "dubbi_specialist_voice"


PEDIAHOME_EMPLOYEE = "Employee"

LOCAL = 'local'
CLOUD = 'cloud'


LOCAL_URL = [PEDIAHOME_ICON, ART_CATEGRY, ART_GENRES, COUNTRY,
             LANGUAGE, DUBBI_PROFILE_INFO_ICON, PROVINCE, CITY]
CLOUD_URL = [ART, ART_IMAGE, ART_VIDEO,
             ART_MATERIAL, DUBBI_PROFILE_IMG, CHARACTER, DUBBI_TALENT_VOICE, DUBBI_SPECIALIST_VOICE]

             