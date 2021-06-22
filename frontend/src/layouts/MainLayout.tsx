import React from "react";
import {
  AppBar,
  Box,
  Container,
  ContainerProps,
  createStyles,
  Fab,
  makeStyles,
  Slide,
  Theme,
  Toolbar,
  useScrollTrigger,
  Zoom,
} from "@material-ui/core";
import { KeyboardArrowUp } from "@material-ui/icons";
import { RouterButton, RouterLink, Spacer } from "components";
import { useAuth } from "contexts/Auth";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      backgroundColor: theme.palette.grey[900],
      display: "flex",
      flexDirection: "column",
      minHeight: "100vh",
    },
    main: {
      padding: 0,
      backgroundColor: theme.palette.grey[50],
    },
    scrollTop: {
      position: "fixed",
      bottom: theme.spacing(2),
      right: theme.spacing(2),
    },
  })
);

function HideOnScroll(props: React.PropsWithChildren<{}>) {
  const classes = useStyles();
  const trigger = useScrollTrigger();

  const handleClick = (event: React.MouseEvent) => {
    window[`scrollTo`]({ top: 0, behavior: `smooth` });
  };

  return (
    <>
      <Slide appear={false} direction="down" in={!trigger}>
        {props.children as React.ReactElement}
      </Slide>
      <Zoom in={trigger}>
        <Fab
          color="secondary"
          size="small"
          onClick={handleClick}
          className={classes.scrollTop}
        >
          <KeyboardArrowUp />
        </Fab>
      </Zoom>
    </>
  );
}

export function MainLayout({ children, ...props }: ContainerProps) {
  const classes = useStyles();
  const { currentUser } = useAuth();

  return (
    <div className={classes.root}>
      <Container {...props} className={classes.main} fixed>
        <HideOnScroll>
          <AppBar>
            <Toolbar disableGutters>
              <Spacer />
              <RouterButton color="inherit" to="/">
                Home
              </RouterButton>
              <Spacer />
              <RouterButton color="inherit" to="/prints">
                プリント作成
              </RouterButton>
              <Spacer />
              <RouterButton color="inherit" to="/archives">
                アーカイブ
              </RouterButton>
              <Spacer />
            </Toolbar>
          </AppBar>
        </HideOnScroll>
        <Toolbar />
        <Box mt={2} mb={4} component="main">
          {children}
        </Box>
        <Box p={2}>
          {currentUser ? (
            `${currentUser.username} is logged in.`
          ) : (
            <RouterLink to="/login">ログイン</RouterLink>
          )}
        </Box>
      </Container>
    </div>
  );
}
