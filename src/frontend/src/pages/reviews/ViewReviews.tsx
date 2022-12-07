import {useState} from 'react';
import axios from "axios";

function ViewReviews() {
  type Props = {};

  const [textInput, setTextInput] = useState<string>("");
  const [output, setOutput] = useState<string>("");

  const reviews = (
    <label htmlFor={output}>\n</label>
  );
  
  const handleSubmit = () => {
    axios.get(`/api/NLP?text=${textInput}`).then((res: any) => {
      console.log(res.data.polarity);
      setOutput(res.data.polarity);
    }).catch((err: any) => console.log(err));
  };

  return (
    <div className="App">
    <header className="App-header">
      <div>
        {reviews}
        <br></br>
        <label htmlFor="char-input">Sentiment analysis on reviews for app (ex: com.ticktick.task): </label>
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


export default ViewReviews;