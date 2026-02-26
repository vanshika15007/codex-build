import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [typing, setTyping] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat, typing]);

  const sendMessage = async () => {
    if (!message) return;

    const userMessage = { sender: "You", text: message };
    setChat((prev) => [...prev, userMessage]);
    setMessage("");
    setTyping(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/chat", {
        text: message,
      });

      setTimeout(() => {
        const botMessage = {
          sender: "Bot",
          text: response.data.response,
        };
        setChat((prev) => [...prev, botMessage]);
        setTyping(false);
      }, 1000); // typing delay
    } catch (error) {
      setTyping(false);
      alert("Backend not connected!");
    }
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <h2 className="chat-title">🎓 AI Student Chatbot</h2>

        <div className="chat-box">
          {chat.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.sender === "You" ? "user" : "bot"
                }`}
            >
              {msg.text}
            </div>
          ))}

          {typing && <div className="typing">Bot is typing...</div>}
          <div ref={chatEndRef} />
        </div>

        <div className="input-area">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type a message..."
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;