import { Audio } from "@remotion/media";
import { linearTiming, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import {
  AbsoluteFill,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {
  ANTIQUE_GOLD,
  BONE,
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

// Every line of copy states what is IN the product, never what it does
// (general food, 식품표시광고법 제8조). Figures come from the carton.

const fadeIn = (frame: number, start: number, length: number) => ({
  opacity: interpolate(frame, [start, start + length], [0, 1], clamp),
  translate: interpolate(
    frame,
    [start, start + length],
    ["0px 24px", "0px 0px"],
    { ...clamp, easing: ease },
  ),
});

const Kicker: React.FC<{ readonly children: React.ReactNode }> = ({
  children,
}) => (
  <div
    style={{
      fontFamily: latinFont,
      fontWeight: 600,
      fontSize: 34,
      letterSpacing: "0.22em",
      color: DEEP_BERRY,
    }}
  >
    {children}
  </div>
);

const Opening: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        backgroundColor: ROSEWATER,
        justifyContent: "center",
        alignItems: "center",
        gap: 40,
      }}
    >
      <BreathMark width={520} />
      <div style={{ textAlign: "center", ...fadeIn(frame, 1.3 * fps, 0.6 * fps) }}>
        <Kicker>OUR FIRST LINE</Kicker>
        <div
          style={{
            fontFamily: koreanFont,
            fontSize: 40,
            color: WARM_GREY,
            marginTop: 18,
          }}
        >
          여러숨의 첫 번째 라인
        </div>
      </div>
    </AbsoluteFill>
  );
};

// A product photo on top (slow push-in) with the copy on a Rosewater field below:
// promise above, proof below, as on the pack.
const PhotoScene: React.FC<{
  readonly src: string;
  readonly objectPosition: string;
  readonly kicker: string;
  readonly title: string;
  readonly korean: string;
  readonly detail?: string;
}> = ({ src, objectPosition, kicker, title, korean, detail }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: ROSEWATER }}>
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 1300,
          overflow: "hidden",
        }}
      >
        <Img
          src={src}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition,
            scale: interpolate(frame, [0, durationInFrames], [1.0, 1.08]),
          }}
        />
      </div>
      <div
        style={{
          position: "absolute",
          top: 1300,
          left: 0,
          right: 0,
          bottom: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          padding: "0 80px",
        }}
      >
        <div
          style={{
            height: 2,
            backgroundColor: ANTIQUE_GOLD,
            marginBottom: 36,
            width: interpolate(frame, [0.2 * fps, 0.9 * fps], [0, 160], {
              ...clamp,
              easing: ease,
            }),
          }}
        />
        <div style={fadeIn(frame, 0.3 * fps, 0.5 * fps)}>
          <Kicker>{kicker}</Kicker>
        </div>
        <div
          style={{
            fontFamily: latinFont,
            fontWeight: 800,
            fontSize: 84,
            letterSpacing: "0.03em",
            color: DEEP_BERRY,
            marginTop: 14,
            ...fadeIn(frame, 0.45 * fps, 0.5 * fps),
          }}
        >
          {title}
        </div>
        <div
          style={{
            fontFamily: koreanFont,
            fontSize: 42,
            color: WARM_GREY,
            marginTop: 12,
            ...fadeIn(frame, 0.6 * fps, 0.5 * fps),
          }}
        >
          {korean}
        </div>
        {detail ? (
          <div
            style={{
              fontFamily: latinFont,
              fontWeight: 400,
              fontSize: 34,
              color: WARM_GREY,
              marginTop: 10,
              ...fadeIn(frame, 0.75 * fps, 0.5 * fps),
            }}
          >
            {detail}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

const Figure: React.FC<{
  readonly value: number;
  readonly unit: string;
  readonly label: string;
  readonly korean: string;
  readonly start: number;
}> = ({ value, unit, label, korean, start }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const shown = Math.round(
    interpolate(frame, [start, start + 0.9 * fps], [0, value], {
      ...clamp,
      easing: ease,
    }),
  );
  return (
    <div style={{ textAlign: "center", ...fadeIn(frame, start, 0.4 * fps) }}>
      <div
        style={{
          fontFamily: latinFont,
          fontWeight: 800,
          color: DEEP_BERRY,
          lineHeight: 1,
        }}
      >
        <span style={{ fontSize: 180 }}>{shown.toLocaleString("en-US")}</span>
        <span style={{ fontSize: 64, marginLeft: 8 }}>{unit}</span>
      </div>
      <div
        style={{
          fontFamily: latinFont,
          fontWeight: 600,
          fontSize: 30,
          letterSpacing: "0.2em",
          color: DEEP_BERRY,
          marginTop: 14,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontFamily: koreanFont,
          fontSize: 34,
          color: WARM_GREY,
          marginTop: 6,
        }}
      >
        {korean}
      </div>
    </div>
  );
};

const Proof: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        backgroundColor: BONE,
        justifyContent: "center",
        alignItems: "center",
        gap: 70,
      }}
    >
      <div style={{ textAlign: "center", ...fadeIn(frame, 0, 0.4 * fps) }}>
        <Kicker>PER STICK</Kicker>
        <div
          style={{
            fontFamily: koreanFont,
            fontSize: 36,
            color: WARM_GREY,
            marginTop: 10,
          }}
        >
          1포당
        </div>
      </div>
      <Figure
        value={2000}
        unit="mg"
        label="FISH COLLAGEN"
        korean="생선콜라겐"
        start={0.3 * fps}
      />
      <Figure
        value={300}
        unit="Da"
        label="AVERAGE MOLECULAR WEIGHT"
        korean="저분자 생선콜라겐의 평균분자량"
        start={0.9 * fps}
      />
      <Figure
        value={100}
        unit="mg"
        label="VITAMIN C"
        korean="비타민 C"
        start={1.5 * fps}
      />
      {/* One Antique Gold hairline under the dosage figures */}
      <div
        style={{
          height: 2,
          backgroundColor: ANTIQUE_GOLD,
          width: interpolate(frame, [2.2 * fps, 3.0 * fps], [0, 560], {
            ...clamp,
            easing: ease,
          }),
        }}
      />
    </AbsoluteFill>
  );
};

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        backgroundColor: ROSEWATER,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <BreathMark width={360} />
      <div
        style={{
          fontFamily: latinFont,
          fontWeight: 800,
          fontSize: 120,
          letterSpacing: "0.19em",
          marginRight: "-0.19em",
          color: DEEP_BERRY,
          marginTop: 30,
          ...fadeIn(frame, 0.6 * fps, 0.6 * fps),
        }}
      >
        YOROSUM
      </div>
      <div
        style={{
          fontFamily: latinFont,
          fontWeight: 600,
          fontSize: 40,
          letterSpacing: "0.3em",
          marginRight: "-0.3em",
          color: DEEP_BERRY,
          marginTop: 20,
          ...fadeIn(frame, 1.0 * fps, 0.6 * fps),
        }}
      >
        GLOW PEPTIDE
      </div>
      <div
        style={{
          fontFamily: koreanFont,
          fontSize: 38,
          color: WARM_GREY,
          marginTop: 12,
          ...fadeIn(frame, 1.2 * fps, 0.6 * fps),
        }}
      >
        여러숨 글로우 펩타이드
      </div>
      <div
        style={{
          height: 2,
          backgroundColor: ANTIQUE_GOLD,
          marginTop: 56,
          width: interpolate(frame, [1.5 * fps, 2.2 * fps], [0, 260], {
            ...clamp,
            easing: ease,
          }),
        }}
      />
      <div
        style={{
          fontFamily: voiceFont,
          fontStyle: "italic",
          fontSize: 64,
          color: DEEP_BERRY,
          marginTop: 40,
          ...fadeIn(frame, 1.8 * fps, 0.8 * fps),
        }}
      >
        “A small breath for yourself, every day.”
      </div>
    </AbsoluteFill>
  );
};

export const ProductIntro: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Audio src={staticFile("audio/glow-peptide-intro.wav")} />
      <TransitionSeries>
        <TransitionSeries.Sequence name="Opening" durationInFrames={3 * fps}>
          <Opening />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 0.4 * fps })}
        />
        <TransitionSeries.Sequence name="Hero" durationInFrames={3.5 * fps}>
          <PhotoScene
            src={staticFile("photos/carton-hero.jpg")}
            objectPosition="45% 50%"
            kicker="INTRODUCING"
            title="GLOW PEPTIDE"
            korean="여러숨 글로우 펩타이드"
            detail="Low molecular fish collagen daily stick"
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 0.4 * fps })}
        />
        <TransitionSeries.Sequence name="Per stick" durationInFrames={4.5 * fps}>
          <Proof />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 0.4 * fps })}
        />
        <TransitionSeries.Sequence name="In the box" durationInFrames={3 * fps}>
          <PhotoScene
            src={staticFile("photos/box-open.jpg")}
            objectPosition="70% 75%"
            kicker="IN THE BOX"
            title="30 STICKS"
            korean="3 g × 30포"
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 0.4 * fps })}
        />
        <TransitionSeries.Sequence name="Flavour" durationInFrames={3 * fps}>
          <PhotoScene
            src={staticFile("photos/stick-powder.jpg")}
            objectPosition="50% 80%"
            kicker="FLAVOUR"
            title="PEACH"
            korean="복숭아맛"
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 0.4 * fps })}
        />
        <TransitionSeries.Sequence name="How to enjoy" durationInFrames={3.5 * fps}>
          <PhotoScene
            src={staticFile("photos/pour-water.jpg")}
            objectPosition="40% 55%"
            kicker="HOW TO ENJOY"
            title="ONE STICK A DAY"
            korean="하루 한 포, 물과 함께"
            detail="with water"
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 0.4 * fps })}
        />
        <TransitionSeries.Sequence name="End card" durationInFrames={4 * fps}>
          <EndCard />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </>
  );
};
