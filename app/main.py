from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home_view():
        return "<h1>Welcome to Geeks for Geeks</h1>"
@app.route('/api/filterAlgo', methods=['GET', 'POST'])
def query_example():
    if not request.json :
        return 'Please Pass a Valid JSON Object'
    else:
        return 'apply(request.json)'
