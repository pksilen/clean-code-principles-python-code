import AbstractAction from "./AbstractAction";

export default class UndoAction<S> extends AbstractAction<S> {
  constructor(
    private readonly actionName: string,
    private readonly ActionBaseClass: abstract new (...args: any[]) => AbstractAction<S>,
    private readonly previousState: S
  ) {
    super();
  }

  override getName(): string {
    return this.actionName;
  }

  override perform(state: S): S {
    return this.previousState;
  }

  getActionBaseClass(): abstract new (...args: any[]) => AbstractAction<S> {
    return this.ActionBaseClass;
  }
}
