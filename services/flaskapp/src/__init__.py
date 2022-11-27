''' This initiate the app object '''
import csv
from flask import Flask, request, render_template, send_file
from src.models import db, UnlabeledData
from src.summarization import preprocess, predict

# Set up flask
app = Flask(__name__)
app.config.from_object("src.config.Config")

# Initialize the database
db.init_app(app)
session = db.session


@app.route('/', methods=['POST', 'GET'])
def index():
    """ This is the main flask route """
    if request.method == 'POST':
        inp = request.form['content']
        print(inp)
        inp_ids = preprocess(inp)
        if inp_ids.nelement() == 0:
            # error case
            return render_template(
                'index.html',
                summary="""Input Error: \
                Make sure that input is English or has max length of 1000"""
                )
        summary = predict(inp_ids)
        print('Summary is: \n', summary)
        session.add(UnlabeledData(raw_text_input=inp, model_output=summary))
        session.commit()
        return render_template('index.html', summary=summary)
    print("GETTING get")
    return render_template('index.html', summary="Nothing to summarize")


@app.route("/unlabeled_data")
def unlabeled_data():
    """ This is the db test flask route """
    with open('dump.csv', 'w', encoding="utf8") as file:
        out = csv.writer(file)
        out.writerow(['id', 'raw_text_input', 'model_output'])

        for item in session.query(UnlabeledData).all():
            out.writerow([item.id, item.raw_text_input, item.model_output])

    return send_file(
        '../dump.csv',
        mimetype='text/csv',
        download_name='Test_datadump.csv',
        as_attachment=True
    )
