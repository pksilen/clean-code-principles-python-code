import { TodoState } from "../state/TodoState";
import AbstractAction from "../../../common/model/actions/AbstractAction";

export default abstract class AbstractTodoAction extends AbstractAction<TodoState> {}
