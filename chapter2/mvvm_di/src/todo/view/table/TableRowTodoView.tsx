import { TodosViewProps } from "../TodosViewProps";

export default function TableRowTodoView({
  toggleTodoDone,
  todo: { id, name, isDone },
}: TodosViewProps) {
  return (
    <tr>
      <td>{id}</td>
      <td>{name}</td>
      <td>
        <input type="checkbox" checked={isDone} onChange={() => toggleTodoDone(id)} />
      </td>
    </tr>
  );
}
