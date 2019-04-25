import main as backend
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


def normalise_name(name):
    # Takes the name and splits it about the underscore
    name = name.split("_")
    # It then rejoins the names with a space and returns it
    return " ".join(name)


def standardise_name(name):
    # imports regex
    import re
    # Splits the name into an array where each item is a word in the name
    names = [x for x in re.split(" |_", str(name)) if x != '']
    # Iterates though each item in the array
    for index in range(len(names)):
        # Capitalises the word in each item of the array
        names[index] = names[index].title()
    # Returns the joined elements of the array which are separated by underscores
    return "_".join(names)


def index_to_team_name(age_group, team):
    # Checks if .ordinal is set to True
    if BC.squads[age_group].ordinal is True:
        # Convert its to a team name ending with XV
        team_name = str(team + 1) + "XV"
    else:
        # Convert its to a team name starting with the age group
        team_name = BC.squads[age_group].age_group + chr(team + 65)
    return team_name


def allowed_file(filename):
    # Returns the allowed file
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['csv']


@app.route('/', methods=['POST', 'GET'])
def index():
    # Sets all_teams to a blank list
    all_teams = []
    # Sets the school to BC.name
    school = BC.name
    # Checks if there was a post request
    if request.method == 'POST':
        # Checks if the data in the post request contained age_group in the response
        if list(request.form.to_dict())[0] == 'age_group':
            # Adds a new squad with the data from the form
            BC.add_squad(request.form['age_group'], None)
            # Redirects to the new squad's page
            return redirect(url_for('squad', age_group=BC.find_squad_index(request.form['age_group']) + 1))
    # Iterates through all the squads
    for i in range(len(BC.squads)):
        # Appends a tuple containing the age_group and an empty list
        all_teams.append((BC.squads[i].age_group,[]))
        # Iterates through all the squads teams
        for j in range(len(BC.squads[i].teams)):
            # Append each team name to the list inside the tuple
            all_teams[i][1].append(index_to_team_name(i, j))
    return render_template('index.html', all_teams=all_teams, school=school)


@app.route('/team/')
@app.route('/team/<age_group>/<team>', methods=['POST', 'GET'])
def team(age_group=None, team=None):
    # A list storing all the Positions
    positions = ["Loosehead Prop", "Hooker", "Tighthead Prop", "Second Row", "Second Row", "Blindside Flanker",
                 "Openside Flanker", "Number Eight", "Scrum-Half", "Fly-Half", "Left Wing", "Inside Centre",
                 "Outside Centre", "Right Wing", "Full-Back"]
    # team is set to one minus the integer version of team
    team = int(team) - 1
    # age_group is set to one minus the integer version of age_group
    age_group = int(age_group) - 1
    # error is set to a empty string
    error = ""
    # Checks if there was a post request
    if request.method == 'POST':
        # Sets data to the dictionary of the data from the request
        data = request.form.to_dict()
        # Extracts the key form the dictionary
        key = list(data)[0]
        # Sets the position to the data from the form
        position = int(request.form[key])
        # Checks to see if the position is empty
        if position != 0:
            # Checks if key was remove
            if key == "remove":
                # Calls the remove_sub function
                BC.squads[age_group].remove_sub(team, position)
                # Calls the build_teams function
                BC.squads[age_group].build_teams(team, None)
            # Checks if key was add
            elif key == "add":
                # Calls the add_sub function
                BC.squads[age_group].add_sub(team, position)
                # Calls the build_teams function
                BC.squads[age_group].build_teams(team, None)
        else:
            error = "No sub has been selected, please select a sub from the dropdown box below"
    # Sets the subs by iterating through the teams subs and adding 1
    subs_positions = [sub + 1 for sub in BC.squads[age_group].subs[team]]
    # Sets the subs by iterating through the positions extracting the subs positions
    subs = ["Substitute " + positions[sub] for sub in BC.squads[age_group].subs[team]]
    # Finds the team name by calling the function index_to_team_name()
    team_name = index_to_team_name(age_group, team)
    return render_template('team.html', team_name=team_name, age_group=age_group+1, team=team+1, subs=subs,
                           subs_positions=subs_positions, positions=positions, error=error)


@app.route('/teamsheet/')
@app.route('/teamsheet/<age_group>/<team>', methods=['POST', 'GET'])
def teamsheet(age_group=None, team=None):
    positions = ["Loosehead Prop", "Hooker", "Tighthead Prop", "Second Row", "Second Row", "Blindside Flanker",
                 "Openside Flanker", "Number Eight", "Scrum-Half", "Fly-Half", "Left Wing", "Inside Centre",
                 "Outside Centre", "Right Wing", "Full-Back"]
    # team is set to one minus the integer version of team
    team = int(team) - 1
    # age_group is set to one minus the integer version of age_group
    age_group = int(age_group) - 1
    # error is set to a empty string
    error = ""
    # Checks if there was a post request
    if request.method == 'POST':
        # Sets data to the dictionary of the data from the request
        data = request.form.to_dict()
        # Extracts the two keys form the dictionary
        key = list(data)[0], list(data)[1]
        # Sets the position to the data form the form
        position = int(request.form[key[0]])
        # Sets the player_id to the data form the form
        player_id = request.form[key[1]]
        # Checks to see if both position and player_id are empty
        if position == 0 and player_id == 0:
            error = "Neither a player or position has been selected, please select both a player and position"
        # Checks to see if position is empty
        elif position == 0:
            error = "No position has been selected, please select a position"
        # Checks to see if player_id is empty
        elif player_id == 0:
            error = "No player has been selected, please select a player"
        else:
            try:
                # Calls the set_player function
                BC.squads[age_group].set_player(team + 1, player_id, position)
            except ValueError as error:
                pass
    # Creates a list of subs by iterating through the teams subs list
    subs = ["Substitute " + positions[sub] for sub in BC.squads[age_group].subs[team]]
    # Creates a list of all the positions by combining positions and subs
    positions = positions + subs
    # Creates a list of names by iterating through all the team names and normalising them
    names = [normalise_name(name) for name in BC.squads[age_group].teams[team]]
    # Creates an empty list all_players
    all_players = []
    # Iterates through all the players in the age_group
    for player in BC.squads[age_group].players:
        # Appends the list with a tuple of the name and normalised name
        all_players.append((player.name, normalise_name(player.name)))
    # Finds the team below by adding 2 to the team
    team_below = team + 2
    # Checks if the team below exists
    if team_below > len(BC.squads[age_group].teams):
        team_below = None
    # Finds the team below by setting it to the team
    team_above = team
    # Checks if the team below exists
    if team_above == 0:
        team_above = None
    # Finds the team name by calling the function index_to_team_name()
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
    # Checks if there was a post request
    if request.method == 'POST':
        # Sets data to the dictionary of the data from the request
        data = request.form.to_dict()
        # Checks if the length of the data is 1
        if len(data) == 1:
            key = list(data)[0]
            # Extracts the key form the dictionary
            if key == "availability":
                # Sets the availability to the data from the form
                availability = request.form[key]
                # Checks if availability was True
                if availability == "True":
                    # Sets the availability to True
                    availability = True
                # Checks if availability was True
                elif availability == "False":
                    # Sets the availability to False
                    availability = False
                # Sets the players availability by calling set_player_availability
                BC.squads[age_group].set_player_availability(name, availability)
                # Updates the team  by calling update_team
                BC.squads[age_group].update_team(BC.squads[age_group].find_players_team(name))
            elif key == "remove":
                # Removes all the ratings by calling remove_ratings
                BC.squads[age_group].remove_ratings(name, int(request.form[key]))
                # Removes all the ranking by calling remove_ranking
                BC.squads[age_group].remove_ranking(name, int(request.form[key]))
                # Updates the team  by calling update_team
                BC.squads[age_group].update_team(BC.squads[age_group].find_players_team(name))
            # Checks if key was delete
            elif key == "delete":
                # Deletes the player by calling remove_player
                BC.squads[age_group].remove_player(name)
                # Redirects to the squad's page
                return redirect(url_for('squad', age_group=age_group+1))
        # Checks if the length of the data is 2
        elif len(data) == 2:
            # Extracts the key form the dictionary
            key = list(data)[0], list(data)[1]
            # Sets the position to the data from the form
            position = int(request.form[key[0]])
            # Sets the rating to the data from the form
            rating = int(request.form[key[1]])
            # Checks to see if both position and rating are empty
            if position == 0 and rating == 0:
                error = "Neither a position or rating has been selected, please select both a player and rating"
            # Checks to see if position is empty
            elif position == 0:
                error = "No position has been selected, please select a position"
            # Checks to see if rating is empty
            elif rating == 0:
                error = "No player has been selected, please select a rating"
            else:
                try:
                    # Adds a rating by calling add_ratings
                    BC.squads[age_group].add_ratings(name, rating, position)
                    # Updates the team  by calling update_team
                    BC.squads[age_group].update_team(BC.squads[age_group].find_players_team(name))
                except ValueError as error:
                    pass
    # Sets text_positions to an empty list
    text_positions = []
    # ratings and int_positions are set to the data returned by the function output_player_positions
    ratings, int_positions = BC.squads[age_group].output_player_positions(name)
    # Iterates through all the position in int_positions
    for position in int_positions:
        # Append the data specific positions from all_positions into text_positions
        text_positions.append(all_positions[position - 1])
    # Finds the team  by calling the function find_players_team()
    team = BC.squads[age_group].find_players_team(name)
    # Checks if team is not None
    if team is not None:
        # Finds the team name by calling the function index_to_team_name()
        team_name = index_to_team_name(age_group, team)
    else:
        # Sets the team_name to None
        team_name = None
    return render_template('player.html', name=name, n_name=normalise_name(name),
                           set_availability=not BC.squads[age_group].player_availability(name), team=team,
                           team_name=team_name, age_group=age_group, ratings=ratings, int_positions=int_positions,
                           text_positions=text_positions, all_positions=all_positions, error=error)


@app.route('/squad/')
@app.route('/squad/<age_group>', methods=['GET', 'POST'])
def squad(age_group=None):
    # age_group is set to one minus the integer version of age_group
    age_group = int(age_group) - 1
    # success is set to a empty string
    success = ""
    # error is set to a empty string
    error = ""
    # player is set to an empty list
    players = []
    # Checks if there was a post request
    if request.method == 'POST':
        # Checks if a file was submitted by the form
        if 'file' in request.files:
            # Sets the file to the data form the form
            file = request.files['file']
            # Checks if the file name is blank
            if file.filename == '':
                error = "No file has been selected, please upload a file"
            else:
                # Checks if the file is allowed using allowed_file
                if file and allowed_file(file.filename):
                    # Sets the file_data to the data form the from
                    file_data = file.stream.read()
                    # Uploads the players by calling upload_players
                    BC.squads[age_group].upload_players(file_data)
                    # Builds the teams with the new players
                    BC.squads[age_group].build_teams(None, None)
                    success = "The file has been uploaded"
                else:
                    error = "This file type is not allowed"
        # Checks if the key was player
        elif list(request.form.to_dict())[0] == 'player':
            try:
                # Adds the player by calling add_player
                BC.squads[0].add_player(request.form['player'])
                # Redirects to the new player's page
                return redirect(url_for('player', name=standardise_name(request.form['player'])))
            except ValueError as error:
                pass
        # Checks if the key was delete
        elif list(request.form.to_dict())[0] == 'delete':
            # Deletes the squad by calling delete_squad
            BC.delete_squad(age_group)
            # Redirects to the index page
            return redirect(url_for('index'))
        # Check if the post request included a file
        elif 'file' not in request.files:
            error = "No file has been selected, please upload a file"
    # Iterates through all the squads teams all the players in the age_group
    for player in BC.squads[age_group].players:
        # Sets the players team by using find_players_team
        team = BC.squads[age_group].find_players_team(player.name)
        if team is not None:
            # Finds the team name by calling the function index_to_team_name()
            team_name = index_to_team_name(age_group, team)
            # Append a tuple containing two tuple containing (player name and normalise name) and (team and team name)
            players.append(((player.name, normalise_name(player.name)), (team + 1, team_name)))
        else:
            # Append a tuple containing two tuple containing (player name and normalise name) and (None and None)
            players.append(((player.name, normalise_name(player.name)), (None, None)))
    # Index is set to one plus the value of age_group
    index = age_group + 1
    # age_group is then set to the age group's name
    age_group = BC.squads[age_group].age_group
    return render_template('squad.html', error=error, success=success, age_group=age_group, index=index,
                           players=players)


@app.after_request
def add_header(response):
    # Prevents caching
    response.no_cache = True
    return response

# Initialises the class School
BC = backend.School("Brighton College")
BC.add_squad("U18", 'u18_players.csv')
BC.add_squad("U16", 'u16_players.csv')
BC.add_squad("U15", 'u15_players.csv')
BC.add_squad("U14", 'u14_players.csv')
BC.squads[0].build_teams(None, None)
BC.squads[1].build_teams(None, None)
BC.squads[2].build_teams(None, None)
BC.squads[3].build_teams(None, None)

if __name__ == '__main__':
    app.run()
