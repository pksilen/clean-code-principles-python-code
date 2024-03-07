import { TodoState } from "../state/TodoState";
import AbstractUndoableAction from "../../../common/model/actions/AbstractUndoableAction";

export default abstract class AbstractTodoAction extends AbstractUndoableAction<TodoState> {}
