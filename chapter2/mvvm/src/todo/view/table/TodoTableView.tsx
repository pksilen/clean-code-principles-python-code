import { connect } from "react-redux";
import { useEffect } from "react";
import { controller, ActionDispatchers, State } from "../../todoController";

type Props = ActionDispatchers & State;

function TodosListView({ toggleTodoDone, startFetchTodos, todos }: Props) {
  useEffect(() => {
    startFetchTodos();
  }, [startFetchTodos]);

  const todoElements = todos.map(({ id, isDone, name }) => (
    <tr key={id}>
      <td>{id}</td>
      <td>{name}</td>
      <td>
        <input type="checkbox" checked={isDone} onChange={() => toggleTodoDone(id)} />
      </td>
    </tr>
  ));

  return (
    <table>
      <tbody>{todoElements}</tbody>
    </table>
  );
}

export default connect(controller.getState, () =>
  controller.getActionDispatchers()
)(TodosListView);
