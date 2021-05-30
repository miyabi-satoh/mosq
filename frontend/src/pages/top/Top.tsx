import axios from "axios";
import { useEffect, useState } from "react";
import { RouterLink } from "components";
import { MainLayout } from "layouts";

function Top() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function fetchMessage() {
      try {
        const resp = await axios.get("/api/hello");
        setMessage(resp.data.message);
      } catch (error) {
        console.log(error);
        if (error.response) {
          const { status, statusText } = error.response;
          setMessage(`Error ${status} : ${statusText}`);
        }
      }
    }

    fetchMessage();
  }, []);

  return (
    <MainLayout>
      <p>Hello React.</p>
      <p>{message}</p>
      <p>
        <RouterLink to={`/prints`}>プリント作成</RouterLink>
      </p>
    </MainLayout>
  );
}

export default Top;
