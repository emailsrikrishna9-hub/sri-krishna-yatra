# Source coverage log (24 Nov 2026)

What was actually opened, how, and what could not be reached. "Read" means the content was seen in this session. Nothing below is claimed as reviewed unless it says Read.

| Source | How accessed | Result |
|---|---|---|
| Live portfolio (GitHub Pages, `sri-krishna-yatra`) | Opened earlier in this project; code, builder and styles read in full | Read |
| Repository `sri-krishna-yatra` (public) | Holds build output only; the source (`world/`, `content/`, `assets/`) read locally | Read |
| Drive folder `resumes` (link you gave) | In-app browser, public link. 10 sub-folders listed, each holds a .docx and a .pdf | Listed all. **Text read: Main, Consulting, Founder's Office** (local copies of the Drive PDFs, diffed against each other). **Not text-read: Sales, Operations, AI, Marketing, B2B, Product Management, E-commerce** (the Drive connector cannot see these files and I did not download them) |
| Second Drive folder, "Resumes generated so far (review copy)" | Drive connector | Opened. It holds resumes for **a different person** (Aman Tulsyan), so none of it was used. Check this is the folder you meant |
| Drive file `sankalp_sri_krishna` (Google Slides) | Drive connector | Read. A competition pitch (a proposal, not shipped work). Its figures conflict with the resumes (60+ years vs 15 years of NITI data; IIM Calcutta rank 17 of 596 vs 17 of 10,000+). Not used on the site |
| Drive, other files | Drive connector search for your name | Only the deck above surfaced |
| LinkedIn profile and recent activity | In-app browser | **Mostly inaccessible** (sign-in wall). One logged-out view rendered: 11K followers, 500+ connections, and the opening of a CaseUnion 4.0 post (truncated). Posts, the pricing post and original-post text were **not readable** |
| GitHub profile | In-app browser + `gh` | Read. 4 public repos: `sri-krishna-yatra`, `sri-krishna-cars24`, `sri-krishna-postcard` (empty), `TEST` |
| GitHub private repos | `gh` (your own login) | Read for `resumefit` (README, 38 commits, docs images, launch graphics) and `saathi-app` (README, 5 commits). Searched all repos for CaseUnion and Careers Club mentions; read only the matching README lines |
| Product Hunt profile `@sri_krishna12` | In-app browser | Read |
| Product Hunt `/products/resumefit-3` | In-app browser | Read: launched about 12 days before 24 Nov, 3 upvotes, 12 followers, 0 reviews, your maker comment |
| ResumeFit live site | In-app browser + headless Chrome screenshot | Read and captured 24 Nov 2026. States "free during the beta" |
| Instagram | Not requested this round | Not opened. Two photos from the earlier pass (Harvard sign, Shodh certificate) came from your Instagram then |
| Claude in Chrome | Extension | Not connected, so LinkedIn could not be read through your signed-in browser |
| Existing photo and certificate pack | Local files from the earlier pass | Re-used only items with captions that say what they show |

## Not done
Real-phone, Safari and Firefox testing. Screen-reader testing with a real screen reader (structure and live-region checks only).
