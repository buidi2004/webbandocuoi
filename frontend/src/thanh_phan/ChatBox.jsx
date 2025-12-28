import React, { useState, useEffect, useRef } from 'react';
import { chatAPI } from '../api/chat';
import '../styles/auth.css'; // Will add chat styles here

const ChatBox = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [user, setUser] = useState(null);
    const scrollRef = useRef();

    useEffect(() => {
        const savedUser = localStorage.getItem('ivie_user');
        if (savedUser) setUser(JSON.parse(savedUser));

        const checkAuth = () => {
            const u = localStorage.getItem('ivie_user');
            setUser(u ? JSON.parse(u) : null);
        };
        window.addEventListener('authChange', checkAuth);
        return () => window.removeEventListener('authChange', checkAuth);
    }, []);

    useEffect(() => {
        if (isOpen && user) {
            fetchMessages();
            const interval = setInterval(fetchMessages, 5000);
            return () => clearInterval(interval);
        }
    }, [isOpen, user]);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const fetchMessages = async () => {
        const token = localStorage.getItem('ivie_token');
        try {
            const res = await chatAPI.layLichSu(token);
            setMessages(res.data);
        } catch (error) {
            console.error("Lỗi lấy tin nhắn:", error);
        }
    };

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || !user) return;

        const token = localStorage.getItem('ivie_token');
        const msgText = input;
        setInput('');

        try {
            const res = await chatAPI.guiTinNhan({ tin_nhan: msgText }, token);
            setMessages([...messages, res.data]);
        } catch (error) {
            console.error("Lỗi gửi tin nhắn:", error);
        }
    };

    if (!user) return null;

    return (
        <div className={`chat-widget ${isOpen ? 'open' : ''}`}>
            {!isOpen && (
                <button className="chat-toggle" onClick={() => setIsOpen(true)}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                    <span>Hỗ trợ</span>
                </button>
            )}

            {isOpen && (
                <div className="chat-box">
                    <div className="chat-header">
                        <h3>IVIE Support</h3>
                        <button onClick={() => setIsOpen(false)}>×</button>
                    </div>
                    <div className="chat-messages" ref={scrollRef}>
                        {messages.length === 0 ? (
                            <p style={{ textAlign: 'center', color: '#999', marginTop: '20px' }}>Gửi tin nhắn để bắt đầu trò chuyện với chúng tôi!</p>
                        ) : (
                            messages.map((m, idx) => (
                                <div key={idx} className={`message ${m.is_from_admin ? 'admin' : 'user'}`}>
                                    <div className="message-content">{m.tin_nhan}</div>
                                </div>
                            ))
                        )}
                    </div>
                    <form className="chat-input" onSubmit={handleSend}>
                        <input
                            placeholder="Nhập tin nhắn..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                        <button type="submit">Gửi</button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default ChatBox;
