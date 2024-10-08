import 'package:flutter/material.dart';
import 'models/user.dart';
import 'models/character.dart';
import 'network/network.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  User user = User('name', 'email');
  Character character =
      Character('name', 'position', 'team', User('name', 'email'));

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('API Data'),
      ),
      body: ListView.builder(
        itemCount: 1,
        itemBuilder: (BuildContext context, int index) {
          return ListTile(
            title: Text(character.name),
            subtitle: Text(
                '${character.position} ${character.team}\n${character.user.username} ${character.user.email}'),
            tileColor: Colors.grey[200],
          );
        },
      ),
    );
  }
}
