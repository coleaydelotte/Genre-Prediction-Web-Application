import { useState } from "react";
import Modal from "../../components/modal/modal";
import './home.css';

function Home() {
  const [modalState, setModalState] = useState(false);
  const components = <button>
    Create
  </button>;

  const Upload = () => {
    console.log("Upload");
  }

  return (
    <div className="home">
      {modalState && (
        <Modal setModalState={setModalState} description={ "This is a modal" } components={components} cName={"modal"} />
      )}
      <div className="flex-content">
        <button className="button" onClick={() => {setModalState(!modalState)}}> Open Modal </button>
        <img src="https://cdn-icons-png.flaticon.com/512/0/532.png" alt="Upload" className="upload"
          onClick={() => {
            Upload();
          }}
        />
      </div>
    </div>
  );
}

export default Home;