import { match, Route, Switch, useRouteMatch } from "react-router";
import { RouterLink } from "components";
import { MainLayout } from "layouts";
import MathContest from "./MathContest";

function urlContest(match: match<{}>) {
  return `${match.url}/contest`;
}

function Index() {
  const match = useRouteMatch();

  return (
    <MainLayout>
      <p>
        <RouterLink to={urlContest(match)}>計算コンテスト</RouterLink>
      </p>
    </MainLayout>
  );
}

function Prints() {
  const match = useRouteMatch();

  return (
    <Switch>
      <Route path={urlContest(match)} component={MathContest} />
      <Route component={Index} />
    </Switch>
  );
}

export default Prints;
