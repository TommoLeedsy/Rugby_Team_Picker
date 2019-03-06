import main as backend
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# logged_in = False


def normalise_name(name):
    name = name.split("_")
    return " ".join(name)


@app.route('/')
def root():
    # if logged_in is True:
    #     return render_template('index.html')
    return render_template('index.html')


@app.route('/teamsheet/')
@app.route('/teamsheet/<team>')
def team(team=None):
    positions = ["Loosehead Prop", "Hooker", "Tighthead Prop", "Second Row", "Second Row", "Blindside Flanker", "Openside Flanker", "Number Eight", "Scrum-Half", "Fly-Half", "Left Wing", "Inside Centre", "Outside Centre", "Right Wing", "Full-Back"]
    team = int(team) - 1
    subs = ["Substitute " + positions[sub] for sub in u18.subs[team]]
    positions = positions + subs
    names = [normalise_name(name) for name in u18.teams[team]]
    team_below = team + 2
    if team_below > len(u18.teams):
        team_below = None
    team_above = team
    if team_above == 0:
        team_above = None
    return render_template('teamsheet.html', positions=positions, team=team+1, names=names, players=u18.teams[team], team_above=team_above, team_below=team_below)


@app.route('/player/')
@app.route('/player/<name>', methods=['POST', 'GET'])
def player(name=None):
    ratings, positions = u18.output_player_positions(name)
    u18.find_player(name)
    team = u18.find_players_team(name)
    if request.method == 'POST':
        u18.set_player_availability(name, not u18.player_availability(name))
        u18.update_team(u18.find_players_team(name))
    return render_template('player.html', name=name, n_name=normalise_name(name), availability=u18.player_availability(name), not_availability=not u18.player_availability(name), team=team, ratings=ratings, positions=positions)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/setup/', methods=['GET', 'POST'])
def upload_file():
    success = ""
    error = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            error = "No file has been selected, please upload a file"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            error = "No file has been selected, please upload a file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = "The file has been uploaded"
            u18.import_players('uploads/' + filename)
    return render_template('setup.html', error=error, success=success)


@app.after_request
def add_header(response):
    response.no_cache = True  # prevents caching
    return response


u18 = backend.Squad("u18")
u18.import_players('players.csv')
u18.add_sub(1, 10)
u18.add_sub(1, 3)
u18.add_sub(1, 6)
u18.build_teams(None)
u18.set_player_availability("Alexander_Macaulay", False)
print(u18.players_not_playing())
print(u18.players_not_available())

if __name__ == '__main__':
    app.run(debug=True)
