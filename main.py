import cadquery as cq
import export

from microdot import Microdot

app = Microdot()

P = 8
CAP_DIAMETER = 4.8
CAP_HEIGHT = 1.7

def lego(rows, columns, style="flat"):
    width = rows * P - 0.2
    length = columns * P - 0.2
    height = 3.2 if style == "flat" else 8
    pitch = 8
    
    tmp = cq.Workplane("front") \
        .box(width, length, height) \
        .faces("<Z") \
        .shell(-1) \
        .faces(">Z") \
        .workplane() \
        .rarray(pitch, pitch, rows, columns) \
        .circle(CAP_DIAMETER/2) \
        .extrude(CAP_HEIGHT) \
        
    
    if rows > 1 and columns > 1:
        tmp = tmp.faces("<Z") \
            .workplane(invert=True) \
            .rarray(pitch, pitch, rows - 1, columns - 1, center = True) \
            .circle(CAP_DIAMETER/2) \
            .circle(CAP_DIAMETER/2 - 0.3) \
            .extrude(height/2)
    
    return tmp

@app.route('/')
async def index(request):
  html = """
    <html>
      <head>
        <title>Lego Generator</title>

        <style>
          body {
            margin: 0;
            background: #222;
          }

          /* This keeps child nodes hidden while the element loads */
          :not(:defined) > * {
            display: none;
          }
          model-viewer {
            height: 100vh;
            width: 100vw;
            overflow: hidden;
          }
        </style>
      </head>
      <body>
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js"></script>

        <model-viewer alt="Lego piece" ar shadow-intensity="1" camera-controls auto-rotate tone-mapping="linear" max-camera-orbit="auto auto auto" touch-action="pan-y"></model-viewer>

        <script>
          function load() {
            const modelViewer = document.querySelector('model-viewer')
            const url = new URL(window.location.href)
            const rows = (url.searchParams.get('rows') || 2)
            const columns = (url.searchParams.get('columns') || 4)
            const style = (url.searchParams.get('style') || 'flat')

            modelViewer.src = `/lego.glb?rows=${rows}&columns=${columns}&style=${style}`
          }

          addEventListener("DOMContentLoaded", load)
        </script>
      </body>
    </html>
  """
  return html, {"content-type": "text/html"}

@app.route("/lego.stl")
async def stl(request):
    rows = int(request.args.get("rows", 4))
    columns = int(request.args.get("columns", 2))
    style = request.args.get("style", 'flat')

    object = lego(rows=rows, columns=columns, style=style)

    data = export.stl(object)

    return data, {"content-type": "model/stl"}

@app.route("/lego.glb")
async def glb(request):
    rows = int(request.args.get("rows", 4))
    columns = int(request.args.get("columns", 2))
    style = request.args.get("style", 'flat')

    assy = cq.Assembly()
    object = lego(rows=rows, columns=columns, style=style)
    assy.add(object, color=cq.Color("cornflowerblue"), name="object")

    data = export.glb(assy)

    return data, {"content-type": "model/gltf-binary"}

app.run(debug=True)
