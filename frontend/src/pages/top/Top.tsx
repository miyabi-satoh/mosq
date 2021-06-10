import { Box, Typography } from "@material-ui/core";

function Top() {
  return (
    <>
      <Box m={2}>
        <Typography component="h1" variant="h3">
          Project MOSQ
        </Typography>
      </Box>
      <Box m={2}>
        <Typography variant="body1">プリント保管庫的なアレです。</Typography>
      </Box>
    </>
  );
}

export default Top;
