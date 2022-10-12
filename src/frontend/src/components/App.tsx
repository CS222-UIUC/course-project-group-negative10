import {useState} from 'react';
import logo from '../logo.svg';
import axios from "axios";
import './App.scss';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Tooltip} from 'recharts';

function App() {
  const [textInput, setTextInput] = useState<string>("");
  const [output, setOutput] = useState<string>("");
  const [myData, setMyData] = useState();

  const renderLineChart = (
    <ResponsiveContainer width="100%" height={400}>
        <LineChart data={myData}>
            <Line type="monotone" dataKey="rating" stroke="#8884d8" />
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey="date" />
            <YAxis dataKey="rating" />
            <Tooltip />
        </LineChart>
    </ResponsiveContainer>
  );

  const handleSubmit = () => {
    axios.get(`/api/getReviews?text=${textInput}`).then(res => {
      console.log(res.data.text);
      setMyData(JSON.parse((res.data.text))['reviews']);
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
          <label htmlFor="char-input">Get reviews for app (ex: com.ticktick.task): </label>
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
