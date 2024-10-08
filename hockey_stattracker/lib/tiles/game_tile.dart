import 'package:flutter/material.dart';
import 'package:hockey_stattracker/models/game.dart';
import 'package:hockey_stattracker/screens/game_detail_screen.dart';

class GameTile extends StatelessWidget {
  final Game game;

  const GameTile({super.key, required this.game});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text("${game.homeTeam} vs ${game.awayTeam}",
          style: const TextStyle(fontWeight: FontWeight.bold)),
      subtitle: Text('Game Date: ${game.date}'),
      tileColor: Colors.grey[200],
      onTap: () {
        Navigator.push(
            context,
            MaterialPageRoute(
                builder: (context) => GameDetailScreen(
                      game: game,
                    )));
      },
    );
  }
}
