import React, { useState, useRef, useEffect } from "react";

export default function App() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hello — ask me about your documents." },
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (e) => {
    e?.preventDefault();
    const text = input.trim();
    if (!text) return;
    const userMsg = { from: "user", text };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setMessages((m) => [...m, { from: "bot", text: "Thinking..." }]);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text }),
      });
      const data = await res.json();
      setMessages((m) => {
        const withoutThinking = m.filter((msg) => msg.text !== "Thinking...");
        return [...withoutThinking, { from: "bot", text: data.reply || JSON.stringify(data) }];
      });
    } catch (err) {
      setMessages((m) => {
        const withoutThinking = m.filter((msg) => msg.text !== "Thinking...");
        return [...withoutThinking, { from: "bot", text: "Error: could not reach backend" }];
      });
    }
  };

  return (
    <div className="container">
      <header className="header">Document RAG — Chat</header>
      <main className="chat">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.from}`}>
            <div className="bubble">{m.text}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </main>
      <form className="composer" onSubmit={send}>
        <input
          placeholder="Type a question about your documents..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
