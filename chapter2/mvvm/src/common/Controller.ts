import AbstractAction from "./model/actions/AbstractAction";

export type Dispatch = (plainActionObject: { type: AbstractAction<any> }) => void;

export default class Controller {
  protected readonly dispatch: (action: AbstractAction<any>) => void;

  // The 'dispatch' is from Redux library
  constructor(dispatch: Dispatch) {
    this.dispatch = (action: AbstractAction<any>) => dispatch({ type: action });
  }
}
