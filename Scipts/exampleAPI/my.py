import webview

html_template = """
<!DOCTYPE html>
<html data-framework="javascript">
  <head>
  </head>
  <body>
    <div id='t'></div>
    <script>
      function on_bridge() {
        if (typeof pywebview !== 'undefined' && pywebview.api) {
          pywebview.api.run().then(function(res){
            console.log(res);
          });
        }
      }
      
      window.addEventListener('DOMContentLoaded', on_bridge);
    </script>
  </body>
</html>
"""

class API:
    def run(self):
        return 'Hi'

def on_bridge(window):
    window.evaluate_js("on_bridge();")

if __name__ == '__main__':
    api = API()
    window = webview.create_window("Test", html=html_template, js_api=api)
    webview.start(on_bridge, window, debug=True)
