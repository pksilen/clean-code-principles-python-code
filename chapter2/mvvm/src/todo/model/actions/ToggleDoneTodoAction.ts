import { TodoState } from "../state/TodoState";
import AbstractTodoAction from "./AbstractTodoAction";

export default class ToggleDoneTodoAction extends AbstractTodoAction {
  constructor(private readonly id: number) {
    super();
  }

  perform(state: TodoState): TodoState {
    const newTodos = state.todos.map((todo) => {
      if (todo.id !== this.id) {
        return todo;
      }

      return {
        ...todo,
        isDone: !todo.isDone,
      };
    });

    return {
      ...state,
      todos: newTodos,
    };
  }
}
