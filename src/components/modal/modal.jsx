import './modal.css';

function Modal(props) {

    const description = props.description
    const components = props.components
    const cName = props.cName

    return (
        <div>
          <div className="modal-overlay" onClick={() => props.setModalState(false)}></div>
          <div className={cName}>
            <h3>{description}</h3>
            {components}
            <button className="modal-button" onClick={() => props.setModalState(false)}> Close </button>
          </div>
        </div>
    )
}

export default Modal;