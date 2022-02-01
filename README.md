# quest

Ядро дипломной работы. 

Переводит код из собственного псевдоязыка - языка квестов, в код на qml.

Для моделирования квеста используется из представление в виде конечного автомата: \
каждое задание квеста является состоянием с различными типами переходов \
(на данный момент по времени правильности/неправильности ответа).

Пример кода на язвке квестов - input.txt

Синтаксис будет иметь вид:
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
