import { Route, Switch } from "react-router-dom";
import Archives from "pages/archives/Archives";
import SignIn from "pages/auth/SignIn";
import NotFound from "./pages/errors/NotFound";
import Prints from "./pages/prints/Prints";
import Top from "./pages/top/Top";

function Router() {
  return (
    <Switch>
      <Route exact path="/" component={Top} />
      <Route path="/prints" component={Prints} />
      <Route path="/archives" component={Archives} />
      <Route path="/login" component={SignIn} />
      <Route component={NotFound} />
    </Switch>
  );
}

export default Router;
