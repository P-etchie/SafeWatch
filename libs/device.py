import kivy.logger, platform, requests
from kivy.properties import StringProperty
from plyer.facades.sms import Sms
from plyer.facades.gps import GPS
from plyer.facades.call import Call
from plyer.facades.email import Email
from plyer.facades.vibrator import Vibrator
from plyer.facades.notification import Notification
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from jnius import autoclass


class MobileFeatures:
    _toll_free_hotline = StringProperty("0800 722 203")
    _law_enforcer = 911

    def __init__(self):
        self.device_status = None
        self.device_os = platform.system()

    def SendCrimeReportSms(self, message):
        sms = Sms()
        try:
            sms.send(recipient=self._toll_free_hotline,
                     message=message)
            return 1
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def SendUserNotification(title, message, toast=False):
        notifier = Notification()
        try:
            notifier.notify(title,
                            message,
                            app_name="SafeWatch",
                            app_icon='assets/images/logo4.ico',
                            timeout=10,
                            ticker="New Crime Alert! Stay Informed, Stay Safe 🚨",
                            toast=toast)
            return 1
        except Exception as _:
            return 0

    @staticmethod
    def VibrateDevice(self):
        vibrator = Vibrator()
        try:
            if vibrator.exists():
                vibrator.pattern(pattern=[0,1], repeat=-1)
                vibrator.vibrate(1)
                return 1
            else:
                kivy.logger.Logger.info("Vibrator Not Supported")
        except:
            kivy.logger.Logger.info("vibrator technical error occurred")
            return 0

    def MakeCall(self, instance):
        if instance is not None:
            caller = Call()
            try:
                caller.dialcall()
                caller.makecall(self._law_enforcer)
                return 1
            except:
                return 0

    @staticmethod
    def GetGPS(self, instance):
        gps = GPS()
        gps.configure(on_status=instance.on_status,
                      on_location=instance.on_location)
        if instance.start:
            gps.start(minTime=1000, minDistance=1)
            return 1

    def get_location(self):
        if self.device_os == "Linux" or self.device_os == "Windows":
            return MDSnackbar(MDLabel(text="GPS not available on this platform!",
                                      text_color="red",
                                      theme_text_color="Custom")
                              ).open()

        elif self.device_os == "Android":
            try:
                Context = autoclass('android.content.Context')
                LocationManager = autoclass('android.location.LocationManager')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')

                activity = PythonActivity.mActivity
                service = activity.getSystemService(Context.LOCATION_SERVICE)

                provider = service.getBestProvider(None, False)
                location = service.getLastKnownLocation(provider)

                if location:
                    return {
                        "latitude": location.getLatitude(),
                        "longitude": location.getLongitude(),
                        "accuracy": location.getAccuracy()
                    }
                else:
                    return MDSnackbar(MDLabel(text="Unable To Get Location",
                                      text_color="red",
                                      theme_text_color="Custom")
                              ).open()
            except Exception as e:
                return MDSnackbar(MDLabel(text=f"Technical Error Occurred {e}",
                                      text_color="red",
                                          font_size="11sp",
                                      theme_text_color="Custom")
                              ).open()

        else:
            return MDSnackbar(MDLabel(text="Unsupported Operating System",
                                      text_color="red",
                                      theme_text_color="Custom")
                              ).open()

    def get_geoip_location(self):
        try:
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
            lat, lon = data["loc"].split(",")
            return {"latitude": lat, "longitude": lon, "city": data["city"], "country": data["country"]}
        except Exception as e:
            return {"error": str(e)}

MobileFeatures().SendUserNotification("Oyaaa", "kaa rada")

