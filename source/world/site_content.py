"""All published copy for the Founder's Office portfolio, in RAC order (Result, Action, Context).
Every sentence maps to a row in docs/CLAIMS.md. Change a result or add a proof asset here, then rebuild.
No em dashes: scripts/validate_world.py rejects them."""

LINKS = dict(
    email="sri.krishna2028@mastersunion.org",
    linkedin="https://www.linkedin.com/in/sri-krishna9/",
    github="https://github.com/emailsrikrishna9-hub",
    ph_profile="https://www.producthunt.com/@sri_krishna12",
    ph_product="https://www.producthunt.com/products/resumefit-3",
    rf_live="https://resumefit-xrme.onrender.com/",
    unstop="https://unstop.com/college-fests/caseunion-40-masters-union-school-of-business-519098",
    site="https://emailsrikrishna9-hub.github.io/sri-krishna-yatra/",
)

HERO = dict(
    kicker="Sri Krishna Taak · Masters' Union, Gurugram",
    h1="I build the first version, bring people together, and move the work forward.",
    sub=("From a Cairo agency and rural field operations to AI prototypes and a national case competition, "
         "I've worked across product, growth, research, and execution. I'm looking for a Founder's Office "
         "internship where that range is useful."),
    entries=[
        dict(go=5, k="Built products", v="ResumeFit and Saathi"),
        dict(go=7, k="Led execution", v="Careers Club and CaseUnion"),
        dict(go=1, k="Worked in the field", v="Icon Creations, government, nonprofit, Shodh Yatra"),
    ],
    start=dict(go=1, label="Start in Cairo"),
    photo=dict(src="assets/img/jagriti-fireside-sri-listening.jpg",
               alt="Sri Krishna Taak seated on stage during a fireside chat at Masters' Union",
               cap="Moderating a fireside chat at Masters' Union"),
)

# kind: single (one item) or group (accordion of items). The chronological journey starts at Icon Creations.
CHAPTERS = [
    dict(id="start", n=0, label="Start", year="Now", board="PLATFORM 0", sub="SRI KRISHNA TAAK", country="IN", mon="charminar", logos=["mu"], biome=0),

    dict(id="icon-creations", n=1, label="Icon Creations", year="2023", board="CAIRO", sub="ICON CREATIONS, 2023", country="EG", mon="pyramids", logos=["icon"], biome=1,
         title="Cairo: where the journey starts", stamp=("IC", "2023"), items=[
             dict(name="Icon Creations", when="Cairo, Jun to Jul 2023", logos=["icon"],
                  r="Recognized as a top-performing intern in a six-week paid placement.",
                  a="Created social content, copy, articles, and research for the agency.",
                  c="My first international operating role, at Icon Creations in Cairo.",
                  src="Source: Icon Creations experience letter and paid-internship certificate (documents held privately)"),
         ]),

    dict(id="campus-government", n=2, label="Government and campus", year="2023 to 2024", board="AHMEDABAD", sub="CAMPUS AND DISTRICT", country="IN", mon="mosque", logos=["telangana", "aiesec", "ted"], biome=4,
         title="Government and campus, 2023 to 2024", stamp=("GC", "2023"), items=[
             dict(name="Collector's Office", when="Narayanpet, Aug to Sep 2023", logos=["telangana"],
                  r="Helped connect 200+ citizens with officials across four grievance sessions.",
                  a="Supported Prajavani sessions and visited 50 public-service sites.",
                  c="Field execution inside district administration in Telangana.",
                  src="Source: résumé"),
             dict(name="AIESEC Ahmedabad", when="Aug 2023 to Jul 2024", logos=["aiesec"],
                  r="Helped secure 10+ exchange approvals and earned Best Team Leader and Best Team recognition.",
                  a="Built international relationships and worked on recruitment and onboarding.",
                  c="A year in a student-run international organization.",
                  src="Source: résumé and AIESEC Ahmedabad experience letter"),
             dict(name="TEDxIIS", when="Dec 2023", logos=["ted"],
                  r="Helped deliver the institute's first TEDx for 250+ attendees.",
                  a="Secured the licence and worked across speakers, sponsorships, and a 30-person organizing team.",
                  c="An event built from the ground up at Gujarat University.",
                  src="Source: résumé; team figures are the team's",
                  thumb=dict(src="assets/work/tedx-team.jpg", alt="The TEDxIIS organizing team standing beside the lit TEDxIIS sign",
                             cap="The TEDxIIS organizing team")),
         ]),

    dict(id="field-research", n=3, label="Field and research", year="2024", board="NAGAUR TO DELHI", sub="FIELD, NONPROFIT, POLICY", country="IN", mon="fort", logos=["akshaya", "niti"], biome=6,
         title="Field and research, 2024", stamp=("FR", "2024"), items=[
             dict(name="Shodh Yatra", when="Rajasthan, Jun 2024", logos=[],
                  r="Helped run a 140 km field journey through 12 villages.",
                  a="Coordinated accommodation, the route, local authorities, and 20+ meetings.",
                  c="Rural innovation work with SRISTI and a diverse volunteer team.",
                  src="Source: résumé, SRISTI certificates and the ICCG 5 photo",
                  thumb=dict(src="assets/work/iccg5-podium.jpg", alt="A speaker at the podium on the stage of the Fifth International Conference on Creativity and Innovation at Grassroots (ICCIG 5) at IIM Ahmedabad, January 2025",
                             cap="Presenting Shodh Yatra learnings at ICCG 5, IIM Ahmedabad, 28 to 30 Jan 2025")),
             dict(name="Akshaya Patra", when="Ahmedabad, Jun 2024", logos=["akshaya"],
                  r="Verified 700+ assets valued at ₹20+ crore.",
                  a="Reviewed the inventory and developed a QR-based tracking approach.",
                  c="An asset-verification internship in nonprofit operations.",
                  src="Source: résumé (figures); completion certificate, 1 to 30 Jun 2024"),
             dict(name="NITI Aayog", when="New Delhi, Aug to Oct 2024", logos=["niti"],
                  r="Produced a research recommendation on pulse-market volatility.",
                  a="Analysed production, import, and price data and compared policy choices.",
                  c="A policy research internship focused on agricultural trade.",
                  src="Source: résumé. Research output; adoption is not claimed"),
         ]),

    dict(id="competing", n=4, label="Competing and organising", year="2025 to 2026", board="HARVARD", sub="BOSTON, FEB 2025", country="US", mon="harvard", logos=["harvard", "mu"], biome=9,
         title="Competing and organising, 2025 to 2026", stamp=("CO", "2025"), items=[
             dict(name="HPAIR Impact Challenge", when="Harvard, Feb 2025", logos=["harvard"],
                  r="Won Round 1 of the HPAIR Impact Challenge on 9 February 2025.",
                  a="Built a finance model for slum schools in Nairobi.",
                  c="A conference competition with participants from 40+ countries. The HPAIR letter confirms the first round only.",
                  src="Source: résumé and HPAIR letter",
                  thumb=dict(src="assets/img/hbs-harvard-business-school.jpg", alt="Sri Krishna standing in front of the Harvard Business School sign",
                             cap="At Harvard Business School during the HPAIR conference")),
             dict(name="Prompts to Profit", when="Hackathon", logos=[],
                  r="Led an AI hackathon with 412 unique registrants, 236 teams, and 86 organizations.",
                  a="Organised the event as Lead Organiser.",
                  c="The figures are event totals from my résumé, not a personal result.",
                  src="Source: résumé"),
             dict(name="Soft Launch", when="Venture", logos=[],
                  r="Generated ₹1 lakh+ in team revenue.",
                  a="Co-built a six-person commerce operation using Shopify, Razorpay, and Shiprocket.",
                  c="A hands-on entrepreneurial experiment. The revenue is the team's, not mine.",
                  src="Source: résumé"),
             dict(name="Bharat Builders Prize", when="Growth team", logos=["mu"],
                  r="Served on the growth team for a national AI competition.",
                  a="Designed strategies for organising hackathons.",
                  c="A role in the Masters' Union Director's Office. The ₹10 lakh was the winner's prize, not mine.",
                  src="Source: résumé"),
         ]),

    dict(id="resumefit", n=5, label="ResumeFit", year="2026", board="RESUMEFIT", sub="BUILT AND LAUNCHED", country="IN", mon="skyline", logos=[], biome=10,
         title="ResumeFit: a résumé tool that cannot invent", stamp=("RF", "NOV 26"), items=[
             dict(name="ResumeFit", when="Built and launched, Nov 2026", logos=[], more="resumefit",
                  r="Built and launched an AI-assisted résumé-tailoring web app.",
                  a="Developed document parsing, job matching, five templates, an application tracker, and a guardrail against invented experience.",
                  c="A personal product build to make role-specific applications easier. I have since left the project.",
                  proof=[("Live product (first load may take up to a minute)", "https://resumefit-xrme.onrender.com/"), ("Product Hunt listing", "https://www.producthunt.com/products/resumefit-3")],
                  thumb=dict(src="assets/work/rf-live-landing.jpg", alt="The ResumeFit home page with the headline 'A tailored resume for every job. Every line true.'",
                             cap="ResumeFit home page, captured 24 Nov 2026")),
         ]),

    dict(id="saathi", n=6, label="Saathi", year="2026", board="SAATHI", sub="PROTOTYPE", country="IN", mon="temple", logos=[], biome=2,
         title="Saathi: a care-coordination prototype", stamp=("SA", "2026"), items=[
             dict(name="Saathi", when="Prototype, 2026", logos=[],
                  r="Won First Prize at Tetr LaunchLab, a 3-day startup sprint, with a working Saathi prototype and a US$300 cash prize.",
                  a="Prototyped a way for families to organize healthcare documents and care information.",
                  c="A personal healthcare coordination experiment, judged on distribution, marketing strategy and execution. I have since left the project.",
                  src="Source: Tetr LaunchLab certificate, issued 8 May 2026",
                  thumb=dict(src="assets/work/tetr-certificate.jpg", alt="Tetr LaunchLab Certificate of Achievement awarding Sri Krishna First Prize in a 3-day startup sprint, with a 300 US dollar cash prize, issued 8 May 2026",
                             cap="Tetr LaunchLab certificate, 8 May 2026")),
         ]),

    dict(id="caseunion", n=7, label="CaseUnion and Careers Club", year="Nov 2026", board="CASEUNION 4.0", sub="MASTERS' UNION", country="IN", mon="indiagate", logos=["mu"], biome=7,
         title="CaseUnion 4.0: a national case competition", stamp=("CU", "NOV 26"), items=[
             dict(name="CaseUnion 4.0 and Careers Club", when="Nov 2026, finale 12 Dec", logos=["mu"], more="caseunion",
                  r="Helped grow CaseUnion 4.0 to 3,800+ registrations by 23 November 2026.",
                  a="As VP Careers, coordinated clubs, partner outreach, and campus teams, and secured ₹4 lakh in sponsorship and ₹3 lakh in kind.",
                  c="A team-run national case competition at Masters' Union, and the school's first collaboration with Harvard (as content partner).",
                  proof=[("Event page on Unstop", "https://unstop.com/college-fests/caseunion-40-masters-union-school-of-business-519098")],
                  thumb=dict(src="assets/work/cu-event-cover.jpg", alt="CaseUnion 4.0 event banner: National Business Case Competition, finale 12 December 2026, prize pool 5 lakh rupees, with partner logos and their roles",
                             cap="Event creative with the finale date and partner roles")),
         ]),

    dict(id="contact", n=8, label="Next stop", year="Mar to May 2027", board="NEXT STOP", sub="A PROBLEM TO MOVE", country="IN", mon="sunrise", logos=[], biome=8,
         title="Bring me an unclear problem", stamp=("GO", "2027"), contact=True, items=[
             dict(name="Founder's Office internship", when="March to May 2027", logos=[],
                  r="I am looking for a Founder's Office internship, March to May 2027.",
                  a="I would like to own one unclear problem and move it forward with your team.",
                  c="If you are hiring, or have a problem like that, send me the problem and a time that suits you."),
         ]),
]

# Longer write-ups for the two featured stories. Blocks: h, p, ul, fig, timeline, nums.
CASES = {
    "caseunion": dict(
        title="CaseUnion 4.0: a national case competition",
        meta=[("Role", "VP Careers"), ("Where", "Masters' Union, Gurugram"), ("Dates", "Festival 15 Nov to 14 Dec 2026; finale 12 Dec")],
        lead="Helped grow CaseUnion 4.0 to 3,800+ registrations by 23 November 2026. This is a dated snapshot while registration was open, not a final outcome, and it is the team's result.",
        blocks=[
            dict(fig=dict(src="assets/work/cu-entries-strip.jpg", alt="Crop of the CaseUnion 24 Hours Left creative: 3,800+ entries from IIMs, IITs and NITs, with Aerostar Helmets as co-powering sponsor, Harvard Business Impact as content partner, and Thinking Spree, Jagriti Yatra and Ditto by Finshots as case partners",
                          cap="Crop of the 23 Nov 2026 event creative. The partner labels are the creative's own.")),
            dict(h="What I did", p=[
                "As VP Careers, I coordinated student clubs, partner outreach, and campus teams, and secured ₹4 lakh in sponsorship and ₹3 lakh in kind. The creative lists me as the registration contact, as CaseUnion Head and VP Careers. The registrations, the partners and the competitions belong to the whole team."]),
            dict(h="What the figures are", ul=[
                "3,800+ is the entry count on the event creative of 23 Nov 2026. The Unstop event page showed 4,745 registrations when I read it on 25 Nov 2026, after registrations closed on 23 Nov. Both are snapshots; the finale is on 12 Dec.",
                "₹4 lakh in sponsorship and ₹3 lakh in kind are the amounts I secured across partners, as I state them. They are separate from the ₹5 lakh, which is the festival's prize pool and not mine.",
                "Harvard Business Impact is labelled as content partner on the creative. It is not a title partnership. I describe it as the school's first collaboration with Harvard; other partner roles are as the creative labels them."]),
            dict(h="Speaking", p=[
                "I was invited to speak about case competitions and careers at Ramaiah University's Arthabodha Economics Club (online, 30 Sep 2026) and at Fetch-a-thon 3.0 at Masters' Union (11 Oct 2026, as VP Careers)."],),
            dict(fig=dict(src="assets/work/fetchathon-speaker.jpg", alt="Fetch-a-thon 3.0 speaker poster: Sri Krishna, VP Careers, Masters' Union, 11 October 2026, 10 AM to 2 PM, Masters' Union Gurugram",
                          cap="Fetch-a-thon 3.0 speaker poster, 11 Oct 2026")),
            dict(h="Separate from CaseUnion", p=[
                "As elected Vice President, I was also part of the broader Careers Club term: 40 events in 5 months across 13 clubs on a ₹25 lakh budget, including three full-day hackathons (two on AI) and 400,000+ impressions. These are club figures from my résumé, not part of the CaseUnion count and not a personal result."]),
        ],
        proof=[("Event page on Unstop", "https://unstop.com/college-fests/caseunion-40-masters-union-school-of-business-519098")],
    ),
    "resumefit": dict(
        title="ResumeFit: a résumé tool that cannot invent",
        meta=[("Role", "Builder"), ("Built with", "Claude (AI-assisted development)"), ("Status", "I have since left the project. The site is still online.")],
        lead="ResumeFit rebuilds a résumé around one job posting using only what the user has done, and reports the requirements they cannot honestly claim. I built it with Claude and launched it in November 2026. I have since left the project.",
        blocks=[
            dict(h="What I built", p=[
                "Sign-up with email confirmation, PDF and Word résumé import into a structured profile, a tailoring pipeline, a match report, five résumé templates, chat refinement, an application tracker, and a free keyword checker that needs no account."]),
            dict(h="The guardrail, enforced three times", ul=[
                "The prompt lets the model cite only fact ids it was given, and every number must appear in a cited fact.",
                "A validator drops bullets without valid citations, restores your own wording when a number was invented, removes skills that are not in your profile, and turns unsupported matches into gaps.",
                "The database re-checks every citation before a version is saved."],
                note="From the project README. The repository is private, so this is documented, not publicly inspectable."),
            dict(fig=dict(src="assets/work/rf-rejected-claim.jpg", alt="Two cards: 'What you wrote: Managed a budget of $4.5K' and an AI rewrite with $4.5M struck out and stamped Rejected, number changed",
                          cap="Product Hunt launch graphic with sample text. It illustrates the rule; it is not a real user's résumé.")),
            dict(fig=dict(src="assets/work/rf-app-doc.jpg", alt="The ResumeFit app showing a tailored one-page résumé for a fictional finance analyst",
                          cap="The app's résumé view with a fictional profile and test data.")),
            dict(h="A product decision", timeline=[
                ("7 Nov 2026", "First commit. A $4, 30-day pass was part of the design."),
                ("About 12 Nov", "Product Hunt launch with one free preview, then $4 for 30 days."),
                ("14 Nov", "I paused payments and made the product free during the beta."),
            ], p=["I made it free because the paid pass was not converting. The dates come from the commit history. The Product Hunt listing shows that it shipped; I have no paying users or traction numbers to report."]),
        ],
        proof=[("Open ResumeFit (first load may take up to a minute)", "https://resumefit-xrme.onrender.com/"), ("Product Hunt listing", "https://www.producthunt.com/products/resumefit-3")],
    ),
}
