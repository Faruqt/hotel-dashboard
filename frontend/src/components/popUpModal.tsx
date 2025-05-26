// components import
import ButtonElement from "./Buttons";

interface ModalProps {
  onConfirm: () => void;
  onClose: () => void;
  message?: string;
}

function Modal({ onConfirm, onClose, message }: ModalProps) {

  return (
    <div className="fixed z-50 top-0 h-full left-0 w-screen py-5 bg-overlay bg-opacity-75 backdrop-blur-sm flex justify-center items-center">
      <div className="max-w-[500px] min-w-[454px] h-[inherit] max-h-fit bg-white rounded-lg p-[30px] overflow-y-scroll font-karla">
        <div className="text-[30px]  text-dark font-medium mb-[23px]">
          Are you sure?
        </div>
        <div className="text-[18px] text-dark mt-2 text-[18px] mb-[31px] font-merriweather font-normal">
          {message ? message : "This action cannot be undone."}
        </div>
        <div className="flex justify-between mt-5 text-[18px] text-dark ">
          <div onClick={onConfirm} className="cursor-pointer w-[161px] h-[50px]">
            <ButtonElement label="Yes Delete" />
          </div>
          <div onClick={onClose} className="cursor-pointer w-[197px] h-[50px]">
            <ButtonElement label="No take me back" bgColor="bg-dark"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Modal;
