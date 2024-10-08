import 'package:flutter/material.dart';
import 'package:hockey_stattracker/models/game.dart';
import 'package:hockey_stattracker/sample.dart';
import 'package:hockey_stattracker/tiles/game_tile.dart';

class Gamescreen extends StatefulWidget {
  const Gamescreen({super.key});

  @override
  State<Gamescreen> createState() => _GamescreenState();
}

class _GamescreenState extends State<Gamescreen> {
  Game game = samplePlayerGame;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Game Screen'),
      ),
      body: Center(
        child: ListView(children: <Widget>[GameTile(game: game)]),
      ),
    );
  }
}
