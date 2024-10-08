import 'package:flutter/material.dart';
import 'package:hockey_stattracker/models/game.dart';

class GameDetailScreen extends StatefulWidget {
  final Game game;
  const GameDetailScreen({required this.game, super.key});

  @override
  State<GameDetailScreen> createState() => _GameDetailScreenState();
}

class _GameDetailScreenState extends State<GameDetailScreen> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        children: <Widget>[
          Text('Game Details'),
          Text('Home Team: ${widget.game.homeTeam}'),
          Text('Away Team: ${widget.game.awayTeam}'),
          Text('Date: ${widget.game.date}'),
          Text('Location: ${widget.game.homeTeam}'),
          Text('Home Team Score: ${widget.game.homeScore}'),
          Text('Away Team Score: ${widget.game.awayScore}'),
        ],
      ),
    );
  }
}
