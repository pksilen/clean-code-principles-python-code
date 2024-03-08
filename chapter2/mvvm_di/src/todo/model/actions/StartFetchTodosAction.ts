import { Inject } from "noicejs";
import { TodoState } from "../state/TodoState";
import AbstractTodoAction from "./AbstractTodoAction";
import { Todo } from "../state/Todo";
import TodoService from "../../service/TodoService";
import FinishFetchTodosAction from "./FinishFetchTodosAction";
import { Dispatch } from "../../../common/Controller";

type Args = {
  dispatch: Dispatch;
  todoService: TodoService;
};

@Inject("todoService")
export default class StartFetchTodosAction extends AbstractTodoAction {
  constructor(private readonly args: Args) {
    super();
  }

  perform(state: TodoState): TodoState {
    this.args.todoService
      .getTodos()
      .then((todos: Todo[]) => {
        this.args.dispatch(new FinishFetchTodosAction(todos));
      })
      .catch((error) => {
        // Handle error
      });

    return state;
  }
}
