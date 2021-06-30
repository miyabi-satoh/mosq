import React, { useState } from "react";
import {
  AppBar,
  Box,
  Container,
  ContainerProps,
  createStyles,
  Fab,
  IconButton,
  makeStyles,
  Menu,
  MenuItem,
  Slide,
  Theme,
  Toolbar,
  useScrollTrigger,
  Zoom,
} from "@material-ui/core";
import { AccountCircle, KeyboardArrowUp, Person } from "@material-ui/icons";
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
      zIndex: 100,
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
          color="default"
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

function AccountMenu() {
  const { currentUser, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleClose();
    logout();
  };

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  return (
    <>
      <IconButton
        color="inherit"
        aria-controls="account-menu"
        aria-haspopup="true"
        onClick={handleClick}
      >
        {currentUser ? <AccountCircle /> : <Person />}
      </IconButton>
      <Menu
        id="account-menu"
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        getContentAnchorEl={null}
        anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
        transformOrigin={{ horizontal: "right", vertical: "top" }}
      >
        {currentUser ? (
          [
            <MenuItem key="1" disabled divider>
              {currentUser.username}
            </MenuItem>,
            <MenuItem key="3" onClick={handleLogout}>
              ログアウト
            </MenuItem>,
          ]
        ) : (
          <MenuItem onClick={handleClose}>
            <RouterLink to="/login">ログイン</RouterLink>
          </MenuItem>
        )}
      </Menu>
    </>
  );
}

export function MainLayout({ children, ...props }: ContainerProps) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Container {...props} className={classes.main} fixed maxWidth="md">
        <HideOnScroll>
          <AppBar>
            <Toolbar disableGutters>
              <Spacer />
              <RouterButton color="inherit" to="/">
                Home
              </RouterButton>
              <Spacer />
              <RouterButton color="inherit" to="/prints">
                プリント選択
              </RouterButton>
              <Spacer />
              <RouterButton color="inherit" to="/archives">
                アーカイブ
              </RouterButton>
              <Spacer />
              <AccountMenu />
            </Toolbar>
          </AppBar>
        </HideOnScroll>
        <Toolbar />
        <Box mt={2} mb={4} component="main">
          {children}
        </Box>
      </Container>
    </div>
  );
}
