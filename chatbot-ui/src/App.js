import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

function App() {
    const [message, setMessage] = useState("");
    const [chat, setChat] = useState([]);
    const [loading, setLoading] = useState(false);
    const chatContainerRef = useRef(null);

    const sendMessage = async () => {
        if (!message.trim()) return;

        const userMessage = { sender: "You", text: message };
        setChat((prevChat) => [...prevChat, userMessage]);
        setMessage("");
        setLoading(true);

        try {
            const response = await axios.post("http://127.0.0.1:8000/chatbot/chat", {
                user_id: 1,
                message: message
            });

            const botMessage = { sender: "Bot", text: response.data.reply };
            setChat((prevChat) => [...prevChat, botMessage]);
        } catch (error) {
            console.error("Error:", error);
            setChat((prevChat) => [...prevChat, { sender: "Bot", text: "Oops! Something went wrong." }]);
        }

        setLoading(false);
    };

    // Auto-scroll to the latest message
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [chat]);

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-purple-500 to-indigo-600">
            <div className="w-full max-w-md bg-white shadow-lg rounded-lg p-4">
                <h2 className="text-2xl font-bold text-center text-gray-800">🤖 AI Chatbot</h2>

                {/* Chat Box */}
                <div className="border rounded-lg p-3 h-80 overflow-y-auto bg-gray-50" ref={chatContainerRef}>
                    {chat.map((msg, index) => (
                        <div 
                            key={index} 
                            className={`p-2 rounded-md mb-2 max-w-[80%] ${
                                msg.sender === "You" 
                                    ? "bg-blue-500 text-white self-end ml-auto" 
                                    : "bg-green-500 text-white self-start"
                            }`}
                        >
                            <strong>{msg.sender}:</strong> {msg.text}
                        </div>
                    ))}
                    {loading && <p className="text-center text-gray-500">Bot is typing...</p>}
                </div>

                {/* Input Field & Send Button */}
                <div className="flex mt-3">
                    <input
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Type a message..."
                        className="flex-grow p-2 border rounded-l-md focus:outline-none"
                    />
                    <button
                        onClick={sendMessage}
                        className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600 transition"
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;