import {
  createStyles,
  makeStyles,
  Theme,
  Container,
  ContainerProps,
} from "@material-ui/core";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      backgroundColor: theme.palette.grey[900],
      display: "flex",
      flexDirection: "column",
      minHeight: "100vh",
    },
    main: {
      marginTop: theme.spacing(4),
      marginBottom: theme.spacing(4),
      paddingTop: theme.spacing(3),
      paddingBottom: theme.spacing(3),
      backgroundColor: theme.palette.grey[50],
    },
  })
);

export function MainLayout(props: ContainerProps) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Container {...props} component="main" className={classes.main} fixed />
    </div>
  );
}
