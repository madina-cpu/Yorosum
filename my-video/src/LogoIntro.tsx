import { loadFont } from "@remotion/fonts";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// Fonts are bundled in public/fonts so the video renders without internet.
const wordmarkFont = "Schibsted Grotesk";
const koreanFont = "Noto Sans KR";
loadFont({
  family: wordmarkFont,
  url: staticFile("fonts/SchibstedGrotesk-ExtraBold.woff2"),
  weight: "800",
});
loadFont({
  family: koreanFont,
  url: staticFile("fonts/NotoSansKR-Regular-subset.woff2"),
  weight: "400",
});

const BURGUNDY = "#8E2149";
const GOLD = "#B08A62";
const CREAM = "#F7F1EA";

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

const WORDMARK = "YOROSUM";

// Logo symbol: a dot with two arcs radiating from it, as in Yorosum_Logo.svg.
const Symbol: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const dotScale = interpolate(frame, [0, 0.6 * fps], [0, 1], {
    ...clamp,
    easing: Easing.spring({ damping: 12 }),
  });
  const arc1 = interpolate(frame, [0.4 * fps, 1.2 * fps], [1, 0], {
    ...clamp,
    easing: ease,
  });
  const arc2 = interpolate(frame, [0.75 * fps, 1.6 * fps], [1, 0], {
    ...clamp,
    easing: ease,
  });
  // Gentle "breathing" of the arcs once they are drawn.
  const breath =
    1 + 0.04 * Math.sin(((frame - 1.6 * fps) / fps) * Math.PI * 0.9) *
      interpolate(frame, [1.6 * fps, 2.2 * fps], [0, 1], clamp);

  return (
    <svg viewBox="-31 -10 140 120" width={700} height={600} overflow="visible">
      {[0, 1, 2].map((i) => {
        const start = (1.3 + i * 0.45) * fps;
        const progress = interpolate(frame, [start, start + 1.6 * fps], [0, 1], {
          ...clamp,
          easing: Easing.out(Easing.quad),
        });
        return (
          <circle
            key={i}
            cx={14}
            cy={50}
            r={9 + progress * 70}
            fill="none"
            stroke={i === 1 ? GOLD : BURGUNDY}
            strokeWidth={1.2}
            opacity={progress > 0 ? 0.35 * (1 - progress) : 0}
          />
        );
      })}
      <circle
        cx={14}
        cy={50}
        r={9}
        fill={BURGUNDY}
        style={{ scale: dotScale, transformOrigin: "14px 50px" }}
      />
      <g style={{ scale: breath, transformOrigin: "14px 50px" }}>
        <path
          d="M36 30 A27 27 0 0 1 36 70"
          stroke={BURGUNDY}
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
          stroke={GOLD}
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
        backgroundColor: CREAM,
        backgroundImage:
          "radial-gradient(circle at 50% 45%, #FFFFFF 0%, rgba(255,255,255,0) 60%)",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Symbol starts large in the centre, then settles above the wordmark */}
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
            ["0px 0px", "0px -260px"],
            { ...clamp, easing: ease },
          ),
          scale: interpolate(frame, [2.4 * fps, 3.4 * fps], [1.25, 0.75], {
            ...clamp,
            easing: ease,
          }),
        }}
      >
        <Symbol />
      </div>

      <div
        style={{
          position: "absolute",
          top: 1010,
          display: "flex",
          fontFamily: wordmarkFont,
          fontWeight: 800,
          fontSize: 120,
          color: BURGUNDY,
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
          top: 1230,
          height: 3,
          backgroundColor: GOLD,
          width: interpolate(frame, [4.0 * fps, 4.8 * fps], [0, 220], {
            ...clamp,
            easing: ease,
          }),
        }}
      />

      <div
        style={{
          position: "absolute",
          top: 1275,
          fontFamily: koreanFont,
          fontSize: 58,
          color: BURGUNDY,
          letterSpacing: "0.8em",
          marginRight: "-0.8em",
          opacity: interpolate(frame, [4.4 * fps, 5.3 * fps], [0, 0.75], clamp),
          translate: interpolate(
            frame,
            [4.4 * fps, 5.3 * fps],
            ["0px 20px", "0px 0px"],
            { ...clamp, easing: ease },
          ),
        }}
      >
        여러숨
      </div>
    </AbsoluteFill>
  );
};
