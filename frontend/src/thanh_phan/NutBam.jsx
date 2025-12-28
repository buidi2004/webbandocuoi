import './Button.css';

const NutBam = ({
    children,
    variant = 'primary',
    onClick,
    type = 'button',
    className = '',
    ...props
}) => {
    return (
        <button
            type={type}
            className={`btn btn-${variant} ${className}`}
            onClick={onClick}
            {...props}
        >
            {children}
        </button>
    );
};

export default NutBam;
