import "dart:convert";
import 'package:http/http.dart' as http;
import "package:hockey_stattracker/models/user.dart";
import "package:hockey_stattracker/models/character.dart";

Future<Map<String, Object>> fetchData() async {
  final userResponse =
      await http.get(Uri.parse('http://127.0.0.1:8000/Novadrive'));
  final charResponse =
      await http.get(Uri.parse('http://127.0.0.1:8000/Novadrive/John'));

  if (charResponse.statusCode == 200 && userResponse.statusCode == 200) {
    User user = User.fromJson(jsonDecode(userResponse.body));
    Character character =
        Character.fromJson(jsonDecode(charResponse.body), user);

    return {
      'user': user,
      'character': character,
    };
  } else {
    throw Exception('Failed to load data');
  }
}
