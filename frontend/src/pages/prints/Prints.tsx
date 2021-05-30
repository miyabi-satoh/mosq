import { useEffect, useState } from "react";
import { Route, Switch } from "react-router";
import { Grid, Typography, Box } from "@material-ui/core";
import { RouterLink } from "components";
import { MainLayout } from "layouts";
import PrintForm from "./PrintForm";
import { apiPrints, TPrintHead } from "api";

// const backUrl = "/";
const thisUrl = "/prints";

function Index() {
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
      <Grid container spacing={4} alignItems="center">
        <Grid item xs={12}>
          <Typography component="h2" variant="h6">
            プリント一覧
          </Typography>
        </Grid>
        <Grid item xs={12}>
          {printList?.length ? (
            <ul>
              {printList.map((printhead) => {
                return (
                  <li key={`printhead-${printhead.id}`}>{printhead.title}</li>
                );
              })}
            </ul>
          ) : (
            <Box textAlign="center">
              <div>プリントが未登録です。</div>
              <div>
                <RouterLink to={`${thisUrl}/add`}>登録する</RouterLink>
              </div>
            </Box>
          )}
        </Grid>
      </Grid>
    </MainLayout>
  );
}

function Prints() {
  return (
    <Switch>
      <Route path={`${thisUrl}/:printId`} component={PrintForm} />
      <Route component={Index} />
    </Switch>
  );
}

export default Prints;
