import {
  AppBar,
  Box,
  Fab,
  Grid,
  Slide,
  Toolbar,
  Zoom,
} from "@material-ui/core";
import { useScrollTrigger } from "@material-ui/core";
import {
  createStyles,
  makeStyles,
  Theme,
  Container,
  ContainerProps,
} from "@material-ui/core";
import { KeyboardArrowUp } from "@material-ui/icons";
import { RouterButton } from "components";
import React from "react";

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

  return (
    <div className={classes.root}>
      <Container {...props} component="main" className={classes.main} fixed>
        <HideOnScroll>
          <AppBar>
            <Toolbar disableGutters>
              <Grid container>
                <Grid item xs={4}>
                  <RouterButton fullWidth color="inherit" to="/">
                    Home
                  </RouterButton>
                </Grid>
                <Grid item xs={4}>
                  <RouterButton fullWidth color="inherit" to="/prints">
                    新規作成
                  </RouterButton>
                </Grid>
                <Grid item xs={4}>
                  <RouterButton fullWidth color="inherit" to="/archives">
                    再印刷
                  </RouterButton>
                </Grid>
              </Grid>
            </Toolbar>
          </AppBar>
        </HideOnScroll>
        <Toolbar />
        <Box mt={2} mb={10}>
          {children}
        </Box>
      </Container>
    </div>
  );
}
