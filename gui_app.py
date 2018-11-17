
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen 
from kivy.core.window import Window
from kivy.properties import ObjectProperty

from arithmetic import Arithmetic

import webbrowser 


class KivyTutorRoot(BoxLayout):
    """The Root of all widgets"""

    # Creating an obj math_screen that is in .kv file
    math_screen = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(KivyTutorRoot, self).__init__(**kwargs)
        # List of previous screens
        self.screen_list = []

    def changeScreen(self, next_screen):
        operation = ("addition susbtraction multiplication division").split()
        question = None

        # if the current screen not in memory then just add it 4 later use
        if self.ids.kivy_screen_manager.current not in self.screen_list:
            self.screen_list.append(self.ids.kivy_screen_manager.current)

        if next_screen == "about this app":
            # This code is telling manager to the make the screen about screen
            self.ids.kivy_screen_manager.current = "about_screen"
        else:
            # make the question_text whatever the name of previous-screen
            self.math_screen.question_text.text = next_screen
            self.ids.kivy_screen_manager.current = "math_screen"

    def on_Back_Btn(self):
        # Check if theris any screen to go back 2
        if self.screen_list: # if there is then just do it
            self.ids.kivy_screen_manager.current = self.screen_list.pop()
            # We don't want to close
            return True
        # no more screen to go back to
        return False


class MathScreen(Screen, Arithmetic):
    """Widget that acts as screen and hold the math questions"""
    def __init__(self, *args, **kwargs):
        super(MathScreen, self).__init__(*args, **kwargs)
            



class KivyTutorApp(App):
    """The Main Application"""
    def __init__(self, **kwargs):
        super(KivyTutorApp, self).__init__(**kwargs)
        # Whene there is a keypress run this method onBackBtn
        Window.bind(on_keyboard=self.onBackBtn)

    def onBackBtn(self, window, key, *args):
        if key == 27: # The code 4 Esc btn
            # go to the root aka KivyTutorRoot and then in run on_Back_Btn()
            return self.root.on_Back_Btn()

    def build(self):
                return KivyTutorRoot()
    # Text for about page
    def getText(self):
        return ("Hey There!\nThis App was built using"
                "[b][ref=kivy] Kivy [/ref][/b]"
                "Feel free to loot at the source code "
                "[b][ref=source]here[/ref][/b]"
                "This app is under the [b][ref=mit]MIT License[/ref][/b]\n")
    # refs for getText() 
    def on_ref_press(self, instance, ref):
        _dict = {
        "source" : "https://github.com/mrgreen777/Kivy-GUI",
        "kivy" : "https://kivy.org",
        "mit" : "https://github.com/mrgreen777/Kivy-GUI/blob/master/LICENSE"}
        webbrowser.open(_dict[ref])

if __name__ == '__main__':
            # the run function is inherited from App class
            KivyTutorApp().run()        