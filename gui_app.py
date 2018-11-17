from kivy.app import App 
from kivy.clock import Clock 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen 
from kivy.uix.button import Button 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
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
        self.math_popup = MathPopup()

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
            

class MathPopup(Popup):
    """Pops for answers"""

    GOOD = ("{} :D")
    BAD = ("{}, Correct answer is [b]{}[/b]")
    GOOD_LIST = ("Awesome! Amazing! Excellent! Correct!".split())
    BAD_LIST = ["Almost!", "Close!", "Sorry", "Don't Worry"]

    message = ObjectProperty()
    wrapped_button = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(MathPopup, self).__init__(*args, **kwargs)

    def open(self, correct=True):
        # if anwser is correct take of btn if it visible
        if correct:
            if self.wrapped_button in self.content.children:
                self.content.remove_widget(self.wrapped_button)
        # if answer is wrong display btn if not visible
        else:       
            if self.wrapped_button not in self.content.children:
                self.content.add_widget(self.wrapped_button)

        # Set up text message
        self.message.text = self._prep_text(correct)

        # Display popup
        super(MathPopup, self).open()
        if correct:
            Clock.schedule_once(self.dismiss, 1)

    def _prep_text(self, correct):
        if correct:
            index = random.randint(0, len(self.GOOD_LIST) - 1)
            return self.GOOD.format(self.GOOD_LIST[index])
        else:
            index = random.randint(0, len(self.BAD_LIST) - 1)
            math_screen = App.get_running_app().root.math_screen
            answer = math_screen.get_answer()
            return self.BAD.format(self.BAD_LIST[index], answer)


class KeyPad(GridLayout):
    """"""
    def __init__(self, *args, **kwargs):
        super(KeyPad, self).__init__(*args, **kwargs)
        self.cols = 3
        self.spacing = 10
        self.createButtons()

    # Creating the numm  pads
    def createButtons(self):
        # list the text of btns
        _list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "", "GO!"]
        for num in _list:
            # adding a btn with txt and event to GridLayout
            self.add_widget(Button(text=str(num), on_release=self.onBtnPress))

    # On press This method launches
    def onBtnPress(self, btn):
        math_screen = App.get_running_app().root.ids.math_screen
        answer_text = math_screen.answer_text

        if btn.text.isdigit(): # check if its a digit
            answer_text.text += btn.text
        if btn.text == "GO!" and answer_text.text != "": # Checking the answer
            answer = math_screen.get_answer()
            root = App.get_running_app().root 
            if int(answer_text.text) == answer:
                root.math_popup.open(True)
            else:
                root.math_popup.open(False)

            #Clearing the answer
            answer_text.text = ""
            question = math_screen.question_text
            # Prepare to get a new question
            question.text = root.prepQuestion(
                    math_screen.get_next_question(True if root.is_mix else False)
                ) 


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