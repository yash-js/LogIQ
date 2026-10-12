import type { ReactElement } from "react";
// Line-drawn emblems for the six worlds. Drawn on a 48×48 grid with currentColor.

const glyphs: Record<number, ReactElement> = {
  // The Crossroads: a signpost pointing two ways.
  1: (
    <>
      <path d="M24 6v36M14 42h20" />
      <path d="M24 11h13l4 4-4 4H24z" />
      <path d="M24 22H11l-4 4 4 4h13z" />
    </>
  ),
  // The Looping Woods: two pines inside a loop arrow.
  2: (
    <>
      <path d="M17 34l-6 0 6-9h-4l6-9 6 9h-4l6 9h-6v5h-4z" />
      <path d="M31 30l-3 0 4-7h-3l4-7 4 7h-3l4 7h-3v4h-4z" />
      <path d="M41 24a17 17 0 1 1-6-13" />
      <path d="M36 5l-1 6 6 1" />
    </>
  ),
  // The Mirror Caves: arches inside arches.
  3: (
    <>
      <path d="M5 42V26a19 19 0 0 1 38 0v16" />
      <path d="M12 42V28a12 12 0 0 1 24 0v14" />
      <path d="M19 42V31a5 5 0 0 1 10 0v11" />
      <path d="M3 42h42" />
    </>
  ),
  // The Iron Rails: track with sleepers, like array cells.
  4: (
    <>
      <path d="M14 4L6 44M34 4l8 40" />
      <path d="M12 12h24M10.5 21h27M9 30h30M7.5 39h33" />
    </>
  ),
  // The Scroll Library: an open scroll with text lines.
  5: (
    <>
      <path d="M12 8h26a4 4 0 0 1 0 8H12" />
      <path d="M12 8a4 4 0 0 0 0 8v20a4 4 0 0 0 4 4h22a4 4 0 0 0 0-8H16" />
      <path d="M19 22h14M19 28h10" />
    </>
  ),
  // The Summit: mountain with a flag.
  6: (
    <>
      <path d="M3 42l15-24 7 10 5-7 15 21z" />
      <path d="M13 26l5 3 3-3 4 2" />
      <path d="M30 21V6l9 4-9 4" />
    </>
  ),
};

export function WorldGlyph({ id, size = 48, className }: { id: number; size?: number; className?: string }) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 48 48"
      fill="none"
      stroke="currentColor"
      strokeWidth={2.2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {glyphs[id]}
    </svg>
  );
}
