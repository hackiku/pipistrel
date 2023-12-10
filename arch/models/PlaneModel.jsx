// AirplaneModel.jsx
// assimp

import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';

const PipistrelVirusComponent = ({ data }) => {
  const mountRef = useRef(null);

  useEffect(() => {
    // Set up scene, camera, and renderer
    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();

    renderer.setSize(width, height);
    mountRef.current.appendChild(renderer.domElement);

    // Add lighting
    const ambientLight = new THREE.AmbientLight(0x404040);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    scene.add(ambientLight);
    scene.add(directionalLight);

    // Load the 3D model using Three.js loaders, for example GLTFLoader
    const loader = new THREE.GLTFLoader();
    // The path to your 3D model file
    const modelPath = '/path/to/your/model.gltf';

    loader.load(modelPath, (gltf) => {
      scene.add(gltf.scene);
    }, undefined, (error) => {
      console.error(error);
    });

    // Set up controls (e.g., OrbitControls)
    const controls = new THREE.OrbitControls(camera, renderer.domElement);

    // Position the camera and set the initial camera angle
    camera.position.set(0, 5, 10);
    controls.update();

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      // Update any dynamic elements of the scene
      controls.update();
      renderer.render(scene, camera);
    };

    // Start the animation loop
    animate();

    // Clean up on unmount
    return () => {
      mountRef.current.removeChild(renderer.domElement);
      scene.remove(gltf.scene);
      // Dispose of other resources (geometries, materials, textures)
    };
  }, [data]); // Re-run the effect if 'data' changes

  return <div ref={mountRef} style={{ width: '100%', height: '100%' }} />;
};

export default PipistrelVirusComponent;
