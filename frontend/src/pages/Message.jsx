import React from "react";

const Message = ({ message }) => {
  const isUser = message.from === "user";

  return (
    <div
      className={`chat-message ${
        isUser ? "chat-message-user" : "chat-message-bot"
      }`}
    >
      {/* Avatar */}
      <div className="chat-avatar">
        {isUser ? (
          <div className="user-avatar">U</div>
        ) : (
          <div className="bot-avatar">
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M12 20h9" />
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
            </svg>
          </div>
        )}
      </div>

      {/* Bubble */}
      <div className="chat-content">
        <div
          className={`chat-bubble ${
            isUser ? "chat-bubble-user" : "chat-bubble-bot"
          }`}
        >
          {/* Plain text message */}
          {message.text && <p>{message.text}</p>}

          {/* Rich content message */}
          {message.html &&
            message.html.map((item, index) => {
              if (typeof item === "string") {
                return (
                  <p key={index} className="chat-line">
                    {item}
                  </p>
                );
              }

              if (item.bold) {
                return (
                  <p key={index} className="chat-bold">
                    {item.bold}
                  </p>
                );
              }

              if (item.bullet) {
                return (
                  <p key={index} className="chat-bullet">
                    • {item.bullet}
                  </p>
                );
              }

              return null;
            })}
        </div>

        <span className="chat-time">{message.time}</span>
      </div>
    </div>
  );
};

export default Message;