# Production Environment Checklist

Use this checklist to ensure your deployment is production-ready.

## Pre-Deployment

### Code Quality
- [ ] All linting passes (`npm run lint`)
- [ ] All TypeScript types pass (`npx tsc --noEmit`)
- [ ] Code is formatted (`npm run biome-write`)
- [ ] No console.log statements in production code
- [ ] No hardcoded secrets or API keys

### Build Verification
- [ ] Build succeeds locally (`npm run build`)
- [ ] Application starts without errors (`npm run start`)
- [ ] All pages render correctly
- [ ] All API routes respond correctly

### Content Review
- [ ] All blog posts render correctly
- [ ] All project pages render correctly
- [ ] Images load properly
- [ ] MDX content has no syntax errors
- [ ] Links are not broken

### SEO & Metadata
- [ ] `robots.ts` allows indexing in production
- [ ] `sitemap.ts` generates correct URLs
- [ ] Open Graph images generate correctly
- [ ] RSS feed works (`/rss` or `/feed.xml`)
- [ ] Favicon is present

---

## Deployment Configuration

### Environment Variables
- [ ] `NODE_ENV=production` is set
- [ ] `PAGE_ACCESS_PASSWORD` set (if using password protection)
- [ ] All required secrets added to platform
- [ ] No `.env` file committed to repo

### Platform Settings (Vercel)
- [ ] Project connected to Git repository
- [ ] Correct production branch set (usually `main`)
- [ ] Environment variables configured
- [ ] Build settings are correct
- [ ] Domain configured (if custom domain)

### Platform Settings (Render)
- [ ] Web service created
- [ ] Build command: `npm install && npm run build`
- [ ] Start command: `npm run start`
- [ ] Environment variables set
- [ ] Auto-deploy enabled

---

## Post-Deployment Verification

### Functionality Tests
- [ ] Homepage loads (`/`)
- [ ] About page loads (`/about`)
- [ ] Blog listing loads (`/blog`)
- [ ] Individual blog posts load
- [ ] Work/Projects listing loads (`/work`)
- [ ] Individual project pages load
- [ ] Gallery loads (`/gallery`)
- [ ] Special pages load (e.g., `/song-of-the-moon`)

### API Routes
- [ ] `/api/authenticate` responds
- [ ] `/api/check-auth` responds
- [ ] `/api/og/generate` generates images
- [ ] `/api/rss` returns valid XML
- [ ] `/rss` redirect works

### Performance
- [ ] Lighthouse Performance score > 90
- [ ] Lighthouse Accessibility score > 90
- [ ] Lighthouse Best Practices score > 90
- [ ] Lighthouse SEO score > 90
- [ ] First Contentful Paint < 2s
- [ ] Largest Contentful Paint < 2.5s

### Security
- [ ] HTTPS enabled (SSL certificate active)
- [ ] Security headers present (check with securityheaders.com)
- [ ] No sensitive data exposed in source
- [ ] Password protection working (if enabled)

### Cross-Browser Testing
- [ ] Chrome (desktop & mobile)
- [ ] Firefox (desktop)
- [ ] Safari (desktop & iOS)
- [ ] Edge (desktop)

### Mobile Responsiveness
- [ ] iPhone SE (375px)
- [ ] iPhone 12/13/14 (390px)
- [ ] iPad (768px)
- [ ] Desktop (1280px+)

---

## Domain & DNS (If Custom Domain)

### DNS Configuration
- [ ] A record points to hosting provider
- [ ] CNAME record for www subdomain
- [ ] DNS propagation complete (check with dnschecker.org)

### SSL Certificate
- [ ] Certificate issued and active
- [ ] Certificate covers www and non-www
- [ ] Auto-renewal enabled
- [ ] No mixed content warnings

### Redirects
- [ ] www → non-www (or vice versa)
- [ ] HTTP → HTTPS
- [ ] Old URLs redirect to new (if migrating)

---

## Monitoring Setup

### Uptime Monitoring
- [ ] Uptime monitor configured (UptimeRobot, Better Uptime, etc.)
- [ ] Alert notifications set up (email, Slack, etc.)
- [ ] Status page created (optional)

### Analytics
- [ ] Vercel Analytics enabled (or Google Analytics, Plausible, etc.)
- [ ] Events tracking configured (if needed)
- [ ] Goals/conversions set up (if needed)

### Error Tracking
- [ ] Error monitoring set up (Sentry, LogRocket, etc.)
- [ ] Source maps uploaded (if using Sentry)
- [ ] Alert thresholds configured

---

## Launch Checklist

### Final Verification
- [ ] All checklist items above completed
- [ ] Team members reviewed the deployment
- [ ] Stakeholders approved for launch

### Announcements
- [ ] Social media posts prepared
- [ ] Email announcement drafted (if applicable)
- [ ] Press release ready (if applicable)

### Post-Launch Monitoring
- [ ] Monitor for first 24 hours
- [ ] Check error logs for issues
- [ ] Monitor performance metrics
- [ ] Respond to user feedback

---

## Emergency Contacts & Procedures

### Rollback Procedure
1. Go to deployment dashboard (Vercel/Render)
2. Find previous successful deployment
3. Promote/rollback to that deployment
4. Verify site is working
5. Investigate and fix the issue

### Key Contacts
- **Primary Developer**: [Name] - [Email/Phone]
- **Platform Support**: Vercel/Render support portal
- **Domain Registrar**: [Provider] - [Support URL]

### Incident Response
1. Acknowledge the incident
2. Assess impact and severity
3. Implement fix or rollback
4. Communicate status to stakeholders
5. Post-incident review

---

## Notes

_Add any project-specific notes here._

---

*Last updated: January 2026*
