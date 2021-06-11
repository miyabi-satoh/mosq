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
      <Box m={4} mt={4}>
        <Typography variant="body1">
          こいつは数学・算数のプリントを作るアレです。
        </Typography>
      </Box>
      <Box m={4}>
        <Typography variant="body1">
          <RouterLink to="/prints">新規作成</RouterLink>では
          プリント内容を新たに定義したり、
          作成済みのプリント定義から新しいプリントを印刷したりできます。
          <br />
          今の所は、計算コンテスト用のプリントしか作れません。
          <br />
          授業時の小テストに使えるプリントも作れるようにする予定。
        </Typography>
      </Box>
      <Box m={4}>
        <Typography variant="body1">
          <RouterLink to="/archives">再印刷</RouterLink>では
          過去に作成したプリントを再印刷できます。
          <br />
          プリントが溜まってきたときに、どうしたら探しやすくなるかなぁ。
          <br />
          ちょっと考えないとなぁ…。
        </Typography>
      </Box>
    </>
  );
}

export default Top;
