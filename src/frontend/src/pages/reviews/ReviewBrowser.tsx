import {useState} from 'react';
import axios from "axios";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Tooltip} from 'recharts';
import DatePicker from 'react-date-picker';
import InfiniteScroll from "react-infinite-scroll-component";

function ReviewBrowser() {

  type Props = {};
  const [textInput, setTextInput] = useState<string>("");
  const [output, setOutput] = useState<string>("");
  const [myData, setMyData] = useState([]);
  const [continuationToken, setContinuationToken] = useState();
  const [storeOption, setStoreOption] = useState("Play Store");
  const [items, setItems] = useState([]);

  const handleDropdownChange = (e: any) => {
    setStoreOption(e.target.value);
  };

  const getMoreReviews = () => {
    axios.get(`/api/getRawReviews?appName=${textInput}&continuationToken=${continuationToken}`).then((res: any) => {
      setMyData(myData.concat(JSON.parse((res.data.text))['reviews']));
      setContinuationToken(JSON.parse((res.data.text))['continuationToken']);
    }).catch((err: any) => console.log(err));
  };

    const style = {
      border: "1px solid green",
      margin: 6,
      padding: 8,
      display: 'inline-block'
    };

  const infiniteScrollConst = (
    <InfiniteScroll
    dataLength={myData.length}
    next={getMoreReviews}
    hasMore={true}
    loader={<h4>Waiting...</h4>} >

    {myData.map((i, index) => (
      <div style={style} key={index}>
          {i['content']}<br></br>
      </div>
    ))}
  </InfiniteScroll>
  );

  return (
    <div className="App">
    <header className="App-header">
      <div>
        <label htmlFor="char-input">Get reviews for app (ex: com.ticktick.task): </label>
        <input
          id="char-input" type="text" value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
        />
        <button onClick={getMoreReviews}>Submit</button>
        <br></br>
        <select value={storeOption} onChange={handleDropdownChange}>
          <option value="Play Store">Play Store</option>
          <option value="App Store">App Store</option>
        </select>
        {infiniteScrollConst}
      </div>
    </header>
  </div>
  );
}
export default ReviewBrowser;