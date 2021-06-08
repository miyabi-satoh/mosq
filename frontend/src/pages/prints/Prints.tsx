import { useEffect, useState } from "react";
import { Route, Switch } from "react-router";
import {
  Grid,
  Typography,
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
} from "@material-ui/core";
import { RouterLink } from "components";
import { MainLayout } from "layouts";
import PrintForm from "./PrintForm";
import { apiPrints, TPrintHead } from "api";
import { Link } from "react-router-dom";

// const useStyles = makeStyles({
//   cardActionArea: {
//     "&:hover": {
//       textDecoration: "none",
//     },
//   },
// });

// const backUrl = "/";
const thisUrl = "/prints";

function Index() {
  // const classes = useStyles();
  const [printList, setPrintList] =
    useState<TPrintHead[] | undefined>(undefined);

  useEffect(() => {
    async function fetchPrints() {
      try {
        setPrintList(await apiPrints.list());
      } catch (error) {}
    }

    fetchPrints();
  }, []);

  return (
    <MainLayout>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm>
          <Typography component="h2" variant="h6">
            プリントセットの一覧
          </Typography>
        </Grid>
        <Grid item xs={12} sm={5}>
          <Button
            fullWidth
            variant="contained"
            color="primary"
            component={Link}
            to={`${thisUrl}/add`}
          >
            プリントセットを追加
          </Button>
        </Grid>
        <Grid item container>
          <Grid item xs={12} sm={6}>
            {printList?.length ? (
              printList.map((printhead) => {
                const question_count = printhead.details.reduce(
                  (prev, current) => {
                    const value = Number(current.quantity);
                    return isNaN(value) ? prev : prev + value;
                  },
                  0
                );

                return (
                  <Card variant="outlined" key={`printhead-${printhead.id}`}>
                    <CardContent>
                      <Typography component="h3" variant="h5">
                        <RouterLink to={`${thisUrl}/${printhead.id}`}>
                          {printhead.title}
                        </RouterLink>
                      </Typography>
                      <Typography color="textSecondary">
                        全 {question_count} 問
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button
                        size="small"
                        color="primary"
                        onClick={() =>
                          window.open(
                            `http://localhost:8000/printout/${printhead.id}/`
                          )
                        }
                      >
                        印刷
                      </Button>
                    </CardActions>
                  </Card>
                );
              })
            ) : (
              <Box textAlign="center" py={4}>
                プリントセットは未登録です。
              </Box>
            )}
          </Grid>
        </Grid>
      </Grid>
    </MainLayout>
  );
}

function Prints() {
  return (
    <Switch>
      <Route exact path={`${thisUrl}/:printId`} component={PrintForm} />
      <Route component={Index} />
    </Switch>
  );
}

export default Prints;
