interface ButtonProps {
  label: string;
  bgColor?: string;
  icon?: React.ReactNode;
  onClick?: () => void;
}

function ButtonElement({
  label,
  icon,
  onClick,
  bgColor = "bg-button",
}: ButtonProps) {
  return (
    <button
      className={`px-4 py-2 ${bgColor} text-white hover:opacity-80 flex items-center ${icon ? "justify-between" : "justify-center"} gap-2 w-full uppercase font-karla text-lg`}
      onClick={onClick}
    >
      {label}
      {icon && <span className="text-lg">{icon}</span>}
    </button>
  );
}

export default ButtonElement;
