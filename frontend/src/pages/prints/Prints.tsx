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
import { RouterButton, RouterLink } from "components";
import PrintForm from "./PrintForm";
import { apiPrints, TPrintHead } from "api";

const thisUrl = "/prints";

function Index() {
  const [printList, setPrintList] =
    useState<TPrintHead[] | undefined>(undefined);

  useEffect(() => {
    let unmounted = false;
    const f = async () => {
      try {
        const data = await apiPrints.list();
        console.log(data);

        if (!unmounted) {
          setPrintList(data.results);
        }
      } catch (error) {}
    };
    f();

    const cleanup = () => {
      unmounted = true;
    };
    return cleanup;
  }, []);

  return (
    <Grid container spacing={2} alignItems="center">
      <Grid item xs={12} sm>
        <Typography component="h2" variant="h6">
          プリントセットの一覧
        </Typography>
      </Grid>
      <Grid item xs={12} sm={5} md={3}>
        <RouterButton
          fullWidth
          variant="contained"
          color="primary"
          to={`${thisUrl}/add`}
        >
          プリントセットを追加
        </RouterButton>
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
                      color="primary"
                      variant="outlined"
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
  );
}

function Prints() {
  return (
    <Box mx={2}>
      <Switch>
        <Route exact path={`${thisUrl}/:printId`} component={PrintForm} />
        <Route component={Index} />
      </Switch>
    </Box>
  );
}

export default Prints;
