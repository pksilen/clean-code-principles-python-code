import { useEffect } from "react";
import { connect } from "react-redux";
import ListItemTodoView from "./list/ListItemTodoView";
import TableRowTodoView from "./table/TableRowTodoView";
import { controller, ActionDispatchers, State } from "../todoController";

type Props = ActionDispatchers &
  State & {
    TodoView: typeof ListItemTodoView | typeof TableRowTodoView;
  };

function TodosView({
  toggleTodoDone,
  startFetchTodos,
  todos,
  TodoView
}: Props) {
  useEffect(() => {
    startFetchTodos();
  }, [startFetchTodos]);

  const todoViews = todos.map((todo) => (
    <TodoView key={todo.id} todo={todo} toggleTodoDone={toggleTodoDone} />
  ));

  return TodoView === ListItemTodoView
      ? <ul>{todoViews}</ul>
      : <table><tbody>{todoViews}</tbody></table>;
}

export default connect(controller.getState, () =>
  controller.getActionDispatchers()
)(TodosView);
