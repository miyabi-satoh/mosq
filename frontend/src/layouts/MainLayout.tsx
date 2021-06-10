import { AppBar, Box, Grid, Slide, Toolbar } from "@material-ui/core";
import { useScrollTrigger } from "@material-ui/core";
import {
  createStyles,
  makeStyles,
  Theme,
  Container,
  ContainerProps,
} from "@material-ui/core";
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
  })
);

function HideOnScroll(props: React.PropsWithChildren<{}>) {
  const trigger = useScrollTrigger();

  return (
    <Slide appear={false} direction="down" in={!trigger}>
      {props.children as React.ReactElement}
    </Slide>
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
                    プリントセット
                  </RouterButton>
                </Grid>
                <Grid item xs={4}>
                  <RouterButton fullWidth color="inherit" to="/archives">
                    アーカイブ
                  </RouterButton>
                </Grid>
              </Grid>
            </Toolbar>
          </AppBar>
        </HideOnScroll>
        <Toolbar />
        <Box my={2}>{children}</Box>
      </Container>
    </div>
  );
}
