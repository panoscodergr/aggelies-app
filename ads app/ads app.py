import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class AdApp(App):
    def build(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

        # Δημιουργία του πίνακα 'users' αν δεν υπάρχει ήδη
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """)

        # Δημιουργία του πίνακα 'messages' αν δεν υπάρχει ήδη
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL
        )
        """)

        # Δημιουργία του πίνακα 'ads' αν δεν υπάρχει ήδη
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            contact_email TEXT NOT NULL
        )
        """)

        # Δημιουργία layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Δημιουργία πεδίων εισόδου
        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True)
        self.email_input = TextInput(hint_text="Email", multiline=False)

        # Δημιουργία κουμπιών
        self.register_button = Button(text="Register")
        self.register_button.bind(on_press=self.register)

        self.send_message_button = Button(text="Send Message")
        self.send_message_button.bind(on_press=self.send_message)

        self.view_messages_button = Button(text="View Messages")
        self.view_messages_button.bind(on_press=self.view_messages)

        self.add_ad_button = Button(text="Add Advertisement")
        self.add_ad_button.bind(on_press=self.add_ad)

        self.view_ads_button = Button(text="View Ads")
        self.view_ads_button.bind(on_press=self.view_ads)

        self.search_ads_button = Button(text="Search Ads")
        self.search_ads_button.bind(on_press=self.search_ads)

        self.delete_ad_button = Button(text="Delete Ad")
        self.delete_ad_button.bind(on_press=self.delete_ad)

        # Προσθήκη widgets στο layout
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.register_button)
        self.layout.add_widget(self.send_message_button)
        self.layout.add_widget(self.view_messages_button)
        self.layout.add_widget(self.add_ad_button)
        self.layout.add_widget(self.view_ads_button)
        self.layout.add_widget(self.search_ads_button)
        self.layout.add_widget(self.delete_ad_button)

        return self.layout

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        email = self.email_input.text

        if not username or not password or not email:
            self.show_popup("Error", "All fields are required!")
            return

        try:
            self.cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            self.conn.commit()
            self.show_popup("Success", "Registration successful!")
            self.clear_inputs()
        except sqlite3.Error as e:
            self.show_popup("Error", f"An error occurred: {str(e)}")

    def send_message(self, instance):
        # Δημιουργία πεδίων εισόδου για αποστολή μηνύματος
        self.message_sender_input = TextInput(hint_text="Sender", multiline=False)
        self.message_receiver_input = TextInput(hint_text="Receiver", multiline=False)
        self.message_subject_input = TextInput(hint_text="Subject", multiline=False)
        self.message_body_input = TextInput(hint_text="Body", multiline=True)

        # Δημιουργία κουμπιού αποστολής μηνύματος
        self.send_button = Button(text="Send Message")
        self.send_button.bind(on_press=self.save_message)

        # Δημιουργία layout για το μήνυμα
        self.message_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.message_layout.add_widget(self.message_sender_input)
        self.message_layout.add_widget(self.message_receiver_input)
        self.message_layout.add_widget(self.message_subject_input)
        self.message_layout.add_widget(self.message_body_input)
        self.message_layout.add_widget(self.send_button)

        self.layout.clear_widgets()
        self.layout.add_widget(self.message_layout)

    def save_message(self, instance):
        sender = self.message_sender_input.text
        receiver = self.message_receiver_input.text
        subject = self.message_subject_input.text
        body = self.message_body_input.text

        if not sender or not receiver or not subject or not body:
            self.show_popup("Error", "All fields are required!")
            return

        try:
            self.cursor.execute("INSERT INTO messages (sender, receiver, subject, body) VALUES (?, ?, ?, ?)",
                                (sender, receiver, subject, body))
            self.conn.commit()
            self.show_popup("Success", "Message sent successfully!")
            self.clear_inputs()
        except sqlite3.Error as e:
            self.show_popup("Error", f"An error occurred: {str(e)}")

    def view_messages(self, instance):
        self.cursor.execute("SELECT * FROM messages")
        messages = self.cursor.fetchall()

        message_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        for message in messages:
            message_layout.add_widget(Label(text=f"From: {message[1]}, To: {message[2]}, Subject: {message[3]}, Body: {message[4]}"))

        scrollview = ScrollView()
        scrollview.add_widget(message_layout)
        self.layout.clear_widgets()
        self.layout.add_widget(scrollview)

    def add_ad(self, instance):
        self.ad_title_input = TextInput(hint_text="Ad Title", multiline=False)
        self.ad_description_input = TextInput(hint_text="Ad Description", multiline=True)
        self.ad_contact_email_input = TextInput(hint_text="Contact Email", multiline=False)

        self.add_ad_button = Button(text="Add Advertisement")
        self.add_ad_button.bind(on_press=self.save_ad)

        self.ad_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.ad_layout.add_widget(self.ad_title_input)
        self.ad_layout.add_widget(self.ad_description_input)
        self.ad_layout.add_widget(self.ad_contact_email_input)
        self.ad_layout.add_widget(self.add_ad_button)

        self.layout.clear_widgets()
        self.layout.add_widget(self.ad_layout)

    def save_ad(self, instance):
        title = self.ad_title_input.text
        description = self.ad_description_input.text
        contact_email = self.ad_contact_email_input.text

        if not title or not description or not contact_email:
            self.show_popup("Error", "All fields are required!")
            return

        try:
            self.cursor.execute("INSERT INTO ads (title, description, contact_email) VALUES (?, ?, ?)",
                                (title, description, contact_email))
            self.conn.commit()
            self.show_popup("Success", "Advertisement added successfully!")
            self.clear_inputs()
        except sqlite3.Error as e:
            self.show_popup("Error", f"An error occurred: {str(e)}")

    def view_ads(self, instance):
        self.cursor.execute("SELECT * FROM ads")
        ads = self.cursor.fetchall()

        ad_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        for ad in ads:
            ad_layout.add_widget(Label(text=f"Title: {ad[1]}, Description: {ad[2]}, Contact: {ad[3]}"))

        scrollview = ScrollView()
        scrollview.add_widget(ad_layout)
        self.layout.clear_widgets()
        self.layout.add_widget(scrollview)

    def search_ads(self, instance):
        search_query = TextInput(hint_text="Search for ads", multiline=False)

        search_button = Button(text="Search")
        search_button.bind(on_press=lambda instance: self.search_in_db(search_query.text))

        self.layout.clear_widgets()
        self.layout.add_widget(search_query)
        self.layout.add_widget(search_button)

    def search_in_db(self, query):
        self.cursor.execute("SELECT * FROM ads WHERE title LIKE ?", ('%' + query + '%',))
        ads = self.cursor.fetchall()

        ad_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        for ad in ads:
            ad_layout.add_widget(Label(text=f"Title: {ad[1]}, Description: {ad[2]}, Contact: {ad[3]}"))

        scrollview = ScrollView()
        scrollview.add_widget(ad_layout)
        self.layout.clear_widgets()
        self.layout.add_widget(scrollview)

    def delete_ad(self, instance):
        delete_query = TextInput(hint_text="Enter Ad Title to Delete", multiline=False)

        delete_button = Button(text="Delete Ad")
        delete_button.bind(on_press=lambda instance: self.delete_ad_from_db(delete_query.text))

        self.layout.clear_widgets()
        self.layout.add_widget(delete_query)
        self.layout.add_widget(delete_button)

    def delete_ad_from_db(self, title):
        try:
            self.cursor.execute("DELETE FROM ads WHERE title = ?", (title,))
            self.conn.commit()
            self.show_popup("Success", "Ad deleted successfully!")
        except sqlite3.Error as e:
            self.show_popup("Error", f"An error occurred: {str(e)}")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text="Close")
        close_button.bind(on_press=self.close_popup)
        content.add_widget(close_button)
        self.popup = Popup(title=title, content=content, size_hint=(0.5, 0.5))
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()

    def clear_inputs(self):
        self.username_input.text = ""
        self.password_input.text = ""
        self.email_input.text = ""

    def on_stop(self):
        self.conn.close()

if __name__ == '__main__':
    AdApp().run()
