import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'models/user.dart';
import 'models/character.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  User user = User('name', 'email');
  Character character =
      Character('name', 'position', 'team', User('name', 'email'));

  Future<void> fetchData() async {
    final userResponse =
        await http.get(Uri.parse('http://127.0.0.1:8000/Novadrive'));
    final charResponse =
        await http.get(Uri.parse('http://127.0.0.1:8000/Novadrive/John'));
    print(charResponse.body);
    if (charResponse.statusCode == 200 && userResponse.statusCode == 200) {
      setState(() {
        user = User.fromJson(jsonDecode(userResponse.body));
        character = Character.fromJson(jsonDecode(charResponse.body), user);
      });
    } else {
      throw Exception('Failed to load data');
    }
  }

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
            subtitle: Text(character.position +
                ' ' +
                character.team +
                '\n' +
                character.user.username +
                ' ' +
                character.user.email),
            tileColor: Colors.grey[200],
          );
        },
      ),
    );
  }
}
