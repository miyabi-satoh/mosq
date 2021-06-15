import {
  Box,
  createStyles,
  Hidden,
  makeStyles,
  Theme,
  Typography,
} from "@material-ui/core";
import { RouterButton, RouterLink, Spacer } from "components";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    authButton: {
      minWidth: 100,
      marginRight: theme.spacing(2),
      "&:last-child": {
        marginRight: 0,
      },
    },
    pageTitle: {
      margin: theme.spacing(2),
      marginBottom: theme.spacing(4),
      [theme.breakpoints.up("sm")]: {
        display: "flex",
        alignItems: "center",
      },
    },
    authButtons: {
      [theme.breakpoints.down("xs")]: {
        marginTop: theme.spacing(2),
      },
    },
  })
);

function Top() {
  const classes = useStyles();

  return (
    <>
      <Box className={classes.pageTitle}>
        <Typography component="h1" variant="h4">
          Project MOSQ
        </Typography>
        <Hidden xsDown>
          <Spacer />
        </Hidden>
        <Box className={classes.authButtons}>
          <RouterButton
            variant="contained"
            color="primary"
            to="/login"
            className={classes.authButton}
          >
            Sign in
          </RouterButton>
          <RouterButton
            variant="contained"
            color="secondary"
            to="/login"
            className={classes.authButton}
          >
            Sign up
          </RouterButton>
        </Box>
      </Box>
      <Box m={4}>
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
