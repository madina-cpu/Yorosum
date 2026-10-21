import { loadFont } from "@remotion/fonts";
import {
  Easing,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// Fonts are bundled in public/fonts so videos render without internet.
// Typefaces follow the Yorosum Brand Design Guide v1.0 ("three voices").
export const latinFont = "Schibsted Grotesk";
export const koreanFont = "Pretendard";
export const voiceFont = "Instrument Serif";
loadFont({
  family: latinFont,
  url: staticFile("fonts/SchibstedGrotesk-Regular.woff2"),
  weight: "400",
});
loadFont({
  family: latinFont,
  url: staticFile("fonts/SchibstedGrotesk-SemiBold.woff2"),
  weight: "600",
});
loadFont({
  family: latinFont,
  url: staticFile("fonts/SchibstedGrotesk-ExtraBold.woff2"),
  weight: "800",
});
loadFont({
  family: koreanFont,
  url: staticFile("fonts/Pretendard-Regular.woff2"),
  weight: "400",
});
loadFont({
  family: voiceFont,
  url: staticFile("fonts/InstrumentSerif-Italic.woff2"),
  style: "italic",
  weight: "400",
});

// Brand colours. Rosewater is the resting field; gold is only ever a line.
export const ROSEWATER = "#F0D5DD";
export const DEEP_BERRY = "#8E2149";
export const ANTIQUE_GOLD = "#B08A62";
export const BONE = "#FBF8F3";
export const WARM_GREY = "#5A4A50";

export const ease = Easing.bezier(0.16, 1, 0.3, 1);
export const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

// The Breath Mark: a still centre dot with two open arcs — breath moving outward.
// Draws itself from the start of its sequence.
export const BreathMark: React.FC<{ readonly width?: number }> = ({
  width = 700,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const dotScale = interpolate(frame, [0, 0.6 * fps], [0, 1], {
    ...clamp,
    easing: Easing.spring({ damping: 12 }),
  });
  const arc1 = interpolate(frame, [0.5 * fps, 1.3 * fps], [1, 0], {
    ...clamp,
    easing: ease,
  });
  const arc2 = interpolate(frame, [0.9 * fps, 1.8 * fps], [1, 0], {
    ...clamp,
    easing: ease,
  });
  // The arcs breathe gently once drawn; the dot stays still.
  const breath =
    1 +
    0.035 *
      Math.sin(((frame - 1.8 * fps) / fps) * Math.PI * 0.8) *
      interpolate(frame, [1.8 * fps, 2.4 * fps], [0, 1], clamp);

  return (
    <svg
      viewBox="-31 -10 140 120"
      width={width}
      height={(width * 120) / 140}
      overflow="visible"
    >
      <circle
        cx={14}
        cy={50}
        r={9}
        fill={DEEP_BERRY}
        style={{ scale: dotScale, transformOrigin: "14px 50px" }}
      />
      <g style={{ scale: breath, transformOrigin: "14px 50px" }}>
        <path
          d="M36 30 A27 27 0 0 1 36 70"
          stroke={DEEP_BERRY}
          strokeWidth={7}
          fill="none"
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={arc1}
          opacity={arc1 < 1 ? 1 : 0}
        />
        <path
          d="M54 22 A38 38 0 0 1 54 78"
          stroke={ANTIQUE_GOLD}
          strokeWidth={7}
          fill="none"
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={arc2}
          opacity={arc2 < 1 ? 1 : 0}
        />
      </g>
    </svg>
  );
};
