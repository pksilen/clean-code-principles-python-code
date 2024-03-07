import React from "react";
import { Provider } from "react-redux";
import store from "../common/model/store";
import TodosView from "../todo/view/TodosView";
import ListItemTodoView from "../todo/view/list/ListItemTodoView";
import TableRowTodoView from "../todo/view/table/TableRowTodoView";
import TodosView2 from "../todo/view/TodosView2";

function App() {
  return (
    <div>
      <Provider store={store}>
        {/*You can change the TodoView to TableRowTodoView */}
        <TodosView TodoView={ListItemTodoView} />
      </Provider>
    </div>
  );
}

export default App;
