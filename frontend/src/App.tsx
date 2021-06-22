import { AuthProvider } from "contexts/Auth";
import { MainLayout } from "layouts";
import { BrowserRouter } from "react-router-dom";
import Router from "./Router";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <MainLayout>
          <Router />
        </MainLayout>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
