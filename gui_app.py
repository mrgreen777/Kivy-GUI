
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 
import webbrowser
# 
class KivyTutorRoot(BoxLayout):
    """The Root of all widgets"""
    def __init__(self, **kwargs):
        super(KivyTutorRoot, self).__init__(**kwargs)

    def changeScreen(self, next_screen):
        operation = ("addition susbtraction multiplication division").split()
        question = None

        if next_screen == "about this app":
            # This code is telling manager to the make the screen about screen
            self.ids.kivy_screen_manager.current = "about_screen"


class KivyTutorApp(App):
    """The Main Application"""
    def __init__(self, **kwargs):
        super(KivyTutorApp, self).__init__(**kwargs)

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