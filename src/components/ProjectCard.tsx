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
import Link from "next/link";
import Image from "next/image";
import styles from "./ProjectCard.module.scss";

interface ProjectCardProps {
  href: string;
  priority?: boolean;
  images: string[];
  title: string;
  description: string;
  link: string;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({
  href,
  priority = false,
  images = [],
  title,
  description,
  link,
}) => {
  // Use only the first image as thumbnail
  const thumbnailImage = images[0] || "/images/placeholder.png";

  return (
    <div className={styles.projectCard}>
      <Link href={href} className={styles.cardLink}>
        <Column fillWidth gap="m" className={styles.cardContent}>
          {/* Square Image Container */}
          <div className={styles.imageContainer}>
            <Image
              src={thumbnailImage}
              alt={title}
              fill
              className={styles.image}
              priority={priority}
              sizes="(max-width: 480px) 100vw, (max-width: 768px) 50vw, 33vw"
            />
          </div>

          {/* Card Text Content */}
          <Flex
            direction="column"
            fillWidth
            paddingTop="m"
            gap="s"
          >
            {title && (
              <Heading as="h3" wrap="balance" variant="heading-strong-l">
                {title}
              </Heading>
            )}
            {description?.trim() && (
              <Text
                wrap="balance"
                variant="body-default-s"
                onBackground="neutral-weak"
                className={styles.description}
              >
                {description}
              </Text>
            )}
          </Flex>
        </Column>
      </Link>
      {/* External link outside of main card link to avoid nested anchors */}
      {link && (
        <Flex gap="s" align="center" className={styles.externalLinkContainer}>
          <SmartLink
            suffixIcon="arrowUpRightFromSquare"
            style={{ margin: "0", width: "fit-content" }}
            href={link}
          >
            <Text variant="body-default-xs">View live</Text>
          </SmartLink>
        </Flex>
      )}
    </div>
  );
};
