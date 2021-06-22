import { useState, useEffect } from "react";
import {
  Box,
  Button,
  Container,
  createStyles,
  Grid,
  makeStyles,
  Paper,
  TextField,
  Theme,
  Typography,
} from "@material-ui/core";
import { Alert } from "@material-ui/lab";
import { SubmitHandler, useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";
import { useAuth } from "contexts/Auth";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    paper: {
      padding: theme.spacing(2),
    },
  })
);

interface IFormInput {
  username: string;
  password: string;
}

export default function SignIn() {
  const classes = useStyles();
  const history = useHistory();
  const [message, setMessage] = useState("");
  const { login, currentUser } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<IFormInput>();

  const onSubmit: SubmitHandler<IFormInput> = async (formData) => {
    try {
      login(formData.username, formData.password);
    } catch (error) {}
  };

  useEffect(() => {
    if (currentUser) {
      history.push("/");
    } else if (currentUser === null) {
      setMessage("認証情報が一致しませんでした。");
    }
  }, [currentUser, history]);

  return (
    <Container maxWidth="xs">
      <Box my={4} textAlign="center">
        <Typography component="h1" variant="h5">
          Sign in to MOSQ
        </Typography>
      </Box>
      <form noValidate onSubmit={handleSubmit(onSubmit)}>
        <Grid container component={Paper} spacing={2} className={classes.paper}>
          {message && (
            <Grid item xs={12}>
              <Alert severity="error">{message}</Alert>
            </Grid>
          )}
          <Grid item xs={12}>
            <TextField
              size="small"
              inputProps={{
                ...register("username"),
              }}
              label="ユーザー名"
              error={!!errors.username}
              helperText={errors.username?.message}
              autoComplete="username"
              fullWidth
              autoFocus
              required
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              size="small"
              type="password"
              inputProps={{
                ...register("password"),
              }}
              label="パスワード"
              error={!!errors.password}
              helperText={errors.password?.message}
              autoComplete="current-password"
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" fullWidth color="primary" variant="contained">
              Sign in
            </Button>
          </Grid>
        </Grid>
      </form>
    </Container>
  );
}
