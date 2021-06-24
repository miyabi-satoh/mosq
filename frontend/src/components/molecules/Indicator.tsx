import { Box, CircularProgress } from "@material-ui/core";

function Indicator() {
  return (
    <Box m={4} textAlign="center">
      <CircularProgress disableShrink />
    </Box>
  );
}

export { Indicator };
