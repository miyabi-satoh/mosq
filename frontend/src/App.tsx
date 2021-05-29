import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function fetchHello() {
      try {
        const resp = await axios.get(`/api/hello/`);
        setMessage(resp.data.message);
      } catch (error) {
        console.log(error);
      }
    }
    fetchHello();
  }, []);

  return <div>{message}</div>;
}

export default App;
