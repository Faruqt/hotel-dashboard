interface LabeledInputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  className?: string;
}

function LabeledInput({
  label,
  className = "",
  ...inputProps
}: LabeledInputProps) {
  return (
    <div className={`flex flex-col mb-[20px] ${className ?? ""}`}>
      <span className="font-semibold text-xs mb-[7px]">{label}</span>
      <input
        className="bg-input w-[600px] h-[44px] p-[15px] text-dark"
        {...inputProps}
      />
    </div>
  );
}

export default LabeledInput;
