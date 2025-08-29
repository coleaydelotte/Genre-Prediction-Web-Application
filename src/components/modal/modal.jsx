// zIndex is their to make sure the implementation
// of the modal can still be styled but the modal will
// still appear the modal overlay.

import './modal.css';

function Modal(props) {

    const description = props.description
    const components = props.components
    const cName = props.cName

    return (
        <div>
          <div className="modal-overlay" onClick={() => props.setModalState(false)}></div>
          <div className={cName} style={{
            zIndex: 1000
          }}>
            <h3>{description}</h3>
            {components}
            <button className="modal-button" onClick={() => props.setModalState(false)}> Close </button>
          </div>
        </div>
    )
}

export default Modal;