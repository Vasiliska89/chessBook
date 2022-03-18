import pyowm
from pyowm.utils.config import get_default_config
import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

kivy.require('1.0.7')
from kivy.app import App
from kivy.uix.button import Button
class TestApp(App):
    text_input = None
    comment = None
    def changeComment(self, value):
        message_text = self.text_input.text
        weather_info1 = 'в городе ' + message_text + ' '

    def build(self):
        message_text = 'Москва'
        weather_info1 = 'в городе '+message_text+' '
        self.text_input = TextInput(text = 'Chasik v radost', multiline = False)
        self.text_input.bind(on_text_validate = self.on_enter)
        layout = BoxLayout(orientation = 'vertical')
        self.comment = Button(text=weather_info1)
        self.comment.bind(on_press=self.on_enter)
        layout.add_widget(self.text_input)
        layout.add_widget(self.comment)
        return layout
if __name__=='__main__':
    TestApp().run()