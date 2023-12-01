import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { useLoader } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

function Model() {
  const gltf = useLoader(GLTFLoader, './virus-sw.glb');
  return <primitive object={gltf.scene} />;
}

export default function PipistrelSWViewer() {
  return (
    // <Canvas camera={{ position: [0, 0, 5] }}></Canvas>
    <Canvas style={{ background: 'black' }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} />
      <Suspense fallback={null}>
        <Model />
        <OrbitControls />
      </Suspense>
    </Canvas>
  );
}

