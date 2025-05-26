import React from "react";

export function PageSpinner({ color = "dark" }) {
  return (
    <div className="flex items-center justify-center">
      <div
        className={`w-28 h-28 border-8 border-dashed ${
          color === "light" ? "border-white" : "border-button"
        } rounded-full animate-spin-slow`}
      ></div>
    </div>
  );
}
