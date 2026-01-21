"use client";

import {
  AvatarGroup,
  Card,
  Column,
  Flex,
  Heading,
  Media,
  SmartLink,
  Text,
} from "@once-ui-system/core";
import styles from "./ProjectCard.module.scss";

interface ProjectCardProps {
  href: string;
  priority?: boolean;
  images: string[];
  title: string;
  content: string;
  description: string;
  avatars: { src: string }[];
  link: string;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({
  href,
  priority = false,
  images = [],
  title,
  content,
  description,
  avatars,
  link,
}) => {
  const thumbnailImage = images[0] || "";

  const handleCardClick = (e: React.MouseEvent<HTMLDivElement>) => {
    // Only navigate if clicking on the card itself, not on a link
    const target = e.target as HTMLElement;
    if (!target.closest("a")) {
      window.location.href = href;
    }
  };

  return (
    <Card
      fillWidth
      className={styles.projectCard}
      transition="micro-medium"
      border="neutral-alpha-weak"
      background="surface"
      padding="0"
      radius="l"
      onClick={handleCardClick}
    >
      <Column fillWidth gap="0">
        {thumbnailImage && (
          <div className={styles.imageWrapper}>
            <Media
              priority={priority}
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
              className={styles.image}
              src={thumbnailImage}
              alt={title}
              aspectRatio="1 / 1"
              objectFit="cover"
            />
            <div className={styles.overlay}>
              <Flex gap="12" wrap>
                {content?.trim() && (
                  <SmartLink
                    suffixIcon="arrowRight"
                    style={{ margin: "0", width: "fit-content" }}
                    href={href}
                    onClick={(e: React.MouseEvent) => e.stopPropagation()}
                  >
                    <Text variant="body-default-s" onBackground="neutral-strong">
                      Read case study
                    </Text>
                  </SmartLink>
                )}
                {link && (
                  <SmartLink
                    suffixIcon="arrowUpRightFromSquare"
                    style={{ margin: "0", width: "fit-content" }}
                    href={link}
                    onClick={(e: React.MouseEvent) => e.stopPropagation()}
                  >
                    <Text variant="body-default-s" onBackground="neutral-strong">
                      View project
                    </Text>
                  </SmartLink>
                )}
              </Flex>
            </div>
          </div>
        )}
        <Flex
          fillWidth
          direction="column"
          paddingX="16"
          paddingTop="16"
          paddingBottom="16"
          gap="12"
        >
          {title && (
            <Heading as="h2" wrap="balance" variant="heading-strong-m">
              {title}
            </Heading>
          )}
          {avatars?.length > 0 && <AvatarGroup avatars={avatars} size="s" reverse />}
        </Flex>
      </Column>
    </Card>
  );
};
