from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'vote_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vote.db'

db = SQLAlchemy(app)

# ================= MODELS =================

class Candidate(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(
        db.String(200),
        nullable=False
    )

    party = db.Column(
        db.String(100),
        nullable=False
    )

    votes = db.Column(
        db.Integer,
        default=0
    )

    def __repr__(self):
        return self.fullname

# ================= ROUTES =================

@app.route('/')
def home():

    candidates = Candidate.query.order_by(
        Candidate.votes.desc()
    ).all()

    return render_template(
        'candidates.html',
        candidates=candidates
    )

@app.route('/add-candidate', methods=['GET', 'POST'])
def add_candidate():

    if request.method == 'POST':

        fullname = request.form['fullname']
        party = request.form['party']

        candidate = Candidate(
            fullname=fullname,
            party=party
        )

        db.session.add(candidate)
        db.session.commit()

        return redirect('/')

    return render_template('add_candidate.html')

@app.route('/vote/<int:id>')
def vote(id):

    candidate = Candidate.query.get_or_404(id)

    candidate.votes += 1

    db.session.commit()

    flash("Vote Added")

    return redirect('/')

@app.route('/delete-candidate/<int:id>')
def delete_candidate(id):

    candidate = Candidate.query.get_or_404(id)

    db.session.delete(candidate)
    db.session.commit()

    return redirect('/')

# ================= MAIN =================

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
