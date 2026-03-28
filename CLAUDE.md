# Digital Asset Lead Finder — Master Project Guide

## Overview
This is a system for finding people who own valuable digital assets (usernames, handles, accounts) on any platform and building an actionable contact list for acquisition. Currently targeting **Discord OG usernames** but the methodology works for any scarce digital asset (Instagram handles, Twitter handles, Minecraft names, domain names, etc.).

## Core Principle
**Every lead is found through manual analysis, not automation.** Scripts collect raw data. Humans (Claude) read every piece of data in context, batch by batch, and make judgment calls. No keyword filtering. No regex extraction without verification. No shortcuts.

## Current Target: Discord OG Usernames
Find Reddit users who own valuable Discord usernames (short, real words, rare) and may not know the market value. Build a contact list: **Discord username + Reddit author + evidence**. These are people to reach out to for under-market acquisition.

## What a Real Lead Looks Like
- u/Studio_Muted: "I somehow managed to get the username 'unc'" → **Lead: @unc, contact u/Studio_Muted**
- u/OccupiedJ1: "mine is 'occupied'" → **Lead: @occupied, contact u/OccupiedJ1**
- u/Complete_Worker_7095: "i have a user called pdzh and im down to sell it for a nitro" → **Lead: @pdzh, massively undervalued**
- u/PaddymanRS: "I managed to get the username 'paddy'" → **Lead: @paddy, contact u/PaddymanRS**
- u/OMG_I_LOVE_CHIPOTLE: "my username is 2 letters" → **Indirect lead: owns 2L, DM to find out which**

## What is NOT a Lead
- "I got **hit** by automod" → "hit" is a verb, not a username
- "selling **4** letter username" → "4" is a quantity
- "selling **EU** val account" → "EU" is a server region
- Any common English word used as normal grammar in a sentence
- Posts about Minecraft servers, friend-finding, job listings, OnlyFans, Valorant accounts

---

## Data Gathering Process

### What Works
1. **Reddit API searches within specific subreddits** — r/discordapp, r/discord, r/OGUsers, r/ThemePages, r/Scams, r/OutOfTheLoop
2. **Both `sort=relevance` and `sort=top`** for key queries — top sort finds the mega-threads with 1000+ comments
3. **Broad global searches** (no subreddit restriction) to find threads in unexpected subs
4. **Deep comment scraping** (4 levels deep) — 90% of leads come from COMMENTS, not post bodies
5. **Incremental saves** — save after EVERY thread. Never lose data.

### What Does NOT Work
- Google `site:reddit.com` searches — returns marketplace sites, not Reddit threads
- Exact-quote Google searches with `""` — too restrictive, bad results
- Generic queries like "dm me on discord", "add me on discord" — pulls in thousands of irrelevant posts
- Gaming sub searches (r/Minecraft, r/FortNiteBR etc.) — 99% irrelevant
- Keyword-based filtering of leads — misses real leads, keeps false ones

### Proven Search Queries (Reddit API)
```
"rare username", "og username", "og usernames",
"got my name", "kept my name", "username rollout",
"name change pomelo", "username pomelo", "pomelo",
"3 letter username", "2 letter username", "4 letter username",
"short username", "is my username rare", "is my name rare",
"username worth", "buy my discord", "selling username",
"username scam", "username change", "discriminator",
"what username did you get", "one word username",
"friend request spam", "4 letter usernames left",
"3 letter usernames taken", "account selling"
```

### High-Converting Thread Types
1. **"Is my username rare?"** threads — people ask, commenters reveal theirs
2. **"Username rollout has begun"** mega-threads — 2000+ comments, people sharing what they got
3. **"Friend request spam"** threads — people with valuable names complaining about harassment (confirms ownership)
4. **"Someone wants to buy my account"** threads on r/Scams — confirms they own something valuable
5. **"Are there any X-letter usernames left?"** — people reveal what they have
6. **General complaint threads about pomelo** — buried in comments are casual reveals

---

## Lead Verification Process — THE MOST IMPORTANT PART

### Rules
1. **Go batch by batch** — 30 comments at a time maximum
2. **Actually read each comment's full context** — no keyword shortcuts
3. **Ask for each one: "Is this person revealing they own a specific Discord username?"**
4. **If the answer isn't clearly yes, it's not a lead**
5. **Never assume a short word extracted by regex is a username** — verify it's being used AS a username, not as normal English
6. **Indirect leads count** — "I got a 3-letter name" is still valuable even without the specific username

### Lead Types
- **OWNER**: Person explicitly says they own a specific username ("mine is X", "my username is X")
- **SELLER**: Person is selling a specific username ("selling @X", "WTS @X")
- **INDIRECT**: Person hints at owning something valuable without revealing the specific name ("I have a 2-letter username", "people keep offering to buy my name")
- **MENTION**: Someone else mentions a username exists ("that guy has @X") — lower priority

### Tier Classification
- **S**: 1-2 character usernames (most valuable)
- **A**: Real English word, 3-5 characters (fire, sky, wolf, paper, laser)
- **B**: 3-character non-word (k9v, pac, xqx)
- **C**: 4-character non-word (zpgy, euiv, abcd)
- **D**: 5+ character words or longer non-words
- **?**: Indirect leads where we don't know the username

**Important**: The tier must reflect actual value. "princess", "acoustic", "wrench" are all real words and should be A-tier, not D-tier. Check if it's a real English word, not just if it's in a hardcoded list.

### Anti-False-Positive Checks
- Is the word being used as a **verb**? ("got rid of" → "rid" is not a username)
- Is it a **number/quantity**? ("selling 4 letter" → "4" is not a username)
- Is it a **region/abbreviation**? (EU, NA, AP near gaming context)
- Is it an **email domain**? (@gmail.com, @discord.com)
- Is the author `[deleted]` or `AutoModerator`? → skip
- Does the source URL actually point to the thread where this comment appeared?

---

## Dashboard

### Setup
- `serve.py` on port 8080 — serves `dashboard.html` with no-cache headers
- Cloudflare tunnel: `cloudflared tunnel --url http://127.0.0.1:8080`
- Data: reads `verified_leads.json` via fetch

### Dashboard Requirements
- Source URL column must be clickable and link to the actual Reddit thread
- Sort by tier (S first, then A, B, C, D, ?)
- Filter by tier, ownership type
- Search by username, author, context
- Show subreddit stats (which subs produce most leads)
- Indirect leads should show their category/reason in context

---

## File Structure
```
C:\Users\haddad\Desktop\Og Owners\
├── CLAUDE.md               # This file — project guide
├── serve.py                # Dashboard HTTP server
├── dashboard.html          # Live dashboard UI
├── verified_leads.json     # THE source of truth — all verified leads
├── raw_comments.json       # Raw scraped comments (12,579+)
├── leads.json              # Old automated extraction (unreliable, reference only)
├── deep_scrape.py          # Scrapes comments from target threads
├── og_scraper.py           # Original broad scraper (reference)
├── og_finder.py            # v1 scraper (reference, deprecated)
├── images/                 # Downloaded screenshots from posts
├── candidates.json         # Old candidate data
├── target_threads.json     # Thread IDs for deep scraping
└── .claude/launch.json     # Preview server config
```

---

## Common Mistakes to Avoid
1. **Don't use keyword filtering to validate leads** — it misses real leads and keeps false ones
2. **Don't try to process hundreds of leads at once** — batch by batch, 30 max
3. **Don't trust regex extraction blindly** — always verify context
4. **Don't lose data** — save incrementally after every API call
5. **Don't waste time on Google searches for Reddit** — use Reddit API directly
6. **Don't add generic queries** like "dm me on discord" — floods results with noise
7. **Don't assume a word is a username just because it's short** — "rid", "hit", "low", "pop" are almost always verbs/adjectives in context
8. **Don't run massive scrapes without checking quality first** — scrape a few threads, verify quality, then scale
9. **Don't classify tiers based only on a hardcoded word list** — any real English word is valuable regardless of whether it's in our list
10. **Source URLs must be verified** — each lead must link to the actual thread where the comment appeared

---

## CRITICAL: Comment Review Rules (NEVER SKIP)

**When reviewing comments from scraped threads, ALWAYS follow these rules:**

1. **Go comment by comment, in order.** Never skip ahead, never jump to "promising" threads, never sample every Nth comment. Every single comment gets read.
2. **Batch size: 20-30 comments max per batch.** Don't try to process hundreds at once — quality drops dramatically.
3. **No keyword filtering during review.** Don't pre-filter comments with patterns like "mine is", "I got" etc. A lead can appear in ANY comment in ANY language. Read the actual context.
4. **Don't be negative about yields.** Even 1 lead per 300 comments is valuable — each lead could be worth thousands of dollars. Never say "zero leads, this is pointless" or try to skip ahead.
5. **Indirect leads are VALUABLE.** Someone saying "I have a 3-letter name" or "people keep messaging me" or "someone offered me money" IS a lead even without the specific username. These people can be DMed.
6. **Don't dismiss based on topic.** A thread about "Discord privacy issues" can have someone casually mentioning their username in comment #147. You won't find it if you skip the thread.
7. **Track progress honestly.** Say where you are (e.g., "comment 2461 of 23,346") and keep going. Don't restart or re-sort.
8. **When scraping new threads, go through ALL comments from those threads before moving on.** Don't scrape 6 threads then only look at 1 of them.
9. **Never take shortcuts.** The user has explicitly asked multiple times to stop skipping, stop jumping around, and stop trying to be clever with filtering. Just read every comment.

---

## Lead Profile Research Process

**For EVERY lead, research their Reddit profile to build contact info.**

### Step 1: Pull their Reddit history
- Use the Reddit overview endpoint (comments+posts combined, up to 300 items)
- Reddit links are blocked in Chrome — always use the Reddit API via curl

### Step 2: Read EVERY post and comment, one by one
- **No keyword filtering.** Do NOT search for "discord" or "add me" — just read each one in order.
- Every person is different. A music producer reveals handles differently than a gamer or a trader.
- Read the FULL text of each comment/post. Context matters — the username might be buried mid-sentence.
- Note what subs they're active in as you go — builds a picture of who they are.
- **Present comments in batches of 20-30.** Show the user what you're reading so they can monitor quality.
- **Be dynamic.** A kid posting on r/Roblox needs different analysis than an OGUsers trader. Adapt your approach per person — don't apply a cookie-cutter template.
- **Note EVERYTHING potentially useful as you go** — links, platforms mentioned, games played, locations, ages, any detail that helps build a profile. You can filter later. Don't pre-judge what's relevant.

### Step 3: Follow links to external profiles
This is THE most important step. **If someone touches a platform, they have a username there.** Don't just note it — GO FIND IT.

**Rules for following links:**
1. **Every link in their comments/posts gets evaluated.** If it leads to a profile page on any platform, visit it in Chrome.
2. **Reddit links are blocked in Chrome** — use the Reddit API via curl instead. But for ALL other platforms, use Chrome.
3. **Ask the user before visiting** if you're unsure whether it's worth checking. Don't waste time on obviously irrelevant links (e.g., a news article), but DO check anything that could be a profile.
4. **Platform activity = username exists.** If they comment in r/Bandlab, they have a Bandlab account. If they play Star Citizen, they have an RSI handle. If they post in r/osu, they have an osu! profile. GO CHECK.

**Platform-specific lookup methods:**
- **Bandlab** → visit bandlab.com/{their_reddit_username} or any linked Bandlab URL. Profile page shows username.
- **Steam** → visit linked Steam profile. Shows username, display name, linked accounts (Discord, Twitter, etc.).
- **YouTube/Twitch/Twitter/Instagram** → visit the profile and note the handle.
- **osu!** → check osu.ppy.sh/users/{username}. Profiles are public.
- **Star Citizen** → check robertsspaceindustries.com/citizens/{handle}. Public profiles.
- **Roblox** → check roblox.com/users/profile (if they link it). Shows display name and username.
- **Gaming LFG subs** (r/ApexLFG, r/ValorantLFG, etc.) → they almost certainly shared their gamertag in the post body. Use the Reddit API to read the post.
- **r/OGUsers** → check if they have Discord/Telegram handles in their post for trades.
- **ANY linked URL** that could be a profile → visit it. Spotify, SoundCloud, Linktree, carrd.co, TikTok, etc.
- **If their Reddit username looks like a real handle** (not auto-generated like Ok_Swordfish8186) → try it on common platforms.

**The principle: Every platform they touch is a potential username discovery.** If someone comments on Bandlab, they have a Bandlab username. If they play Star Citizen, they have a Star Citizen handle. Don't just note "active in r/Bandlab" — go find the actual username. Visit the profile page and grab the handle.

### Step 4: Check images
- If any of their posts contain images (i.redd.it, imgur, etc.), view them.
- If images/ folder has files matching their post IDs, view those.
- Screenshots of profiles (Discord, TikTok, Instagram) are the highest-value finds.

### Step 5: Record what you found
- **Only record confirmed handles** — things they explicitly stated, linked to, or are visible in screenshots.
- **Do NOT guess** — if their Reddit name is "katyusha-the-smol", don't assume that's their Discord too unless they said so.
- **Do NOT put subreddit names in contact** (e.g. "r/Norway") — translate to interests/context.
- **Do NOT put vague descriptions** like "goes by Zay online" — we need exact handles with platform.
- **Note games/platforms** they use even without handles — "Plays osu!, Star Citizen" tells us where to look.

### Step 6: Save after every lead
- Update verified_leads.json immediately after each lead
- The dashboard reads the JSON on refresh — no need to touch dashboard.html
- Never batch up multiple leads before saving

### Step 6.5: Verify images from their posts
- If they posted images (i.redd.it, imgur links), view them using the Read tool (local images/) or Chrome (external URLs).
- Screenshots of Discord profiles, game accounts, social media profiles are the highest-value finds.
- Match images to the right person — OP images ≠ commenter images. Always check who posted what.
- See the full **Image Analysis Process** section below for detailed rules.

### What NOT to do
- Do NOT use keyword searches on their history — read every comment
- Do NOT use scripts for analysis — each person is unique
- Do NOT skip comments that seem irrelevant — the handle could be anywhere
- Do NOT assume a generated Reddit name (e.g. Sufficient-Snow9197) means they have no handles
- Do NOT record platforms without visiting them when possible — actually go check
- Do NOT jump ahead to "promising" comments — read in order
- Do NOT batch decisions — present findings to the user as you go so they can monitor
- Do NOT assume a link is irrelevant without evaluating it — if it could lead to a profile, check it

**Contact column format:** `Active: YYYY-MM-DD | Discord: @handle | Twitter: @handle | Instagram: @handle` etc.
If nothing found: `Active: YYYY-MM-DD | Reddit DM only`
If account is deleted/suspended: `INACTIVE`

---

## Image Analysis Process

**Images are a critical source of leads and contact info.** People post screenshots of their Discord profiles, TikTok accounts, Instagram pages, etc. Text-only review misses these entirely.

### When to Check Images
1. **Every lead that has an `images` array** in verified_leads.json — view every image
2. **Every thread with downloaded images** in the `images/` folder — cross-reference post IDs
3. **During profile research** — if a user posts image links (i.redd.it, imgur, imgtr.ee) in their comments/posts, view them
4. **OGUsers selling posts** — sellers almost always include Discord profile screenshots as proof of ownership

### What to Look For in Images
- **Discord profile screenshots**: Username, display name, member since date, badges (Early Supporter, Active Dev, HypeSquad, Nitro), clan tag, bio text, connected accounts
- **TikTok/Instagram/Twitter profiles**: Handle, follower count, bio — these are alternative contact channels
- **Game screenshots**: In-game names visible in scoreboard, chat, profile screens
- **Trading/selling proof**: Screenshots showing ownership of accounts, often with usernames visible
- **Friend request screenshots**: Shows the person has a desirable name (118 pending FRs = valuable name)

### What We've Found from Images (Proven Results)
- **@pbxz** (u/hereliespb) — ENTIRELY missed during text review, only visible in their Discord profile screenshot
- **@budf Instagram** (u/unduped) — their IG profile screenshot revealed an alternative contact channel with 1,159 followers
- **@topfloorboss78 TikTok** (u/underagechildbeater) — seller's TikTok account (59.7K followers) visible in screenshot
- **@dh. profile** (u/Short_Possibility794) — seller's Discord profile confirmed: member since Oct 2016, Early Supporter badge
- **@3v profile** (u/Shirt-Stunning) — display name "mercy" confirmed from profile screenshot
- **u/Dailzay TikTok OGs** — @MAG1cz and @eqoz TikTok profiles found only in images, not mentioned in text
- **u/SamirMishra27** — Discord identity "EpicCargo#9440" revealed in their pomelo update screenshot

### Image Analysis Rules
1. **Always view images locally first** (Read tool on `images/` folder) — faster than browser
2. **External URLs (imgur, imgtr.ee) may be dead** — imgtr.ee is fully down, some imgur links are broken
3. **Match images to the correct person** — thread OP images ≠ commenter images. Check who posted the thread vs who commented
4. **Note EVERYTHING visible**: username, display name, badges, member since date, bio, connected accounts, clan tags
5. **Cross-platform screenshots are gold** — a Discord user posting their TikTok/IG/Twitter profile gives you multiple contact channels
6. **GIF files may be too large** to read directly — try other image formats first
7. **Most images in the folder are from irrelevant subs** (airsoft, Star Citizen, Dota 2, etc.) — always cross-reference the post ID with Discord-related threads before viewing
8. **Add `"images"` array to the lead** when you find relevant images, and note findings in the `"contact"` field
9. **Mark image-only discoveries** with "FOUND VIA IMAGE REVIEW" in the context field so we can track the method's value

### Image File Naming Convention
Images are stored as `{reddit_post_id}_{index}.{ext}` in the `images/` folder.
- Example: `1qc4v5p_0.jpg` = first image from Reddit post `1qc4v5p`
- To find images for a lead: extract post ID from their `source_url`, then look for `{post_id}_*.{jpg,png,gif}`

---

## CURRENT TASK: Lead-by-Lead Profile Research

**What we're doing:** Going through every lead on the dashboard, reading their FULL Reddit post/comment history, and finding:
1. **Exact usernames on ANY platform** — Discord, osu!, Steam, Twitter, Instagram, TikTok, YouTube, Twitch, Xbox, PSN, Roblox, League, etc. ONLY confirmed handles (explicitly stated or linked), no guesses.
2. **Last active date** — so we know if they're reachable
3. **Games/platforms they use** — "Plays osu!, League, Valorant" tells us where else to find them
4. **Any post where they share contact info** — "add me", "dm me", their Discord in a gaming LFG post, commission post, etc.

**Rules:**
- Go lead by lead, reading EVERY comment and post
- Do NOT use a script — each lead is different and needs human judgment
- Do NOT guess usernames — only record what they explicitly stated or linked
- Do NOT put subreddit names in contact (e.g. "r/Norway") — translate to interests/context
- Do NOT put vague descriptions like "goes by Zay online" — we need exact handles
- SAVE to verified_leads.json after each lead
- The dashboard reads the JSON on refresh — no need to touch dashboard.html
- Use the Reddit overview endpoint (comments+posts combined, up to 300 items)
- For the specific lead: search for their known username if we have one
- If they play specific games (osu!, Valorant, etc.) note those — they have public profiles on those platforms
- Read CONTEXT of every comment — "add me", "dm me", "my discord is", commission posts, LFG posts, trading posts all reveal handles
- Customize the search per lead — a seller active on r/OGUsers needs different keywords than a casual user on r/discordapp
- If someone mentions playing a game, they likely have a username there — note the game/platform even if we don't have the handle

**Contact format examples:**
- `Active: 2026-03-04 | Discord: @z8 | Plays osu!, BattleBit, Elden Ring | Reddit DM`
- `Active: 2025-06-01 | Discord: @xx | Twitter: @johndoe | Steam: johndoe123 | Reddit DM`
- `INACTIVE - 0 posts/comments visible`
- `SUSPENDED/DELETED`

**Progress:** Working through all leads on the dashboard by value.

### Completed Profile Research
**S-Tier leads (re-analyzed properly):**
- u/Shirt-Stunning (@3v) — 29 comments, drug/RC community, crypto seller, no other handles. Reddit DM only.
- u/Short_Possibility794 (@dh.) — 13 items, OGUsers seller, $150-200 PayPal, said "add me on Discord". Portuguese speaker.
- u/katyusha-the-smol (@v) — 119 items, US Navy aviation, makes music (linked Bandlab post), Star Citizen, furry. No handles.
- u/zayroncana (@z8) — 60 items, Dutch 24yo in Norway, osu! player, plays Nightreign/Shadow Slave. No handles.
- u/Ok_Swordfish8186 (@xx) — 1 comment ever, owns @xx + ~13 3L names. Dead end for contact.
- u/Greedy-Problem700 (@eh + @rrv) — already researched.
- u/Rickel2Hero (@hm) — found Twitter: @Rickel via Chrome visit.
- u/joppa9 (indirect 2L) — Steam 20yr/7k games, Swedish gamer.
- u/ibeatyou9 (@eve) — already researched.

**A-Tier real word owners (properly analyzed):**
- u/NotSoArtsyCharley (@charley) — 397 items, ASU CS grad, Phoenix AZ. Found Pokemon Go handle: "Lyricless". No Discord shared.
- u/DepressedRS (@depressed) — 220 items, Purdue student, Carmel Indiana. Found YouTube: vialli, MapleStory: ILlaiv20. Had #0001 tag.
- u/Holiday_Clerk8739 (@boring) — 41 items, ~20yo. Said "imboring or boring" used everywhere, verified on most platforms, started music. FashionReps buyer.
- u/aLexyYa (@lexy) — 300+ items, Romanian uni student, freelance anime artist. Found art portfolio: xmooniiq (carrd.co, Instagram, TikTok, Twitter, Tumblr). Has Roblox account.

**Indirect leads (properly analyzed):**
- u/TheNedi14 — BEST FIND. Claims 47 Discord accounts from 2015. Multi-platform trader (Roblox, Fortnite). Has Fortnite OG 3L name. Lithuanian in Denmark.
- u/SuperZebra3693 — Desirable name + Early Bot Dev badge, offered money. Financially struggling. Motivated seller potential.
- u/GrimReaper888 — Confirmed 2-letter username. UK, Tesco worker, DBD player, 3D printing hobbyist.
- u/Curious_Cantaloupe94 — Short word username, being offered money. Tech/cybersecurity literate. Only 10 comments, ghost online.
- u/ima4chan — Daily buy requests + friend requests. German IT apprentice, heavy gamer. Very active but never shares handles.
- u/Sekh765 — PARTNER owns the 3L, not them. Fed employee, very active gamer. Would need to ask about partner's name.
- u/Final_Natural_2499 — Wants to sell rare name. 1 comment ever. Likely never checks Reddit.
- u/demfuzzypickles — Common 6-letter word, daily friend requests. Very privacy-conscious (censors own username). Active today.

---

## Patterns Learned from Profile Research

### What Actually Produces Handles
1. **Art commission pages** (carrd.co, ko-fi, etc.) — artists link ALL their socials. u/aLexyYa → xmooniiq on 4 platforms.
2. **YouTube video links** — people post their own gameplay/content videos. u/DepressedRS → YouTube "vialli".
3. **Pokemon Go friend codes** — people share their trainer name. u/NotSoArtsyCharley → "Lyricless".
4. **LFG / "add me" posts** — gaming subs where people share gamertags.
5. **OGUsers posts** — traders list Discord/Telegram handles for contact.
6. **Profile screenshots in images/** — Discord profiles, TikTok, Instagram visible in posted screenshots.
7. **"I use this name everywhere"** statements — u/Holiday_Clerk8739 said "imboring" used on all platforms + verified.

### What Has Been Less Productive (but don't skip — every account is different)
These patterns have produced fewer handles SO FAR, but that doesn't mean you skip them. One piece of buried info could be the key to a lead worth thousands. These are tendencies, not rules:
1. **Political/debate-heavy histories** — tend to have fewer handle reveals, but someone could drop "add me on discord" in comment #247 of a political thread.
2. **Auto-generated Reddit names** (Ok_Swordfish8186, Final_Natural_2499) — often throwaway accounts, but some people use auto-names and are still very active with handles elsewhere.
3. **Meme/shitpost accounts** — younger users posting on r/copypasta tend not to share, but they DO play games and COULD have handles buried in a gaming sub comment.
4. **Single-comment accounts** — harder to reach but the lead itself (what they said) is still valuable for building our database.
5. **Privacy-conscious users** — may not share publicly but could respond to a DM.

**NEVER assume a category means "skip this person."** Every account is unique. The handle could be in any comment on any sub. Read everything.

### Lead Value Hierarchy (What to Prioritize)
1. **S-tier sellers** (actively selling) > **S-tier owners** (might sell) > **A-tier real word owners** > **Indirect leads being spammed/offered money** > **Indirect leads with unknown names**
2. **Real English words are money.** @boring, @depressed, @charley, @lexy are all high value regardless of length.
3. **3-letter random non-words (mep, zsq, bqj) are worth very little.** Don't prioritize these.
4. **"A friend owns it" = indirect lead**, not a direct lead. You can't contact the actual owner through the friend easily.
5. **Having #0001 tag does NOT mean they have the OG pomelo username.** Many #0001 users got random names assigned.
6. **Indirect leads being spammed/harassed are VERY valuable** — confirms they own something desirable, and they're reachable.
7. **People who want to sell but don't know where** (u/Final_Natural_2499) are the easiest acquisitions IF you can reach them.
8. **Multi-platform traders** (u/TheNedi14 with 47 accounts) are the highest-volume targets.

### Contact Research Process Notes
- **Every account is different.** A music producer, a gamer, a trader, and a teenager all reveal info in completely different ways. Never apply a template — adapt to who the person is.
- **One buried detail can make a lead.** Someone's handle could be in comment #200 on an unrelated sub. A link to a carrd.co page could reveal 4 platform handles at once. Never assume you've "seen enough."
- **Read everything, note everything.** Even if it doesn't seem relevant now — a game they play, a country they're in, a platform they mention — it builds a picture that helps with outreach.
- **Reddit API gives max 300 items.** For users with 300+, you've seen their recent history. For users with 1-5 items, those few items are all you get — make them count.
- **Reddit links are blocked in Chrome.** Always use the Reddit API via curl. All other platforms use Chrome.
- **Follow EVERY link** that could lead to a profile. Don't pre-judge — a link to a carrd.co page in an art commission comment gave us 4 handles for @lexy.
- **Save after EVERY lead.** Never batch multiple leads before saving to verified_leads.json.
- **The dashboard auto-refreshes every 15 seconds.** Just save the JSON and the site updates.
- **Don't rush.** Quality over speed. Missing one handle because you skimmed is worse than taking an extra 2 minutes per lead.

---

## ABSOLUTE RULE: NO KEYWORD SEARCHING ON USER HISTORIES (NEVER BREAK THIS)

**When analyzing a Reddit user's comment/post history, you MUST read every single comment in display order. NEVER use keyword filtering (grep, regex, `if any(x in body for x in [...])`  etc.) to scan for handles.**

### Why this rule exists
- **u/lancito01** shared their Discord tag `Lancito01#0001` in a comment on r/Gta5Modding about being a mod menu staff member. No keyword like "discord", "add me", or "@" appeared near it. It was buried in comment #54. Keyword searching would have missed it completely.
- Handles appear in unexpected contexts: LFG posts, commission pages, gaming discussions, arguments, bio-style comments. There is no reliable keyword set.
- Every time keyword filtering was used, we missed things. Every time we read comment by comment, we found things.

### The rule
1. **Pull the full history** (up to 300 items via Reddit API)
2. **Display every comment/post in order**, in batches of 30
3. **Read each one.** Note anything useful — platforms mentioned, links, games played, locations, ages, any detail
4. **Follow external links in Chrome** when they could lead to a profile
5. **NEVER run a script that filters comments by keywords.** Not even as a "quick scan first." Not even "just to find the links." Read them all.
6. **If you catch yourself writing `if any(x in body` or similar filtering code on a user's history, STOP. You are breaking the rule.**

This is the single most important rule in the entire project. The $5,000 handle is in comment #247 on r/crochet. You will not find it with `grep "discord"`. You will only find it by reading.
