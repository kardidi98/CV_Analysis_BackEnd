from flask import Flask, request
import TextRecignitionFromPDF as txtFromPdf
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.route('/api/getGraph', methods=['POST'])
def get_graph():

    file = request.files["file"]
    if file.filename != '':
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join("static/Docs", filename))

        return txtFromPdf.get_pie_chart("static/Docs/"+filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

