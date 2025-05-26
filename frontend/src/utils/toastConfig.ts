import { ToastPosition } from "react-toastify";

interface ReactToastConfig {
  position: ToastPosition;
  autoClose: number;
  hideProgressBar: boolean;
  closeOnClick: boolean;
  draggable: boolean;
}

const ToastConfig: ReactToastConfig = {
  position: "top-right" as ToastPosition,
  autoClose: 3000,
  hideProgressBar: true,
  closeOnClick: true,
  draggable: true,
};

export default ToastConfig;
