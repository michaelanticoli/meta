# GitHub Copilot Instructions for Magic Portfolio

This repository is a portfolio website built with Next.js, TypeScript, and the Once UI design system. It features MDX-based content for blog posts and project showcases.

## Project Overview

- **Framework**: Next.js 16.0.10 with App Router
- **Language**: TypeScript (strict mode enabled)
- **React Version**: 19.2.0
- **Design System**: Once UI (@once-ui-system/core)
- **Styling**: SASS with CSS modules
- **Content**: MDX for blog posts and project pages

## Development Workflow

### Available Scripts

```bash
npm run dev        # Start development server (default port 3000)
npm run build      # Build for production
npm start          # Start production server
npm run lint       # Run ESLint
npm run biome-write # Format code with Biome
npm run sync-images # Sync project images
```

### Before Making Changes

1. Always run `npm run dev` to test changes locally
2. Run `npm run lint` to check for linting errors
3. Run `npm run biome-write` to format code before committing

## Code Style Guidelines

### Formatting

- **Formatter**: Biome (primary) with ESLint for additional checks
- **Indentation**: 2 spaces
- **Line Width**: 100 characters
- **Quote Style**: Double quotes for JavaScript/TypeScript
- **TypeScript**: Strict mode enabled

### Naming Conventions

- **Components**: PascalCase (e.g., `ProjectCard.tsx`, `GalleryView.tsx`)
- **Utilities**: camelCase (e.g., `formatDate.ts`, `utils.ts`)
- **Files**: Use descriptive names matching the main export

### Import Paths

- Use `@/` alias for imports from `src/` directory
- Example: `import { Person } from "@/types"`

## Project Structure

```
src/
├── app/              # Next.js App Router pages
│   ├── blog/         # Blog posts (MDX in posts/)
│   ├── work/         # Project showcase (MDX in projects/)
│   ├── gallery/      # Image gallery
│   ├── about/        # About/CV page
│   └── api/          # API routes
├── components/       # React components
├── resources/        # Configuration and content
│   ├── content.tsx   # Main content configuration
│   ├── once-ui.config.ts  # Design system config
│   └── icons.ts      # Icon definitions
├── types/            # TypeScript type definitions
└── utils/            # Utility functions
```

## Content Management

### Configuration Files

- **`src/resources/content.tsx`**: Main content configuration (person info, social links, sections)
- **`src/resources/once-ui.config.ts`**: Design system theming and tokens
- **`src/resources/icons.ts`**: Custom icon definitions

### Adding Blog Posts

1. Create a new `.mdx` file in `src/app/blog/posts/`
2. Include required frontmatter: title, date, description
3. Images should be placed in `public/images/blog/`

### Adding Projects

1. Create a new `.mdx` file in `src/app/work/projects/`
2. Include required frontmatter: title, date, description, images
3. Images should be placed in `public/images/projects/`

## Key Technologies

### MDX Integration

- Uses `@next/mdx` and `next-mdx-remote` for MDX processing
- Supports custom React components within MDX content
- Frontmatter is parsed with `gray-matter`

### Once UI System

- Component library: `@once-ui-system/core`
- Key components: `Row`, `Column`, `Text`, `Flex`, `Grid`, `Button`, etc.
- Design tokens configured in `once-ui.config.ts`
- Custom theming via data attributes

### Routing

- App Router structure (Next.js 13+)
- Dynamic routes: `[slug]` for blog posts and projects
- Route protection available via `RouteGuard` component

## TypeScript Guidelines

- All new files should use TypeScript (`.ts`/`.tsx`)
- Define types in `src/types/` for reusable interfaces
- Use existing types from `src/types/content.types.ts` and `src/types/config.types.ts`
- Avoid `any` types; use proper typing

## Testing & Building

### Development

```bash
npm run dev  # Test changes at http://localhost:3000
```

### Production Build

```bash
npm run build  # Verify build succeeds
npm start      # Test production build
```

### Linting

```bash
npm run lint           # Run ESLint checks
npm run biome-write    # Auto-format with Biome
```

## Special Features

### Password Protection

- URLs can be password-protected via the content configuration
- Implementation in `src/components/RouteGuard.tsx`

### Newsletter Integration

- Mailchimp integration available
- Configuration in `src/resources/content.tsx`

### Image Optimization

- Next.js Image component used for automatic optimization
- Remote images configured in `next.config.mjs`
- Sync script available: `npm run sync-images`

### Social Links

- Configured in `src/resources/content.tsx`
- Icons defined in `src/resources/icons.ts`
- Automatically displayed in footer and about page

## Git Push to Local Machine

This repository includes scripts to push changes to a local machine:
- See `PUSH_TO_LOCAL.md` for detailed setup instructions
- Quick setup: Run `./setup-local-remote.sh`

## Common Tasks

### Updating Personal Information

Edit `src/resources/content.tsx`:
- `person` object: Name, email, location, avatar
- `social` array: Social media links
- `newsletter` object: Newsletter settings

### Customizing Design

Edit `src/resources/once-ui.config.ts`:
- Color schemes and themes
- Typography settings
- Component variants

### Adding New Pages

1. Create a new directory in `src/app/`
2. Add `page.tsx` for the route
3. Update navigation if needed

## Best Practices

1. **Component Structure**: Keep components focused and reusable
2. **Type Safety**: Always define proper TypeScript types
3. **Performance**: Use Next.js Image for all images
4. **Accessibility**: Follow WCAG guidelines, use semantic HTML
5. **Code Organization**: Group related functionality together
6. **Git Commits**: Write clear, descriptive commit messages
7. **Testing**: Always test locally before committing

## Dependencies

- Prefer using existing Once UI components before creating custom ones
- Check `package.json` for installed packages before adding new dependencies
- Use exact versions for stability (avoid `^` or `~` where possible)

## Deployment

- Optimized for Vercel deployment
- See README.md for one-click deploy button
- Build checks: Ensure `npm run build` succeeds locally first
