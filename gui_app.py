
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen 
from kivy.core.window import Window
from kivy.properties import ObjectProperty

from arithmetic import Arithmetic

import random
import webbrowser 


class KivyTutorRoot(BoxLayout):
    """The Root of all widgets"""

    # Creating an obj math_screen that is in .kv file
    math_screen = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(KivyTutorRoot, self).__init__(**kwargs)
        # List of previous screens
        self.screen_list = []
        self.is_mix = False

    def changeScreen(self, next_screen):
        operations = ("addition subtraction  multiplication division".split())
        question = None

        # if the current screen not in memory then just add it 4 later use
        if self.ids.kivy_screen_manager.current not in self.screen_list:
            self.screen_list.append(self.ids.kivy_screen_manager.current)

        if next_screen == "about this app":
            # This code is telling manager to the make the screen about screen
            self.ids.kivy_screen_manager.current = "about_screen"
        else:
            if next_screen == "mix!": # randomly select an operation
                self.is_mix = True
                index = random.randint(0, len(operations) - 1)#Rnd number
                next_screen = operations[index] #Rnd Screen
            else:
                self.is_mix = False
            for operation in operations: #find a question for operation
                  if next_screen == operation:
                    # Question come from math_screen class which inherite from Arthmetic which the questions are stored
                    question = ("self.math_screen.get_{}_question()".format(operation))
            # make the question_text whatever the name of previous-screen
            self.math_screen.question_text.text = KivyTutorRoot.prepQuestion(
                    eval(question) if question is not None else None
                )
            self.ids.kivy_screen_manager.current = "math_screen"

    @staticmethod
    def prepQuestion(question):
        """Prepars for math question with markup"""
        if question == None:
            return "EROOR"
        text_list = question.split()
        text_list.insert(2, "[b]")
        text_list.insert(len(text_list), "[/b]")
        print("This is  : {}".format( text_list))
        return (" ".join(text_list))

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