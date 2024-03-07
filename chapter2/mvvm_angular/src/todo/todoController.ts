import store from "../common/model/state/store";
import { AppState } from "../common/model/state/AppState";
import ToggleDoneTodoAction from "./model/actions/ToggleDoneTodoAction";
import StartFetchTodosAction from "./model/actions/StartFetchTodosAction";
import Controller from "../common/Controller";

class TodoController extends Controller {
  getState(appState: AppState) {
    return {
      todos: appState.todosState.todos,
    };
  }

  getActionDispatchers() {
    return {
      toggleTodoDone: (id: number) =>
        this.dispatch(new ToggleDoneTodoAction(id)),

      startFetchTodos: () => {
        this.dispatch(new StartFetchTodosAction());
      }
    };
  }
}

export const controller = new TodoController(store.dispatch);
export type State = ReturnType<typeof controller.getState>;

export type ActionDispatchers = ReturnType<
  typeof controller.getActionDispatchers
>;

