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
import { RouterButton, RouterLink, Spacer } from "components";
import PrintForm from "./PrintForm";
import { apiPrints, TPrintHead } from "api";
import { Alert } from "@material-ui/lab";

const thisUrl = "/prints";

function Index() {
  const [printList, setPrintList] =
    useState<TPrintHead[] | undefined>(undefined);

  const handleRemove = async (id: string) => {
    try {
      await apiPrints.delete(id);
      const data = await apiPrints.list();
      console.log(data);

      setPrintList(data.results);
    } catch (error) {}
  };

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
          プリント定義の一覧
        </Typography>
      </Grid>
      <Grid item xs={12} sm={5} md={3}>
        <RouterButton
          fullWidth
          variant="contained"
          color="primary"
          to={`${thisUrl}/add`}
        >
          プリント定義を追加
        </RouterButton>
      </Grid>
      <Grid item container>
        {printList?.length ? (
          <>
            <Grid item xs={12}>
              <Box mb={2}>
                <Alert severity="warning">
                  このページから印刷すると、問題はランダムに抽出されます。
                  また、生成されたプリントはアーカイブされます。
                </Alert>
              </Box>
            </Grid>
            {printList.map((printhead) => {
              const question_count = printhead.details.reduce(
                (prev, current) => {
                  const value = Number(current.quantity);
                  return isNaN(value) ? prev : prev + value;
                },
                0
              );

              return (
                <Grid item xs={12} md={6} key={`printhead-${printhead.id}`}>
                  <Card variant="outlined">
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
                      <Spacer />
                      <Button
                        color="secondary"
                        variant="outlined"
                        onClick={() => handleRemove(`${printhead.id}`)}
                      >
                        削除
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              );
            })}
          </>
        ) : (
          <Grid item xs={12}>
            <Box textAlign="center" py={4}>
              プリントセットは未登録です。
            </Box>
          </Grid>
        )}
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
