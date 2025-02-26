import webview

from test2 import sapi
from globalVaribles import *

class Api:
    def __init__(self):
        self.ssapi = sapi()

    def load(self):
        window.evaluate_js('make();')
    
    def display(self):
        print("Message")

html = """
<script>
function make() {
    pywebview.api.display();
    pywebview.api.ssapi.idk();
}
</script>
"""

class initiateApp:
    def __init__(self):
        global window
        API_Cont=Api()
        window = webview.create_window("Micah's Encryption Suite", html=html, js_api=API_Cont)
        set_global_var('my_global_var', window)
        
        webview.start(API_Cont.load, debug=True)

initiateApp()
