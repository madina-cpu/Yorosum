import { loadFont } from "@remotion/fonts";
import { Audio } from "@remotion/media";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// Fonts are bundled in public/fonts so the video renders without internet.
// Typefaces follow the Yorosum Brand Design Guide v1.0 ("three voices").
const wordmarkFont = "Schibsted Grotesk";
const koreanFont = "Pretendard";
const voiceFont = "Instrument Serif";
loadFont({
  family: wordmarkFont,
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
const ROSEWATER = "#F0D5DD";
const DEEP_BERRY = "#8E2149";
const ANTIQUE_GOLD = "#B08A62";
const WARM_GREY = "#5A4A50";

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

const WORDMARK = "YOROSUM";

// The Breath Mark: a still centre dot with two open arcs — breath moving outward.
const BreathMark: React.FC = () => {
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
    <svg viewBox="-31 -10 140 120" width={700} height={600} overflow="visible">
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

export const LogoIntro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const lettersStart = 3.0 * fps;
  const letterStagger = 0.07 * fps;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: ROSEWATER,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Audio src={staticFile("audio/yorosum-intro.wav")} />

      {/* Mark starts large in the centre, then settles above the wordmark */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          translate: interpolate(
            frame,
            [2.4 * fps, 3.4 * fps],
            ["0px 0px", "0px -330px"],
            { ...clamp, easing: ease },
          ),
          scale: interpolate(frame, [2.4 * fps, 3.4 * fps], [1.25, 0.75], {
            ...clamp,
            easing: ease,
          }),
        }}
      >
        <BreathMark />
      </div>

      <div
        style={{
          position: "absolute",
          top: 930,
          display: "flex",
          fontFamily: wordmarkFont,
          fontWeight: 800,
          fontSize: 120,
          color: DEEP_BERRY,
          letterSpacing: "0.19em",
          marginRight: "-0.19em",
        }}
      >
        {WORDMARK.split("").map((letter, i) => {
          const start = lettersStart + i * letterStagger;
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                opacity: interpolate(frame, [start, start + 0.5 * fps], [0, 1], clamp),
                translate: interpolate(
                  frame,
                  [start, start + 0.7 * fps],
                  ["0px 60px", "0px 0px"],
                  { ...clamp, easing: ease },
                ),
              }}
            >
              {letter}
            </span>
          );
        })}
      </div>

      <div
        style={{
          position: "absolute",
          top: 1110,
          fontFamily: koreanFont,
          fontSize: 50,
          color: WARM_GREY,
          letterSpacing: "0.8em",
          marginRight: "-0.8em",
          opacity: interpolate(frame, [4.0 * fps, 4.9 * fps], [0, 1], clamp),
          translate: interpolate(
            frame,
            [4.0 * fps, 4.9 * fps],
            ["0px 20px", "0px 0px"],
            { ...clamp, easing: ease },
          ),
        }}
      >
        여러숨
      </div>

      {/* Antique Gold hairline rule */}
      <div
        style={{
          position: "absolute",
          top: 1250,
          height: 2,
          backgroundColor: ANTIQUE_GOLD,
          width: interpolate(frame, [4.8 * fps, 5.6 * fps], [0, 260], {
            ...clamp,
            easing: ease,
          }),
        }}
      />

      <div
        style={{
          position: "absolute",
          top: 1300,
          fontFamily: voiceFont,
          fontStyle: "italic",
          fontSize: 64,
          color: DEEP_BERRY,
          opacity: interpolate(frame, [5.6 * fps, 6.6 * fps], [0, 1], clamp),
          translate: interpolate(
            frame,
            [5.6 * fps, 6.6 * fps],
            ["0px 16px", "0px 0px"],
            { ...clamp, easing: ease },
          ),
        }}
      >
        “A small breath for yourself, every day.”
      </div>
    </AbsoluteFill>
  );
};
