import { useMemo } from "react";

// Topographic contour lines: the map texture behind the world trail.

function rng(seed: number) {
  let s = seed >>> 0;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 2 ** 32;
  };
}

function contour(cx: number, cy: number, r: number, wob: number[], squash: number) {
  const pts: string[] = [];
  const N = 64;
  for (let i = 0; i <= N; i++) {
    const a = (i / N) * Math.PI * 2;
    let k = 1;
    wob.forEach((w, j) => (k += w * Math.sin(a * (j + 2) + j * 1.7)));
    const x = cx + Math.cos(a) * r * k;
    const y = cy + Math.sin(a) * r * k * squash;
    pts.push(`${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`);
  }
  return pts.join(" ") + "Z";
}

export function Topo({ seed = 7, peaks = 4, width = 1200, height = 900, className }: {
  seed?: number;
  peaks?: number;
  width?: number;
  height?: number;
  className?: string;
}) {
  const paths = useMemo(() => {
    const r = rng(seed);
    const out: { d: string; o: number }[] = [];
    for (let p = 0; p < peaks; p++) {
      const cx = r() * width;
      const cy = r() * height;
      const wob = [r() * 0.12, r() * 0.08, r() * 0.05];
      const squash = 0.6 + r() * 0.5;
      const rings = 6 + Math.floor(r() * 6);
      for (let k = 1; k <= rings; k++) out.push({ d: contour(cx, cy, k * (28 + r() * 10), wob, squash), o: k % 4 === 0 ? 0.16 : 0.07 });
    }
    return out;
  }, [seed, peaks, width, height]);

  return (
    <svg className={className} viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      {paths.map((p, i) => (
        <path key={i} d={p.d} fill="none" stroke="currentColor" strokeOpacity={p.o} strokeWidth={1} />
      ))}
    </svg>
  );
}
