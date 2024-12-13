import { useState } from "react";
import './home.css';

function Home() {
  const [modalState, setModalState] = useState(false);
  return (
    <div className="home">
      {modalState && (
        <div>
          <div className="modal-overlay" onClick={() => setModalState(false)}></div>
          <div className="modal">
            <h3>This is a modal.</h3>
            <button className="modal-button" onClick={() => setModalState(false)}>Close</button>
          </div>
        </div>
      )}
      <button className="modal-button" onClick={() => {setModalState(!modalState)}}> Open Modal </button>
    </div>
  );
}

export default Home;