class User {
  final String username;
  final String email;

  User(this.username, this.email);

  User.fromJson(Map<String, dynamic> json)
      : username = json['username'],
        email = json['email'];

  Map<String, dynamic> toJson() => {
        'username': username,
        'email': email,
      };

  @override
  String toString() {
    return 'User{username: $username, email: $email}';
  }
}
