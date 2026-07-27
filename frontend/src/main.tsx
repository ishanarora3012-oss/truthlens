import React from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";

function App(): React.JSX.Element {
  return <main>TRUTHLENS dashboard scaffold</main>;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode><App /></React.StrictMode>,
);
