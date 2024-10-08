import 'user.dart';

class Character {
  final String name;
  final String position;
  final String team;
  final User user;

  Character(this.name, this.position, this.team, this.user);

  Character.fromJson(Map<String, dynamic> json, User user)
      : name = json['name'],
        position = json['position'],
        team = json['team'],
        this.user = user;

  Map<String, dynamic> toJson() => {
        'name': name,
        'position': position,
        'team': team,
        'user': user.username,
      };

  @override
  String toString() {
    return 'Character{name: $name, position: $position, team: $team, user: $user}';
  }
}
