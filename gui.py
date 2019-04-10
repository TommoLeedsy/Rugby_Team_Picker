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
    all_teams = []
    school = BC.name
    for i in range(len(BC.squads)):
        all_teams.append((BC.squads[i].age_group,[]))
        for j in range(len(BC.squads[i].teams)):
            if BC.squads[i].ordinal is True:
                all_teams[i][1].append(str(j + 1) + "XV")
            else:
                all_teams[i][1].append(BC.squads[i].age_group + chr(j + 65))
    return render_template('index.html', all_teams=all_teams, school=school)


@app.route('/teamsheet/')
@app.route('/teamsheet/<age_group>/<team>')
def team(age_group=None,team=None):
    positions = ["Loosehead Prop", "Hooker", "Tighthead Prop", "Second Row", "Second Row", "Blindside Flanker",
                 "Openside Flanker", "Number Eight", "Scrum-Half", "Fly-Half", "Left Wing", "Inside Centre",
                 "Outside Centre", "Right Wing", "Full-Back"]
    team = int(team) - 1
    age_group = int(age_group) - 1
    subs = ["Substitute " + positions[sub] for sub in BC.squads[age_group].subs[team]]
    positions = positions + subs
    names = [normalise_name(name) for name in BC.squads[age_group].teams[team]]
    team_below = team + 2
    if team_below > len(BC.squads[age_group].teams):
        team_below = None
    team_above = team
    if team_above == 0:
        team_above = None
    if BC.squads[age_group].ordinal is True:
        team_name = str(team + 1) + "XV"
    else:
        team_name = BC.squads[age_group].age_group + chr(team + 65)
    return render_template('teamsheet.html', positions=positions, team_name=team_name, age_group=age_group+1,
                           names=names, players=BC.squads[age_group].teams[team], team_above=team_above,
                           team_below=team_below)


@app.route('/player/')
@app.route('/player/<name>', methods=['POST', 'GET'])
def player(name=None):
    age_group = BC.find_player_age_group(name)
    if request.method == 'POST':
        BC.squads[age_group].set_player_availability(name, not BC.squads[age_group].player_availability(name))
        BC.squads[age_group].update_team(BC.squads[age_group].find_players_team(name))
    ratings, positions = BC.squads[age_group].output_player_positions(name)
    team = BC.squads[age_group].find_players_team(name)
    if team is not None:
        if BC.squads[age_group].ordinal is True:
            team_name = str(team + 1) + "XV"
        else:
            team_name = BC.squads[age_group].age_group + chr(team + 65)
    else:
        team_name = None
    return render_template('player.html', name=name, n_name=normalise_name(name),
                           availability=BC.squads[age_group].player_availability(name),
                           not_availability=not BC.squads[age_group].player_availability(name), team=team,
                           team_name=team_name, age_group=age_group, ratings=ratings, positions=positions)


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
            BC.squads[0].import_players('uploads/' + filename)
    return render_template('setup.html', error=error, success=success)


@app.after_request
def add_header(response):
    response.no_cache = True  # prevents caching
    return response


BC = backend.School("Brighton College")
BC.add_squad("U18", True, 'BC_players.csv')
BC.add_squad("U16", False, 'u16_players.csv')
BC.add_squad("U15", False, 'u15_players.csv')
BC.add_squad("U14", False, 'u14_players.csv')
BC.squads[0].build_teams(None)
BC.squads[1].build_teams(None)
BC.squads[2].build_teams(None)
BC.squads[3].build_teams(None)

if __name__ == '__main__':
    app.run(debug=True)
