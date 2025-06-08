from flask import Flask, request, render_template
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ROBOFLOW_API_KEY = "hf_mqok6DFxn2SGYFSmGxkF"
ROBOFLOW_MODEL = "american-sign-language-letters/1"
ROBOFLOW_URL = f"https://detect.roboflow.com/{ROBOFLOW_MODEL}?api_key={ROBOFLOW_API_KEY}"

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    filename = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, 'rb') as image_file:
                response = requests.post(
                    ROBOFLOW_URL,
                    files={"file": image_file},
                    data={"name": filename}
                )

            data = response.json()
            try:
                prediction = data['predictions'][0]['class']
            except:
                prediction = "Tiada huruf dikesan."

    return render_template('index.html', prediction=prediction, filename=filename)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
