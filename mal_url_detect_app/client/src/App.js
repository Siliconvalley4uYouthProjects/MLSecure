import logo from "./logo.svg";
import axios from "axios";
import { useState, useEffect } from "react";

import "./App.css";

function App() {
  const [data, setData] = useState();
  const [counter, setCounter] = useState(0);
  const [status, setStatus] = useState([]);
  const [input, setInput] = useState("");

  async function getData(e) {
    const apiResult = await axios.get("http://localhost:5000/test");
    console.log(apiResult);
    setData(apiResult.data);

    const result = [1, 2, 3];
    setStatus(result);
  }

  function increaseCounter(e) {
    e.preventDefault();
    setCounter(counter + 1);
  }

  useEffect(() => {
    (async () => {
      data = await getData();
    })();
  }, []);

  function updateInput(e) {
    setInput(e.target.value);
  }

  return (
    <div className="App">
      <nav class="navbar navbar-default">
        <h1>Malicious URLs Detector App</h1>
      </nav>
      <input type="text" value={input} onChange={updateInput} />
      <div class="jumbotron">
        <form>
          <button onClick={increaseCounter}>{counter}</button>
          <h1>Data: {data}</h1>
          <button>Test</button>
          <label>Enter URLs or any texts (Emails, Messages)</label>
          <textarea name="search_text" class="form-control"></textarea>

          <label>Choose URL Status</label>
          <select name="url_status" id="url_status">
            <option value="all">All</option>
          </select>
          {status.map((item) => (
            <p>{item}</p>
          ))}
        </form>
      </div>
    </div>
  );
}

export default App;
