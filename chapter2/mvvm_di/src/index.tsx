import React from "react";
import ReactDOM from "react-dom/client";
import AppView from "./app/AppView";
import diContainer from "./common/di/diContainer";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

diContainer.configure().then(() => {
  root.render(<AppView />);
});
