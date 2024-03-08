import undoActions from "../actions/undoActions";
import AbstractAction from "../actions/AbstractAction";
import UndoAction from "../actions/UndoAction";

export default function createReducer<S>(
  initialState: S,
  ActionBaseClass: abstract new (...args: any[]) => AbstractAction<S>
) {
  return function (state: S = initialState, action: { type: AbstractAction<S> }) {
    let newState = state;

    if (
      action.type instanceof UndoAction &&
      action.type.getActionBaseClass() === ActionBaseClass
    ) {
      newState = action.type.perform(state);
    } else if (action.type instanceof ActionBaseClass) {
      if (action.type.isUndoable()) {
        undoActions.unshift(
          new UndoAction(action.type.getName(), ActionBaseClass, state)
        );
      }

      newState = action.type.perform(state);
    }

    return newState;
  };
}
