import { useState } from "react";
import Modal from "../../components/modal/modal";
import './home.css';

function Home() {
  const [modalState, setModalState] = useState(false);
  const components = <div>Very Cool!</div>;

  return (
    <div className="home">
      {modalState && (
        <Modal setModalState={setModalState} description={ "This is a modal" } components={components} cName={"modal"} />
      )}
      <button className="button" onClick={() => {setModalState(!modalState)}}> Open Modal </button>
    </div>
  );
}

export default Home;