import 'package:hockey_stattracker/models/user.dart';
import 'package:hockey_stattracker/models/character.dart';
import 'package:hockey_stattracker/models/game.dart';

User sampleUser = User('Tony Bony', 'TBoney@boney.ca');
Character sampleCharacter = Character('Chad', 'C', 'Oilers', sampleUser);
Game samplePlayerGame = PlayerGame(
    5,
    2,
    3,
    1,
    2,
    20,
    1,
    1,
    1,
    1,
    1,
    1,
    'Oilers',
    'Flames',
    'Oilers',
    7,
    1,
    '2022-01-01',
    '2021-2022',
    'NHL',
    false,
    sampleCharacter);
