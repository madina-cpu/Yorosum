import { Audio } from "@remotion/media";
import {
  AbsoluteFill,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {
  ANTIQUE_GOLD,
  BreathMark,
  clamp,
  DEEP_BERRY,
  ease,
  koreanFont,
  latinFont,
  ROSEWATER,
  voiceFont,
  WARM_GREY,
} from "./brand";

const WORDMARK = "YOROSUM";

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
          fontFamily: latinFont,
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
