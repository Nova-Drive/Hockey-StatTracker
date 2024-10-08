import 'package:flutter/material.dart';
import '../models/user.dart';
import '../models/character.dart';
import '../network/network.dart';
import '../sample.dart';
import 'game_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    //fetchData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
      body: ListView.builder(
        itemCount: 1,
        itemBuilder: (BuildContext context, int index) {
          return ListTile(
            title: Text(sampleCharacter.name),
            subtitle: Text(
                '${sampleCharacter.position} ${sampleCharacter.team}\n${sampleCharacter.user.username} ${sampleCharacter.user.email}'),
            tileColor: Colors.grey[200],
          );
        },
      ),
    );
  }
}
