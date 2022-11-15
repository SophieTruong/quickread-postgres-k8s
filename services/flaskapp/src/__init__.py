''' This initiate the app object '''
from flask import Flask, request, render_template
from src.models import db,UnlabeledData
from src.summarization import preprocess,predict

# Set up flask
app = Flask(__name__)
app.config.from_object("src.config.Config")

# Initialize the database
db.init_app(app)

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
                summary="Input Error: Make sure that input is English or has max character count of 1000"
                )
        summary = predict(inp_ids)
        print('Summary is: \n', summary)
        db.session.add(UnlabeledData(raw_text_input=inp,model_output=summary))
        db.session.commit()
        return render_template('index.html', summary=summary)
    print("GETTING get")
    return render_template('index.html', summary="Nothing to summarize")

@app.route("/unlabeled_data")
def unlabeled_data():
    """ This is the db test flask route """
    num_unlabeled_data = UnlabeledData.query.count()
    return f"Number of unlabeled_data: {num_unlabeled_data}"
