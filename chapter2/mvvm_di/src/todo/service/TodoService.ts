import { Todo } from "../model/state/Todo";

export default interface TodoService {
  getTodos(): Promise<Todo[]>;
}
