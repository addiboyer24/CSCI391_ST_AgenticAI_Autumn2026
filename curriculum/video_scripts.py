"""Scripts for the robot-narrated "Encore Lectures".

Written from the instructor's lecture notes and class recordings, then fully
re-scripted so that no student name, voice, face, question, or presentation
appears. Narration is synthetic (Windows TTS); the on-screen lecturer is
"Encore", a robot modeled on the course's Encore Ensemble artwork.

Scene types: title | bullets | quote | image   (each has "lines" = narration, one sentence per item)
Rebuild with:  python curriculum/build_videos.py [module ids]
"""

# Narration voices viewers can pick on the site. The first is the default (files <id>.mp4 / <id>.vtt);
# others render to <id>-<voice id>.mp4 / .vtt. Engines are Windows System.Speech voice names.
VOICES = [
    {"id": "david", "name": "David", "engine": "Microsoft David Desktop"},
    {"id": "zira", "name": "Zira", "engine": "Microsoft Zira Desktop"},
]


def media_stem(lec_id, voice):
    return lec_id if voice["id"] == VOICES[0]["id"] else f"{lec_id}-{voice['id']}"


LECTURES = [
    {
        "id": "m01", "track": "Track 01", "name": "Opening Act",
        "module": "What Is an AI Agent?", "chapters": "Chapter 1",
        "scenes": [
            {"type": "title", "lines": [
                "Hi, I'm Encore, your lecturer for this course, and this is track one: Opening Act.",
                "Before we build a single agent, we need to agree on what an agent actually is, and what it isn't.",
            ]},
            {"type": "quote", "kicker": "Opening case", "quote": "They hadn't built an agent. They'd built a chatbot with write access to a database.", "lines": [
                "A mid-sized software company shipped what its marketing team called an autonomous refund agent.",
                "It worked for a small set of low-risk products. Then came a routine model update.",
                "The new model was better at fuzzy matching, and its product lookup tool read from a stale catalog.",
                "So it cheerfully approved refunds for items the company had never sold.",
                "They rolled it back that afternoon. The postmortem took months.",
            ]},
            {"type": "bullets", "kicker": "Working definition", "heading": "An agentic AI system…",
             "bullets": ["Is given a goal in natural language", "Chooses its own next action from a set of tools", "Executes it against an external environment", "Observes the result and repeats — until done or it gives up"], "lines": [
                "Here's our working definition.",
                "An agentic system is given a goal in natural language.",
                "It chooses its own next action from a set of tools, and executes that action against an external environment.",
                "Then it observes the result, and repeats the cycle until it judges the goal is met, or gives up.",
            ]},
            {"type": "bullets", "kicker": "What an agent is not", "heading": "Four common confusions",
             "bullets": ["A chatbot — RAG gives information, not agency", "RPA — scripted UI clicks; nothing decides", "A workflow engine — the workflow owns the plan", "A classical planner — a cousin, not a twin"], "lines": [
                "Four kinds of systems get confused with agents.",
                "A chatbot produces text a person reads. An agent produces actions a system executes. Retrieval gives a chatbot information, not agency.",
                "Robotic process automation drives a user interface from a script. Music comes out of a player piano, but nothing inside is deciding.",
                "A workflow engine owns its plan. An agent owns its plan. If you can draw your problem on a whiteboard as a graph, you probably want a workflow.",
                "And classical planners are serious ancestors of agents. Cousins, not twins.",
            ]},
            {"type": "bullets", "kicker": "Production failure modes", "heading": "The three horsemen",
             "bullets": ["Unbounded loops", "Confidently wrong answers", "Stubborn retries"], "lines": [
                "In production, agent incidents tend to arrive as three horsemen.",
                "Unbounded loops. Confidently wrong answers. And stubborn retries.",
                "Every production agent needs explicit termination conditions, limits, and a way to recognize when it can't safely finish the job.",
            ]},
            {"type": "quote", "kicker": "Enterprise lens", "quote": "Autonomy theater: impressive in the demo, collapses in production.", "lines": [
                "From the enterprise side, there's a name for this: autonomy theater.",
                "Systems that look autonomous in a demo, and collapse in production.",
                "It's usually not a technical failure. It's a product decision, made before anyone asked whether an agent was the right tool.",
                "So before asking, is the model good enough, ask, have we built the right thing for the problem?",
            ]},
            {"type": "image", "src": "m01-mindmap.svg", "lines": [
                "Here's today's map. Use it to review before the quiz.",
                "Next time, we'll build the smallest thing that deserves to be called an agent. See you then.",
            ]},
        ],
    },
    {
        "id": "m02", "track": "Track 02", "name": "First Riff",
        "module": "The Minimum Viable Agent & a Short History of Agents", "chapters": "Chapter 2",
        "scenes": [
            {"type": "title", "lines": [
                "Welcome back. This is track two: First Riff.",
                "We'll build the minimum viable agent, place it on a five-level ladder, and take a short, honest tour of fifty years of agent history.",
            ]},
            {"type": "quote", "kicker": "A single request", "quote": "“I ordered the blue kettle two weeks ago and it arrived dented. I'd like a refund.”", "lines": [
                "Start with one customer message about a dented kettle.",
                "A chatbot apologizes and suggests contacting support.",
                "An agent looks up the order, checks refund eligibility, issues the refund through a narrowly scoped tool, and confirms.",
                "Each step is chosen based on what it observed in the step before.",
            ]},
            {"type": "bullets", "kicker": "Minimum viable agent", "heading": "Three ingredients and a loop",
             "bullets": ["A system prompt", "A set of tools", "The user's message", "Reason → act → observe → repeat"], "lines": [
                "The minimum viable agent needs three ingredients: a system prompt, a set of tools, and the user's message.",
                "Then a loop: reason, act, observe, and reason again.",
                "Good tools each do one narrow thing, with an explicit schema.",
                "And remember: the toolset defines the agent's blast radius.",
            ]},
            {"type": "bullets", "kicker": "Five-level taxonomy", "heading": "How agentic is it, really?",
             "bullets": ["L0 Scripted automation", "L1 LLM as a text function", "L2 Tool-using LLM", "L3 Goal-directed, with planning", "L4 Adaptive, with persistent memory", "L5 Multi-agent and computer use"], "lines": [
                "Use this five-level ladder to name a system honestly.",
                "Level zero is scripted automation. No model required.",
                "Level one uses a language model as a text function. Level two adds tools.",
                "Level three adds explicit planning. Level four adds memory that persists across sessions, and with it, the risk of memory poisoning.",
                "Level five is multiple agents, or general computer use, with failure modes all its own.",
            ]},
            {"type": "bullets", "kicker": "Pitfalls", "heading": "Three traps to avoid",
             "bullets": ["Treating the LLM as ground truth", "Assuming longer thinking is better", "Confusing tool breadth with capability"], "lines": [
                "Three classic traps.",
                "Treating the model as ground truth instead of checking the system of record.",
                "Assuming that longer thinking always means better answers.",
                "And confusing a long list of tools with real capability. More tools often means more confusion.",
            ]},
            {"type": "bullets", "kicker": "A short, honest history", "heading": "Old problems, new substrate",
             "bullets": ["1971 STRIPS · 1972 SHRDLU", "Expert systems and the frame problem", "BDI: beliefs, desires, intentions", "Today: tool-using LLMs and MCP"], "lines": [
                "Following Caldwell's chapter two, very little here is brand new.",
                "STRIPS and SHRDLU, in the early seventies, already planned actions toward goals.",
                "Expert systems ran into the frame problem: knowing what doesn't change when you act.",
                "The belief, desire, intention model gave us vocabulary we still use.",
                "What changed recently is the infrastructure: models trained to use tools, and protocols to connect them.",
            ]},
            {"type": "bullets", "kicker": "From the field · Addison Boyer", "heading": "Expert systems didn't pay for themselves",
             "bullets": ["DENDRAL: molecules from mass spectrometry", "MYCIN: diagnosing bacterial infections", "Years of hand-authored knowledge", "Hard to extend, rarely broke even"], "lines": [
                "Your course designer, Addison Boyer, has a personal connection to this era.",
                "Addison's first job after graduate school was at a startup whose product ran on Lisp routines inside AutoCAD. A lot of CAD and mapping software still has Lisp under the hood.",
                "The expert systems of that lineage did impressive things. DENDRAL identified molecules from mass spectrometry data. MYCIN diagnosed bacterial infections.",
                "But each one took years of hand-authored expertise, and couldn't easily be extended to anything new.",
                "Most never broke even on the effort. That's a cost lesson worth remembering when you scope an agent today.",
            ]},
            {"type": "image", "src": "m02-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "In the enterprise world, most systems shipped at level one or two call themselves level four. Name the level honestly in your design doc.",
                "In lab, you'll build your first minimum viable agent. See you there.",
            ]},
        ],
    },
    {
        "id": "m03", "track": "Track 03", "name": "Five-Piece Band",
        "module": "The Anatomy of an Agent", "chapters": "Chapter 3",
        "scenes": [
            {"type": "title", "lines": [
                "Hi, I'm Encore, and this is track three: Five-Piece Band.",
                "Today we take an agent apart, organ by organ, and find out which one teams forget most often.",
            ]},
            {"type": "quote", "kicker": "Opening case", "quote": "The refund agent invented a refund policy instead of saying “I'm not sure.”", "lines": [
                "Remember the refund agent from our first lecture?",
                "When it wasn't confident, it didn't say so. It invented a refund policy and acted on it.",
                "That agent wasn't missing intelligence. It was missing an organ.",
                "Specifically, the termination check that would have forced it to say, I don't know, before doing anything else.",
            ]},
            {"type": "bullets", "kicker": "Chapter 3 framework", "heading": "Five parts — not four, not six",
             "bullets": ["Model — does the reasoning", "Tool set — what it can do in the world", "Memory — at minimum, a rolling context window",
                         "Loop — alternates deliberation and action", "Termination policy — knows when to stop"], "lines": [
                "Following Caldwell's chapter three, a production agent has five parts.",
                "The model does the reasoning and decides which tool to call.",
                "The tool set defines what the agent can actually do in the world, like a web search, a database query, or a calculator.",
                "Memory, at minimum, is a rolling context window, and ideally more.",
                "The loop alternates between thinking and acting.",
                "And the termination policy knows when to stop.",
                "Most framework documentation lists three or four of these. The one that usually goes missing is the last one.",
            ]},
            {"type": "image", "src": "m03-mindmap.svg", "lines": [
                "Here's the whole anatomy on one map.",
                "Notice that the model reasons and emits tool calls, but it never executes privileged operations itself.",
                "Tools take typed, validated inputs. The loop observes every result before deciding the next step.",
            ]},
            {"type": "bullets", "kicker": "From the field · Addison Boyer", "heading": "When the model invents a schema",
             "bullets": ["Tool expects one expression string", "Model sends two made-up operands", "Validate inputs before running", "Return typed, actionable errors"], "lines": [
                "Here's an example from Addison's own testing.",
                "A calculator tool accepted a single expression as a string. The model called it with two arguments, a left operand and a right operand, a schema it simply made up.",
                "So validate inputs before you run anything. Does the number of parameters even match?",
                "And when a call fails, don't hand the model a raw stack trace. Return a typed result: a success flag, and a clear message, like, customer email must be a valid email address.",
                "Your tool names and descriptions become the living documentation of your agent, so write them carefully.",
            ]},
            {"type": "bullets", "kicker": "Enterprise lens", "heading": "Make it reproducible",
             "bullets": ["Pin model versions", "Log seeds and settings", "Trace the exact messages you sent", "Termination policy in code, not prose"], "lines": [
                "Here's the enterprise lens.",
                "Production systems pin model versions, log their seeds, and keep traces of the exact messages they sent.",
                "If you can't replay a run, you can't debug it.",
                "And make the termination policy code, not prose: a step limit, a spending limit, a time limit, and an explicit way to say, I can't complete this safely.",
            ]},
            {"type": "bullets", "kicker": "Before next time", "heading": "Your turn",
             "bullets": ["Which part is most often mistaken for the whole agent?", "Design a stop condition for an agent with no natural “done”", "Lab: build the Coffee Shop Agent"], "lines": [
                "Two questions to think about.",
                "Which component is most often mistaken for the entire agent?",
                "And what does a termination policy look like for an agent that has no natural done state?",
                "In lab, you'll put all five parts together in the Coffee Shop Agent. See you there.",
            ]},
        ],
    },
    {
        "id": "m04", "track": "Track 04", "name": "Know When to Unplug",
        "module": "When Not to Build an Agent", "chapters": "Chapter 4",
        "scenes": [
            {"type": "title", "lines": [
                "This is track four: Know When to Unplug.",
                "Today's most valuable skill might be recognizing when an agent is the wrong answer.",
            ]},
            {"type": "bullets", "kicker": "Why agents get picked", "heading": "The wrong reasons",
             "bullets": ["Demo bias", "Vendor marketing", "Résumé appeal", "They feel general — like a Swiss Army knife"], "lines": [
                "Agents become the default answer for reasons that have nothing to do with the problem.",
                "They look more impressive in a demo than a simple classifier.",
                "Model providers market the products that make them money.",
                "And agent sounds great on a résumé.",
                "Agents are a Swiss Army knife. Sometimes you only need the screwdriver, but you carry the cost of the scissors and the toothpick too.",
            ]},
            {"type": "bullets", "kicker": "The decision rule", "heading": "Four questions before you build",
             "bullets": ["Is the trajectory open-ended?", "Do inputs vary beyond what a schema captures?", "Is the output space itself open?", "Is there genuine action in the world?"], "lines": [
                "Ask four questions.",
                "Is the trajectory open-ended, so you can't know the steps in advance? Research, yes. Classification, no.",
                "Do the inputs vary in ways a schema can't capture?",
                "Is the output space open, rather than one of a few labels or a fixed object?",
                "And is there genuine action in the world, interleaved with observation?",
                "If all four aren't clearly yes, stop and look for something simpler.",
            ]},
            {"type": "bullets", "kicker": "Cheaper alternatives", "heading": "Climb the ladder slowly",
             "bullets": ["Function call: input X → output Y", "Prompted classifier: cheap to build", "Fine-tuned or trained classifier: cheap to run", "Workflow engine: you own the plan"], "lines": [
                "Here's the ladder of alternatives.",
                "A single function call with structured output handles any task where input X becomes output Y, like extracting entities or summarizing an email.",
                "A prompted classifier is cheap to build but costs more to run.",
                "A fine-tuned model or a traditional classifier is expensive to build and cheap to run.",
                "And a classifier's accuracy ceiling is visible from the outside, in a confusion matrix.",
            ]},
            {"type": "bullets", "kicker": "From the field · Addison Boyer", "heading": "A healthcare workflow — not an agent",
             "bullets": ["Eligibility → enrollment → enrollment review", "Decomposed at design time", "LLMs inside steps (e.g., read an insurance card)", "No agent loop: it's orchestration"], "lines": [
                "Here's a real example from Addison's work in the healthcare industry.",
                "A program enrollment process has three steps: check eligibility, enroll, then review the enrollment.",
                "Because the steps could be decomposed at design time, it's a workflow.",
                "Models still help inside the steps. At review, one can check whether an uploaded image is really an insurance card, and extract its text.",
                "But there's no agent loop. It's a straight shot, known in advance. That's orchestration, and that's fine.",
                "Reach for an agent when the plan can only be made after the model sees the context, and you can't enumerate the possible plans.",
            ]},
            {"type": "quote", "kicker": "Enterprise lens", "quote": "Ask for ten real inputs and the ideal outputs. If the outputs have a fixed shape, it's a function call.", "lines": [
                "From the enterprise side: when someone asks for an agent, ask for ten real inputs and the outputs they want.",
                "Half the time, the outputs have a fixed shape. That's a function call, not an agent.",
                "Before switching, run both systems side by side on real traffic and review the disagreements by hand.",
                "And if breaking a rule would cause a production incident, put that rule in code or a re-injected constraint, not deep in a long prompt.",
            ]},
            {"type": "image", "src": "m04-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "Next, we open up the model itself, and the tools it calls. See you there.",
            ]},
        ],
    },
    {
        "id": "m05", "track": "Track 05", "name": "Tuning the Instrument",
        "module": "LLMs as Reasoning Engines & Tools as Contracts", "chapters": "Chapters 5–6",
        "scenes": [
            {"type": "title", "lines": [
                "This is track five: Tuning the Instrument.",
                "We'll look at the model as a reasoning engine, and the tools as contracts that decide what actually happens.",
            ]},
            {"type": "bullets", "kicker": "How tool-using models are made", "heading": "Four training stages",
             "bullets": ["Pre-training: language and world facts", "Instruction tuning: act like an assistant", "Tool-use training: know when to call a tool", "Alignment: reward accurate, safe tool use"], "lines": [
                "Today's agent models are almost always instruction-tuned language models with tool-use support.",
                "Pre-training on huge amounts of text teaches language, reasoning patterns, and facts.",
                "Instruction tuning teaches the model to act like an assistant instead of an autocomplete.",
                "Tool-use training teaches it to recognize when it lacks information and to emit a precise tool call.",
                "And alignment rewards accurate, safe tool use, and penalizes guessing.",
            ]},
            {"type": "quote", "kicker": "Big idea", "quote": "Treating the model as deterministic is the most common mistake in agent projects.", "lines": [
                "Here's the big idea.",
                "The model has implicit objectives shaped by training you didn't run and can't inspect, and the provider can update it at any time.",
                "So treat it as a black box with an interface: messages and tool definitions go in, text or a tool call comes out.",
                "Your engineering question is what you can reliably cause it to do, and what you can't.",
            ]},
            {"type": "bullets", "kicker": "Evaluate models on your task", "heading": "Before you switch models",
             "bullets": ["30–100 held-out, realistic inputs", "Happy paths, edge cases, known failures", "Track tokens, cache hits, steps, retries", "Check current pricing before go-live"], "lines": [
                "Benchmarks are not your task. Build a held-out set of thirty to a hundred realistic inputs.",
                "Include happy paths, edge cases, and failures you already know about.",
                "Trade off cost, latency, and quality with evidence, tracking tokens, cache behavior, step counts, and retries.",
            ]},
            {"type": "bullets", "kicker": "Chapter 6", "heading": "Tools are contracts",
             "bullets": ["Narrow, explicit, versioned schemas", "Say what the tool does NOT do", "Retryable vs. terminal errors", "Idempotency keys on every write"], "lines": [
                "Tool-use quality is bounded by the quality of your tool definitions.",
                "Keep schemas narrow, explicit, and versioned.",
                "In one case, a single added sentence describing what a tool does not do eliminated an entire class of production bugs.",
                "Tell the caller whether an error is retryable or terminal, and protect every write with an idempotency key so a retry can't do it twice.",
            ]},
            {"type": "image", "src": "m05-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "In lab, you'll build a tool router that picks the right toolset before the agent even starts. See you there.",
            ]},
        ],
    },
    {
        "id": "m06", "track": "Track 06", "name": "Muscle Memory",
        "module": "Memory: Working, Episodic, Semantic, Procedural", "chapters": "Chapter 7",
        "scenes": [
            {"type": "title", "lines": [
                "This is track six: Muscle Memory.",
                "A brilliant agent with amnesia is still frustrating to work with. Today we fix that.",
            ]},
            {"type": "quote", "kicker": "Opening case", "quote": "After two weeks, usage dropped sixty percent.", "lines": [
                "An analyst agent was excellent on day one.",
                "But every session, users had to re-explain their competitors, their preferred frameworks, and their open research threads.",
                "After two weeks, usage dropped sixty percent. Starting from scratch was more frustrating than the agent was useful.",
                "Adding a memory layer didn't make it smarter. It made it something you could have a continuing relationship with.",
            ]},
            {"type": "bullets", "kicker": "Chapter 7 framework", "heading": "Four types of memory",
             "bullets": ["Working — what the model attends to now", "Episodic — what happened in past sessions", "Semantic — facts that don't expire", "Procedural — routines learned over time"], "lines": [
                "Following Caldwell's chapter seven, there are four kinds of memory.",
                "Working memory is what the model is attending to right now.",
                "Episodic memory is what happened in past sessions.",
                "Semantic memory holds facts and knowledge that don't expire.",
                "And procedural memory is the routines an agent accumulates over the lifetime of its deployment.",
            ]},
            {"type": "bullets", "kicker": "Storage", "heading": "Match the store to the memory",
             "bullets": ["Key-value: fast-changing session state", "Vector + keyword (hybrid) search", "Graphs for relationship questions", "Start simple; add stores on evidence"], "lines": [
                "Each memory type wants a different store.",
                "Fast-changing session state, like the current project or the tool-call count, fits a key-value store.",
                "For recall, hybrid search, combining vector similarity with keyword search, beats pure vector search on most production tasks.",
                "And when the question is about relationships, like competitors, board members, or subsidiaries, reach for a graph.",
            ]},
            {"type": "bullets", "kicker": "Enterprise lens", "heading": "What breaks after months",
             "bullets": ["Overlapping, duplicate summaries", "Stale facts that conflict with live data", "Names, affiliations, financial data", "Retention and deletion are requirements"], "lines": [
                "Here's what shows up after months in production.",
                "A user who asks about the same company in ten sessions leaves ten overlapping summaries. Design consolidation from day one.",
                "Memory also accumulates names, affiliations, and financial data. Retention, tenancy boundaries, and deletion are requirements, not features.",
                "And add stores only when production evidence justifies the cost, not because the diagram looks elegant.",
            ]},
            {"type": "image", "src": "m06-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "Your midterm project, Encore, puts all four memory types to work in a music agent. Have fun with it.",
            ]},
        ],
    },
    {
        "id": "m07", "track": "Track 07", "name": "The Setlist",
        "module": "Planning & Decomposition", "chapters": "Chapter 8",
        "scenes": [
            {"type": "title", "lines": [
                "This is track seven: The Setlist.",
                "Every good show starts with a plan. So does every agent that has more than one thing to do.",
            ]},
            {"type": "quote", "kicker": "Opening case", "quote": "Twenty steps deep on initiative one — and no attention left for the rest.", "lines": [
                "A planning agent was asked to research a list of engineering initiatives and produce a prioritized roadmap.",
                "With four or five initiatives, it was fine. With more, it failed every time.",
                "It followed a chain of dependencies on the first initiative for twenty steps, and never got to the others.",
                "The fix was a planning step: list the initiatives, what to learn about each, and a step budget for each. About two hundred tokens and one extra call.",
            ]},
            {"type": "bullets", "kicker": "Chapter 8 framework", "heading": "Four planning strategies",
             "bullets": ["ReAct — think, act, observe, interleaved", "Plan-and-Execute — plan up front", "Reflexion — revise after failure", "Tree-of-Thoughts — explore alternatives"], "lines": [
                "Following Caldwell's chapter eight, there are four planning strategies.",
                "ReAct interleaves thought, action, and observation. It's fluid, but it drifts without budgets.",
                "Plan-and-Execute writes the plan up front and executes it step by step, which makes checkpoints easy.",
                "Reflexion revises the plan in response to failure.",
                "And Tree-of-Thoughts explores several plans in parallel, when being wrong is expensive.",
            ]},
            {"type": "bullets", "kicker": "Enterprise lens", "heading": "Planning in production",
             "bullets": ["Plan, execute a step, verify", "Replan only on real deviation", "Reflect when a tool fails or a validator rejects", "Persist the plan"], "lines": [
                "In production, these get blended.",
                "Propose a plan, execute one step, verify it, and replan only when an observation meaningfully changes the picture.",
                "Reflection fires per step, when a tool call fails or a validator rejects output, not by replaying whole episodes.",
                "Tree-of-Thoughts needs a judge to pick a branch, and that judge is another probabilistic model. Test the judge.",
                "And persist the plan. A plan that lives only in the context window can't be audited, resumed, or reviewed.",
            ]},
            {"type": "image", "src": "m07-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "This week's lab is a midterm workshop. Bring your Encore agent and your questions.",
            ]},
        ],
    },
    {
        "id": "m08", "track": "Track 08", "name": "Plug and Play?",
        "module": "Model Context Protocol (MCP)", "chapters": "Chapter 9",
        "scenes": [
            {"type": "title", "lines": [
                "This is track eight: Plug and Play?",
                "Notice the question mark. Today we look at the Model Context Protocol, and at what it does and doesn't promise.",
            ]},
            {"type": "quote", "kicker": "Big idea", "quote": "MCP standardizes the envelope, not the contents.", "lines": [
                "You'll hear MCP called the USB-C of AI, a protocol that lets any agent talk to any tool.",
                "Those framings are wrong in a way that matters for design.",
                "MCP is a JSON-RPC wire format with a small standard library of messages for discovering and calling tools, reading resources, and looking up prompt templates.",
                "It's to agent tools what HTTP is to documents. A shared envelope, not shared meaning.",
            ]},
            {"type": "bullets", "kicker": "Chapter 9 framework", "heading": "MCP building blocks",
             "bullets": ["Host → client → server", "Initialize and negotiate capabilities", "Tools · resources · prompts", "Transports: stdio and Streamable HTTP"], "lines": [
                "Following Caldwell's chapter nine, a host coordinates a client that talks to one or more servers.",
                "The connection starts with initialization, where both sides negotiate versions and capabilities.",
                "Servers expose tools you call, resources you read, and prompts you reuse.",
                "And messages travel over standard input and output for local servers, or Streamable HTTP for remote ones.",
            ]},
            {"type": "bullets", "kicker": "Why it matters", "heading": "Integration cost moved to the right place",
             "bullets": ["Before: a different tool format per framework", "After: one envelope everyone speaks", "Still yours: the domain model", "Servers crash — clients must expect it"], "lines": [
                "Before MCP, each framework solved tool connectivity its own way. Three years of bespoke abstractions.",
                "MCP fixed the envelope. But an MCP server for a customer platform still has to understand that platform's domain model.",
                "It moved integration cost from the wire format, where it never belonged, to the semantic layer, where it always did.",
            ]},
            {"type": "bullets", "kicker": "Enterprise lens", "heading": "Production-grade MCP",
             "bullets": ["Audit-log every tool call", "Transports don't authorize anything", "Scope credentials per server", "Expose only what this user and task need"], "lines": [
                "From the enterprise side: audit logging on every tool call is what separates a production server from a development server.",
                "It's your forensic record for security incidents, and your best source for debugging.",
                "Transports move bytes. They don't authorize anything. Enforce permissions in the host and the server.",
                "And only enable capabilities the current user and task actually need. A long tool catalog is an attack surface.",
            ]},
            {"type": "image", "src": "m08-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "In the extra credit lab, you'll build and connect your own MCP server. See you there.",
            ]},
        ],
    },
    {
        "id": "m09", "track": "Track 09", "name": "Solo Practice",
        "module": "Single-Agent Patterns", "chapters": "Chapter 10",
        "scenes": [
            {"type": "title", "lines": [
                "This is track nine: Solo Practice.",
                "Before forming a band, learn to play well alone. Today is about structuring a single agent.",
            ]},
            {"type": "quote", "kicker": "Opening case", "quote": "Nothing changed — not the model, the tools, or the prompt. Then it started failing.", "lines": [
                "A customer support agent ran well for six months.",
                "Then, at higher volume, it started offering refunds on unverified orders, skipping steps, and calling the same tool three or four times in a row.",
                "Nobody had changed the model, the tools, or the prompt.",
                "The failures came from context growth, tool complexity, and a new mix of requests, all hitting one flat loop.",
                "Separating routing from execution, and tracking state between steps, fixed all three within a week. It didn't get more capable. It got more organized.",
            ]},
            {"type": "bullets", "kicker": "Chapter 10 framework", "heading": "Core single-agent patterns",
             "bullets": ["Router → executor", "Validator wrapper", "Step machine with explicit state", "Scratchpad with an explicit plan", "Explicit, tested escalation"], "lines": [
                "Following Caldwell's chapter ten, here are the core patterns.",
                "A router classifies the request, then hands it to an executor with a smaller, focused toolset.",
                "A validator checks outputs before they leave, using schemas, tests, or a second model.",
                "A step machine makes states and transitions explicit, like an onboarding flow that must collect certain fields before creating an account.",
                "A scratchpad gives the agent a written plan it keeps outside the conversation: the steps, what's done, and what it has learned so far.",
                "Your code re-injects the scratchpad on every step, and the agent checks items off as it goes, so a long task doesn't lose its place in a growing context.",
                "And escalation is a real code path: when the agent can't finish safely, it hands the case to a person.",
                "Most production agents combine two or three of these.",
            ]},
            {"type": "bullets", "kicker": "Enterprise lens", "heading": "Add structure on evidence",
             "bullets": ["Start with a flat ReAct loop", "Add a pattern for a failure you've seen", "Validators: the minimum that catches it", "Escalation: in code and in tests"], "lines": [
                "The flat loop is still the right place to start.",
                "Add a pattern only when production evidence shows the failure it prevents.",
                "Keep validators to the minimum needed to catch failures you've actually seen. Every check costs latency.",
                "And if an escalation path isn't in the code, and covered by a test, it doesn't exist.",
            ]},
            {"type": "image", "src": "m09-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "Next time, we form the band: multiple agents working together.",
            ]},
        ],
    },
    {
        "id": "m10", "track": "Track 10", "name": "Forming the Band",
        "module": "Multi-Agent Systems & Shared Infrastructure", "chapters": "Chapter 11",
        "scenes": [
            {"type": "title", "lines": [
                "This is track ten: Forming the Band.",
                "Agents talking to each other isn't an architecture. Today we look at what is.",
            ]},
            {"type": "quote", "kicker": "Opening case", "quote": "The extractor couldn't know in advance what the researcher would need.", "lines": [
                "A legal technology company built a paralegal pipeline: extract facts, research precedent, draft.",
                "On paper it was clean. On document sets hundreds of pages long, it failed.",
                "Connecting facts to precedent required understanding the extraction step couldn't produce up front, and mismatched schemas between stages made it worse.",
            ]},
            {"type": "bullets", "kicker": "Chapter 11 patterns", "heading": "Ways to organize a band",
             "bullets": ["Supervisor and workers", "Pipeline of stages", "Parallel fan-out", "Hierarchies — usually two levels"], "lines": [
                "Following Caldwell's chapter eleven, there are a few common patterns.",
                "A supervisor assigns work to specialized workers and combines the results.",
                "A pipeline passes work through explicit stages.",
                "Parallel fan-out suits independent tasks, like the same research run against many companies.",
                "Hierarchies can go deep, but most production systems settle at two levels: one supervisor, several workers.",
            ]},
            {"type": "bullets", "kicker": "Shared infrastructure", "heading": "What every band needs",
             "bullets": ["Shared state with locks or optimistic concurrency", "Typed, versioned, validated messages", "First result wins (Redis SETNX)", "Explicit ownership and bounded fan-out"], "lines": [
                "Whatever the pattern, the same infrastructure shows up.",
                "Shared state needs locking or optimistic concurrency, or two agents will overwrite each other's work.",
                "Messages between agents need schemas both sides agree on, with versions.",
                "And retries need idempotency. With an atomic set-if-not-exists, only the first agent to finish a task records its result.",
            ]},
            {"type": "quote", "kicker": "Enterprise lens", "quote": "Mismatched schemas between stages are the most common source of pipeline failures.", "lines": [
                "From the enterprise side: version every message contract.",
                "Mismatched schemas between stages cause more pipeline failures than anything else.",
                "Multiple agents multiply both specialization and coordination risk. Spend your effort on shared state and recovery, not role-play.",
            ]},
            {"type": "image", "src": "m10-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "Next, we bring the humans back in: who approves what, and when.",
            ]},
        ],
    },
    {
        "id": "m11", "track": "Track 11", "name": "The Mixing Desk",
        "module": "Human-in-the-Loop & Human-on-the-Loop", "chapters": "Chapter 12",
        "scenes": [
            {"type": "title", "lines": [
                "This is track eleven: The Mixing Desk.",
                "Every band needs someone at the board with approve, modify, and reject buttons. Today, that's the human.",
            ]},
            {"type": "quote", "kicker": "Opening case", "quote": "Right on the clear cases. Confidently wrong on the hard fifteen percent.", "lines": [
                "A fraud-detection agent was deployed fully autonomously.",
                "It handled the clear eighty-five percent of cases well.",
                "But on the unclear fifteen percent, human reviewers disagreed with it almost half the time.",
                "It didn't know when it was outside its reliable range. Neither did the team.",
                "The fix: decide above a confidence threshold, and below it, escalate with a short explanation a reviewer can approve, modify, or reject in one click.",
            ]},
            {"type": "bullets", "kicker": "Chapter 12 framework", "heading": "Two oversight models",
             "bullets": ["HITL: agent pauses for a human", "HOTL: agent proceeds; human monitors", "Choose by risk, not task difficulty"], "lines": [
                "Following Caldwell's chapter twelve, there are two models.",
                "With a human in the loop, the agent stops and waits for approval before passing a checkpoint. Think payments, external emails, production deploys, or court filings.",
                "With a human on the loop, the agent keeps going, and a person monitors and can intervene. Think high-volume content moderation.",
                "The choice is a risk calculation, not a judgment about how hard the task is.",
            ]},
            {"type": "bullets", "kicker": "Minimum viable HOTL", "heading": "The smallest real human-on-the-loop",
             "bullets": ["Log every decision, with its reason", "A review queue: sample, plus low confidence", "Alerts on thresholds and anomalies", "A stop button, and a way to undo"], "lines": [
                "So what's the smallest human-on-the-loop system that actually works? Four pieces.",
                "First, the agent logs every action it takes, with a one-line reason, the inputs it used, and its confidence.",
                "Second, a review queue. A person reviews a random sample of decisions, plus every decision below the confidence threshold, after the fact.",
                "Third, alerts. When volume spikes, error rates climb, or reviewers start disagreeing with the agent, someone gets paged.",
                "And fourth, a stop button. One switch pauses the agent, and every action it takes has a known way to be reversed.",
                "Without all four, nobody is really on the loop. They're just hoping.",
            ]},
            {"type": "bullets", "kicker": "Placing intervention points", "heading": "Three questions, two rules",
             "bullets": ["How reversible is the action?", "How often is the agent out of range?", "How costly is the review delay?", "Rule: before irreversible actions", "Rule: below a measured confidence"], "lines": [
                "Ask three questions. How reversible is the action? How often does the agent operate outside its reliable range? And how expensive is the delay of a human review?",
                "Then follow two rules.",
                "Place intervention points before irreversible actions, like sending an email, committing a transaction, or deleting data.",
                "And place them where the agent's confidence drops below a threshold you've measured.",
            ]},
            {"type": "bullets", "kicker": "Enterprise lens", "heading": "Design from the reviewer's chair",
             "bullets": ["A summary, not a raw trace", "Approve · modify · reject", "The threshold is a tunable parameter", "Durable run state across the pause"], "lines": [
                "Design from the reviewer's chair. What do they need to know, and what do they need to be able to do?",
                "Usually that's a concise summary and three buttons, not a raw trace.",
                "Treat the threshold as a tunable parameter. Track how often reviewers agree, and move it with evidence.",
                "And paused runs must survive restarts. Keep run state in a database, and confirm nothing changed before resuming.",
            ]},
            {"type": "image", "src": "m11-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "Next, we take agents on the road: runs that last hours, or days.",
            ]},
        ],
    },
    {
        "id": "m12", "track": "Track 12", "name": "The Long Tour",
        "module": "Long-Running & Asynchronous Agents", "chapters": "Chapter 13",
        "scenes": [
            {"type": "title", "lines": [
                "This is track twelve: The Long Tour.",
                "Machines reboot, networks flap, APIs throttle, and users change their minds. Long-running agents have to survive all of it.",
            ]},
            {"type": "quote", "kicker": "Opening case", "quote": "A forty-minute job became a $340 bill and a half-finished briefing saved nowhere.", "lines": [
                "A fintech team built an agent to monitor regulatory filings, cross-reference their product roadmap, and write a weekly briefing.",
                "On paper, it took forty minutes.",
                "In practice, the filings site throttled requests, document parsing hit retry storms, and summarization calls piled up.",
                "They woke up to a $340 bill, a half-finished briefing saved nowhere, and a crash when the container was recycled after six hours.",
                "The tools were fine. The agent had been designed like a synchronous function call.",
            ]},
            {"type": "bullets", "kicker": "Chapter 13 framework", "heading": "Durable execution essentials",
             "bullets": ["Checkpoint at named stages", "Asynchronous task queues", "Step-level cost accounting", "Heartbeats, progress, cancellation"], "lines": [
                "Following Caldwell's chapter thirteen, the core shift is this: agent state is a persistent artifact, not a variable in memory.",
                "Checkpoint at well-defined stages, so a crash at hour five doesn't throw away hours one through four.",
                "Use task queues so runs can pause, resume, and cancel without losing their place.",
                "Account for cost at every step, so you can stop a runaway run.",
                "And report progress, send heartbeats, and handle cancellation cleanly.",
            ]},
            {"type": "bullets", "kicker": "Checkpoints", "heading": "What a checkpoint holds",
             "bullets": ["Current stage and its inputs", "All outputs so far", "Tokens used and tool-call history", "Model, temperature, and tool config"], "lines": [
                "At minimum, a checkpoint holds the current stage, its inputs, and every output so far.",
                "In practice, add operational metadata: when the stage started, tokens consumed, the tool-call history, and the exact model and settings.",
                "Resuming from a checkpoint should produce the same result as one continuous run.",
            ]},
            {"type": "quote", "kicker": "Enterprise lens", "quote": "It's the saga pattern from distributed systems, applied to agents.", "lines": [
                "From the enterprise side, this is the saga pattern from distributed systems.",
                "Named stages with deterministic outputs, persisted before moving on. You trade a little flexibility for recoverability.",
                "Make idempotency a first-class constraint, so retried tools don't repeat side effects.",
                "And put budget alarms in the run loop, not in next month's invoice.",
            ]},
            {"type": "image", "src": "m12-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "Next, the sound check: how to see what your agent is actually doing.",
            ]},
        ],
    },
    {
        "id": "m13", "track": "Track 13", "name": "Sound Check",
        "module": "Observability, Evaluation & Drift", "chapters": "Chapter 14",
        "scenes": [
            {"type": "title", "lines": [
                "This is track thirteen: Sound Check.",
                "Not just, did it run and how fast, but did it behave correctly, why, and is it drifting?",
            ]},
            {"type": "quote", "kicker": "Opening case", "quote": "Every test passed. Customers still found it rude.", "lines": [
                "A support agent passed every integration test.",
                "Two weeks later, customers noticed it was subtly rude, in a specific and reproducible way, and complaints ran three times higher than with the humans it replaced.",
                "The cause: whenever it detected emotional language, it leaned heavily on a coldly worded legal FAQ.",
                "Nothing was wrong with any single step, so no log surfaced it. Diagnosis took three days, because nobody had recorded what was retrieved, or why.",
            ]},
            {"type": "bullets", "kicker": "Chapter 14 framework", "heading": "The agent observability stack",
             "bullets": ["Span-based tracing (OpenTelemetry)", "Structured logs of tool calls and tokens", "LLM-as-judge for semantic quality", "Regression suites that catch drift"], "lines": [
                "Following Caldwell's chapter fourteen, agents need more than metrics, logs, and traces.",
                "Their behavior is non-deterministic, and they fail semantically: answers that are valid, but wrong, off-tone, or off-policy.",
                "So trace every step with spans, log tool calls and token spend in a structured way, score quality with a calibrated LLM judge, and keep regression suites that catch drift before customers do.",
            ]},
            {"type": "bullets", "kicker": "Detecting drift", "heading": "Three-sigma and CUSUM",
             "bullets": ["σ: a metric's normal day-to-day wobble", "3σ: catches big, sudden spikes", "CUSUM: catches small, sustained drift", "Both need a known-good baseline"], "lines": [
                "Standard deviation measures how much a metric normally wobbles.",
                "The three-sigma rule flags a day more than three wobbles from the average. It catches big, sudden spikes.",
                "CUSUM adds up small deviations over time, so it catches slow drift that never crosses three sigma on any single day.",
                "Both depend on a baseline from a known-good period.",
            ]},
            {"type": "bullets", "kicker": "Enterprise lens", "heading": "Make quality visible",
             "bullets": ["Cost per run is a leading signal", "Link every score to a trace ID", "Baseline → gate → monitor", "Shadow-evaluate before promoting"], "lines": [
                "From the enterprise side: a spike in cost per run often signals a behavior change before quality metrics move.",
                "Link every evaluation score to a trace, so a drop is one click from the run that caused it.",
                "Baseline, gate releases, monitor live traffic, and shadow-evaluate a new version beside production before you promote it.",
            ]},
            {"type": "image", "src": "m13-mindmap.svg", "lines": [
                "Here's the map for this module.",
                "Last track: keeping the show safe.",
            ]},
        ],
    },
    {
        "id": "m14", "track": "Track 14", "name": "Stage Security",
        "module": "Safety, Alignment & Guardrails", "chapters": "Chapter 15",
        "scenes": [
            {"type": "title", "lines": [
                "This is track fourteen, our encore: Stage Security.",
                "No prompt, by itself, is a security boundary. Today we build the ones that are.",
            ]},
            {"type": "quote", "kicker": "What alignment means", "quote": "An aligned agent's actions stay true to the intent and values of the people who built it.", "lines": [
                "Start with the word alignment.",
                "When you build an agent, you have an intention: what it's for. And you have values: what it must never do along the way.",
                "But at runtime, its instructions come from everywhere: users, documents, web pages, tool results, even other agents.",
                "An agent is aligned when its actions keep matching its creator's intent and values, no matter who is talking to it, or for how long.",
                "Misalignment rarely looks like rebellion. It looks like a goal followed too literally, a rule that quietly decays, or a user who steers it somewhere it shouldn't go.",
                "Guardrails are how we enforce alignment in code, at every boundary where text comes in, and every boundary where actions go out.",
            ]},
            {"type": "bullets", "kicker": "Input guardrails", "heading": "Three ways to check what comes in",
             "bullets": ["Regular expressions — known-bad strings and formats", "Semantic similarity — close to known attack patterns", "Agentic classification — a model labels intent and use case", "Then block, sanitize, or escalate"], "lines": [
                "Input guardrails check everything before the agent acts on it. There are three common layers, from cheapest to smartest.",
                "Regular expressions catch exact patterns: phrases like ignore your previous instructions, hidden markup, secrets, card numbers, and other personal data. They're fast and predictable, but easy to dodge with a paraphrase.",
                "Semantic similarity embeds the input and compares it to a library of known bad-actor patterns, like jailbreak role-plays and injection phrasings. It catches the paraphrases that regular expressions miss.",
                "Agentic classification asks a small, separate model to label the intent and the use case, and compares that label to what this agent is allowed to do. It catches new attacks, and requests that are simply out of scope.",
                "Each layer then blocks the input, strips the dangerous part, or sends it to a human.",
            ]},
            {"type": "bullets", "kicker": "Output guardrails", "heading": "Check what goes out, too",
             "bullets": ["Validate schema and policy", "Redact secrets and personal data", "Pipeline: one agent's output is the next one's input", "Guard every boundary in both directions"], "lines": [
                "Output guardrails check what the agent produces before anyone, or anything, uses it.",
                "Validate it against a schema and your policies, and redact secrets and personal data before they leave.",
                "Now recall the pipeline pattern from track ten. One agent's output becomes the next agent's input.",
                "So a poisoned document that slips past the first stage arrives at the second stage looking like trusted, internal data.",
                "That's why every boundary in a pipeline gets both checks: an output guardrail as it leaves one agent, and an input guardrail as it enters the next.",
            ]},
            {"type": "bullets", "kicker": "Agent grooming", "heading": "Many small nudges, across many sessions",
             "bullets": ["Each message looks harmless on its own", "Judge the request with episodic context", "Watch the trajectory, not just the turn", "Past agreements are not permissions"], "lines": [
                "There's a slower attack, called agent grooming.",
                "A human operator nudges an agent a little at a time, across many turns and many sessions, until it does something it was never supposed to do. Each message, on its own, looks harmless.",
                "A guardrail that only reads the current message will never see it.",
                "So include episodic context: give the guardrail a summary of this user's past sessions and requests, not just today's input.",
                "Now it can see the trajectory, a steady drift toward a forbidden action, and flag it for a human.",
                "And make sure memory never turns an earlier conversation into permission. Policy lives in code, not in what the agent was talked into last week.",
            ]},
            {"type": "quote", "kicker": "Enterprise lens", "quote": "The guardrail that matters still holds if the model misreads every sentence.", "lines": [
                "From the enterprise side, the guardrail that matters is the one that still holds if the model misreads every sentence.",
                "That's always code: allowlists, scopes, least-privilege credentials, and validators.",
                "Log policy decisions without logging secrets or personal data, and test against direct injection, indirect injection, and grooming.",
                "And in your capstone, bring evidence: traces, evaluation scores, a threat model, and a rollback plan.",
            ]},
            {"type": "image", "src": "m14-mindmap.svg", "lines": [
                "Here's the map for our final module.",
                "Justify the agent, constrain it, observe it, evaluate it, and keep humans in charge. That's the whole show. Thanks for being here.",
            ]},
        ],
    },
]


# Walkthrough tracks for the labs and projects. Same format as the lectures; "for" is the activity link they belong to.
PRACTICE_TRACKS = [
    {
        "id": "lab1", "track": "Lab Track 1", "name": "Tuning Up", "kind": "lab", "for": "Assignments/Labs/Lab1/Lab1.html",
        "module": "Lab 1 · Environment Setup & First Chatbot", "chapters": "Chapter 1",
        "scenes": [
            {"type": "title", "lines": [
                "This is lab track one: Tuning Up.",
                "You'll set up your workbench, build your first LLM application, and then ask a hard question about it.",
            ]},
            {"type": "quote", "kicker": "The big question", "quote": "An application that calls an LLM is not automatically an agent.", "lines": [
                "Lab one has two halves.",
                "First, a bare-bones chatbot: a system prompt, your question, one call to a model through OpenRouter, and the reply printed to the screen.",
                "Then you give it web search with Tavily, and compare what changes.",
                "Along the way, you'll hold it up against our definition of an agent and find where it falls short.",
            ]},
            {"type": "bullets", "kicker": "Part 1", "heading": "Set up the workbench",
             "bullets": ["Git, VS Code, and Python 3.12", "Install the lab requirements", "Your OpenRouter key in a .env file", "Never commit a key"], "lines": [
                "Install Git, Visual Studio Code, and Python three point twelve, and clone the course repository.",
                "Install the lab requirements with pip, from the labs folder.",
                "Put your OpenRouter key in a local .env file, and load it at runtime with python dotenv.",
                "Never paste a key into your source code, and never commit the .env file.",
            ]},
            {"type": "bullets", "kicker": "Parts 2 and 3", "heading": "Build it, then test it",
             "bullets": ["System prompt + user message", "One request, one reply", "Tests that probe the limits", "Record what you observe"], "lines": [
                "Complete the starter's to-do items. Every request carries a messages list: a system message that sets the assistant's role, and the user's message.",
                "Send it to the chat completions endpoint, and print the reply, or the error if something goes wrong.",
                "Then run the tests. Some questions it should answer well. Others, like today's weather or this week's news, are designed to expose what a model alone can't know.",
                "Record each result, and explain what it shows. A fluent, confident answer is not the same as a current one.",
            ]},
            {"type": "bullets", "kicker": "Parts 4 and 5", "heading": "Is it an agent? Then add search",
             "bullets": ["Goal · tools · environment · loop", "Add Tavily web search", "Who decides when to search?", "The system prompt shapes behavior"], "lines": [
                "Use the definition from track one: a goal, choosing its own next action from tools, acting on an environment, observing, and repeating.",
                "Then extend the chatbot with Tavily web search, so its answers can draw on current information.",
                "Notice who decides when to search. In this lab, your code does. Next lab, the model will.",
                "And experiment with the system prompt. It's the simplest way to change how the whole application behaves.",
            ]},
            {"type": "image", "src": "", "lines": [
                "Here's the whole lab on one board.",
                "Next, in lab two, we hand the model the controls. See you there.",
            ]},
        ],
    },
    {
        "id": "lab2", "track": "Lab Track 2", "name": "First Rehearsal", "kind": "lab", "for": "Assignments/Labs/Lab2/Lab2.html",
        "module": "Lab 2 · Agent Anatomy & Automation", "chapters": "Chapters 2–3",
        "scenes": [
            {"type": "title", "lines": [
                "This is lab track two: First Rehearsal.",
                "Today your chatbot becomes a minimum viable agent, with a loop you can watch and a limit it can't cross.",
            ]},
            {"type": "quote", "kicker": "The shift", "quote": "Not what can it answer, but what does it mean for it to act?", "lines": [
                "In lab one, your code decided when to search. In lab two, the model decides.",
                "Before you code, read chapter two of the A I textbook on intelligent agents: percepts, actions, environments, and performance measures.",
                "Then classify a few systems on the five-level ladder from track two, from scripted automation up to multiple agents.",
            ]},
            {"type": "bullets", "kicker": "Minimum viable agent", "heading": "Four essential pieces",
             "bullets": ["Goal — a system prompt", "Tools — calculator and web search", "Context — the request plus observations", "Loop — decide, act, observe, repeat"], "lines": [
                "Your agent has four pieces.",
                "A goal, set by the system prompt.",
                "Tools: a calculator and a web search, written as ordinary Python functions that return results to your code.",
                "Context: the user's request, plus every observation the tools return.",
                "And the loop: thought, action, observation, and again, until a final answer, or until it gives up.",
            ]},
            {"type": "bullets", "kicker": "Build it carefully", "heading": "Bounded, observable, correct",
             "bullets": ["A hard step limit", "Log every thought, action, observation", "Never eval() model text unguarded", "Watch for repeats and missing info"], "lines": [
                "Make the loop bounded: a hard limit on steps, so it can never spin forever.",
                "Make it observable: print or log every thought, action, and observation, so you can see why it did what it did.",
                "Treat model output as untrusted. A calculator built on Python's eval needs a restricted namespace, or a safer parser.",
                "Then try to break it, with missing information, repeated actions, and the wrong tool, and write down what happens.",
            ]},
            {"type": "image", "src": "", "lines": [
                "Here's the lab on one board.",
                "Defend the level of agency you built. Next, lab three hardens it for the long haul.",
            ]},
        ],
    },
    {
        "id": "lab3", "track": "Lab Track 3", "name": "Road Case", "kind": "lab", "for": "Assignments/Labs/Lab3/Lab3.html",
        "module": "Lab 3 · Hardening the Agent", "chapters": "Chapter 5",
        "scenes": [
            {"type": "title", "lines": [
                "This is lab track three: Road Case.",
                "Lab two asked, does the loop work? Lab three asks, does it keep working?",
            ]},
            {"type": "quote", "kicker": "The stress test", "quote": "Longer tasks, more tools, and a model that changes under you.", "lines": [
                "You'll take your lab two agent and stress it: longer conversations, more tool calls, and a bigger step budget.",
                "You'll run it two ways: online through OpenRouter, and offline against a local model served by llama dot c p p.",
                "And you'll tier it: a cheap model drives tool selection, and an expensive model writes only the final answer.",
            ]},
            {"type": "bullets", "kicker": "Failure modes", "heading": "Defend against what goes wrong at scale",
             "bullets": ["Context saturation → windowed summaries", "Instruction drift → re-inject constraints", "Confabulation → structured outputs", "Silent tools → fail loudly"], "lines": [
                "As context grows, details in the middle get lost. Summarize older turns in a window, so the context stays bounded.",
                "Critical rules fade over a long run. Re-inject them on every step.",
                "Models invent arguments with confidence. Enforce a schema on every tool call, online and offline.",
                "And design tools that fail loudly, with an explicit error, instead of quietly returning an empty result.",
            ]},
            {"type": "bullets", "kicker": "Measure it", "heading": "Observability and drift",
             "bullets": ["Log every tool call", "Schemas a junior engineer could follow", "Pinned model vs. model actually served", "Latency, tokens, run-to-run variance"], "lines": [
                "Log every tool call as a structured record: the tool, the arguments, the result, and the time it took.",
                "Write tool names and descriptions so clear that a junior engineer, or a small model, gets them right the first time.",
                "Check which model actually answered. Pinning a version in configuration doesn't guarantee it's the one being served.",
                "Then measure latency, token cost, and how much the answers vary from run to run, on the same prompt.",
            ]},
            {"type": "image", "src": "", "lines": [
                "Here's the lab on one board.",
                "Next, lab four decides which tools the agent sees before it even starts.",
            ]},
        ],
    },
    {
        "id": "lab4", "track": "Lab Track 4", "name": "Stage Manager", "kind": "lab", "for": "Assignments/Labs/Lab4/Lab4.html",
        "module": "Lab 4 · Tool Routing", "chapters": "Chapter 6",
        "scenes": [
            {"type": "title", "lines": [
                "This is lab track four: Stage Manager.",
                "Before the show starts, someone decides who's on stage. Today you build that someone.",
            ]},
            {"type": "quote", "kicker": "The problem", "quote": "Every tool on every call costs tokens, and invites the wrong pick.", "lines": [
                "As an agent gains tools, every request carries every tool definition, and the model has more ways to choose wrong.",
                "The fix is a routing step. Before the agent runs, a cheap model reads the request and picks which toolsets it needs.",
                "You'll build it as a meta tool called get available tools. It does no work for the user. It only decides what the real work will need.",
            ]},
            {"type": "bullets", "kicker": "The router", "heading": "Classify, then hand over a toolset",
             "bullets": ["Four domains: calendar · email · files · billing", "Plus none, for no tools", "Force the classification with tool_choice", "Return domains and their tools"], "lines": [
                "There are four toolset domains, calendar, email, files, and billing, plus none, for requests that need no tools.",
                "One request can touch several domains, so the router returns a list.",
                "Use tool choice to force the model to call the classifier, instead of replying in prose.",
                "Then return the chosen domains, and the tool names that belong to them.",
            ]},
            {"type": "bullets", "kicker": "Enums, not descriptions", "heading": "Constrain it, then check it",
             "bullets": ["A JSON Schema enum lists the valid values", "A description is only a hint", "Validate with jsonschema anyway", "Fall back safely when it's invalid"], "lines": [
                "Constrain the output with a JSON schema enum: a fixed list of valid values, where case and spelling count.",
                "Listing the values in a description isn't enough. A description is a hint the model may ignore.",
                "Even with an enum, validate the result in your own code. Some backends treat the schema as a suggestion, and small local models drift.",
                "If the output won't parse, fails validation, or comes back empty, fall back to a safe default.",
            ]},
            {"type": "image", "src": "", "lines": [
                "Here's the lab on one board.",
                "Your router becomes part of Encore, your midterm. Next, the extra credit lab: M C P.",
            ]},
        ],
    },
    {
        "id": "lab5", "track": "Lab Track 5", "name": "Patch Bay", "kind": "lab", "for": "Assignments/Labs/Lab5/Lab5.html",
        "module": "Lab 5 · Model Context Protocol (extra credit)", "chapters": "Chapter 9",
        "scenes": [
            {"type": "title", "lines": [
                "This is lab track five: Patch Bay. It's extra credit.",
                "Instead of tools living inside your agent's script, you'll move them into a server any client can plug into.",
            ]},
            {"type": "quote", "kicker": "The idea", "quote": "The client learns the tools at runtime, not when you write the code.", "lines": [
                "With MCP, a client connects to a server, asks what it offers with tools list, and calls what it needs with tools call.",
                "You'll build a small review toolkit server with Gradio, and connect it to the MCPJam web app, a client with a built-in chat. You won't write any client code.",
            ]},
            {"type": "bullets", "kicker": "The server", "heading": "Three tools, one Gradio app",
             "bullets": ["sentiment_analysis — provided", "text_statistics — you write it", "rank_sentences — you write it", "Launch with mcp_server and a share link"], "lines": [
                "Sentiment analysis comes from the Hugging Face MCP course, and it's already done.",
                "You add text statistics, which counts words and sentences.",
                "And rank sentences, which orders sentences by sentiment and returns the top few.",
                "Then launch with the MCP server turned on, and a temporary public share link, because the web client only connects over H T T P S.",
            ]},
            {"type": "bullets", "kicker": "Descriptions drive choices", "heading": "Your code becomes the schema",
             "bullets": ["Function name → tool name", "Docstring → description", "Type hints → property types", "Radio input → an enum, like lab four"], "lines": [
                "Gradio builds each tool's schema from your code.",
                "The function name becomes the tool name, the docstring becomes its description, and type hints become property types.",
                "A radio input becomes an enum, the same pattern you wrote by hand in lab four.",
                "Leave out a docstring, and the tool is published with an empty description. Watch what that does to the model's choices.",
            ]},
            {"type": "image", "src": "", "lines": [
                "Here's the lab on one board.",
                "You'll use a public M C P server for real in Encore Ensemble, your final project.",
            ]},
        ],
    },
    {
        "id": "encore", "track": "Project Track · Midterm", "name": "Encore", "kind": "project", "for": "Assignments/Midterm/Midterm.html",
        "module": "A ListenBrainz music agent that remembers", "chapters": "Chapters 5–7",
        "scenes": [
            {"type": "title", "lines": [
                "This is the project track for your midterm: Encore.",
                "A music agent that sits on top of your own ListenBrainz account, and remembers.",
            ]},
            {"type": "quote", "kicker": "One request, start to finish", "quote": "Make me a forty-minute focus playlist like last week's, but nothing I've played lately.", "lines": [
                "Encore answers questions about your listening, finds music, builds playlists in your account, and exports them to a streaming service.",
                "For a request like this one, it recalls last week's session, checks your recent listens, finds candidates, and verifies every recording is real.",
                "Then it creates the playlist and exports it, and both of those writes wait for your approval.",
                "Your code never scripts that sequence. The model chooses each step after reading the last result.",
            ]},
            {"type": "bullets", "kicker": "Built on your labs", "heading": "A real agent, against real APIs",
             "bullets": ["Bounded ReAct loop, at most 12 steps", "About 20 tools with JSON schemas", "Typed results and an error taxonomy", "Approval gates on every write"], "lines": [
                "Encore reuses your bounded loop, your lab three hardening, and your lab four router.",
                "It has about twenty tools, across listening, the music catalog, discovery, your library, and memory.",
                "Every tool returns a typed result, and errors are observations too, so the model can try something else.",
                "And anything that changes your account waits for approval, with rate limits and timeouts around every call.",
            ]},
            {"type": "bullets", "kicker": "Chapter 7", "heading": "Four kinds of memory",
             "bullets": ["Working — this conversation", "Episodic — past sessions", "Semantic — how ListenBrainz works", "Procedural — Encore's own rules"], "lines": [
                "What makes Encore more than a chatbot is memory, all four kinds from track six.",
                "Working memory holds this conversation. Episodic memory recalls the one from last week.",
                "Semantic memory knows how ListenBrainz and its exports work. Procedural memory follows Encore's rules, like never exporting without approval.",
                "Add a retention policy, a way to delete everything about a user, and defenses against stale or polluted memories.",
            ]},
            {"type": "bullets", "kicker": "Prove it", "heading": "Evaluate, then present",
             "bullets": ["Evaluate retrieval before the agent", "Held-out requests", "Accuracy · latency · cost · variance", "Present your evidence"], "lines": [
                "Evaluate your retrieval first: chunking, recall, and hybrid search, before you build the agent layer on top.",
                "Then test the whole agent on held-out requests, and measure accuracy, latency, cost, and run-to-run variance.",
                "There are two workshop checkpoints along the way, and you'll present your Encore, with its evidence, to the class.",
            ]},
            {"type": "image", "src": "", "lines": [
                "Here's the project on one board.",
                "Build it well. Your final project starts from this code.",
            ]},
        ],
    },
    {
        "id": "ensemble", "track": "Project Track · Final", "name": "Encore Ensemble", "kind": "project", "for": "Assignments/Final_Project/Final.html",
        "module": "From soloist to band", "chapters": "Chapters 8–11",
        "scenes": [
            {"type": "title", "lines": [
                "This is the project track for your final: Encore Ensemble.",
                "Your midterm was a soloist. Now it becomes a band.",
            ]},
            {"type": "quote", "kicker": "The central rule", "quote": "Pattern selection follows failure-mode identification, not architectural preference.", "lines": [
                "Encore Ensemble isn't a new project. It's your midterm, extended, and every guarantee it made must still hold.",
                "Somewhere in your midterm traces, Encore chased one sub-goal and forgot the rest, skipped a step, or claimed something no tool supported.",
                "For every pattern you add, show a failure it fixes, then the same requests after the fix. A pattern with no failure behind it earns at most half credit.",
            ]},
            {"type": "bullets", "kicker": "Choose one from each", "heading": "Four sections, one band",
             "bullets": ["Planning — Plan-and-Execute, Reflexion, Tree-of-Thoughts", "MCP — a public server, a new feature", "Single-agent — validator, step machine, or scratchpad", "Multi-agent — supervisor, pipeline, debate, and more"], "lines": [
                "You choose one capability from each of four textbook topics.",
                "A planning pattern, like Plan-and-Execute, Reflexion, or Tree-of-Thoughts.",
                "A public third-party M C P server, and a new user-facing feature built on it.",
                "A single-agent pattern: a validator wrapper, a stateful step machine, or a scratchpad with an explicit plan.",
                "And a multi-agent pattern, like supervisor and workers, a pipeline, or a debate.",
            ]},
            {"type": "bullets", "kicker": "Make it production-minded", "heading": "Legible, bounded, typed",
             "bullets": ["Plans logged and legible to code", "Budgets on steps, retries, branches", "Typed messages at every boundary", "Optional: human oversight, extra credit"], "lines": [
                "Every plan or reflection is logged as its own trace event, and your code can read it, not just the model.",
                "Everything is bounded: step budgets, retry counts, and branch counts.",
                "Between agents, use typed messages and checkpoints, so a failure resumes where it broke.",
                "Human oversight, in or on the loop, is optional extra credit.",
            ]},
            {"type": "image", "src": "", "lines": [
                "Here's the project on one board.",
                "Bring your traces, your evaluation, and a recorded presentation. That's the whole tour. Enjoy the show.",
            ]},
        ],
    },
]
LECTURES = LECTURES + PRACTICE_TRACKS
