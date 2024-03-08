import { TodoState } from "../state/TodoState";
import AbstractTodoAction from "./AbstractTodoAction";
import { Todo } from "../state/Todo";

export default class FinishFetchTodosAction extends AbstractTodoAction {
  constructor(private readonly todos: Todo[]) {
    super();
  }

  perform(state: TodoState): TodoState {
    return {
      todos: this.todos,
    };
  }
}
