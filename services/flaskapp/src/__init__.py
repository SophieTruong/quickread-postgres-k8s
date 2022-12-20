''' This initiate the app object '''
import csv
import json
import pandas as pd
import plotly
import plotly.express as px

from flask import Flask, request, render_template, send_file
from src.models import db, UnlabeledData
from src.summarization import preprocess, predict
from rouge_score import rouge_scorer

DATA_OUTPUT = 'dump.csv'

# Set up flask
app = Flask(__name__)
app.config.from_object("src.config.Config")

# Initialize the database
db.init_app(app)
session = db.session

def get_db_data():
    """ Write db data to csv """
    with open(DATA_OUTPUT, 'w', encoding="utf8") as file:
        out = csv.writer(file)
        out.writerow(['id', 'raw_text_input', 'model_output'])

        for item in session.query(UnlabeledData).all():
            out.writerow([item.id, item.raw_text_input, item.model_output])

def get_rouge_score(scores, rouge_category):
    """ Return F1 score for the inputed rouge_category
    Input:
        scores: Dict Obj
        rouge_category: string
    """
    return scores[rouge_category][2]

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
    get_db_data()
    return send_file(
        '../'+DATA_OUTPUT,
        mimetype='text/csv',
        download_name='Test_datadump.csv',
        as_attachment=True
    )


@app.route("/eval", methods=['GET'])
def get_rouge():
    """ Get and plot ROUGE score """
    rouge1 = 'rouge1'
    rouge_lsum = 'rougeLsum'
    scorer = rouge_scorer.RougeScorer([rouge1, rouge_lsum], use_stemmer=True)

    get_db_data()
    df = pd.read_csv(DATA_OUTPUT)
    print(df)
    df['temp'] = df.apply(lambda x: scorer.score(x.raw_text_input, x.model_output), axis=1)
    df[rouge1] = df['temp'].apply(lambda x: get_rouge_score(x, rouge1))
    df[rouge_lsum] = df['temp'].apply(lambda x: get_rouge_score(x, rouge_lsum))
    print()
    print(df)
    df = df[['rouge1', 'rougeLsum']]
    print()
    print(df)

    fig = px.bar(df, barmode='group')
    fig = fig.update_layout(
        xaxis_title="Index",
        yaxis_title="ROUGE scores",
        legend_title="ROUGE metrics",
        font=dict(
            family="Courier New, monospace",
            size=18,
        )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('eval_page.html', graphJSON=graphJSON)
