import ListItemTodoView from "./list/ListItemTodoView";
import TableRowTodoView from "./table/TableRowTodoView";

export default function createTodosView(
    TodoView: typeof ListItemTodoView | typeof TableRowTodoView,
    todoViews: JSX.Element[]
): JSX.Element {
    if (TodoView === ListItemTodoView) {
        return <ul>{todoViews}</ul>;
    } else {
        return <table><tbody>{todoViews}</tbody></table>;
    }
}
