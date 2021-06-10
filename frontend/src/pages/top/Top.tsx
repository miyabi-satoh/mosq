import { Box, Typography } from "@material-ui/core";
import { RouterLink } from "components";

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
      <Box m={2}>
        <Typography variant="body1">
          <RouterLink to="/prints">プリントセット</RouterLink>では
          プリント内容を新たに定義したり、
          作成済みのプリント定義から新しいプリントを印刷したりできます。
        </Typography>
      </Box>
      <Box m={2}>
        <Typography variant="body1">
          <RouterLink to="/archives">アーカイブ</RouterLink>では
          作成済みのプリントを再印刷できます。
        </Typography>
      </Box>
    </>
  );
}

export default Top;
