// import {useState} from 'react';
// import React from 'react';
import {useState} from 'react';
import axios from "axios";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Tooltip} from 'recharts';
import { DataGrid } from '@mui/x-data-grid';

function ReviewsOverTime() {

  type Props = {};


  const [textInput, setTextInput] = useState<string>("");
  const [output, setOutput] = useState<string>("");
  const [myData, setMyData] = useState();

  const renderLineChart = (
    <ResponsiveContainer width="100%" height={400}>
        <LineChart data={myData}>
            <Line type="monotone" dataKey="rating" stroke="#8884d8" />
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey="date" />
            <YAxis dataKey="rating" domain={[0, 5]}/>
            <Tooltip />
        </LineChart>
    </ResponsiveContainer>
  );

  const handleSubmit = () => {
    axios.get(`/api/getReviews?text=${textInput}`).then((res: any) => {
      console.log(res.data.text);
      setMyData(JSON.parse((res.data.text))['reviews']);
    }).catch((err: any) => console.log(err));
  };

    return (
      <div className="App">
      <header className="App-header">
        <div>
          {renderLineChart}
          <label htmlFor="char-input">Get reviews for app (ex: com.ticktick.task): </label>
          <input
            id="char-input" type="text" value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
          />
          <button onClick={handleSubmit}>Submit</button>
        </div>
      </header>
    </div>
    );
}
export default ReviewsOverTime;