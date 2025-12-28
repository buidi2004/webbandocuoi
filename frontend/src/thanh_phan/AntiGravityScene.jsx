import React, { useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Environment, OrbitControls } from '@react-three/drei';

// Single floating object (Sphere / Box / Torus)
function FloatingObject({ id, type = 'sphere', position = [0, 0, 0], baseColor = '#9AD3FF' }) {
  const ref = useRef();
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  // Smoothly interpolate scale & color in the render loop
  useFrame((state, delta) => {
    // Lerp scale
    const targetScale = hovered ? 1.35 : 1;
    ref.current.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.08);

    // Lerp color
    const mat = meshRef.current.material;
    const from = new THREE.Color(mat.color.getHex());
    const to = new THREE.Color(hovered ? '#FFD37A' : baseColor);
    mat.color.lerp(to, 0.06);

    // gentle rotation
    ref.current.rotation.y += 0.2 * delta;
    ref.current.rotation.x += 0.08 * delta;
  });

  const geometry = (() => {
    switch (type) {
      case 'box':
        return <boxBufferGeometry args={[1.2, 1.2, 1.2]} />;
      case 'torus':
        return <torusBufferGeometry args={[0.6, 0.22, 16, 100]} />;
      case 'sphere':
      default:
        return <sphereBufferGeometry args={[0.85, 32, 32]} />;
    }
  })();

  return (
    <Float
      speed={0.8 + Math.random() * 0.8} // vertical speed
      rotationIntensity={0.4 + Math.random() * 0.8} // rotation amplitude
      floatIntensity={0.8 + Math.random() * 0.8} // how high it floats
    >
      <group ref={ref} position={position}>
        <mesh
          ref={meshRef}
          onPointerOver={(e) => { e.stopPropagation(); setHovered(true); }}
          onPointerOut={(e) => { e.stopPropagation(); setHovered(false); }}
          castShadow
          receiveShadow
        >
          {geometry}
          <meshStandardMaterial color={baseColor} metalness={0.2} roughness={0.35} />
        </mesh>
      </group>
    </Float>
  );
}

// The full scene component
export default function AntiGravityScene({ count = 4, style = { height: '70vh', width: '100%' } }) {
  // Pre-generate items with random types/positions/colors
  const items = useMemo(() => {
    const types = ['sphere', 'box', 'torus'];
    const colors = ['#9AD3FF', '#A0E7B8', '#FFD37A', '#F6A6FF', '#FFD6A5'];
    const arr = [];
    for (let i = 0; i < Math.max(3, Math.min(6, count)); i++) {
      arr.push({
        id: i,
        type: types[Math.floor(Math.random() * types.length)],
        position: [ (Math.random() - 0.5) * 6, (Math.random() - 0.2) * 2.6, (Math.random() - 0.5) * 4 ],
        color: colors[Math.floor(Math.random() * colors.length)]
      });
    }
    return arr;
  }, [count]);

  return (
    <div style={{ position: 'relative', ...style }}>
      <Canvas
        shadows
        camera={{ position: [0, 2.5, 8], fov: 50 }}
        style={{ background: 'transparent' }}
      >
        <ambientLight intensity={0.6} />
        <directionalLight position={[5, 8, 5]} intensity={0.8} castShadow />

        {/* Realistic lighting + background */}
        <Environment preset="studio" blur={0.6} />

        {/* Floating Objects */}
        {items.map(item => (
          <FloatingObject key={item.id} id={item.id} type={item.type} position={item.position} baseColor={item.color} />
        ))}

        {/* OrbitControls are optional for dev / exploration */}
        <OrbitControls enablePan={false} autoRotate={false} />

        {/* subtle ground to catch shadow (helps depth) */}
        <mesh rotation-x={-Math.PI / 2} position={[0, -2, 0]} receiveShadow>
          <planeBufferGeometry args={[50, 50]} />
          <meshStandardMaterial color="#fffaf0" metalness={0} roughness={0.9} opacity={0.02} transparent />
        </mesh>
      </Canvas>
    </div>
  );
}

/*
Explanation (key params):
 - <Float speed>        controls vertical oscillation speed (higher => faster bobbing).
 - rotationIntensity    how much child rotates while floating.
 - floatIntensity       amplitude of vertical motion.
 - Environment preset   provides image-based lighting (studio / city / dawn / night).
 - meshStandardMaterial metalness/roughness tune the specular quality.
 - onPointerOver/out    used to detect hover and trigger smooth scale/color lerps in useFrame.
*/