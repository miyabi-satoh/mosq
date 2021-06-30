import { useEffect, useState } from "react";
import { Route, Switch } from "react-router";
import {
  Grid,
  Typography,
  Box,
  Card,
  CardActions,
  CardContent,
} from "@material-ui/core";
import { Indicator, RouterButton, RouterLink } from "components";
import { apiPrints, TPrintHead } from "api";
import { useAuth } from "contexts/Auth";
import { AddCircleOutline } from "@material-ui/icons";
import PrintForm from "./PrintForm";
import PrintOut from "./PrintOut";

const thisUrl = "/prints";

function Index() {
  const { currentUser } = useAuth();
  const [printList, setPrintList] = useState<TPrintHead[] | undefined>(
    undefined
  );

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

  if (printList === undefined) {
    return <Indicator />;
  }

  return (
    <Grid container spacing={2} alignItems="center">
      <Grid item xs={12} sm>
        <Typography component="h2" variant="h6">
          プリント選択
        </Typography>
      </Grid>
      {currentUser && (
        <Grid item xs={12} sm={5} md={3}>
          <RouterButton
            fullWidth
            variant="contained"
            color="primary"
            startIcon={<AddCircleOutline />}
            to={`${thisUrl}/add`}
          >
            プリント定義を追加
          </RouterButton>
        </Grid>
      )}
      {printList.length === 0 ? (
        <Grid item xs={12}>
          <Box textAlign="center" py={4}>
            プリント定義が未登録です。
          </Box>
        </Grid>
      ) : (
        <Grid item container spacing={2}>
          {printList.map((printhead) => {
            return (
              <Grid item xs={12} md={6} key={`printhead-${printhead.id}`}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography component="h3" variant="h6">
                      <RouterLink to={`${thisUrl}/${printhead.id}`}>
                        {printhead.title}
                      </RouterLink>
                    </Typography>
                    <Typography color="textSecondary">
                      {printhead.description}
                    </Typography>
                  </CardContent>
                  {currentUser && (
                    <CardActions>
                      <RouterButton
                        color="primary"
                        to={`${thisUrl}/${printhead.id}/edit`}
                        size="small"
                      >
                        編集
                      </RouterButton>
                      {/* <Button
                        color="primary"
                        variant="outlined"
                        onClick={() =>
                          window.open(
                            `http://localhost:8000/printout/${printhead.id}/`
                          )
                        }
                      >
                        作成のみ
                      </Button>
                      <Button
                        color="secondary"
                        variant="outlined"
                        onClick={() =>
                          window.open(
                            `http://localhost:8000/printout/${printhead.id}/?archive`
                          )
                        }
                      >
                        作成してアーカイブ
                      </Button> */}
                    </CardActions>
                  )}
                </Card>
              </Grid>
            );
          })}
        </Grid>
      )}
    </Grid>
  );
}

function Prints() {
  return (
    <Box mx={2}>
      <Switch>
        <Route exact path={`${thisUrl}/add`} component={PrintForm} />
        <Route exact path={`${thisUrl}/:printId/edit`} component={PrintForm} />
        <Route exact path={`${thisUrl}/:printId`} component={PrintOut} />
        <Route component={Index} />
      </Switch>
    </Box>
  );
}

export default Prints;
