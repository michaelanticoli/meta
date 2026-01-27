# Deployment Guide

This guide covers deploying the Magic Portfolio application to production. We support multiple deployment platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Option 1: Vercel (Recommended)](#option-1-vercel-recommended)
- [Option 2: Render.com](#option-2-rendercom)
- [Option 3: Docker](#option-3-docker)
- [Option 4: Self-Hosted](#option-4-self-hosted)
- [Environment Variables](#environment-variables)
- [Domain & SSL Setup](#domain--ssl-setup)
- [Post-Deployment Checklist](#post-deployment-checklist)
- [Monitoring & Analytics](#monitoring--analytics)
- [Troubleshooting](#troubleshooting)
- [Rollback Procedures](#rollback-procedures)

---

## Prerequisites

Before deploying, ensure:

1. **Node.js 20+** installed locally
2. **Git** repository connected to GitHub/GitLab/Bitbucket
3. **Environment variables** configured (see [Environment Variables](#environment-variables))
4. **Build passes locally**:
   ```bash
   npm install
   npm run build
   npm run start
   # Visit http://localhost:3000 to verify
   ```

---

## Option 1: Vercel (Recommended)

Vercel is the creator of Next.js and offers the best deployment experience.

### Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/your-repo)

### Manual Setup

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   # Preview deployment
   vercel

   # Production deployment
   vercel --prod
   ```

4. **Configure Environment Variables**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Select your project
   - Settings → Environment Variables
   - Add your variables (see [Environment Variables](#environment-variables))

### Vercel Configuration

The `vercel.json` file is pre-configured with:
- Security headers (X-Content-Type-Options, X-Frame-Options, etc.)
- Cache headers for static assets
- API function timeout settings
- RSS feed rewrites

### Auto-Deploy

Once connected to GitHub, Vercel will:
- Deploy `main` branch to production automatically
- Create preview deployments for pull requests
- Run builds on every push

---

## Option 2: Render.com

Render offers a free tier and easy deployment.

### Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Setup

1. **Create Render Account**: [render.com](https://render.com)

2. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `magic-portfolio`
     - **Runtime**: Node
     - **Build Command**: `npm install && npm run build`
     - **Start Command**: `npm run start`
     - **Plan**: Free or Starter

3. **Environment Variables**:
   - Add variables in the Environment section
   - See [Environment Variables](#environment-variables)

### Blueprint Deployment

Use the included `render.yaml` for infrastructure-as-code:

```bash
# In your Render dashboard:
# New → Blueprint → Connect your repo
# Render will auto-detect render.yaml
```

---

## Option 3: Docker

Deploy to any container platform (AWS ECS, Google Cloud Run, DigitalOcean, etc.)

### Build Image

```bash
# Build the image
docker build -t magic-portfolio .

# Run locally
docker run -p 3000:3000 -e PAGE_ACCESS_PASSWORD=your-password magic-portfolio

# Visit http://localhost:3000
```

### Push to Registry

```bash
# Tag for your registry
docker tag magic-portfolio your-registry/magic-portfolio:latest

# Push
docker push your-registry/magic-portfolio:latest
```

### Docker Compose

```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.prod.yml up -d
```

---

## Option 4: Self-Hosted

Deploy to your own server (VPS, dedicated server, etc.)

### Using PM2

1. **Install PM2**:
   ```bash
   npm install -g pm2
   ```

2. **Clone and Build**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   npm install
   npm run build
   ```

3. **Start with PM2**:
   ```bash
   pm2 start npm --name "magic-portfolio" -- start
   pm2 save
   pm2 startup
   ```

4. **Nginx Reverse Proxy**:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

5. **SSL with Certbot**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NODE_ENV` | Environment mode | `production` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PAGE_ACCESS_PASSWORD` | Password protect pages | (none) |
| `NEXT_PUBLIC_SITE_URL` | Your domain URL | `http://localhost:3000` |

### Setting Variables

**Vercel**:
```bash
vercel env add PAGE_ACCESS_PASSWORD
```

**Render**: Set in Dashboard → Environment

**Docker**:
```bash
docker run -e PAGE_ACCESS_PASSWORD=secret -p 3000:3000 magic-portfolio
```

**Local Development**:
```bash
cp .env.example .env
# Edit .env with your values
```

---

## Domain & SSL Setup

### Custom Domain on Vercel

1. Go to Project Settings → Domains
2. Add your domain (e.g., `yourdomain.com`)
3. Configure DNS:
   - **A Record**: `76.76.19.61`
   - **CNAME**: `cname.vercel-dns.com`
4. SSL is automatic

### Custom Domain on Render

1. Go to Service Settings → Custom Domains
2. Add your domain
3. Configure DNS as instructed
4. SSL is automatic

### DNS Configuration Example

```
Type    Name    Value                   TTL
A       @       76.76.19.61            300
CNAME   www     cname.vercel-dns.com   300
```

---

## Post-Deployment Checklist

### Immediate (Day 22-24)

- [ ] Verify site loads at production URL
- [ ] Test all page routes:
  - [ ] Home page (`/`)
  - [ ] About page (`/about`)
  - [ ] Blog listing (`/blog`)
  - [ ] Individual blog posts (`/blog/[slug]`)
  - [ ] Work/Projects (`/work`)
  - [ ] Individual projects (`/work/[slug]`)
  - [ ] Gallery (`/gallery`)
- [ ] Test API routes:
  - [ ] RSS feed (`/rss` or `/feed.xml`)
  - [ ] OG image generation (`/api/og`)
- [ ] Verify images load correctly
- [ ] Test password protection (if enabled)
- [ ] Check mobile responsiveness

### Domain Setup (Day 25-26)

- [ ] Custom domain configured
- [ ] SSL certificate active (https://)
- [ ] www redirect working
- [ ] Old URLs redirect (if migrating)

### Performance (Day 27-28)

- [ ] Run Lighthouse audit (aim for 90+ scores)
- [ ] Verify caching headers on static assets
- [ ] Check Core Web Vitals in Search Console
- [ ] Test loading speed from multiple locations

### Beta Testing (Day 29)

- [ ] Share with 5-10 beta users
- [ ] Collect feedback via form or email
- [ ] Fix critical bugs found
- [ ] Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] Test on mobile devices (iOS Safari, Android Chrome)

### Launch (Day 30)

- [ ] Remove any "beta" or "coming soon" notices
- [ ] Submit sitemap to Google Search Console
- [ ] Verify robots.txt is accessible
- [ ] Announce on social media
- [ ] Update any external links to point to new domain

---

## Monitoring & Analytics

### Vercel Analytics

```bash
npm install @vercel/analytics
```

Add to `src/app/layout.tsx`:
```tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### Error Monitoring (Sentry)

```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

### Uptime Monitoring

- [UptimeRobot](https://uptimerobot.com/) (free)
- [Better Uptime](https://betteruptime.com/)
- [Pingdom](https://www.pingdom.com/)

---

## Troubleshooting

### Build Failures

**Error: "Module not found"**
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run build
```

**Error: "Out of memory"**
```bash
# Increase Node memory
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

### Runtime Errors

**500 Internal Server Error**
- Check Vercel/Render logs for detailed error
- Verify environment variables are set
- Check API route implementations

**404 on Dynamic Routes**
- Verify page files exist in `src/app/`
- Check for TypeScript errors in page components
- Ensure MDX content files are in correct location

### Performance Issues

**Slow Initial Load**
- Enable compression in hosting platform
- Optimize images with Next.js Image component
- Check for large dependencies in bundle

**High Memory Usage**
- Reduce concurrent builds
- Optimize image processing
- Check for memory leaks in API routes

---

## Rollback Procedures

### Vercel

```bash
# List deployments
vercel ls

# Promote previous deployment to production
vercel promote [deployment-url]
```

Or in Dashboard:
1. Go to Deployments
2. Find the previous working deployment
3. Click "..." → "Promote to Production"

### Render

1. Go to Service → Events
2. Find previous successful deploy
3. Click "Rollback" button

### Docker

```bash
# Pull previous version
docker pull your-registry/magic-portfolio:previous-tag

# Stop current container
docker stop magic-portfolio

# Start previous version
docker run -d --name magic-portfolio -p 3000:3000 your-registry/magic-portfolio:previous-tag
```

### Git-based Rollback

```bash
# Revert to previous commit
git revert HEAD
git push origin main

# Or reset to specific commit (use with caution)
git reset --hard [commit-hash]
git push origin main --force
```

---

## Support

- **Documentation**: See README.md for project setup
- **Issues**: Report bugs on GitHub Issues
- **Vercel Support**: [vercel.com/support](https://vercel.com/support)
- **Render Support**: [render.com/docs](https://render.com/docs)

---

*Last updated: January 2026*
