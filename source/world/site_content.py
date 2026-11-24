"""All published copy for the Yatra Express portfolio, in RAC order (Result, Action, Context).
Every sentence maps to a row in docs/CLAIMS.md. Do not add a number here that is not in that ledger.
No em dashes: validate.py rejects them."""

LINKS = dict(
    email="sri.krishna2028@mastersunion.org",
    linkedin="https://www.linkedin.com/in/sri-krishna9/",
    github="https://github.com/emailsrikrishna9-hub",
    ph_profile="https://www.producthunt.com/@sri_krishna12",
    ph_product="https://www.producthunt.com/products/resumefit-3",
    rf_live="https://resumefit-xrme.onrender.com/",
    site="https://emailsrikrishna9-hub.github.io/sri-krishna-yatra/",
)

HERO = dict(
    kicker="Sri Krishna Taak · Masters' Union, Gurugram",
    h1="I build products and run programmes where the problem is still unclear.",
    sub="Looking for a Summer 2027 internship (March to May 2027) in Founder's Office, strategy, consulting, operations or product. Three pieces of work to start with:",
    chips=[
        dict(go=1, k="ResumeFit", v="A live AI resume tool, launched on Product Hunt in November 2026"),
        dict(go=3, k="Careers Club", v="40 events in 5 months as elected Vice President"),
        dict(go=5, k="NITI Aayog", v="Pulse price cycle diagnosed from 15 years of data"),
    ],
    photo=dict(src="assets/img/jagriti-fireside-sri-listening.jpg",
               alt="Sri Krishna Taak seated on stage during a fireside chat at Masters' Union",
               cap="Moderating a fireside chat at Masters' Union"),
)

# Each chapter is one stop. 'sub' is the line on the station board. 'biome' picks the scenery.
CHAPTERS = [
    dict(id="start", n=0, label="Start", year="Now", board="PLATFORM 0", sub="SRI KRISHNA TAAK", country="IN", mon="charminar", logos=["mu"]),

    dict(id="resumefit", n=1, label="ResumeFit", year="Nov 2026", board="RESUMEFIT", sub="LIVE, NOV 2026", country="IN", mon="skyline", logos=[],
         title="ResumeFit: a resume tool that cannot invent",
         featured=True, stamp=("RF", "NOV 26"),
         rac=[
             "ResumeFit is live. You upload a resume, paste a job posting, and it rebuilds the resume around that posting using only what you have actually done, then lists the requirements you cannot honestly claim.",
             "I designed it and built it end to end with Claude: PDF and Word import, a match report, five templates, an application tracker, and a check that throws out any AI-written line whose skill, title or number is not in your profile.",
             "AI resume tools sound impressive by adding things you do not have, and you find out in the interview.",
         ],
         proof=[("Live product", "https://resumefit-xrme.onrender.com/"), ("Product Hunt launch", "https://www.producthunt.com/products/resumefit-3")],
         thumb=dict(src="assets/work/rf-live-landing.jpg", alt="The ResumeFit home page with the headline 'A tailored resume for every job. Every line true.'",
                    cap="ResumeFit home page, captured 24 Nov 2026 (free beta)")),

    dict(id="saathi", n=2, label="Saathi", year="2026", board="SAATHI", sub="LAUNCHLAB WINNER", country="IN", mon="temple", logos=[],
         title="Saathi: one shared record for a parent's care",
         featured=False, stamp=("SA", "2026"),
         rac=[
             "Saathi won Tetr LaunchLab and its US$300 cash prize.",
             "I built the first version in Lovable as an AI tool that extracts data from documents for elder care, then rebuilt the idea as a Phase 1 prototype: family spaces with owner, editor and viewer roles, a medicine list, and a review-and-confirm step before any extracted value is saved.",
             "It is built for families who manage a parent's care from another city or country. It is a prototype with demo data, not a launched product.",
         ],
         proof=[("Resume entry", "resume.pdf"), ("Source: private repo, demo on request", "")],
         thumb=None),

    dict(id="careers-club", n=3, label="Careers Club", year="2026", board="CAREERS CLUB", sub="MASTERS' UNION", country="IN", mon="skyline", logos=["mu"],
         title="Careers Club: 40 events in five months",
         featured=True, stamp=("CC", "2026"),
         rac=[
             "During my term as elected Vice President, the Careers Club delivered 40 events in 5 months across 13 clubs on a ₹25 lakh budget, including three full-day hackathons (two on AI) and 400,000+ impressions.",
             "I was elected to the role, and I also served on the Growth Team in the Director's Office, where I designed strategies for organising hackathons for the Bharat Builders Prize.",
             "That prize is a national, three-round AI competition with a ₹10 lakh winner's prize.",
         ],
         proof=[("Resume entry", "resume.pdf")],
         thumb=None),

    dict(id="akshaya-patra", n=4, label="Akshaya Patra", year="Jun 2024", board="AKSHAYA PATRA", sub="AHMEDABAD, JUN 2024", country="IN", mon="mosque", logos=["akshaya"],
         title="Akshaya Patra: tracking 700+ assets with QR",
         featured=False, stamp=("AP", "JUN 24"),
         rac=[
             "I built a QR asset-tracking automation that The Akshaya Patra Foundation adopted. I projected it would save 120+ staff-hours a year; that figure is a projection, not a measured saving.",
             "As Operations Intern in Ahmedabad, I first verified 700+ assets worth ₹20+ crore by reviewing the foundation's operational inventory, then built the AI-enabled QR system around that list.",
             "The inventory had to be verified before it could be tracked, and the QR system is what keeps it tracked.",
         ],
         proof=[("Resume entry", "resume.pdf")],
         thumb=None),

    dict(id="niti-aayog", n=5, label="NITI Aayog", year="Aug to Oct 2024", board="NITI AAYOG", sub="NEW DELHI, 2024", country="IN", mon="indiagate", logos=["niti"],
         title="NITI Aayog: why pulse prices swing",
         featured=True, stamp=("NA", "OCT 24"),
         rac=[
             "I diagnosed a cobweb price cycle in India's pulses market and recommended a stable, multi-year trade policy with periodic reviews and strategic reserves.",
             "As Policy Research Intern in New Delhi, I analysed 15 years of production, import and price data, including ₹28,523 crore of peak imports and landed price against MSP, and linked CPI swings from +25% in 2014 to -19% in 2016 to reactive trade curbs.",
             "Pulse prices kept swinging, and trade policy reacted to each swing instead of smoothing it. This was internship research; adoption of the recommendation is not claimed.",
         ],
         proof=[("Resume entry", "resume.pdf")],
         thumb=None),

    dict(id="field-notes", n=6, label="Field notes", year="2023 to 2025", board="FIELD NOTES", sub="NAGAUR TO IIM-A", country="IN", mon="fort", logos=["ted", "jagriti"],
         title="Field notes: how I run things off-campus",
         featured=False, stamp=("FN", "2024"),
         rac=[
             "I have run three projects where the plan meets the ground: Shodh Yatra, a 140-km expedition across 12 villages; TEDxIIS, the institute's first TEDx, for 250+ attendees; and Jagriti Yatra, an 8,000-km entrepreneurship journey I joined on a ₹70,000 scholarship.",
             "As Shodh Yatra's Project Lead I coordinated logistics with the district administration and police and ran a ₹3 lakh rural-innovation programme with 20+ stakeholder engagements, then presented the learnings at ICCG 5, IIM Ahmedabad. For TEDxIIS I secured the TED licence and led a 30-member team.",
             "Shodh Yatra was SRISTI's 51st, in Nagaur in June 2024; TEDxIIS was in December 2023. Resume only: a self-funded solo trip through all 28 Indian states on ₹80,000.",
         ],
         proof=[("Resume entries", "resume.pdf")],
         thumb=dict(src="assets/img/shodh-iima-podium.jpg", alt="Sri Krishna speaking at a podium at IIM Ahmedabad",
                    cap="Presenting Shodh Yatra learnings at ICCG 5, IIM Ahmedabad, January 2025")),

    dict(id="harvard-iift", n=7, label="Harvard and IIFT", year="2025 to 2026", board="HARVARD", sub="BOSTON, FEB 2025", country="US", mon="harvard", logos=["harvard", "iift"],
         title="Harvard and IIFT: competing outside the classroom",
         featured=False, stamp=("HV", "FEB 25"),
         rac=[
             "I won Round 1 of the HPAIR Impact Challenge at Harvard in February 2025 with a financial model for a Nairobi slum school, against delegates from 40+ countries. My team placed 3rd among 100+ B-school teams at The Policy Gazette 2026, hosted by IIFT Delhi, analysing AI policy issues for Praxis.",
             "I crowdfunded the cost of attending HPAIR after I was selected to go.",
             "HPAIR is a student conference at Harvard. The Policy Gazette is a B-school policy competition.",
         ],
         proof=[("Resume entries", "resume.pdf")],
         thumb=dict(src="assets/img/hbs-harvard-business-school.jpg", alt="Sri Krishna standing in front of the Harvard Business School sign",
                    cap="At Harvard Business School during HPAIR")),

    dict(id="contact", n=8, label="Next stop", year="Summer 2027", board="NEXT STOP", sub="A PROBLEM TO SOLVE", country="IN", mon="sunrise", logos=[],
         title="Bring me a messy, specific problem",
         featured=False, stamp=("GO", "2027"),
         rac=[
             "I am looking for a Summer 2027 internship, March to May 2027, where I can own one unclear problem inside a Founder's Office, strategy, operations or product team.",
             "If you are hiring, or you have a problem like that, send me the problem and a time that suits you. I will reply with how I would start.",
         ],
         proof=[], thumb=None, contact=True),
]

# Deeper write-ups for the three featured stops. Blocks: h (heading), p (paragraphs), ul, fig, timeline, svg, nums.
CASES = {
    "resumefit": dict(
        title="ResumeFit: a resume tool that cannot invent",
        meta=[("Role", "Founder and builder"), ("Built with", "Claude (AI-assisted development)"), ("Status", "Live, free during the beta")],
        lead="ResumeFit is a live web app that rebuilds a resume around one job posting using only what the user has done, and reports the requirements they cannot honestly claim. I designed it, built it with Claude, and launched it on Product Hunt in November 2026.",
        blocks=[
            dict(h="What I built", p=[
                "Sign-up with email confirmation, PDF and Word resume import into a structured profile, a tailoring pipeline, a match report, five resume templates with layout controls, chat refinement, an application tracker, and a free keyword checker that needs no account.",
                "I built it through AI-assisted development with Claude."]),
            dict(h="The rule, enforced three times", ul=[
                "The prompt lets the model cite only fact ids it was given, and every number must appear in a cited fact.",
                "A validator drops bullets without valid citations, restores your own wording when a number was invented, removes skills that are not in your profile, and turns unsupported matches into gaps.",
                "The database re-checks every citation before a version is saved."],
                note="From the project README. The repository is private, so this is documented, not publicly inspectable."),
            dict(fig=dict(src="assets/work/rf-rejected-claim.jpg", alt="Two cards: 'What you wrote: Managed a budget of $4.5K' and an AI rewrite with $4.5M struck out and stamped Rejected, number changed",
                          cap="Product Hunt launch graphic with sample text. It illustrates the rule; it is not a real user's resume.")),
            dict(fig=dict(src="assets/work/rf-app-doc.jpg", alt="The ResumeFit app showing a tailored one-page resume for a fictional finance analyst",
                          cap="The app's resume view with a fictional profile and test data, captured before the free beta.")),
            dict(h="The pricing decision", timeline=[
                ("7 Nov", "First commit. A $4, 30-day pass was part of the design."),
                ("About 12 Nov", "Product Hunt launch. My maker comment said one free preview, then $4 for 30 days, no subscription."),
                ("14 Nov", "Commit: pause payments, everything free for now."),
                ("24 Nov", "Live site: everything free during the beta, with fair-use limits."),
            ], p=["The $4 pass did not convert, so I paused payments and made the product free to learn from real use. The reason is as I stated in my LinkedIn post; the dates come from the repository history and the live pages."]),
            dict(h="What I learned", p=[
                "Shipping was the easy half. Whether people need it is the open question, and the free beta exists to answer it. I do not have traction numbers worth quoting yet, and a Product Hunt listing shows that it shipped, not that it works as a business."]),
        ],
        proof=[("Open ResumeFit", "https://resumefit-xrme.onrender.com/"), ("Product Hunt page", "https://www.producthunt.com/products/resumefit-3"), ("Maker profile", "https://www.producthunt.com/@sri_krishna12")],
    ),
    "careers-club": dict(
        title="Careers Club: 40 events in five months",
        meta=[("Role", "Elected Vice President; Growth Team intern"), ("Where", "Masters' Union, Gurugram")],
        lead="During my term as elected Vice President, the Careers Club delivered 40 events in 5 months across 13 clubs on a ₹25 lakh budget, including three full-day hackathons (two on AI), and generated 400,000+ impressions.",
        blocks=[
            dict(nums=[("40", "events in 5 months"), ("13", "clubs"), ("3", "full-day hackathons, 2 on AI"), ("400,000+", "impressions"), ("₹25 lakh", "budget")],
                 cap="Figures as listed on my resume. The event pages are not public."),
            dict(h="What I did", p=[
                "I was elected to the Vice President role. Separately, I served on the Growth Team in the Director's Office for the Bharat Builders Prize, a national, three-round AI competition with a ₹10 lakh winner's prize, where I designed strategies for organising hackathons.",
                "I was also Lead Organiser of Prompts to Profit, an AI hackathon that drew 412 unique registrants across 236 teams and 86 organisations. Those are the event's totals, delivered by an organising team, not a personal result."]),
            dict(h="Whose numbers these are", p=[
                "The 40 events, 13 clubs, budget and impressions describe what the club delivered during my term, with a student team. They do not measure my individual contribution, which I would rather walk you through than assert here."]),
        ],
        proof=[("Resume (PDF)", "resume.pdf")],
    ),
    "niti-aayog": dict(
        title="NITI Aayog: why pulse prices swing",
        meta=[("Role", "Policy Research Intern"), ("When", "Aug to Oct 2024, New Delhi"), ("Status", "Completed internship")],
        lead="I diagnosed a cobweb price cycle in India's pulses market and recommended a stable, multi-year trade policy with periodic reviews and strategic reserves to stabilise prices.",
        blocks=[
            dict(nums=[("15 years", "of production, import and price data"), ("₹28,523 crore", "peak imports"), ("+25% to -19%", "CPI swing, 2014 to 2016")],
                 cap="Figures as listed on my resume. The dataset belongs to the project and is not published."),
            dict(h="What I did", p=[
                "I analysed 15 years of production, import and price data, set landed price against MSP, and traced how CPI swings from +25% in 2014 to -19% in 2016 lined up with reactive trade curbs. From that I recommended a stable, multi-year trade policy, reviewed periodically and backed by strategic reserves."]),
            dict(svg="cobweb", cap="Concept diagram I drew to explain the mechanism. It is an illustration, not NITI Aayog data."),
            dict(h="The problem", p=[
                "A high price pushes farmers to plant more and pushes government toward import relief. A glut follows and prices fall. Farmers cut back, supply tightens, and the cycle repeats. When trade curbs react to each swing, they can feed the cycle instead of damping it."]),
            dict(h="What I do not claim", p=[
                "This was internship research. I do not claim the recommendation was adopted. A completion letter dated 27 Dec 2024 exists, but it carries personal contact details and is not published until a redacted copy exists."]),
        ],
        proof=[("Resume (PDF)", "resume.pdf")],
    ),
}

RESUMES = [("Main resume (PDF)", "resume.pdf"), ("Founder's Office version", "resume-founders-office.pdf"), ("Consulting version", "resume-consulting.pdf")]
