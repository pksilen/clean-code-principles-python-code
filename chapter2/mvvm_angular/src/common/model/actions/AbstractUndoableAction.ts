import AbstractAction from "./AbstractAction";

export default abstract class AbstractUndoableAction<S> extends AbstractAction<S> {
  override isUndoable(): boolean {
    return true;
  }
}
