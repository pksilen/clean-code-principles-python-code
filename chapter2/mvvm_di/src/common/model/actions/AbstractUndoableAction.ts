import AbstractAction from "./AbstractAction";

export default abstract class AbstractUndoableAction<S> extends AbstractAction<S> {
  isUndoable(): boolean {
    return true;
  }
}
