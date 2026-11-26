"""The Aideation course catalog: every course the site offers, and the roles a person can join one in.

One course today. A new course is one more entry here (and, later, its own repository that builds its own page).
"""

BRAND = {
    "name": "Aideation",
    "parent": "A Boyer company",
    "tagline": "Learn to build AI that acts — and that you can trust.",
    "logo": "brand/aideation-logo.webp",
    "mark_lg": "brand/aideation-mark-lg.webp",
    "mark": "brand/aideation-mark.png",
    "favicon": "brand/favicon.png",
}

# Where sign-up and log-in go. Empty until the Aideation API is deployed (Render); the site then
# explains that accounts open soon and that everything is open without one.
API_BASE = ""

# Who you are decides what you can see. Instructors are approved by hand and must use a second factor.
ROLES = [
    {"id": "student", "name": "Student", "who": "I'm taking the course for credit",
     "gets": ["Every track, reading, and practice check", "Progress saved across devices", "Lab and project briefs"]},
    {"id": "explorer", "name": "Explorer", "who": "I'm learning on my own",
     "gets": ["Every track, reading, and practice check", "Progress saved across devices", "No deadlines, no grades"]},
    {"id": "instructor", "name": "Instructor", "who": "I want to teach or adopt the course",
     "gets": ["Everything students see", "The instructor's guide: scripts, outlines, question banks", "Course repository access, after approval"],
     "note": "Approved by hand · passkey or authenticator app required"},
]

COURSES = [
    {
        "id": "csci391", "code": "CSCI 391", "page": "csci391.html",
        "title": "Agentic Artificial Intelligence",
        "blurb": "Design, build, and operate AI agents that reason, plan, use tools, remember, and know when to stop.",
        "kind": "Course", "level": "Intermediate", "length": "15 weeks", "subject": "Computer science · Artificial intelligence",
        "partner": "Piloted at the University of Montana",
        "cover": "curriculum/img/encore-ensemble-cover.webp",
        "overview": "overview",          # the course-level overview track
        "map": "curriculum/img/overview-board.pdf",
        "skills": ["AI agents", "Tool use", "Agent memory", "Planning", "MCP", "Multi-agent systems", "Human oversight", "Evaluation", "Guardrails"],
        "badges": ["Free", "New"],
    },
]
