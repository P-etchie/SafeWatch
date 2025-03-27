import kivy.logger, hashlib, json 
from firebase_admin.auth import create_user
from kivymd.app import MDApp
import firebase_admin, json
from firebase_admin import firestore
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar
from libs.device import MobileFeatures
# from firebase_admin import storage

class FirebaseConnection:
    def __init__(self):
        self.cred = firebase_admin.credentials.Certificate("safewatch-227f0-ad06271af4b8.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.case_listener = None
        self.mobile_features = MobileFeatures()
        self.load_crime_data()

    def add_new_user(self, user_data):
        try:
            if self.db.collection("Users").document(user_data['username']).get().exists:
                user_ref = self.db.collection("Users").document(user_data['username'])
                user_ref.set(user_data, merge=True)
                user_case_doc = f"{user_data['username']}.case"
                self.db.collection("Cases").add({}, user_case_doc)
                return 1, "add-success"
            else:
                return 0, "user-exists"

        except Exception as e:
            return 0, e

    def get_user_info(self, username):
        if self.db.collection("Users").document(username).get().exists:
            user_ref = self.db.collection("Users").document(username)
            user_info = user_ref.get().to_dict()
            return user_info
        else:
            return "user404"

    def update_user_password(self, username, new_pass):
        try:
            user_ref = self.db.collection("Users").document(username)
            new_hashed_passwd = hashlib.sha512(bytes(new_pass, "utf-8")).hexdigest()
            user_ref.update({"passwd": new_hashed_passwd})
            return 1, "success"
        except Exception as exc:
            return 0, exc

    def get_user_reports(self, username):
        doc_case = f"{username}.case"
        try:
            user_ref = self.db.collection("Cases").document(doc_case)
            user_cases = user_ref.get().to_dict()
            return user_cases
        except Exception as _:
            return None

    def get_all_reports(self):
        try:
            cases_ref = self.db.collection("Cases")
            all_cases = cases_ref.stream()

            reports = {}
            for case in all_cases:
                reports[case.id] = case.to_dict()

            return 1, reports
        except Exception as exc:
            return 0, exc

    def user_total_crime_reports(self, username):
        user_case_doc = f'{username}.case'
        user_doc = self.db.collection("Cases").document(user_case_doc)
        total_crime_reports = len(user_doc.get().to_dict().keys())
        return total_crime_reports

    def delete_user_account(self, username):
        try:
            if self.db.collection("Users").document(username).get().exists:
                user_ref = self.db.collection("Users").document(username)
                user_ref.delete()
            else:
                return 0, "user404"
            return 1, "delete-success"
        except Exception as e:
            return 0, e

    def validate_user_login(self, username, password):
        try:
            if self.db.collection("Users").document(username).get().exists:
                user_ref = self.db.collection("Users").document(username).get()
                user_data = user_ref.to_dict()
                stored_password = str(user_data.get("passwd"))
                if stored_password == hashlib.sha512(bytes(password,"utf-8")).hexdigest():
                    return 1, "success"
                else:
                    return 0, "invalidPasswd"
            else:
                return 0, "user404"
        except Exception as e:
            return 0, f"Error: {e}"

    def register_new_user(self, user_data):
        try:
            if self.db.collection("Users").document(user_data['username']).get().exists:
                return 0, "user-exists"

            self.db.collection("Users").add(user_data, user_data['username'])
            user_case_doc = f"{user_data['username']}.case"
            self.db.collection("Cases").add({}, user_case_doc)
            return 1, "success"

        except Exception as e:
            return 0, f"Error: {e}"

    def delete_user_report(self, report_id):
        try:
            case_ref = self.db.collection("Cases").document("UserCaseReport")
            case_ref.update({report_id: firestore.DELETE_FIELD})
            return 1, "Report deleted successfully"
        except Exception as e:
            return 0, e

    @staticmethod
    def load_crime_data():
        app = MDApp.get_running_app()
        with open('safewatch.json', "r", encoding="utf-8") as crime_json:
            data = json.load(crime_json)
            app.app_data = data
            
    def upload_blob(self, file_path):
        """
        bucket = storage.bucket()
        file_name = os.path.basename(file_path)
        blob = bucket.blob(f"user_uploads/{file_name}")

        try:
            blob.upload_from_filename(file_path)
            blob.make_public()
            file_url = blob.public_url
            MDSnackbar(MDLabel(text=f"Upload successful!", text_color="green")).open()
            print(f"File URL: {file_url}")
        except Exception as e:
            MDSnackbar(MDLabel(text=f"Upload failed: {str(e)}", text_color="red")).open()
        """
    def save_user_report(self, user_crime_report, username):
        doc_case = f"{username}.case"

        try:
            user_ref = self.db.collection("Cases").document(doc_case)
            doc = user_ref.get()

            if not doc.exists:
                user_ref.set({"report1": user_crime_report})
                return 1, user_ref.get().to_dict()

            else:
                existing_reports = doc.to_dict()
                report_count = len(existing_reports)
                new_report_name = f"report{report_count + 1}"

                user_ref.update({new_report_name: user_crime_report})
                # print(f"[+] {new_report_name} written successfully")
                return 1, user_ref.get().to_dict()

        except Exception as e:
            return 313, e

    def listen_for_new_cases(self, username):
        doc_case = f"{username}.case"
        user_cases_ref = self.db.collection("Cases").document(doc_case)

        def on_snapshot(doc_snapshot, changes, read_time):
            for change in changes:
                if change.type.name == "ADDED":
                    new_report = change.document.to_dict()
                    category = new_report.get("Category", "New Crime Report")
                    location = new_report.get("Location", "Unknown Location")

                    self.mobile_features.SendUserNotification(title=category, message=location)

        self.case_listener = user_cases_ref.on_snapshot(on_snapshot)

