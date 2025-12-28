import React from 'react';
import Atropos from 'atropos/react';
import 'atropos/css';

const WrapperAtropos = ({ children, className = "", activeOffset = 40, shadowScale = 1.05 }) => {
    return (
        <div className={`atropos-container ${className}`} style={{ height: '100%', borderRadius: '8px' }}>
            <Atropos
                activeOffset={activeOffset}
                shadowScale={shadowScale}
                className="my-atropos"
                style={{ height: '100%', borderRadius: '8px' }}
                highlight={true}
                rotateTouch={true}
                rotateXMax={25} /* Increased from default */
                rotateYMax={25} /* Increased from default */
                scaleClassName="atropos-scale"
                rotateClassName="atropos-rotate"
                innerClassName="atropos-inner"
            >
                {children}
            </Atropos>
        </div>
    );
};

export default WrapperAtropos;
