# quest

The core of my bachelor's thesis.

Translates code from it's own pseudo-language - the Quest language, into QML code.

To model the quest, a representation in the form of a finite state machine is used: \
Each quest task is a state with different types of transitions\

Example code in quest language - input.txt

The syntax will look like:
```
document -> txt
txt -> txt id_init
| txt command
| id_init
| command
id_init -> ID LPAREN text_param COMMA text_param RPAREN
command -> TEXT LPAREN ID COMMA ID COMMA jump_param RPAREN
| TEXT LPAREN ID RPAREN
| TEXT LPAREN ID COMMA ID RPAREN
| TEXT LPAREN ID COMMA ID COMMA ID RPAREN
jump_param -> TEXT COLON TEXT
text_param -> QUOTES TEXT QUOTES
```
