import { BrowserRouter, Route, Switch } from "react-router-dom";
import NotFound from "./pages/errors/NotFound";
import Prints from "./pages/prints/Prints";
import Top from "./pages/top/Top";

function Router() {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" component={Top} />
        <Route path="/prints" component={Prints} />
        <Route component={NotFound} />
      </Switch>
    </BrowserRouter>
  );
}

export default Router;
