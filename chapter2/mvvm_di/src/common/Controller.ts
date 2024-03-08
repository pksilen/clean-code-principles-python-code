import AbstractAction from "./model/actions/AbstractAction";

export type Dispatch = (action: AbstractAction<any>) => void;

export type ReduxDispatch = (reduxActionObject: {
  type: AbstractAction<any>;
}) => void;

export default class Controller {
  protected readonly dispatch: Dispatch;

  constructor(reduxDispatch: ReduxDispatch) {
    this.dispatch = (action: AbstractAction<any>) =>
      reduxDispatch({ type: action });
  }

  dispatchWithDi(
    diContainer: { create: (...args: any[]) => Promise<any> },
    ActionClass: abstract new (...args: any[]) => AbstractAction<any>,
    otherArgs?: {}
  ) {
    diContainer
      .create(ActionClass, {
        dispatch: this.dispatch,
        ...(otherArgs ?? {}),
      })
      .then((action: any) => this.dispatch(action));
  }
}
