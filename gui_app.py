
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 

# 
class KivyTutorRoot(BoxLayout):
    """The Root of all widgets"""
    def __init__(self, **kwargs):
        super(KivyTutorRoot, self).__init__(**kwargs)


class KivyTutorApp(App):
    """The Main Application"""
    def __init__(self, **kwargs):
        super(KivyTutorApp, self).__init__(**kwargs)

    def build(self):
                return KivyTutorRoot()


if __name__ == '__main__':
            # the run function is inherited from App class
            KivyTutorApp().run()        