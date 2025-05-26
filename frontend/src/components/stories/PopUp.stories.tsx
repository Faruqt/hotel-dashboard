import Modal from "../PopUpModal";

export default {
  title: "Components/Modal",
  component: Modal,
};

export const Default = {
  args: {
    onClick: () => alert("Clicked!"),
    onSuccess: () => alert("Success!"),
    onClose: () => alert("Closed!"),
  },
};
