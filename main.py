class Player:
    def __init__(self, name):
        self._name = name
        # List of tuples of (rating, position)
        self.ratings = []
        # Stores if the Player is available
        self.availability = True

    def add_rating(self, rating, position):
        # Validates if the rating is between 1 and 10
        if 0 < rating > 10:
            # raise ValueError("The rating entered must be between 1 and 10: " + str(rating) + " is out of range")
            print("The rating entered must be between 1 and 10: " + str(rating) + " is out of range")
        # Validates if the rating is between 1 and 10
        elif 0 < position > 15:
            # raise ValueError("The position entered must be between 1 and 15: " + str(position) + " is out of range")
            print("The position entered must be between 1 and 15: " + str(position) + " is out of range")
        # If nothing is in the list then the tuple is appended to it to start the list
        elif len(self.ratings) == 0:
            self.ratings.append((rating, position))
        # Checks if a rating in this position already exist if it does then it updates the rating
        elif self.position_exists(position) is True:
            # Checks if the position exists and if it does then the rating is updates
            self.update_rating(rating, position)
        else:
            # Goes though all the other ratings the player has
            for index in range(len(self.ratings)):
                # Find a rating that is less than the one we are trying to add the new position goes between this one
                # and the previous one
                if rating > self.ratings[index][0]:
                    # Inserts the tuple into the list at the point specified by index
                    self.ratings.insert(index, (rating, position))
                    return
            # This rating was lower than all the others so just append
            self.ratings.append((rating, position))

    def position_exists(self, position):
        # Checks through all the positions to see if one exist
        for rating in self.ratings:
            # Checks if the position exists as one of the player's ratings
            if rating[1] == position:
                return True
        return False

    def delete_rating(self, position):
        # Finds the index of the position in the player's rating array
        for index in range(len(self.ratings)):
            if self.ratings[index][1] == position:
                # Deletes the tuple at the index found
                self.ratings.remove((self.ratings[index][0], position))
                return True
        raise ValueError("The position entered must be in the list: " + str(position) + " is not in the list")

    def update_rating(self, rating, position):
        # Finds the position in the player's rating array and then deletes it
        if self.delete_rating(position) is True:
            # Adds a new rating to the player's ratings
            self.add_rating(rating, position)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Validates if a players name populated is less then 40 characters
        if len(value) > 40:
            raise ValueError("The name entered must be less than 40 characters: "+str(value)+" is too long")
        else:
            self._name = value


class Squad:
    def __init__(self, age_group, ordinal):
        #  Stores the Age Group
        self._age_group = age_group
        # Stores the age group
        self._ordinal = ordinal
        # Stores an array of player objects
        self.players = []
        # Stores all the teams
        self.teams = []
        # Stores the amount of subs each teams needs and their positions
        self.subs = [[]]
        # Initialises the first team's array
        self.rankings = []
        # Creates the 15 other arrays within rankings
        for _ in range(15):
            self.rankings.append([])

    @staticmethod
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

    def add_player(self, name):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        name = self.standardise_name(name)
        if len(name) > 40:
            raise ValueError("The name entered must be less than 40 characters: "+str(name)+" is too long")
        elif self.find_player(name) is None:
            # Appends the standardised name to the class Player
            self.players.append(Player(name))

    def remove_player(self, name):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        name = self.standardise_name(name)
        # Finds the players index in players
        index = self.find_player(name)
        # Deletes the player from players
        del self.players[index]
        # Removes all the player's rankings from the rankings
        self.remove_all_rankings(name)

    def set_player_availability(self, player, availability):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        player = self.standardise_name(player)
        # Finds the players index in players
        index = self.find_player(player)
        # Checks if the player's availability is the same as it is being set to
        if self.players[index].availability is not availability:
            # Sets the player's availability
            self.players[index].availability = availability
            # Checks if the availability is false
            if availability is False:
                # Removes all the player's rankings if the player's availability set to false
                self.remove_all_rankings(player)
            elif availability is True:
                # Adds all the player's rankings if the player's availability set to true
                self.add_all_rankings(player)

    def player_availability(self, player):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        player = self.standardise_name(player)
        # Finds the players index in players
        index = self.find_player(player)
        # Returns the player's availability
        return self.players[index].availability

    def add_ratings(self, name, rating, position):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        name = self.standardise_name(name)
        # Finds the players index in players
        index = self.find_player(name)
        # Validates if the player exists
        if index is None:
            raise ValueError(name + " does not exist as a Player")
        else:
            # Adds a rating to the player
            self.players[index].add_rating(rating, position)
            # Adds the ranking to the
            self.add_ranking(name, rating, position)

    def remove_ratings(self, name, position):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        name = self.standardise_name(name)
        # Finds the players index in players
        index = self.find_player(name)
        print(index)
        # Validates if the player exists
        if index is None:
            raise ValueError(name + " does not exist as a Player")
        else:
            # Iterates through all the player's ratings
            for ratings in self.players[index].ratings:
                # Finds the position in the player's rating array and then deletes it
                if ratings[1] == position:
                    self.players[index].delete_rating(position)
                    self.remove_ranking(name, position)

    def update_ratings(self, name, rating, position):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        name = self.standardise_name(name)
        # Finds the players index in players
        index = self.find_player(name)
        # Validates if the player exists
        if index is None:
            raise ValueError(name + " does not exist as a Player")
        else:
            # Updates the player's rating for the specified position
            self.players[index].update_rating(rating, position)
            # Calls the update_rankings function
            self.update_rankings(name, rating, position)

    def find_player(self, player):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        player = self.standardise_name(player)
        # Integrates though every player
        for index in range(len(self.players)):
            # Checks if the player is equal to the player stored at the current index
            if player == self.players[index].name:
                return index
        return None

    def add_ranking(self, player, rating, position):
        position = position - 1
        index = self.find_player(player)
        # Checks if the Players Availability
        if self.players[index].availability is False:
            return
        # Checks if the length of the positions ranking array is 0
        elif len(self.rankings[position]) == 0:
            # appends the player's name and ranking to the positions array
            self.rankings[position].append((player, rating))
        else:
            # Iterates though all the other ratings the player has
            for index in range(len(self.rankings[position])):
                # Checks is the players rating is already in the ranking array
                if (player, rating) == self.rankings[position][index]:
                    return
                # If we find a rating that is less than the one we are trying to add the new position goes between this
                # one and the previous one
                elif rating > self.rankings[position][index][1]:
                    # Inserts the tuple into the list at the point specified by index
                    self.rankings[position].insert(index, (player, rating))
                    return
            # This rating was lower than all the others so just append
            self.rankings[position].append((player, rating))

    def add_all_rankings(self, player):
        # Finds the position of the player in players array
        index = self.find_player(player)
        # Iterates through all the player's ratings
        for positions in range(len(self.players[index].ratings)):
            # Calls the add_ranking function
            self.add_ranking(player, self.players[index].ratings[positions][0],
                             self.players[index].ratings[positions][1])

    def remove_ranking(self, player, position):
        position = position - 1
        # Iterates through the rankings in the position
        for rankings in range(0, len(self.rankings[position])):
            # Checks if the Player's name is equal to the current ranking's name
            if self.rankings[position][rankings][0] == player:
                # Deletes the ratings it is on
                del self.rankings[position][rankings]
                break

    def remove_all_rankings(self, player):
        # Finds the position of the player in players array
        index = self.find_player(player)
        # Iterates through all the player's ratings
        for positions in range(len(self.players[index].ratings)):
            # Calls the remove_ranking function
            self.remove_ranking(player, self.players[index].ratings[positions][1])

    def update_rankings(self, player, rating, position):
        # Calls the remove_ranking function
        self.remove_ranking(player, position)
        # Calls the add_ranking function
        self.add_ranking(player, rating, position)

    def update_team(self, team):
        # Checks if team is None
        if team is None:
            # Empties the array teams
            self.teams = []
            # Runs build_teams function
            self.build_teams(team, None)
        else:
            # Clears the team by setting the object to a blank list
            for i in range(team, len(self.teams) - team):
                del self.teams[team]
            # Calls the build_teams function
            self.build_teams(team, None)

    def build_teams(self, team, player):
        if player is None:
            player = [None, None, None]
        # Checks if team is None
        if team is None:
            # Sets the index to the integer value of team
            index = 0
            # Sets self.teams to a empty list
            self.teams = []
        else:
            # Sets the index to the integer of team
            index = int(team)
        # checks if the value of index is equal to the length of the list teams
        if index == len(self.teams):
            # Appends a new list to the subs list
            self.teams.append([])
        # checks if the value of index is equal to the length of the list subs
        if index == len(self.subs):
            # Appends a new list to the subs list
            self.subs.append([])
        # Sets the current value of the list to a blank list
        self.teams[index] = []
        # Iterates through the positions
        for positions in range(15):
            if positions == player[2] and index == player[0]:
                self.teams[index].append(player[1])
            else:
                # Iterates thorough the all the position's rankings
                for levels in range(index, len(self.rankings[positions])):
                    # Checks to see if the player is already in any teams
                    if any(self.rankings[positions][levels][0] in sublist for sublist in self.teams) is False and \
                            self.rankings[positions][levels][0] != player[1]:
                        # Appends the player to the team
                        # "team.append(self.rankings[positions][levels])" should be used when the raking wants to be stored
                        # "team.append(self.rankings[positions][levels][0])" should be used when the raking wants to be
                        # discarded
                        self.teams[index].append(self.rankings[positions][levels][0])
                        break
        if len(self.subs[index]) != 0:
            # Iterates thorough all the items in the list subs[index]
            for positions in range(len(self.subs[index])):
                # Iterates thorough the amount of subs that are needed
                for levels in range(index, len(self.rankings[self.subs[index][positions]])):
                    # Checks to see if the player is already in any teams
                    if any(self.rankings[self.subs[index][positions]][levels][0] in sublist for sublist in self.teams)\
                            is False and self.rankings[positions][levels][0] != player[1]:
                        # Appends the player to the team
                        # "team.append(self.rankings[self.subs[index][positions]][levels])" should be used when the
                        # raking wants to be stored
                        # "team.append(self.rankings[self.subs[index][positions]][levels][0])" should be used when the
                        # raking wants to be discarded
                        self.teams[index].append(self.rankings[self.subs[index][positions]][levels][0])
                        break
        # Checks if all 15 positions has been filled
        if len(self.teams[index]) == 15 + len(self.subs[index]):
            # Checks if team is not None
            if team is None:
                # This calls the build_teams function again but with team + 1 as an argument
                self.build_teams(1, player)
            else:
                # This calls the build_teams function again but with None as an argument
                self.build_teams(team + 1, player)
        else:
            # This deletes the team if not all the positions are filled
            del self.teams[index]

    def set_player(self, team, player, position):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        player = self.standardise_name(player)
        # Finds the position of the player in players array
        index = self.find_player(player)
        # Decrements the value of team by 1
        team -= 1
        # Decrements the value of position by 1
        position -= 1
        # Checks if the player exists
        if index is None:
            raise ValueError("The player dose not exist")
        else:
            # Sets the data at that index to player
            self.teams[team][position] = player
            # This calls the build_teams function again but with tuple (team, player, position) as an argument
            self.build_teams(None, (team, player, position))

    def players_not_playing(self):
        # Initialises the list not_playing, which is used for players that are not playing
        not_playing = []
        # Iterates through all the players in the squad
        for player in self.players:
            # Checks if any of they players are not in a team
            if any(player.name in sublist for sublist in self.teams) is False:
                # Appends the players name to the list not_playing
                not_playing.append(player.name)
        # Returns the list not_playing
        return not_playing

    def players_not_available(self):
        # Initialises the list not_available, which is used for players that are not available
        not_available = []
        # Iterates through all the players in the squad
        for player in self.players:
            # Checks if the player's availability is False
            if player.availability is False:
                # Appends the players name to the list not_available
                not_available.append(player.name)
        # Returns the list not_available
        return not_available

    def add_sub(self, team, position):
        # Decrements the value of position by 1
        position -= 1
        # Validates if the team exist
        if team + 1 > len(self.subs):
            raise ValueError("The team entered does not exist")
        # Checks if the positions is already a sub
        elif position in self.subs[team]:
            return
        else:
            # Iterates through all the subs
            for index in range(len(self.subs[team])):
                # Checks is the position is less than the current position`
                if position < self.subs[team][index]:
                    # Inserts the position into the list at the point specified by index
                    self.subs[team].insert(index, position)
                    return
            # This position was higher than all the others so it was appended
            self.subs[team].append(position)

    def remove_sub(self, team, position):
        # Decrements the value of position by 1
        position -= 1
        # Validates if the team exist
        if team + 1 > len(self.subs):
            raise ValueError("The team entered does not exist")
        # Checks if the positions is a sub
        elif position in self.subs[team]:
            # Removes the position form the list of subs
            self.subs[team].remove(position)
        else:
            return

    def clear_sub(self, team):
        # Decrements the value of team by 1
        team -= 1
        # Validates if the team exist
        if team + 1 > len(self.subs):
            raise ValueError("The team entered does not exist")
        else:
            # Sets the list subs[team] to a blank list
            self.subs[team] = []

    def import_players(self, file):
        import csv
        try:
            # Opens the CSV file
            with open(file, 'r') as csv_file:
                # Sets the the CSV to player_reader
                player_reader = csv.reader(csv_file)
                # Iterates through all the rows in the CSV
                for row in player_reader:
                    # Calls add player on the data in the first column
                    self.add_player(row[0])
                    # Checks if there are more than 1 column
                    if (len(row) - 1) % 2 == 0:
                        # Iterates through all the rankings in the CSV
                        for ratings in range((len(row) - 1) // 2):
                            # Calls the add_ratings of the data from the CSV
                            self.add_ratings(row[0], int(row[(ratings * 2) + 2]), int(row[(ratings * 2) + 1]))
        except FileNotFoundError:
            raise FileNotFoundError("The file entered: " + file + " does not exist")

    def find_players_team(self, name):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        name = self.standardise_name(name)
        for index in range(len(self.teams)):
            for player in self.teams[index]:
                if player == name:
                    return index
        return None

    def output_player_positions(self, name):
        # Takes the name and passes it to standardise_name() and this outputs a standardised name
        name = self.standardise_name(name)
        # Finds the position of the player in players array
        index = self.find_player(name)
        # Initialises ratings as an empty list
        ratings = []
        # Initialises positions as an empty list
        positions = []
        # Iterates trough all the player's ratings
        for rating in self.players[index].ratings:
            # Appends the rating to the ratings list
            ratings.append(rating[0])
            # Appends the position to the positions list
            positions.append(rating[1])
        # Returns a tuple of containing the list of positions and the list of ratings
        return ratings, positions

    @property
    def age_group(self):
        return self._age_group

    @age_group.setter
    def age_group(self, value):
        # Validates if the rating's length is less than 30 characters
        if len(value) > 30:
            raise ValueError("The age group entered must be less than 30 characters: "+str(value)+" is too long")
        else:
            self._age_group = value

    @property
    def ordinal(self):
        return self._ordinal

    @ordinal.setter
    def ordinal(self, value):
        # Validates if the rating's length is less than 30 characters
        if value is not True and value is not False:
            raise ValueError("The argument for ordinal entered must be a boolean")
        else:
            self._ordinal = value


class School:
    def __init__(self, name):
        # Stores the name of the School
        self._name = name
        # Stores a list of Squads
        self.squads = []

    def add_squad(self, age_group, ordinal, csv):
        # Sets the index of the new squad to the current number of squads
        index = len(self.squads)
        # Appends the new squad to the list of squads
        self.squads.append(Squad(age_group, ordinal))
        # Checks id csv is not None
        if csv is not None:
            # It then runs the function import_players to import the players into the new squad
            self.squads[index].import_players(csv)

    def find_player_age_group(self, name):
        # Iterates through all the squads
        for index in range(len(self.squads)):
            # Checks if the payer is in the squad
            if self.squads[index].find_player(name) is not None:
                return index
        return None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Validates if the name's length is less than 30 characters
        if len(value) > 30:
            raise ValueError("The school name entered must be less than 30 characters: " + str(value) + " is too long")
        else:
            self._name = value
