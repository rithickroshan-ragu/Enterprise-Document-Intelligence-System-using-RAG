import React, { useState, useRef, useEffect } from "react";

export default function App() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hello — ask me about your documents." },
  ]);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

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

  const handleUpload = async (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".pdf") && file.type !== "application/pdf") {
      setMessages((m) => [...m, { from: "bot", text: "Only PDF files are accepted." }]);
      e.target.value = null;
      return;
    }

    setMessages((m) => [...m, { from: "user", text: `Uploading ${file.name}...` }]);
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/upload_pdf", {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Upload failed");
      setMessages((m) => [...m, { from: "bot", text: `Uploaded: ${data.filename}` }]);
      setUploadedFiles((f) => [data.filename, ...f]);
    } catch (err) {
      setMessages((m) => [...m, { from: "bot", text: `Upload error: ${err.message}` }]);
    } finally {
      e.target.value = null;
    }
  };

  const clearAll = async () => {
    const ok = window.confirm("Clear all uploaded files and chat history? This cannot be undone.");
    if (!ok) return;
    try {
      await fetch("http://127.0.0.1:8000/api/clear_session", { method: "POST" });
    } catch (err) {
      // ignore backend errors, still clear UI
    }
    setUploadedFiles([]);
    setMessages([{ from: "bot", text: "Hello — ask me about your documents." }]);
  };

  return (
    <div className="container">
      <header className="header">
        <div>Document RAG — Chat</div>
        <div>
          <button className="clear-btn" onClick={clearAll}>Clear All</button>
        </div>
      </header>
      <main className="layout">
        <aside className="sidebar">
          <div className="uploads">
            <div className="uploads-title">Uploaded Files (session)</div>
            {uploadedFiles.length === 0 ? (
              <div className="uploads-empty">No files uploaded</div>
            ) : (
              <ul className="uploads-list">
                {uploadedFiles.map((f, idx) => (
                  <li key={idx} className="uploads-item">{f}</li>
                ))}
              </ul>
            )}
          </div>
        </aside>

        <section className="chat-column">
          <div className="chat">
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.from}`}>
                <div className="bubble">{m.text}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <form className="composer" onSubmit={send}>
            <input
              placeholder="Type a question about your documents..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <div style={{ display: "flex", gap: "8px" }}>
              <button type="button" onClick={() => fileInputRef.current?.click()}>
                Upload PDF
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf,.pdf"
                style={{ display: "none" }}
                onChange={handleUpload}
              />
              <button type="submit">Send</button>
            </div>
          </form>
        </section>
      </main>
    </div>
  );
}
