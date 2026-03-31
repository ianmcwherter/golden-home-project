# Golden Home Project — Business Brain
# ============================================================
# This file is the single source of truth for the business.
# Every agent reads it at start. Every agent updates it at end.
# Humans review it weekly. Never delete history — append only.
# Last updated: 2026-03-31
# ============================================================

## BUSINESS IDENTITY
- **Name**: Golden Home Project LLC
- **Model**: Amazon affiliate marketing (tag: `goldenhomep06-20`)
- **Niche**: Home organization, kitchen upgrades, bedroom/bathroom transformation
- **Mission**: Help people make their homes beautiful and functional on a budget
- **Revenue model**: Affiliate commissions from Amazon + brand partnerships via Impact/CJ/Awin

---

## LIVE METRICS (update each week)
| Metric | Value | Last Updated |
|--------|-------|--------------|
| YouTube subscribers | 6,710 | 2026-03-31 |
| YouTube total views | 17,665 | 2026-03-31 |
| YouTube videos | 93 | 2026-03-31 |
| Instagram followers | 0 | 2026-03-31 |
| Facebook followers | 0 | 2026-03-31 |
| Amazon affiliate revenue (MTD) | $0 confirmed | 2026-03-31 |
| Active affiliate platforms | Amazon, Impact, CJ, Awin | 2026-03-31 |

---

## CONTENT STRATEGY (current — do not change without reason)
### What works (data-backed):
- **Transformation format** "before → after → products": 5,779 views vs 200 for product roundups
- Specific dollar amounts in hooks ("$47", "$34") dramatically increase click-through
- Series content ("Room by Room Ep 1, 2, 3") builds subscribers over time
- Voiceover + Ken Burns animation on AI frames = professional enough for current stage

### Posting cadence:
- YouTube Shorts: 4/week (Tue, Thu, Sat, Sun) via GitHub Actions at noon ET
- Instagram Reels: Saturdays only (rate-limit recovery, then rebuild)
- Long-form YouTube: bi-weekly (highest revenue per video — 15-20 affiliate links)

### Content formats ranked by revenue:
1. Transformation before/after + specific cost
2. "I tested $X vs $Y" comparison
3. "I use this every morning" daily utility
4. Weird/surprising finds — high share rate
5. Room series episodes — subscriber compounding

### Hooks that convert:
- "My [room] looked like this. Same [room]. $[amount]."
- "I've been doing [X] wrong for [N] years. This fixed it."
- "I was skeptical. I was wrong."
- "I use this every single morning."

---

## AFFILIATE PARTNERSHIPS (active)
| Platform | Brand | Commission | Status | Notes |
|----------|-------|------------|--------|-------|
| Amazon | All home categories | 3-8% | Active | Tag: goldenhomep06-20 |
| Impact | Syruvia Syrups | 20% | PENDING ACCEPTANCE | Contract proposed by David — accept ASAP |
| Impact | HermanRx | $250 CPA | Declined | Off-niche (telehealth/GLP-1) |
| CJ | AliExpress | 5.8% | Invited | Home goods overlap — accept and integrate |
| Awin | Various | TBD | Pending | Check for home brand invitations |
| Direct | Canoly (3-in-1 juicer) | TBD | Draft reply sent | April 30 deadline, IG collab, sample available |

---

## CONTENT PIPELINE STATUS
| Item | Status | Location |
|------|--------|----------|
| Posts 001-060 | ✅ Published | YouTube + FB + IG |
| Posts 061-070 | ✅ YouTube published | IG rate-limited (retry) |
| April Shorts 001-013, 015 | ✅ Generated + in repo | /videos/transformation/ |
| April Shorts 014, 016 | 🔄 Generating | Local machine |
| April Shorts posting | ✅ Automated | GitHub Actions daily-poster.yml |
| Long-form video (Kitchen) | ❌ Not started | Highest revenue priority |
| Long-form video (Apt tour) | ❌ Not started | April 22 scheduled |

---

## PLATFORM CREDENTIALS (reference — actual secrets in GitHub + .env)
| Service | Account | Notes |
|---------|---------|-------|
| YouTube | goldenhomeprojectllc@gmail.com | OAuth token in yt_token.json |
| Instagram | @goldenhomeproject | Meta Graph API, IG ID: 17841444356554286 |
| Amazon Associates | goldenhomep06-20 | Dashboard: affiliate.amazon.com |
| Impact.com | goldenhomeprojectllc@gmail.com | Pending: Syruvia contract |
| CJ Affiliate | goldenhomeprojectllc@gmail.com | Pending: AliExpress join |
| Awin | goldenhomeprojectllc@gmail.com | Pending: review invitations |
| Pexels | goldenhomeprojectllc@gmail.com | API key in .env |

---

## AGENT ROLES & RESPONSIBILITIES
| Agent | Frequency | Primary Job | Reads | Writes |
|-------|-----------|-------------|-------|--------|
| Email Monitor | Daily 8am ET | Brand deals, affiliate alerts | BUSINESS_BRAIN.md | affiliate partnerships table, email log |
| Trend Research | Mondays 8am ET | Competitor research, content ideas | BUSINESS_BRAIN.md | content strategy, weekly trend report |
| Affiliate Optimizer | Thursdays 10am ET | Revenue optimization, commission tracking | BUSINESS_BRAIN.md | affiliate partnerships table, revenue metrics |
| Brand Outreach | Tuesdays 10am ET | Proactive brand pitches | BUSINESS_BRAIN.md | outreach drafts, partnership pipeline |
| GitHub Actions Poster | Daily noon ET | Post pre-generated content | /videos/transformation/ | posting logs |

---

## WHAT'S WORKING (validated by data)
- Pollinations.ai: reliable at <3 concurrent requests
- Ken Burns animation + text overlays: professional-looking output
- edge-tts voiceover: natural, free, multiple voices
- GitHub Actions posting: live and scheduled
- Pexels API: now integrated for BEFORE frames (real footage > AI)
- Gmail MCP: connected, can read/draft email

## WHAT'S NOT WORKING / NEEDS FIX
- Instagram/Facebook: 0 followers, API rate-limited (bulk posting)
- No affiliate revenue confirmed (check Associates dashboard)
- Long-form videos not created (highest revenue potential, not started)
- IG rate limit: retry posts 061-070 after rate limit clears
- trans_014 and trans_016: still generating

---

## LESSONS LEARNED (never forget)
1. **Bulk posting kills Meta accounts** — max 1 IG post/day, Saturdays only for now
2. **Product roundups fail** — 50-200 views. Transformation format = 5,779 views. Never revert.
3. **Pollinations 429** — only 1-2 concurrent requests max. Add sleep(8) between calls.
4. **Specific dollar amounts convert** — "$47" > "affordable". Always use exact cost.
5. **Series content compounds** — Room by Room series drives follows, not just views.
6. **Long-form = real money** — 15-20 affiliate links per video vs 3-4 in Shorts.
7. **Off-niche deals hurt trust** — declined HermanRx (telehealth). Stick to home.

---

## WEEKLY REVIEW LOG
### 2026-W13 (week of 2026-03-31)
- Full strategy pivot to transformation format
- April 2026 content calendar created (16 Shorts + 2 long-form)
- GitHub Actions daily poster deployed — no Mac dependency for posting
- Claude Code cloud agents set up — no API key dependency
- Pexels API integrated for real BEFORE footage
- Weekly trend research automation built (cron + cloud)
- Email drafts: AliExpress accepted (CJ), HermanRx declined, Canoly draft ready
- Syruvia contract pending acceptance on Impact.com (20% commission — high priority)
- All secrets added to GitHub Actions

---

## NEXT ACTIONS (priority order)
- [ ] Accept Syruvia contract on Impact.com (20% commission, home-adjacent — syrups for kitchen)
- [ ] Accept AliExpress on CJ Affiliate (5.8% commission, huge product catalog)
- [ ] Send Canoly draft reply (April 30 deadline, IG collab, free sample)
- [ ] Check Awin pending invitations
- [ ] Generate + post long-form "Kitchen Makeover" video (April 8)
- [ ] Retry IG posts 061-070 (rate limit should be clear)
- [ ] Add trans_014 and trans_016 to repo when generation completes
- [ ] Set up 4 cloud agents at claude.ai/code/scheduled

---
*This file is automatically updated by agents. Human review recommended weekly.*
*Agents: always read this file first. Always update relevant sections. Commit to claude/ branch.*
