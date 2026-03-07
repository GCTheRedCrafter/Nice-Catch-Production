# mobile_ui_login.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.image import Image as KivyImage

import os
from PIL import Image as PILImage

from modules.storage import Storage
from modules.logic import check_password
from modules.models import Dog, UserProfile

# Fenstergröße für Tests am PC (auf Handy ignoriert)
Window.size = (360, 640)

KV = """
ScreenManager:
    LoginScreen:
    RegisterScreen:

<LoginScreen>:
    name: "login"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(10)

        Image:
            source: "img/logo.jpeg"
            size_hint_y: None
            height: dp(120)
            allow_stretch: True
            keep_ratio: True

        Label:
            text: "NiceCatch Login"
            font_size: "22sp"
            bold: True
            size_hint_y: None
            height: dp(40)

        TextInput:
            id: username
            hint_text: "Benutzername"
            multiline: False
            size_hint_y: None
            height: dp(40)

        TextInput:
            id: password
            hint_text: "Passwort"
            password: True
            multiline: False
            size_hint_y: None
            height: dp(40)

        Button:
            text: "Login"
            size_hint_y: None
            height: dp(45)
            on_release:
                root.do_login(username.text, password.text)

        Button:
            text: "Registrieren"
            size_hint_y: None
            height: dp(45)
            on_release:
                app.root.current = "register"

        Widget:
            size_hint_y: 1

<RegisterScreen>:
    name: "register"
    BoxLayout:
        orientation: "vertical"
        padding: dp(15)
        spacing: dp(8)

        ScrollView:
            do_scroll_x: False

            BoxLayout:
                id: form_box
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(8)

                Label:
                    text: "Registrieren"
                    font_size: "22sp"
                    bold: True
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: username
                    hint_text: "Benutzername"
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: password
                    hint_text: "Passwort"
                    password: True
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: age
                    hint_text: "Alter"
                    multiline: False
                    size_hint_y: None
                    height: dp(40)
                    input_filter: "int"

                TextInput:
                    id: city
                    hint_text: "Stadt"
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: bio
                    hint_text: "Beschreibung"
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: interests
                    hint_text: "Interessen (durch Kommata getrennt)"
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: dog_name
                    hint_text: "Name des Hundes"
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: dog_age
                    hint_text: "Alter des Hundes"
                    multiline: False
                    size_hint_y: None
                    height: dp(40)
                    input_filter: "int"

                TextInput:
                    id: dog_sex
                    hint_text: "Geschlecht des Hundes (Rüde/Hündin)"
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: dog_description
                    hint_text: "Beschreibung des Hundes"
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                BoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(10)

                    Button:
                        text: root.image_button_text
                        on_release: root.open_image_chooser()

                Label:
                    id: image_status
                    text: root.image_status_text
                    color: 0, 0.6, 0, 1
                    font_size: "12sp"
                    size_hint_y: None
                    height: dp(20)

        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(10)

            Button:
                text: "Zurück"
                on_release: app.root.current = "login"

            Button:
                text: "Registrieren"
                on_release: root.register_user()
"""


class LoginScreen(Screen):
    def do_login(self, username: str, password: str):
        app = App.get_running_app()
        storage = app.storage

        user_id = check_password(storage, username, password)
        if user_id:
            # Für jetzt: nur Popup – später zu MainScreen wechseln
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label

            Popup(title="Erfolg",
                  content=Label(text=f"Willkommen zurück, {username}!"),
                  size_hint=(0.8, 0.3)).open()

            #self.manager.current = "main"
        else:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label

            Popup(title="Fehler",
                  content=Label(text="Ungültiger Benutzername oder Passwort."),
                  size_hint=(0.8, 0.3)).open()


class RegisterScreen(Screen):
    selected_image_path = None
    image_button_text = "Profilbild auswählen (PNG)"
    image_status_text = ""

    def open_image_chooser(self):
        """Öffnet Dateiauswahl für PNG (am Handy später über native Picker)"""
        chooser = FileChooserIconView(filters=["*.png"])

        def on_selection(instance, selection):
            if selection:
                self.selected_image_path = selection[0]
                filename = os.path.basename(self.selected_image_path)
                self.image_button_text = "Profilbild ändern"
                self.image_status_text = f"✅ {filename} wird verwendet"
                self.ids.image_status.text = self.image_status_text
                popup.dismiss()

        chooser.bind(on_selection=on_selection)

        popup = Popup(title="Profilbild auswählen (PNG)",
                      content=chooser,
                      size_hint=(0.9, 0.9))
        popup.open()

    def register_user(self):
        app = App.get_running_app()
        storage = app.storage

        ids = self.ids

        try:
            dog_obj = Dog(
                id=len(storage.data["users"]) + 1,
                name=ids.dog_name.text.strip(),
                age_years=int(ids.dog_age.text.strip()),
                sex=ids.dog_sex.text.strip(),
                description=ids.dog_description.text.strip()
            )
            user_obj = UserProfile(
                id=len(storage.data["users"]) + 1,
                name=ids.username.text.strip(),
                password=ids.password.text.strip(),
                age=int(ids.age.text.strip()),
                city=ids.city.text.strip(),
                bio=ids.bio.text.strip(),
                interests=[i.strip() for i in ids.interests.text.split(",") if i.strip()],
                dog=dog_obj
            )

            storage.add_user(user_obj)

            user_id = user_obj.id
            if self.selected_image_path:
                self.save_profile_image(storage, self.selected_image_path, user_id)

            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            Popup(title="Erfolg",
                  content=Label(text="Registrierung erfolgreich!"),
                  size_hint=(0.8, 0.3)).open()

            App.get_running_app().root.current = "login"

        except Exception as e:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            Popup(title="Fehler",
                  content=Label(text=f"Registrierung fehlgeschlagen:\\n{e}"),
                  size_hint=(0.8, 0.4)).open()

    def save_profile_image(self, storage: Storage, file_path: str, user_id: int):
        try:
            os.makedirs("img", exist_ok=True)
            new_path = f"img/profile_{user_id}.png"

            img = PILImage.open(file_path)
            img.thumbnail((400, 500), PILImage.Resampling.LANCZOS)
            img.save(new_path, "PNG", quality=95)

            storage.data["users"][-1]["profile_image"] = new_path
            storage.save()
        except Exception as e:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            Popup(title="Bildfehler",
                  content=Label(text=f"PNG konnte nicht gespeichert werden:\\n{e}"),
                  size_hint=(0.8, 0.4)).open()


class NiceCatchMobileApp(App):
    def build(self):
        self.storage = Storage()
        return Builder.load_string(KV)


if __name__ == "__main__":
    NiceCatchMobileApp().run()