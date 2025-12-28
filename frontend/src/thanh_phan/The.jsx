import React from 'react';

const The = ({ children, className = '', hover = true }) => {
    return (
        <div className={`card ${hover ? 'hover:shadow-lg' : ''} ${className}`} style={{
            backgroundColor: 'var(--light)',
            borderRadius: '8px',
            overflow: 'hidden',
            border: '1px solid var(--border)'
        }}>
            {children}
        </div>
    );
};

export default The;
