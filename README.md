Parametric Lego block
---------------------

Create a Lego block of **any size** and download it for **3D printing**.

## How it works

The CAD model is generated dynamically using [cadquery](https://github.com/cadquery/cadquery) and served using [Microdot](https://github.com/miguelgrinberg/microdot) web server.

The CAD model is exported as a glTF binary file and displayed in the browser using [`<model-viewer>`](https://modelviewer.dev/).

The user can click "Download STL" and receives an `.stl` file suitable for 3D printing.

## Screenshot

![Screenshot](/screenshot.png)

## Usage

Download this repo:

```
gh repo clone joshnuss/lego-generator
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the app:

```sh
python main.py
```

Visit the app in your browser:

```
http://localhost:5000
```

**Note**: The query params `rows`, `columns` and `style` can be used to dynamically adjust the dimensions of the Lego piece.

## License

MIT
