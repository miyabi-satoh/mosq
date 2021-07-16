import { createMuiTheme } from "@material-ui/core";
import { indigo } from "@material-ui/core/colors";

export const theme = createMuiTheme({
  palette: {
    type: "light",
    primary: indigo,
  },
  props: {
    MuiCheckbox: {
      color: "primary",
    },
    MuiRadio: {
      color: "primary",
    },
    MuiSwitch: {
      color: "primary",
    },
    MuiTextField: {
      variant: "outlined",
    },
  },
  typography: {
    button: {
      textTransform: "none",
    },
    fontFamily: [
      "Roboto",
      '"Meiryo UI"',
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
