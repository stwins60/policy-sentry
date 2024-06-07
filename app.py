from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, send, emit
import json
from werkzeug.utils import secure_filename
import shutil
# import string
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(CURRENT_DIR, 'uploads')
if os.path.exists(UPLOAD_FOLDER):
    shutil.rmtree(UPLOAD_FOLDER)
else:
    pass
# for f in os.listdir(UPLOAD_FOLDER):
#     if f.endswith(".yaml"):
#         os.remove(os.path.join(UPLOAD_FOLDER, f))
#     else:
#         pass
# create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


ALLOWED_EXTENSIONS = {'yaml'}

app = Flask(__name__)
secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)

for f in os.listdir(app.config['UPLOAD_FOLDER']):
    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f)) and f.endswith(".yaml"):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
    else:
        pass

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    choices = ["Create Policy", "Get Roles"]
    selected_option = "Create Policy"
    output = ""
    file = ""
    # if file end with .yaml, rename to policy-sentry.yml
    if request.method == 'POST':
        selected_option = request.form.get('iam_service')
        # print(selected_option)
        if selected_option == "Create Policy":
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                output = "No file selected"
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                for f in os.listdir(app.config['UPLOAD_FOLDER']):
                    if "policy-sentry.yml" in f:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
                    if f.endswith(".yaml"):
                        os.rename(os.path.join(app.config['UPLOAD_FOLDER'], f), os.path.join(app.config['UPLOAD_FOLDER'], "policy-sentry.yml"))
                    else:
                        pass
                command = ["policy_sentry", "write-policy", "--input-file", f"{app.config['UPLOAD_FOLDER']}/policy-sentry.yml"]
                output = os.popen(' '.join(command)).read()
                # fomat output as json
                output = json.dumps(json.loads(output), indent=4)
            else:
                output = "File not allowed"
        elif selected_option == "Get Roles":
            service = request.form.get('service')
            role_access = request.form.get('role_access')
            resource_type = request.form.get('resource_type')
            print(service, role_access, resource_type)
            command = ["policy_sentry", "query", "action-table", "--service", f"{service.lower()}", "-a", f"{role_access.lower()}", "--fmt", "yaml"]
            output = os.popen(' '.join(command)).read()
            

    # Render the HTML template and pass the terminal output
    return render_template('index.html', output=output, choices=choices, selected_option=selected_option)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    pass

if __name__ == '__main__':
    socketio.run(debug=True, app=app, host='0.0.0.0', port=5000)
