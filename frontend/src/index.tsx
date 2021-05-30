import { createMuiTheme, CssBaseline, ThemeProvider } from "@material-ui/core";
import ReactDOM from "react-dom";
import axios from "axios";
import App from "./App";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const theme = createMuiTheme({
  palette: {
    type: "light",
  },
  typography: {
    fontFamily: [
      "Roboto",
      '"M PLUS Rounded 1c"',
      "-apple-system",
      "BlinkMacSystemFont",
      '"Segoe UI"',
      '"Helvetica Neue"',
      "Arial",
      "sans-serif",
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(),
  },
});

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <App />
  </ThemeProvider>,
  document.getElementById("root")
);
