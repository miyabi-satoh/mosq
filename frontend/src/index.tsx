import { CssBaseline, ThemeProvider } from "@material-ui/core";
import ReactDOM from "react-dom";
import { theme } from "theme";
import App from "./App";

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <App />
  </ThemeProvider>,
  document.getElementById("root")
);
