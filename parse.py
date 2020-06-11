import ply.lex as lex
import ply.yacc as yacc

list_state = {}
finalState = 'ZZ999'
initialState = ''

tokens = (
    'TEXT',
    'ID',
    'LPAREN',
    'RPAREN',
    'QUOTES',
    'COMMA',
    'COLON'
)

# Regular expression rules for tokens
t_TEXT = r'[\w\+\=\-\!\?\&\: ]+'
t_ID = r'S[A-Z][A-Z][0-9][0-9][0-9]'
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_QUOTES = r'\"'
t_COMMA = r','
t_COLON = r':'

# A string containing ignored characters (spaces, tabs, new line and carriage return)
t_ignore = " \t\n\r"

### ERROR PROCESSING ###


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def p_error(p):
    # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])
    print('Syntax error in input! Parser State:{} {} . {}'.format(parser.state, stack_state_str, p))


# Build the lexer
lexer = lex.lex()


### Parsing rules ###


def p_document(t):
    ' document : txt '
    # print(list_state)


def p_txt_id(t):
    ' txt : id_init '
    print("here - id_init")


def p_txt_command(t):
    ' txt : command '


def p_txt_many_ids(t):
    ' txt : txt id_init '


def p_txt_many_commands(t):
    ' txt : txt command '


def p_id_init(t):
    ' id_init : ID LPAREN text_param COMMA text_param RPAREN '
    list_state[t[1][1:]] = {"task": t[3], "code": t[5]}


def p_text_param(t):
    ' text_param : QUOTES TEXT QUOTES '
    t[0] = t[2]


def p_command_jump(t):
    ' command : TEXT LPAREN ID COMMA ID COMMA jump_param RPAREN '
    if t[1][1:] == "JUMP":
        if id_exist(t[3][1:]) and id_exist(t[5][1:]):
            if t[5][2] == 'A':
                list_state[t[3][1:]]['to_task'] = t[5][1:]
            elif t[5][2] == 'B':
                list_state[t[3][1:]]['to_help'] = t[5][1:]
            list_state[t[3][1:]][t[7][0]] = t[7][1]
    else:
        print("err wrong command params!")


def p_jump_param(t):
    ' jump_param : TEXT COLON TEXT'
    t[0] = [t[1], t[3]]


def p_command_one_param(t):
    ' command : TEXT LPAREN ID RPAREN '
    if t[1][1:] == "BEGIN":
        global initialState
        initialState = t[3][1:]
    elif t[1][1:] == "END":
        list_state[finalState] = {"task": 'end', "code": '0'}
        if id_exist(t[3]):
            list_state[t[3]]['to_task'] = finalState
    else:
        print("err wrong command or params!")


def p_command_two_params(t):
    ' command : TEXT LPAREN ID COMMA ID RPAREN '
    if t[1][1:] == "END":
        list_state[finalState] = {"task": 'end', "code": '0'}
        if id_exist(t[3][1:]):
            list_state[t[3][1:]]['to_task'] = finalState
        if id_exist(t[5][1:]):
            list_state[t[5][1:]]['to_task'] = finalState
    else:
        print("err wrong command params!")


def p_command_thee_params(t):
    ' command : TEXT LPAREN ID COMMA ID COMMA ID RPAREN '
    if t[1][1:] == "END":
        list_state[finalState] = {"task": 'end', "code": '0'}
        if id_exist(t[3][1:]):
            list_state[t[3][1:]]['to_task'] = finalState
        if id_exist(t[5][1:]):
            list_state[t[5][1:]]['to_task'] = finalState
        if id_exist(t[7][1:]):
            list_state[t[7][1:]]['to_task'] = finalState
    else:
        print("err wrong command params!")


def id_exist(p):
    if p in list_state:
        return True
    else:
        print('try to use non declare ID: '+p)
        return False


### GENERATE CODE PART ###


def make_game_script():
    script = "import QtQuick 2.0\n" \
        + "import QtQml.StateMachine 1.14 as DSM\n\n" \
        + "DSM.StateMachine {\n" \
        + "\tid: stateMachine\n" \
        + "\tproperty string rightCode\n" \
        + "\tsignal check(string code)\n" \
        + "\tsignal notify(string message)\n\n" \
        + "\tfunction send(code) {\n" \
        + "\t\tif (code === rightCode) {\n" \
        + "\t\t\tnotify('Верно! Правильный код: ' + code)\n" \
        + "\t\t} else {\n" \
        + "\t\t\tnotify('Неверно! Подумайте ещё!')\n" \
        + "\t\t}\n" \
        + "\t\tcheck(code)\n" \
        + "\t}\n\n" \
        + "\t /* Initialization states */\n\n"
    if initialState != '':
        script += "\tinitialState: s" + initialState + "\n" \
                  + "\trunning: true\n\n"
    else:
        print('err: not enough data - initialState')
    for key, value in list_state.items():
        script += make_state(key, value)
    if finalState != '':
        script += "\tDSM.FinalState {\n" \
                  + "\t\tid: s" + finalState + "\n" \
                  + "\t}\n\n"
    else:
        print('err: not enough data - finalState')
    script += "\tonFinished: {\n" \
        + "\t\tnotify(\"Congratulaions! Your quest is completed!\")\n" \
        + "\t}\n"
    script += "}"
    open("Game.qml", "w").write(script)


def make_state(key, value):
    state = "\tDSM.State {\n" \
        + "\t\tid: s" + key + "\n\n"
    if 'to_task' in value:
        state += "\t\tDSM.SignalTransition {\n" \
            + "\t\t\ttargetState: s" + value['to_task'] + "\n" \
            + "\t\t\tsignal: stateMachine.check\n" \
            + "\t\t\tguard: code === stateMachine.rightCode\n" \
            + "\t\t}\n\n"
    if 'to_help' in value:
        state += "\t\tDSM.TimeoutTransition {\n" \
            + "\t\t\ttargetState: s" + value['to_help'] + "\n"
        if 'time' in value:
            state += "\t\t\ttimeout: " + value['time'] + "\n"
        else:
            print('err: not enough data - timeout')
        state += "\t\t}\n\n"
    if 'code' in value and 'task' in value:
        state += "\t\tonEntered: {\n" \
            + "\t\t\tstateMachine.rightCode = " + value['code'] + "\n" \
            + "\t\t\tnotify(\"Задание" + value['task'] + "\")\n" \
            + "\t\t}\n"
    else:
        print('err: not enough data - code or task')
    state += "\t}\n\n"
    return state


parser = yacc.yacc()
parser.parse(open("input.txt", "r").read())
print(list_state)
make_game_script()


