import React, {useEffect, useRef} from 'react';

interface Orb {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  baseColor: {r: number; g: number; b: number};
  pulse: number;
  pulseSpeed: number;
}

const NeuralNetwork: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const orbsRef = useRef<Orb[]>([]);
  const animationRef = useRef<number>();

  // Black and dark blue color scheme
  const colors = [
    {r: 10, g: 10, b: 20},     // almost black
    {r: 20, g: 30, b: 60},     // very dark blue
    {r: 30, g: 58, b: 138},    // dark blue
    {r: 59, g: 130, b: 246},   // bright blue
    {r: 15, g: 23, b: 42},     // dark navy
    {r: 45, g: 80, b: 150},    // medium blue
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const resizeCanvas = () => {
      const parent = canvas.parentElement;
      if (parent) {
        canvas.width = parent.clientWidth;
        canvas.height = parent.clientHeight;
      }
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Create glowing orbs
    const createOrbs = () => {
      const orbs: Orb[] = [];
      const orbCount = Math.floor((canvas.width * canvas.height) / 12000);

      for (let i = 0; i < orbCount; i++) {
        const color = colors[Math.floor(Math.random() * colors.length)];
        orbs.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 2,
          vy: (Math.random() - 0.5) * 2,
          radius: Math.random() * 10 + 10,
          baseColor: color,
          pulse: Math.random() * Math.PI * 2,
          pulseSpeed: 0.02 + Math.random() * 0.02,
        });
      }
      orbsRef.current = orbs;
    };

    createOrbs();

    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const orbs = orbsRef.current;

      // Update and draw orbs
      orbs.forEach((orb, i) => {
        // Update position
        orb.x += orb.vx;
        orb.y += orb.vy;
        orb.pulse += orb.pulseSpeed;

        // Wrap around edges
        if (orb.x < -30) orb.x = canvas.width + 30;
        if (orb.x > canvas.width + 30) orb.x = -30;
        if (orb.y < -30) orb.y = canvas.height + 30;
        if (orb.y > canvas.height + 30) orb.y = -30;

        // Draw connections (neural synapses)
        for (let j = i + 1; j < orbs.length; j++) {
          const other = orbs[j];
          const dx = orb.x - other.x;
          const dy = orb.y - other.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 200) {
            const opacity = (1 - distance / 200) * 0.3;
            ctx.beginPath();
            ctx.moveTo(orb.x, orb.y);
            ctx.lineTo(other.x, other.y);
            ctx.strokeStyle = `rgba(59, 130, 246, ${opacity})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      });

      // Draw orbs with minimal glow
      orbs.forEach((orb) => {
        const pulseSize = orb.radius + Math.sin(orb.pulse) * 2;
        const glowIntensity = 0.4 + Math.sin(orb.pulse) * 0.15;
        const {r, g, b} = orb.baseColor;

        // Subtle outer glow (reduced)
        const outerGlow = ctx.createRadialGradient(
          orb.x,
          orb.y,
          0,
          orb.x,
          orb.y,
          pulseSize * 1.5
        );
        outerGlow.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${glowIntensity * 0.3})`);
        outerGlow.addColorStop(1, 'transparent');

        ctx.beginPath();
        ctx.arc(orb.x, orb.y, pulseSize * 1.5, 0, Math.PI * 2);
        ctx.fillStyle = outerGlow;
        ctx.fill();

        // Main orb body
        const coreGradient = ctx.createRadialGradient(
          orb.x - pulseSize * 0.3,
          orb.y - pulseSize * 0.3,
          0,
          orb.x,
          orb.y,
          pulseSize
        );
        coreGradient.addColorStop(0, `rgb(${Math.min(255, r + 80)}, ${Math.min(255, g + 80)}, ${Math.min(255, b + 80)})`);
        coreGradient.addColorStop(0.5, `rgb(${r}, ${g}, ${b})`);
        coreGradient.addColorStop(1, `rgb(${Math.max(0, r - 20)}, ${Math.max(0, g - 20)}, ${Math.max(0, b - 20)})`);

        ctx.beginPath();
        ctx.arc(orb.x, orb.y, pulseSize, 0, Math.PI * 2);
        ctx.fillStyle = coreGradient;
        ctx.fill();

        // Small highlight
        ctx.beginPath();
        ctx.arc(orb.x - pulseSize * 0.3, orb.y - pulseSize * 0.3, pulseSize * 0.25, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${0.4 + Math.sin(orb.pulse) * 0.1})`;
        ctx.fill();
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 0,
        pointerEvents: 'none',
      }}
    />
  );
};

export default NeuralNetwork;
