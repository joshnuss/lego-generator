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
            .circle(CAP_DIAMETER/2 - 0.5) \
            .extrude(height/2)
    
    return tmp

@app.route('/')
async def index(request):
  html = """
    <html>
      <head>
        <title>Lego Generator</title>

        <link rel="preconnect" href="https://rsms.me/">
        <link rel="stylesheet" href="https://rsms.me/inter/inter.css">

        <style>
          :root {
            font-family: Inter, sans-serif;
            font-feature-settings: 'liga' 1, 'calt' 1; /* fix for Chrome */
          }
          @supports (font-variation-settings: normal) {
            :root { font-family: InterVariable, sans-serif; }
          }
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

            .loading & {
              opacity: 0.7;
            }
          }

          #loader {
            position: fixed;
            top: 0;
            left: 0;
            background: #ccc;
            border-radius: 9px;
            margin: 2rem;
            color: #333;
            padding: 10px;
            font-size: 20px;
            gap: 10px;
            align-items: center;
            display: none;

            .loading & {
              display: flex;
            }
          }

          .download {
            position: fixed;
            right: 2rem;
            bottom: 2rem;
            color: white;
            display: flex;
            gap: 15px;
            font-size: 28px;
            background: cornflowerblue;
            padding: 15px 20px;
            border-radius: 11px;
            transition-property: background, color;
            transition-duration: 0.2s;
            transition-timing-function: ease-in;
            text-decoration: none;

            &:hover {
              background: #98baf7;
              color: #333;
            }

            .loading & {
              opacity: 0.7;
            }
          }

          aside {
            position: fixed;
            top: 1rem;
            right: 1rem;
          }
        </style>
      </head>
      <body>
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js"></script>

        <div id='loader'>
          <svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" viewBox="0 0 24 24">
            <path d="M0 0h24v24H0z" fill="none" />
            <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3c4.97 0 9 4.03 9 9">
              <animateTransform attributeName="transform" dur="1.5s" repeatCount="indefinite" type="rotate" values="0 12 12;360 12 12" />
            </path>
          </svg>
          Loading...
        </div>

        <model-viewer alt="Lego piece" ar shadow-intensity="1" camera-controls auto-rotate tone-mapping="linear" shadow-intensity="1" shadow-softness="1"  max-camera-orbit="auto auto auto" touch-action="pan-y"></model-viewer>

        <aside>
          <form>
            <input type="number" id="rows" min="1" max="20"/>
            <input type="number" id="columns" min="1" max="20"/>
            <select id='style'>
              <option value="flat">Flat</option>
              <option value="tall">Tall</option>
            </select>
          </form>
        </aside>

        <a class="download" href="#">
          <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
            <path d="M0 0h24v24H0z" fill="none" />
            <g class="download-outline">
              <g fill="currentColor" fill-rule="evenodd" class="Vector" clip-rule="evenodd">
                <path d="M7 22a5 5 0 0 1-5-5v-3a1 1 0 1 1 2 0v3a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3v-3a1 1 0 1 1 2 0v3a5 5 0 0 1-5 5z" />
                <path d="M17.715 10.9a1 1 0 0 1-.016 1.415l-4.5 4.4a1 1 0 0 1-1.398 0l-4.5-4.4a1 1 0 1 1 1.398-1.43l2.801 2.739V5a1 1 0 1 1 2 0v8.624l2.8-2.739a1 1 0 0 1 1.415.016Z" />
              </g>
            </g>
          </svg>
          Download
        </a>

        <script>
          let modelViewer, loader, downloadLink, columnInput, rowInput, styleInput
          let url, rows, columns

          function load() {
            modelViewer = document.querySelector('model-viewer')
            loader = document.querySelector('#loader')
            downloadLink = document.querySelector('a.download')
            rowInput = document.querySelector('#rows')
            columnInput = document.querySelector('#columns')
            styleInput = document.querySelector('#style')

            url = new URL(window.location.href)
            rows = (url.searchParams.get('rows') || 2)
            columns = (url.searchParams.get('columns') || 4)
            style = (url.searchParams.get('style') || 'flat')

            rowInput.value = rows
            columnInput.value = columns
            styleInput.value = style

            modelViewer.addEventListener('progress', (event) => {
              if (event.detail.totalProgress >= 1) {
                document.body.classList.remove('loading')
                return
              }

              document.body.classList.add('loading')
            })

            rowInput.addEventListener('input', () => {
              rows = rowInput.value
              update()
            })

            columnInput.addEventListener('input', () => {
              columns = columnInput.value
              update()
            })

            styleInput.addEventListener('input', () => {
              style = styleInput.value
              update()
            })

            update()
          }

          function update() {
            modelViewer.src = `/lego.glb?rows=${rows}&columns=${columns}&style=${style}`

            downloadLink.download = `lego-${rows}x${columns}-${style}.stl`
            downloadLink.href = `/lego.stl?rows=${rows}&columns=${columns}&style=${style}`

            const path = window.location.protocol + "//" + window.location.host + window.location.pathname + `?rows=${rows}&columns=${columns}&style=${style}`
            window.history.pushState({ path }, '', path)
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
