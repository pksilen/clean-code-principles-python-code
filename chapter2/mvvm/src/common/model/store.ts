import { combineReducers, createStore } from "redux";
import createReducer from "./utils/createReducer";
import initialTodosState from "../../todo/model/state/initialTodoState";
import AbstractTodoAction from "../../todo/model/actions/AbstractTodoAction";

const rootReducer = combineReducers({
  todosState: createReducer(initialTodosState, AbstractTodoAction),
});

export default createStore(rootReducer);
