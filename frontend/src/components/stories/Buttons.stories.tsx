import ButtonElement from "../Buttons";

export default {
  title: "Components/ButtonElement",
  component: ButtonElement,
};

export const Default = {
  args: {
    label: "Click Me",
    onClick: () => alert("Button clicked!"),
  },
};

export const WithCustomColor = {
  args: {
    label: "Delete",
    bgColor: "bg-red-600",
    onClick: () => alert("Delete clicked!"),
  },
};

export const WithIcon = {
  args: {
    label: "Download",
    icon: "⬇️",
    onClick: () => alert("Download clicked!"),
  },
};
