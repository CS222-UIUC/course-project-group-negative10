import React from 'react';
import axios from "axios";
import {useState} from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Label,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

type Props = {};

function AppDetails() {
  const [textInput, setTextInput] = useState<string>("");
  const [appName, setAppName] = useState<string>("");
  const [summary, setSummary] = useState<string>("");
  const [installs, setInstalls] = useState<string>("");
  const [rating, setRating] = useState<string>("");
  const [myData, setMyData] = useState();
  
  const renderBarChart = (
    <BarChart width={520} height={200} data={myData}>
    <XAxis
      dataKey={`rating`}
      interval={"preserveStart"}
      className="axis-legend"
    />
    <YAxis allowDecimals={false} className="axis-legend">
      <Label
        value="number of ratings"
        angle={-90}
        fill="#666"
        dx={-30}
      />
    </YAxis>
    <Tooltip />
    <Bar dataKey="count" fill="#ffaa15" stackId="a" />
  </BarChart>
  );

  const handleSubmit = () => {
    axios.get(`/api/appDetails?appName=${textInput}`).then((res: any) => {
      console.log(res.data.text);
      let data = JSON.parse((res.data.text));
      setAppName(data['title']);
      setSummary(data['summary']);
      setInstalls(data['realInstalls']);
      setRating(data['score']);
      setMyData(data['histogram']);
    }).catch((err: any) => console.log(err));
  };

    return (
      <div className="App">
      <header className="App-header">
        <div>
          
          <label htmlFor="char-input">Get details for app (ex: com.ticktick.task): </label>
          <input
            id="char-input" type="text" value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
          />
          <button onClick={handleSubmit}>Submit</button>
          <br></br>
          <h4>{appName}</h4>
          <h5>Summary:  </h5> <p>{summary}</p>
          <h5>Installs:  </h5> <p>{installs}</p>
          <h5>Rating: </h5> <p>{rating}</p>
          <h5> Rating Histogram: </h5>
          {renderBarChart}
        </div>
      </header>
    </div>
    );
  };

export default AppDetails;