import {
  Box,
  createStyles,
  makeStyles,
  Theme,
  Typography,
} from "@material-ui/core";
import { RouterLink } from "components";

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
      </Box>
      <Box m={4}>
        <Typography variant="body1">
          こいつは計算プリントを作る何かです。
        </Typography>
      </Box>
      <Box m={4}>
        <Typography variant="body1">
          <RouterLink to="/prints">プリント選択</RouterLink>
          では、定義済みのプリント仕様から新しいプリントを作成できます。
          <br />
          プリント仕様を追加したい場合は、管理者に依頼してください。
        </Typography>
      </Box>
      <Box m={4}>
        <Typography variant="body1">
          <RouterLink to="/archives">アーカイブ</RouterLink>
          では、過去に作成したプリントを再利用できる予定です。
          <br />
          まだ実装していません。
        </Typography>
      </Box>
    </>
  );
}

export default Top;
