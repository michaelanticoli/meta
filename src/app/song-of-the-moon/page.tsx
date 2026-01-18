import { Column, Flex, Heading, Text } from "@once-ui-system/core";
import { SongOfTheMoon } from "@/components/SongOfTheMoon";
import { Meta } from "@once-ui-system/core";
import { baseURL, person } from "@/resources";

export async function generateMetadata() {
  const title = `Song of the Moon – ${person.name}`;
  const description =
    "An immersive sonic journey through lunar frequencies. Experience the Moon's resonance through interactive audio visualization.";

  return Meta.generate({
    title,
    description,
    baseURL: baseURL,
    path: "/song-of-the-moon",
    image: `/api/og/generate?title=${encodeURIComponent(title)}`,
  });
}

export default function SongOfTheMoonPage() {
  return (
    <Flex fillWidth paddingY="l" direction="column" horizontal="center">
      <Column fillWidth maxWidth="l" gap="32">
        {/* Page Header */}
        <Column fillWidth gap="16" horizontal="center" paddingY="24">
          <Heading variant="display-strong-xl" align="center">
            Song of the Moon
          </Heading>
          <Column fillWidth maxWidth={600} horizontal="center">
            <Text variant="body-default-l" align="center" onBackground="neutral-medium">
              An interactive sonic meditation tuned to the frequency of the Moon. Let the
              vibrations of lunar cycles guide you through an immersive audio-visual experience.
            </Text>
          </Column>
        </Column>

        {/* Song of the Moon Component */}
        <SongOfTheMoon showVisualization={true} />

        {/* Additional Context */}
        <Column fillWidth gap="24" paddingY="32">
          <Column fillWidth gap="12">
            <Heading variant="heading-strong-l">The Science & Philosophy</Heading>
            <Text variant="body-default-m" onBackground="neutral-weak">
              The Song of the Moon is tuned to 210.42 Hz, a frequency derived from the Moon's
              orbital period around Earth (27.3 days). This frequency, often called the "OM"
              frequency in sound healing traditions, is believed to resonate with lunar cycles and
              natural rhythms.
            </Text>
            <Text variant="body-default-m" onBackground="neutral-weak">
              By translating celestial mechanics into sound, we create a bridge between the cosmic
              and the personal—a sonic reminder that we are always moving in rhythm with forces far
              greater than ourselves.
            </Text>
          </Column>

          <Column fillWidth gap="12">
            <Heading variant="heading-strong-l">How to Experience</Heading>
            <Text variant="body-default-m" onBackground="neutral-weak">
              Find a comfortable space where you can focus without distraction. Press play, adjust
              the volume to a level that feels resonant, and allow the evolving soundscape to guide
              your awareness.
            </Text>
            <Text variant="body-default-m" onBackground="neutral-weak">
              The visualization shows the waveforms and frequencies in real-time—watch how the
              patterns shift and flow, mirroring the ever-changing phases of the Moon itself.
            </Text>
            <Text variant="body-default-m" onBackground="neutral-weak">
              This is not background music. This is a sonic meditation—an invitation to slow down,
              breathe deeply, and attune to the rhythms that connect us all.
            </Text>
          </Column>

          <Column fillWidth gap="12">
            <Heading variant="heading-strong-l">Technical Details</Heading>
            <Column as="ul" gap="8" paddingLeft="20">
              <Text as="li" variant="body-default-m" onBackground="neutral-weak">
                <strong>Base Frequency:</strong> 210.42 Hz (Moon's orbital frequency)
              </Text>
              <Text as="li" variant="body-default-m" onBackground="neutral-weak">
                <strong>Harmonics:</strong> Includes overtones at 2x, 3x, 4x, 5x, and 8x base
                frequency
              </Text>
              <Text as="li" variant="body-default-m" onBackground="neutral-weak">
                <strong>Technology:</strong> Generated in real-time using Web Audio API
              </Text>
              <Text as="li" variant="body-default-m" onBackground="neutral-weak">
                <strong>Visualization:</strong> Real-time waveform and frequency analysis
              </Text>
              <Text as="li" variant="body-default-m" onBackground="neutral-weak">
                <strong>Waveforms:</strong> Combination of sine, triangle, and sawtooth waves for
                rich harmonic content
              </Text>
            </Column>
          </Column>

          <Column fillWidth gap="12">
            <Heading variant="heading-strong-l">About the Creator</Heading>
            <Text variant="body-default-m" onBackground="neutral-weak">
              {person.name} is a sonic innovator and systems thinker who explores the intersection
              of data, sound, and storytelling. Through projects like MoonTuner and Quantumelodics,
              Michael translates complex patterns into immersive sonic experiences that resonate on
              both intellectual and emotional levels.
            </Text>
            <Text variant="body-default-m" onBackground="neutral-weak">
              The Song of the Moon is part of a broader exploration into how celestial mechanics,
              natural cycles, and human creativity can harmonize through sound.
            </Text>
          </Column>
        </Column>
      </Column>
    </Flex>
  );
}
