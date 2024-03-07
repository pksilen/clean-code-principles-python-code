import { Todo } from "../model/state/Todo";

export type TodosViewProps = {
  toggleTodoDone: (id: number) => void;
  todo: Todo;
};
