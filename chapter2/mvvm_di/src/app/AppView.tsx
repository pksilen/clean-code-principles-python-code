import React from "react";
import { Provider } from "react-redux";
import store from "../common/model/state/store";
import TodosView from "../todo/view/TodosView";
import ListItemTodoView from "../todo/view/list/ListItemTodoView";

function AppView() {
  return (
    <div>
      <Provider store={store}>
        {/*You can change the TodoView to TableRowTodoView */}
        <TodosView TodoView={ListItemTodoView} />
      </Provider>
    </div>
  );
}

export default AppView;
