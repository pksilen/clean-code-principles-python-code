import { Todo } from "../model/state/Todo";
import TodoService from "./TodoService";

export default class FakeTodoService implements TodoService {
  // Provides an array of static todos with 2500ms delay
  getTodos(): Promise<Todo[]> {
    return new Promise<Todo[]>((resolve, reject) => {
      setTimeout(() => {
        resolve([
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
        ]);
      }, 2500);
    });
  }
}
