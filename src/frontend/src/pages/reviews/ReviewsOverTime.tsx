// import {useState} from 'react';
// import React from 'react';
import {useState} from 'react';
import axios from "axios";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Tooltip} from 'recharts';
import DatePicker from 'react-date-picker';

function ReviewsOverTime() {

  type Props = {};
  const [textInput, setTextInput] = useState<string>("");
  const [output, setOutput] = useState<string>("");
  const [myData, setMyData] = useState();
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [storeOption, setStoreOption] = useState("Play Store");

  const handleDropdownChange = (e: any) => {
    setStoreOption(e.target.value);
  };

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
    axios.get(`/api/getReviews?appName=${textInput}&startDate=${startDate.getFullYear() + "-" + (startDate.getMonth()+1) + "-" +   startDate.getDate()}&endDate=${endDate.getFullYear() + "-" + (endDate.getMonth()+1) + "-" +  endDate.getDate()}&store=${storeOption}`).then((res: any) => {
      console.log(res.data.text);
      setMyData(JSON.parse((res.data.text))['reviews']);
    }).catch((err: any) => console.log(err));
  };

    return (
      <div className="App">
      <header className="App-header">
        <div>
        From: <DatePicker onChange={setStartDate} value={startDate} />
        To: <DatePicker onChange={setEndDate} value={endDate} />

          {renderLineChart}
          <label htmlFor="char-input">Get reviews for app (ex: com.ticktick.task): </label>
          <input
            id="char-input" type="text" value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
          />
          <button onClick={handleSubmit}>Submit</button>
          <br></br>
          <select value={storeOption} onChange={handleDropdownChange}>
            <option value="Play Store">Play Store</option>
            <option value="App Store">App Store</option>
          </select>
        </div>
      </header>
    </div>
    );
}
export default ReviewsOverTime;