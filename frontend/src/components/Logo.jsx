import React from "react";

export default function Logo({ size = 8 }) {
  return (
    <div
      style={{
        width: size * 4,
        height: size * 4,
        borderRadius: 12,
        background: "linear-gradient(135deg, #7c3aed, #6366f1)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <svg
        width="60%"
        height="60%"
        viewBox="0 0 24 24"
        fill="none"
        stroke="white"
        strokeWidth="2"
      >
        <path d="M12 20h9" />
        <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
      </svg>
    </div>
  );
}