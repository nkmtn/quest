import QtQuick 2.0
import QtQml.StateMachine 1.14 as DSM

DSM.StateMachine {
	id: stateMachine
	property string rightCode
	signal check(string code)
	signal notify(string message)

	function send(code) {
		if (code === rightCode) {
			notify('Верно! Правильный код: ' + code)
		} else {
			notify('Неверно! Подумайте ещё!')
		}
		check(code)
	}

	 /* Initialization states */

	initialState: sAA010
	running: true

	DSM.State {
		id: sAA010

		onEntered: {
			stateMachine.rightCode = 123
			notify("ЗаданиеTASK 100 + 23")
		}
	}

	DSM.State {
		id: sAB010

		onEntered: {
			stateMachine.rightCode = 123
			notify("ЗаданиеПодсказка: Это 124 - 1")
		}
	}

	DSM.State {
		id: sAB011

		onEntered: {
			stateMachine.rightCode = 123
			notify("ЗаданиеВторая подсказка: Это 122 + 1")
		}
	}

	DSM.State {
		id: sAA020

		DSM.SignalTransition {
			targetState: sZZ999
			signal: stateMachine.check
			guard: code === stateMachine.rightCode
		}

		onEntered: {
			stateMachine.rightCode = 321
			notify("ЗаданиеЗадание: А теперь наоборот")
		}
	}

	DSM.State {
		id: sAB020

		DSM.SignalTransition {
			targetState: sZZ999
			signal: stateMachine.check
			guard: code === stateMachine.rightCode
		}

		onEntered: {
			stateMachine.rightCode = 321
			notify("ЗаданиеПодсказка: Просто запиши код предыдущего задания наоборот")
		}
	}

	DSM.State {
		id: sAB021

		onEntered: {
			stateMachine.rightCode = 321
			notify("ЗаданиеПодсказка: Наоборот - это с конца")
		}
	}

	DSM.State {
		id: sZZ999

		onEntered: {
			stateMachine.rightCode = 0
			notify("Заданиеend")
		}
	}

	DSM.FinalState {
		id: sZZ999
	}

	onFinished: {
		notify("Congratulaions! Your quest is completed!")
	}
}
