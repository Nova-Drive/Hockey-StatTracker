import 'character.dart';

abstract class Game {
  final int gameID;
  final String homeTeam;
  final String awayTeam;
  final String playerTeam;
  final String date;
  final String season;
  final String league;
  final bool playoffGame;
  final Character character;

  Game(this.gameID, this.homeTeam, this.awayTeam, this.playerTeam, this.date,
      this.season, this.league, this.playoffGame, this.character);

  //Game.fromJson(Map<String, dynamic> json);

  Map<String, dynamic> toJson();
}

class PlayerGame extends Game {
  final int shots;
  final int goals;
  final int assists;
  final int plusMinus;
  final int penaltyMinutes;
  final int toi;
  final int powerPlayGoals;
  final int powerPlayAssists;
  final int shortHandedGoals;
  final int shortHandedAssists;
  final int gameWinningGoals;

  PlayerGame(
      this.shots,
      this.goals,
      this.assists,
      this.plusMinus,
      this.penaltyMinutes,
      this.toi,
      this.powerPlayGoals,
      this.powerPlayAssists,
      this.shortHandedGoals,
      this.shortHandedAssists,
      this.gameWinningGoals,
      int gameID,
      String homeTeam,
      String awayTeam,
      String playerTeam,
      String date,
      String season,
      String league,
      bool playoffGame,
      Character character)
      : super(gameID, homeTeam, awayTeam, playerTeam, date, season, league,
            playoffGame, character);

  PlayerGame.fromJson(Map<String, dynamic> json, Character character)
      : shots = json['shots'],
        goals = json['goals'],
        assists = json['assists'],
        plusMinus = json['plusMinus'],
        penaltyMinutes = json['penaltyMinutes'],
        toi = json['toi'],
        powerPlayGoals = json['powerPlayGoals'],
        powerPlayAssists = json['powerPlayAssists'],
        shortHandedGoals = json['shortHandedGoals'],
        shortHandedAssists = json['shortHandedAssists'],
        gameWinningGoals = json['gameWinningGoals'],
        super(
          json['gameID'],
          json['homeTeam'],
          json['awayTeam'],
          json['playerTeam'],
          json['date'],
          json['season'],
          json['league'],
          json['playoffGame'],
          character,
        );

  Map<String, dynamic> toJson() => {
        'gameID': gameID,
        'homeTeam': homeTeam,
        'awayTeam': awayTeam,
        'playerTeam': playerTeam,
        'date': date,
        'season': season,
        'league': league,
        'playoffGame': playoffGame,
        'character': character.name,
        'shots': shots,
        'goals': goals,
        'assists': assists,
        'plusMinus': plusMinus,
        'penaltyMinutes': penaltyMinutes,
        'toi': toi,
        'powerPlayGoals': powerPlayGoals,
        'powerPlayAssists': powerPlayAssists,
        'shortHandedGoals': shortHandedGoals,
        'shortHandedAssists': shortHandedAssists,
        'gameWinningGoals': gameWinningGoals,
      };
}

class GoalieGame extends Game {
  final int shotsAgainst;
  final int goalsAgainst;
  final int saves;
  final int savePercentage;
  final int shutouts;
  final int minutesPlayed;
  final double goalsAgainstAverage;

  GoalieGame(
      this.shotsAgainst,
      this.goalsAgainst,
      this.saves,
      this.savePercentage,
      this.shutouts,
      this.minutesPlayed,
      this.goalsAgainstAverage,
      int gameID,
      String homeTeam,
      String awayTeam,
      String playerTeam,
      String date,
      String season,
      String league,
      bool playoffGame,
      Character character)
      : super(gameID, homeTeam, awayTeam, playerTeam, date, season, league,
            playoffGame, character);

  GoalieGame.fromJson(Map<String, dynamic> json, Character character)
      : shotsAgainst = json['shotsAgainst'],
        goalsAgainst = json['goalsAgainst'],
        saves = json['saves'],
        savePercentage = json['savePercentage'],
        shutouts = json['shutouts'],
        minutesPlayed = json['minutesPlayed'],
        goalsAgainstAverage = json['goalsAgainstAverage'],
        super(
          json['gameID'],
          json['homeTeam'],
          json['awayTeam'],
          json['playerTeam'],
          json['date'],
          json['season'],
          json['league'],
          json['playoffGame'],
          character,
        );

  Map<String, dynamic> toJson() => {
        'gameID': gameID,
        'homeTeam': homeTeam,
        'awayTeam': awayTeam,
        'playerTeam': playerTeam,
        'date': date,
        'season': season,
        'league': league,
        'playoffGame': playoffGame,
        'character': character.name,
        'shotsAgainst': shotsAgainst,
        'goalsAgainst': goalsAgainst,
        'saves': saves,
        'savePercentage': savePercentage,
        'shutouts': shutouts,
        'minutesPlayed': minutesPlayed,
        'goalsAgainstAverage': goalsAgainstAverage,
      };
}
