import { TodoState } from "../state/TodoState";
import AbstractTodoAction from "./AbstractTodoAction";

export default class StartFetchTodosAction extends AbstractTodoAction {
  // We return a static response for demonstration purposes
  // In real-life, you would call a method of a class implementing
  // TodoService interface to fetch todos from remote API
  // You should use dependency injection to inject an instance
  // implementing TodoService interface here.
  // In that way, you can switch to a new todo service API implementation
  // without modifying any existing code (open-closed principle)
  perform(state: TodoState): TodoState {
    return {
      todos: [
        {
          id: 1,
          name: "Todo 1",
          isDone: false,
        },
        {
          id: 2,
          name: "Todo 2",
          isDone: false,
        },
      ],
    };
  }
}
