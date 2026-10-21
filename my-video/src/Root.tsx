import { Composition, Folder } from "remotion";
import { MyComposition } from "./Composition";
import { LogoIntro } from "./LogoIntro";
import { ProductIntro } from "./ProductIntro";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <MyComposition />
      <Folder name="Instagram">
        <Composition
          id="YorosumLogoIntro"
          component={LogoIntro}
          durationInFrames={270}
          fps={30}
          width={1080}
          height={1920}
        />
        <Composition
          id="GlowPeptideIntro"
          component={ProductIntro}
          durationInFrames={663}
          fps={30}
          width={1080}
          height={1920}
        />
      </Folder>
    </>
  );
};
