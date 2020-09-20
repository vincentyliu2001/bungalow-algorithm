from flask import Flask, request #import main Flask class and request object
from Algo import apply
app = Flask(__name__) #create the Flask app

@app.route('/api/filterAlgo', methods=['GET', 'POST'])
def query_example():
    if not request.json :
        return 'Please Pass a Valid JSON Object'
    else:
        return apply(request.json)

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
