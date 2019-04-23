import main as backend
from flask import Flask, redirect, url_for, render_template, request

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def normalise_name(name):
    name = name.split("_")
    return " ".join(name)


def standardise_name(name):
    # imports regex
    import re
    # Splits the name into an array where each item is a word in the name
    names = [x for x in re.split(" |_", str(name)) if x != '']
    # Iterates though each item in the array
    for index in range(len(names)):
        # Capitalises the word in each item of the array
        names[index] = names[index].capitalize()
    # Returns the joined elements of the array which are separated by underscores
    return "_".join(names)


def index_to_team_name(age_group, team):
    if BC.squads[age_group].ordinal is True:
        team_name = str(team + 1) + "XV"
    else:
        team_name = BC.squads[age_group].age_group + chr(team + 65)
    return team_name


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def root():
    all_teams = []
    school = BC.name
    for i in range(len(BC.squads)):
        all_teams.append((BC.squads[i].age_group,[]))
        for j in range(len(BC.squads[i].teams)):
            all_teams[i][1].append(index_to_team_name(i, j))
    return render_template('index.html', all_teams=all_teams, school=school)


@app.route('/team/')
@app.route('/team/<age_group>/<team>', methods=['POST', 'GET'])
def team(age_group=None, team=None):
    positions = ["Loosehead Prop", "Hooker", "Tighthead Prop", "Second Row", "Second Row", "Blindside Flanker",
                 "Openside Flanker", "Number Eight", "Scrum-Half", "Fly-Half", "Left Wing", "Inside Centre",
                 "Outside Centre", "Right Wing", "Full-Back"]
    team = int(team) - 1
    age_group = int(age_group) - 1
    error = ""
    if request.method == 'POST':
        data = request.form.to_dict()
        key = list(data)[0]
        position = int(request.form[key])
        if position != 0:
            if key == "remove":
                BC.squads[age_group].remove_sub(team, position)
            elif key == "add":
                BC.squads[age_group].add_sub(team, position)
            BC.squads[age_group].build_teams(team, None)
        else:
            error = "No sub has been selected, please select a sub from the dropdown box below"
    subs_positions = [sub + 1 for sub in BC.squads[age_group].subs[team]]
    subs = ["Substitute " + positions[sub] for sub in BC.squads[age_group].subs[team]]
    team_name = index_to_team_name(age_group, team)
    return render_template('team.html', team_name=team_name, age_group=age_group+1, team=team+1, subs=subs,
                           subs_positions=subs_positions, positions=positions, error=error)


@app.route('/teamsheet/')
@app.route('/teamsheet/<age_group>/<team>', methods=['POST', 'GET'])
def teamsheet(age_group=None, team=None):
    positions = ["Loosehead Prop", "Hooker", "Tighthead Prop", "Second Row", "Second Row", "Blindside Flanker",
                 "Openside Flanker", "Number Eight", "Scrum-Half", "Fly-Half", "Left Wing", "Inside Centre",
                 "Outside Centre", "Right Wing", "Full-Back"]
    team = int(team) - 1
    age_group = int(age_group) - 1
    error = ""
    if request.method == 'POST':
        data = request.form.to_dict()
        key = list(data)[0], list(data)[1]
        position = int(request.form[key[0]])
        player_id = request.form[key[1]]
        if position == 0 and player_id == 0:
            error = "Neither a player or position has been selected, please select both a player and position"
        elif position == 0:
            error = "No position has been selected, please select a position"
        elif player_id == 0:
            error = "No player has been selected, please select a player"
        else:
            try:
                BC.squads[age_group].set_player(team + 1, player_id, position)
            except ValueError as error:
                pass
    subs = ["Substitute " + positions[sub] for sub in BC.squads[age_group].subs[team]]
    positions = positions + subs
    names = [normalise_name(name) for name in BC.squads[age_group].teams[team]]
    all_players = []
    for player in BC.squads[age_group].players:
        all_players.append((player.name, normalise_name(player.name)))
    team_below = team + 2
    if team_below > len(BC.squads[age_group].teams):
        team_below = None
    team_above = team
    if team_above == 0:
        team_above = None
    team_name = index_to_team_name(age_group, team)
    return render_template('teamsheet.html', positions=positions, team_name=team_name, age_group=age_group+1,
                           team=team+1, names=names, players=BC.squads[age_group].teams[team], team_above=team_above,
                           team_below=team_below, all_players=all_players, error=error)


@app.route('/player/')
@app.route('/player/<name>', methods=['POST', 'GET'])
def player(name=None):
    all_positions = ["Loosehead Prop", "Hooker", "Tighthead Prop", "Second Row", "Second Row", "Blindside Flanker",
                 "Openside Flanker", "Number Eight", "Scrum-Half", "Fly-Half", "Left Wing", "Inside Centre",
                 "Outside Centre", "Right Wing", "Full-Back"]
    age_group = BC.find_player_age_group(name)
    error = ""
    if request.method == 'POST':
        data = request.form.to_dict()
        if len(data) == 1:
            key = list(data)[0]
            if key == "availability":
                availability = request.form[key]
                if availability == "True":
                    availability = True
                elif availability == "False":
                    availability = False
                BC.squads[age_group].set_player_availability(name, availability)
                BC.squads[age_group].update_team(BC.squads[age_group].find_players_team(name))
            elif key == "remove":
                BC.squads[age_group].remove_ratings(name, int(request.form[key]))
                BC.squads[age_group].remove_ranking(name, int(request.form[key]))
                BC.squads[age_group].update_team(BC.squads[age_group].find_players_team(name))
            elif key == "delete":
                BC.squads[age_group].remove_player(name)
                return redirect(url_for('squad', age_group=age_group+1))
        else:
            key = list(data)[0], list(data)[1]
            position = int(request.form[key[0]])
            rating = int(request.form[key[1]])
            if position == 0 and rating == 0:
                error = "Neither a position or rating has been selected, please select both a player and rating"
            elif position == 0:
                error = "No position has been selected, please select a position"
            elif rating == 0:
                error = "No player has been selected, please select a rating"
            else:
                try:
                    BC.squads[age_group].add_ratings(name, rating, position)
                    BC.squads[age_group].update_team(BC.squads[age_group].find_players_team(name))
                except ValueError as error:
                    pass
    text_positions = []
    ratings, int_positions = BC.squads[age_group].output_player_positions(name)
    for position in int_positions:
        text_positions.append(all_positions[position - 1])
    team = BC.squads[age_group].find_players_team(name)
    if team is not None:
        team_name = index_to_team_name(age_group, team)
    else:
        team_name = None
    return render_template('player.html', name=name, n_name=normalise_name(name),
                           set_availability=not BC.squads[age_group].player_availability(name), team=team,
                           team_name=team_name, age_group=age_group, ratings=ratings, int_positions=int_positions,
                           text_positions=text_positions, all_positions=all_positions, error=error)


@app.route('/squad/')
@app.route('/squad/<age_group>', methods=['GET', 'POST'])
def squad(age_group=None):
    age_group = int(age_group) - 1
    success = ""
    error = ""
    players = []
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                error = "No file has been selected, please upload a file"
            else:
                if file and allowed_file(file.filename):
                    file_data = file.stream.read()
                    success = "The file has been uploaded"
                    BC.squads[age_group].upload_players(file_data)
                else:
                    error = "This file type is not allowed"
        elif list(request.form.to_dict())[0] == 'player':
            try:
                BC.squads[0].add_player(request.form['player'])
                return redirect(url_for('player', name=standardise_name(request.form['player'])))
            except ValueError as error:
                pass
        # check if the post request has the file part
        elif 'file' not in request.files:
            error = "No file has been selected, please upload a file"
    for player in BC.squads[age_group].players:
        team = BC.squads[age_group].find_players_team(player.name)
        if team is not None:
            if BC.squads[age_group].ordinal is True:
                team_name = str(team + 1) + "XV"
            else:
                team_name = BC.squads[age_group].age_group + chr(team + 65)
            team += 1
        else:
            team_name = None
        players.append(((player.name, normalise_name(player.name)), (team, team_name)))
    index = age_group + 1
    age_group = BC.squads[age_group].age_group
    return render_template('squad.html', error=error, success=success, age_group=age_group, index=index, players=players)


@app.after_request
def add_header(response):
    response.no_cache = True  # prevents caching
    return response


BC = backend.School("Brighton College")
BC.add_squad("U18", True, 'BC_players.csv')
BC.add_squad("U16", False, 'u16_players.csv')
BC.add_squad("U15", False, 'u15_players.csv')
BC.add_squad("U14", False, 'u14_players.csv')
BC.squads[0].build_teams(None, None)
BC.squads[1].build_teams(None, None)
BC.squads[2].build_teams(None, None)
BC.squads[3].build_teams(None, None)

if __name__ == '__main__':
    app.run(debug=True)
