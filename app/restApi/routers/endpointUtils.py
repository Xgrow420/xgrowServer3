from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import FileResponse

router = APIRouter(
    prefix="/api/utils",
    tags=["Utils"]
)

@router.get('/endpoints')
def list_endpoints(request: Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list

@router.get("/getconfig", status_code=status.HTTP_200_OK)
def getXgrowConfig():
    configContent = """#  =======================================================================================
#   _    _     ______    ______      _____     _  _  _                      ___ _
#  \ \  / /   / _____)  (_____ \    / ___ \   | || || |                    / __|_)
#   \ \/ /   | /  ___    _____) )  | |   | |  | || || |    ____ ___  ____ | |__ _  ____
#    )  (    | | (__ )  | ____ (   | |   | |  | ||_|| |   / ___) _ \|  _ \|  __) |/ _  |
#   / /\ \   | \___| |  | |   | |  | |___| |  | |___| |  ( (__| |_| | | | | |  | ( ( | |
#  /_/  \_\   \_____/   |_|   |_|   \_____/    \______|   \____)___/|_| |_|_|  |_|\_|| |
#                                                                                (_____|
#  =======================================================================================

# Ten plik konfiguracyjny pomoże wprowadzić dane niezbędne do działania aplikacji Xgrow bez konieczności
# podłączania monitora, myszy i klawiatury. Należy jednak pamiętać, że jego poprawność nie jest gwarantowana
# w przypadku popełnienia błędu lub braku połączenia z internetem, które również trzeba skonfigurować.

# This configuration file will help you input the necessary data for the Xgrow application to function without
# the need for connecting a monitor, mouse, and keyboard. However, please note that it does not guarantee
# the proper functioning of the application in case of errors in this file or the lack of an internet connection,
# which you need to configure beforehand.


# ==== Login Settings:
# Set your Username and Password below:
User: {username}
Password: {userPassword}

# ==== Autologin Function:
# PL: Funkcja Autologin pozwala na automatyczne zalogowanie urządzenia Xgrow przy użyciu wcześniej ustawionego
# loginu i hasła podczas uruchamiania aplikacji XgrowMainApp.exe.
# EN: The autologin function allows the Xgrow device to automatically log in using the previously set
# username and password when launching the XgrowMainApp.exe application
AutoLogin: true

# ==== WIFI Configuration:
# PL: Ustaw nazwe sieci i haslo do Wifi z którym Xgrow ma się połączyć.
# EN: Set the network name and password for the WiFi that Xgrow should connect to.
WifiSSID: {wifiSSID}
WifiPWD: {wifiPassword}
CountryID: {countryID}


# ==== Server Path to connect:
serverPath: xgrow.pl/api/

# ==== Set the Camera resolution in Xgrow system
CameraResolution:
  width: 1920
  height: 1080

Display: false

# ==== PERMISSIONS:

potPermissions:

  #PL: potName odpowiada za uprawnienia do edycji pola Nazwa Doniczki. Nazwa Doniczki umożliwia łatwiejsze jej rozpoznanie.
  #EN: potName is responsible for permissions to edit the Pot Name field. Pot Name makes it easier to identify the pot.
  potName: true

  #PL: active odpowiada za uprawnienia do edycji pola Status. Status określa czy doniczka jest aktywowana czy dezaktywowana.
  #EN: active is responsible for permissions to edit the Pot Status field. Pot Status indicates whether this pot is enabled or disabled.
  active: true

  #PL: manualWateringTimeLimit odpowiada za uprawnienia do ustawienia limitu czasu podlewania ręcznego. Limit czasu chroni przed zalaniem doniczki.
  #EN: manualWateringTimeLimit is responsible for permissions to set the limit of manual watering time. The time limit secures the watering system before flooding the growbox.
  manualWateringTimeLimit: true

  #PL: autoWateringFunction odpowiada za uprawnienia do włączenia i wyłączenia automatu do podlewania. Automatyczne podlewanie umożliwia podlewanie doniczki zgodnie z ustawieniami.
  #EN: autoWateringFunction is responsible for permissions to enable or disable the automatic watering function. Automatic watering enables watering the pot according to the set parameters.
  autoWateringFunction: true

  #PL: minMoisture odpowiada za uprawnienia do ustawienia minimalnej wilgotności podłoża doniczki. Doniczka zostanie podlana jeśli wilgotność podłoża będzie niższa od tej wartości.
  #EN: minMoisture is responsible for permissions to set the minimum soil moisture for the pot. The pot will be watered if the soil moisture is lower than this value.
  minMoisture: true

  #PL: moistureSensorCalibration odpowiada za uprawnienia do kalibracji czujnika wilgotności podłoża. Kalibracja umożliwia dokładne pomiar wilgotności podłoża.
  #EN: moistureSensorCalibration is responsible for permissions to calibrate the soil moisture sensor. Calibration enables precise measurement of soil moisture.
  moistureSensorCalibration: true

  #PL: automaticWateringTime odpowiada za uprawnienia do ustawienia częstotliwości automatycznego podlewania. Określa jak często ma występować cykl podlewania (w godzinach).
  #EN: automaticWateringTime is responsible for permissions to set the frequency of automatic watering. It indicates how often the watering cycle should occur (in hours).
  automaticWateringTime: true

  #PL: automaticWateringCycleDuration odpowiada za uprawnienia do ustawienia czasu trwania automatycznego podlewania (w sekundach).
  #EN: automaticWateringCycleDuration is responsible for permissions to set the duration of automatic watering (in seconds).
  automaticWateringCycleDuration: true

  #PL: all odpowiada za uprawnienia do wszystkich opcji związanych z konfiguracją doniczki.
  #EN: all is responsible for permissions related to all pot configuration options.
  all: true

  #PL: manualWateringFunction odpowiada za uprawnienia do opcji ręcznego podlewania doniczki.
  #EN: manualWateringFunction is responsible for permissions related to the manual pot watering option.
  manualWateringFunction: true

devicePermissions:

  #PL: Pole ikona odpowiada za uprawnienia do wyboru ikony dla urządzenia. Ikona zostanie wyświetlona na pulpicie.
  #EN: The "Icon" field is responsible for permissions to select an icon for the device. The selected icon will be displayed on the dashboard.
  icon: true

  #PL: Pole Nazwa urządzenia odpowiada za uprawnienia do nadania urządzeniu nazwy, co ułatwi jego identyfikację.
  #EN: The "Device Name" field is responsible for permissions to add a name to the device to make it easier to identify.
  deviceName: true

  #PL: Pole Status urządzenia odpowiada za uprawnienia do aktywacji lub deaktywacji urządzenia.
  #EN: The "Device Status" field is responsible for permissions to enable or disable the device.
  active: true

  #PL: Pole Typ czasomierza odpowiada za uprawnienia do wyboru trybu czasomierza dla urządzenia.
  #EN: The "Timer Type" field is responsible for permissions to select a timer mode for the device.
  deviceFunction: true

  #PL: Pole Odwróć cykl odpowiada za uprawnienia do uruchomienia urządzenia w cyklu odwrotnym, tzn. po włączeniu warunków wyłączy się, a po wyłączeniu włączy się.
  #EN: The "Reverse Trigger" field is responsible for permissions to activate the device in reverse cycle, meaning that turning on the conditions will result in turning off and vice versa.
  reversal: true

  #PL: Pole Trigger urządzenia odpowiada za uprawnienia do ustawienia warunków uruchamiania urządzenia.
  #EN: The "Device Trigger" field is responsible for permissions to set the conditions for triggering the device.
  triggers: true

  #PL: Pole all odpowiada za uprawnienia do wszystkich opcji konfiguracji urządzenia.
  #EN: The "all" field is responsible for permissions to access all device configuration options.
  all: true
"""
    return configContent