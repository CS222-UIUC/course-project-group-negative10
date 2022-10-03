import {useState} from 'react';
import logo from '../logo.svg';
import axios from "axios";
import './App.scss';
import { LineChart, Line, CartesianGrid, XAxis, YAxis } from 'recharts';

const data = [{name: 'Page A', uv: 400, pv: 2400, amt: 2400}];

const renderLineChart = (
  <LineChart width={600} height={300} data={data}>
    <Line type="monotone" dataKey="uv" stroke="#8884d8" />
    <CartesianGrid stroke="#ccc" />
    <XAxis dataKey="name" />
    <YAxis />
  </LineChart>
);

function App() {
  const [textInput, setTextInput] = useState<string>("");
  const [output, setOutput] = useState<string>("");

  const handleSubmit = () => {
    axios.get(`/api/test?text=${textInput}`).then(res => {
      setOutput(res.data.text);
    }).catch(err => console.log(err));
  };

  return (
    <div className="App">
      <header className="App-header">
        <pre>django-react-docker-heroku-template</pre>
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <img src={logo} className="App-logo" alt="logo"/>

        <div>
          {renderLineChart}
          <p>Test connection with API:</p>
          <label htmlFor="char-input">Make this text uppercase: </label>
          <input
            id="char-input" type="text" value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
          />
          <button onClick={handleSubmit}>Submit</button>
          <h3>{output}</h3>
        </div>
      </header>
    </div>
  );
}

export default App;
