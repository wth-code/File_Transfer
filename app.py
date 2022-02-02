import os
import random
import string
import time
from flask import *
from werkzeug.utils import secure_filename
from multiprocessing import Process

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'


def delete(filename):
    # wait 30 min
    time.sleep(60 * 30)
    # delete file
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        # get the file
        f = request.files["file"]
        # random generate 4 digit number
        rand_num = ''.join(random.choice(string.digits) for i in range(4))
        # change the file name
        filename = f"{rand_num}______{secure_filename(f.filename)}"
        print(filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # start a new process to delete the file
        p = Process(target=delete, args=(filename,))
        p.start()
        return {"status": "success", "receive_code": rand_num}


@app.route("/download/<string:receive_code>")
def download(receive_code):
    # get all files in directory
    files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))
    # filter the file with receive_code
    files = [f for f in files if receive_code in f]
    # if there is no file, return code not found
    if len(files) == 0:
        return "Code not found"
    # if there is more than one file, return error
    if len(files) > 1:
        return "Error"
    # if there is one file, return the file
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], files[0]), as_attachment=True)
    


if __name__ == "__main__":
    app.run(debug=True)
