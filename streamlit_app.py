-- coding: utf-8 --
Tr. Mubarak Almutlakah
=====================================================================
The Live-World Simulator | Mega Goal 3 - Unit 1: Two Is Better Than One
Developed by: Tr. Mubarak Almutlakah
جميع الحقوق محفوظة © المعلم مبارك آل مطلقة - عام 2026م
=====================================================================
Run locally : pip install streamlit requests
streamlit run app.py
API keys : put them in .streamlit/secrets.toml (or environment variables)
PERPLEXITY_API_KEY = "pplx-..."
FIRECRAWL_API_KEY = "fc-..."
Real Playwright (optional): pip install playwright && playwright install chromium
then set the environment variable USE_REAL_PLAYWRIGHT=1
Without keys the app runs fully in SIMULATION mode.
===================================================================== 

import os
import re 

import requests
import streamlit as st 

st.set_page_config(
page_title="The Live-World Simulator",
page_icon="🌍",
layout="centered",
initial_sidebar_state="collapsed",
) 

st.markdown("<!-- Tr. Mubarak Almutlakah -->", unsafe_allow_html=True) 

st.markdown(
"""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 3rem; max-width: 760px;}
.stButton > button, .stFormSubmitButton > button {
width: 100%; border-radius: 14px; padding: .65rem 1rem; font-weight: 700;}
.hero {background: linear-gradient(135deg,#0f2a4a,#1565c0); color:#fff;
padding:18px; border-radius:18px; text-align:center; margin-bottom:12px;}
.hero h1 {margin:0; font-size:1.5rem; color:#fff;}
.hero p {margin:4px 0 0; opacity:.9; font-size:.9rem;}
.card {background: rgba(21,101,192,.08); border-left:5px solid #1565c0;
padding:12px 14px; border-radius:12px; margin:8px 0; line-height:1.8;}
.say {padding:10px 12px; border-radius:12px; margin:6px 0; line-height:1.7;}
.team-a {background: rgba(25,118,210,.14);}
.team-b {background: rgba(229,57,53,.14);}
.chip {display:inline-block; padding:3px 10px; margin:3px; border-radius:20px;
font-size:.8rem; background:rgba(128,128,128,.18);}
.chip-on {background:#2e7d32; color:#fff;}
.footer {text-align:center; opacity:.75; font-size:.8rem; margin-top:30px; direction:rtl;}
</style>
""",
unsafe_allow_html=True,
) 

=====================================================================
1) SERVICE LAYER - Playwright / Firecrawl / Perplexity
(real calls when keys exist, otherwise a clear simulation)
=====================================================================
USE_REAL_PLAYWRIGHT = os.environ.get("USE_REAL_PLAYWRIGHT", "0") == "1"


def get_key(name):
"""Read an API key from Streamlit secrets or environment variables."""
try:
value = st.secrets.get(name)
if value:
return str(value)
except Exception:
pass
return os.environ.get(name, "")


SIM_PAGES = {
"crocodile": (
"<html><nav>Home | Menu | Login</nav><div class='ad'>BUY NOW!!! 50% OFF</div>"
"<article><h1>The Crocodile and the Plover</h1>"
"<p>The Egyptian plover, called zic-zac in Arabic, walks beside the Nile crocodile "
"and picks leftover food from its teeth.</p>"
"<p>The bird gets a free meal and the crocodile keeps its teeth clean. "
"Biologists call this kind of partnership mutualism, although some experts say "
"the evidence for this exact story is limited.</p></article>"
"<script>track()</script><footer>Cookies | Contact us</footer></html>"
),
} 

SIM_FACTS = {
"crocodile": (
"1) Mutualism means both partners gain something.\n"
"2) The plover-crocodile story is very old, but scientists still debate how often it happens.\n"
"3) Other famous partners: clownfish and sea anemones, bees and flowers."
),
"price": (
"1) Used items usually sell for 60-80% of the asking price after negotiation.\n"
"2) Polite offers with a clear reason are accepted more often.\n"
"3) Compare at least three similar listings before you make an offer."
),
"default": (
"1) This topic is popular with teenagers around the world.\n"
"2) Use comparison words (other, others, another) to describe different options.\n"
"3) Add a real example to make your speaking and writing stronger."
),
}


def playwright_fetch(topic):
"""Automation layer. Real Playwright if enabled, otherwise a simulated page."""
if USE_REAL_PLAYWRIGHT:
try:
from playwright.sync_api import sync_playwright 

url = "https://en.wikipedia.org/wiki/" + topic.strip().replace(" ", "_")
with sync_playwright() as p:
browser = p.chromium.launch(headless=True)
page = browser.new_page()
page.goto(url, timeout=15000)
html = page.content()
browser.close()
return html, "Playwright (real browser)", url
except Exception as exc:
note = "Playwright unavailable (" + type(exc).name + ") - simulated page used"
return _sim_page(topic), note, None
return _sim_page(topic), "Playwright (simulated)", None


def _sim_page(topic):
t = topic.lower()
if "crocodile" in t or "plover" in t:
return SIM_PAGES["crocodile"]
return (
"<html><nav>Menu</nav><article><h1>" + topic + "</h1>"
"<p>This is a simulated article about " + topic + ". "
"Replace this function with real browser automation when ready.</p></article>"
"<footer>Cookies</footer></html>"
)


def firecrawl_clean(raw_html, url=None):
"""Cleaning layer. Real Firecrawl if key + URL exist, otherwise local cleaning."""
key = get_key("FIRECRAWL_API_KEY")
if key and url:
try:
r = requests.post(
"https://api.firecrawl.dev/v1/scrape",
headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
json={"url": url, "formats": ["markdown"], "onlyMainContent": True},
timeout=30,
)
r.raise_for_status()
return r.json()["data"]["markdown"][:3000], "Firecrawl API (live)"
except Exception:
pass
text = re.sub(r"(?is)<(script|style|nav|footer|header|aside)[^>]>.?</\1>", " ", raw_html)
text = re.sub(r"(?is)<div[^>]class=['"]ad['"][^>]>.*?</div>", " ", text)
text = re.sub(r"(?s)<[^>]+>", " ", text)
text = re.sub(r"\s+", " ", text).strip()
return text[:3000], "Firecrawl (simulated local cleaning)"


def perplexity_enrich(topic, context=""):
"""Live-content layer. Real Perplexity API if key exists, otherwise simulated facts."""
key = get_key("PERPLEXITY_API_KEY")
note = ""
if key:
try:
r = requests.post(
"https://api.perplexity.ai/chat/completions",
headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
json={
"model": "sonar",
"messages": [
{
"role": "system",
"content": "You help a Saudi secondary English teacher. "
"Answer in simple English (B1), maximum 90 words.",
},
{
"role": "user",
"content": "Give 3 short, accurate, up-to-date facts about: "
+ topic + ". Context: " + context[:800],
},
],
},
timeout=20,
)
r.raise_for_status()
return r.json()["choices"][0]["message"]["content"], "Perplexity API (live)"
except Exception as exc:
note = " [API error: " + type(exc).name + " - fallback used]"
t = topic.lower()
if "crocodile" in t or "plover" in t or "symbio" in t:
facts = SIM_FACTS["crocodile"]
elif any(w in t for w in ["price", "bike", "laptop", "ticket", "market"]):
facts = SIM_FACTS["price"]
else:
facts = SIM_FACTS["default"]
return facts, "Perplexity (simulated)" + note


@st.cache_data(ttl=900, show_spinner=False)
def live_pipeline(topic):
"""Playwright -> Firecrawl -> Perplexity."""
raw, s1, url = playwright_fetch(topic)
clean, s2 = firecrawl_clean(raw, url)
answer, s3 = perplexity_enrich(topic, clean)
log = [
"1) " + s1 + " -> " + str(len(raw)) + " characters of raw HTML",
"2) " + s2 + " -> " + str(len(clean)) + " characters of clean text",
"3) " + s3 + " -> enriched answer",
]
return {"clean": clean, "answer": answer, "log": log}


def show_live(topic, label="🌐 Pull live content"):
if st.button(label, key="live_" + topic):
with st.spinner("Playwright → Firecrawl → Perplexity ..."):
res = live_pipeline(topic)
st.success(res["answer"])
with st.expander("🔧 Pipeline log"):
for line in res["log"]:
st.write(line)
st.caption("Clean text: " + res["clean"][:300])


=====================================================================
2) HELPERS & STATE
=====================================================================
def hl(text):
"""Turn word into a highlighted HTML tag."""
return re.sub(r"**(.+?)**", r"<b style='color:#d81b60'>\1</b>", text)


WH = {"what", "where", "when", "why", "how", "who", "which", "do", "does", "did", "and", "or"}
PRON = {"you", "he", "she", "they", "we", "i", "it", "not", "n't", "my", "your", "his", "her", "our",
"their", "the", "a", "an", "this", "that", "these", "those", "them", "him", "us", "me", "some", "any"}


def detect_structures(text):
"""Detect the Unit-1 target structures in a student's text."""
t = text.replace("’", "'")
found = set()
if re.search(r"\banother\b", t, re.I):
found.add("another")
if re.search(r"\bthe others\b", t, re.I):
found.add("the others")
if re.search(r"\bthe other\b", t, re.I):
found.add("the other")
if re.search(r"(?<!the )\bothers\b", t, re.I):
found.add("others")
if re.search(r"(?<!the )(?<!an )\bother\b", t, re.I):
found.add("other")
for m in re.finditer(r"\b([A-Za-z']+)\s+(do|does|did)\s+([A-Za-z']+)\b", t, re.I):
prev, nxt = m.group(1).lower(), m.group(3).lower()
if prev not in WH and nxt not in PRON:
found.add("emphatic do")
return found


def init_state():
defaults = {
"name": "", "points": 0, "energy": 100,
"debate": [], "gram_awarded": [], "gram_last": None, "gq_result": None, "gq_awarded": False,
"celebrate": False,
"rd_idx": 0, "rd_result": {}, "rd_hints": [], "rd_over": False,
"deal_scn": None, "deal_msgs": [], "deal_meter": 25, "deal_round": 0,
"deal_used": [], "deal_state": "playing", "deal_offer": None,
"w_step": 0, "w_data": ["", "", "", ""], "w_awarded": False,
}
for k, v in defaults.items():
if k not in st.session_state:
st.session_state[k] = v


=====================================================================
3) CONTENT BANKS
=====================================================================
INTERESTS = {
"⚽ Football": {"s": "player", "p": "players", "t1": "Messi", "t2": "Ronaldo",
"obj": "football", "topic": "football"},
"🎮 Gaming": {"s": "game", "p": "games", "t1": "Minecraft", "t2": "Fortnite",
"obj": "gaming", "topic": "video games"},
"🚗 Cars": {"s": "car", "p": "cars", "t1": "Toyota", "t2": "Hyundai",
"obj": "cars", "topic": "cars"},
"📱 Technology": {"s": "app", "p": "apps", "t1": "WhatsApp", "t2": "Telegram",
"obj": "technology", "topic": "technology"},
"🍔 Food": {"s": "dish", "p": "dishes", "t1": "Kabsa", "t2": "Pizza",
"obj": "food", "topic": "food"},
"✈️ Travel": {"s": "city", "p": "cities", "t1": "Abha", "t2": "Dubai",
"obj": "travel", "topic": "travel"},
}


def build_debate(d):
s, p, t1, t2, obj = d["s"], d["p"], d["t1"], d["t2"], d["obj"]
return [
("A", "Team " + t1, "I love " + t1 + ", but I'd like to try another " + s + ".",
"another + اسم مفرد = واحد إضافي (One more)"),
("B", "Team " + t2, "There are many other " + p + " out there. Some are old; others are brand new.",
"other + اسم جمع | others = بديل عن (other + جمع) بدون ذكر الاسم"),
("A", "Team " + t1, "Between " + t1 + " and " + t2 + ", one is more popular, and the other is more creative.",
"the other = الثاني المحدد من اثنين"),
("B", "Team " + t2, "Look at all the " + p + " in the market: two are famous, but the others are almost unknown.",
"the others = بقية المجموعة المحددة"),
("A", "Team " + t1, "You think I don't care about " + obj + "? I do care about " + obj + "!",
"Emphatic do: للتأكيد أو تصحيح اعتقاد الطرف الآخر (do/does/did + المصدر)"),
("B", "Team " + t2, "My friend does know a lot about " + obj + ", and he did win a prize last year!",
"does للمفرد الغائب، did للماضي - والفعل بعدهما بصيغة المصدر"),
]


GQ = [
{"q": "I finished my juice. Can I have ____ glass?", "o": ["another", "other", "others", "the others"],
"a": "another"},
{"q": "Some students like football; ____ prefer swimming.", "o": ["another", "other", "others", "the other"],
"a": "others"},
{"q": "I have two brothers. One is a doctor and ____ is an engineer.",
"o": ["another", "others", "the other", "the others"], "a": "the other"},
{"q": "There are ____ ways to learn English online.", "o": ["another", "other", "others", "the other"],
"a": "other"},
{"q": "Three pens are on the desk. One is red; ____ are blue.",
"o": ["the others", "another", "other", "the other"], "a": "the others"},
{"q": "A: You never study! B: I ____ study every day!", "o": ["do", "does", "am", "did to"], "a": "do"},
{"q": "She ____ know the answer, even though you think she doesn't.",
"o": ["do", "does", "is", "did to"], "a": "does"},
] 

PASSAGE = (
"Along the banks of the Nile, a <b>Nile crocodile</b> lies still in the sun with its huge mouth open. "
"A small bird called the <b>Egyptian plover</b> (the <i>zic-zac</i>) hops <b>fearlessly</b> inside and picks "
"bits of food from between the crocodile's sharp teeth. The bird is brave, but it is also clever: "
"it gets a free meal. The crocodile <b>benefits</b> too, because its teeth stay clean and free from infection. "
"Biologists call a partnership in which both partners gain <b>mutualism</b>. When one animal gains and the other "
"is not affected, it is <b>commensalism</b>, like a white bird resting on a buffalo. In <b>parasitism</b>, one animal "
"gains while the other suffers, like a tick on a dog. Some scientists believe the crocodile-plover story is "
"partly a legend, so a good detective must always check the evidence."
) 

RQ = [
{"q": "Why does the crocodile keep its mouth open when the plover comes in?",
"o": ["It trusts the bird because it gains from the cleaning.", "It is sleeping deeply.",
"It is angry with the bird.", "It cannot close its mouth."],
"a": "It trusts the bird because it gains from the cleaning.",
"hint": "Look for what the crocodile gets: clean teeth, no infection.",
"why": "Inference: the text says the crocodile benefits, so opening its mouth is a smart choice."},
{"q": "In the passage, the word 'benefits' is closest in meaning to:",
"o": ["gains an advantage", "loses energy", "feels afraid", "moves away"],
"a": "gains an advantage",
"hint": "Read the sentence after 'benefits': what good thing happens?",
"why": "Context clue: 'its teeth stay clean' is a positive result = an advantage."},
{"q": "What would most likely happen if there were no plovers at the river?",
"o": ["The crocodile's teeth might get dirty or infected.", "The crocodile would become a bird.",
"The Nile would dry up.", "Nothing could ever change."],
"a": "The crocodile's teeth might get dirty or infected.",
"hint": "Think: who cleans the teeth?",
"why": "Inference: remove the cleaner, and the problem the cleaner solved comes back."},
{"q": "A tick drinking a dog's blood is an example of:",
"o": ["parasitism", "mutualism", "commensalism", "teamwork"],
"a": "parasitism",
"hint": "One gains, the other suffers.",
"why": "Parasitism = one gains while the other suffers."},
{"q": "Why must 'a good detective' check the evidence?",
"o": ["Because some scientists think part of the story may be a legend.",
"Because plovers cannot fly.", "Because crocodiles never eat.", "Because the Nile is small."],
"a": "Because some scientists think part of the story may be a legend.",
"hint": "Find the sentence that begins with 'Some scientists'.",
"why": "Critical reading: the author warns that the story is not fully proven."},
{"q": "The word 'fearlessly' in the passage means:",
"o": ["without fear", "with a loud voice", "very slowly", "in the dark"],
"a": "without fear",
"hint": "-less means without.",
"why": "fear + less + ly = without fear."},
] 

NEGOTIATING = [
"Let's make a deal", "How about", "I'm willing to", "I can offer you", "Would you consider",
"What if", "Can we meet halfway", "That's my final offer", "I'm afraid I can't",
"I'd be happy to", "Let me suggest", "I'd like to propose",
] # عدّل هذه القائمة لتطابق عبارات الجدول الأزرق (Negotiating) في كتاب الطالب حرفياً. 

SCENARIOS = {
"🚲 Buy a used bike": {"item": "mountain bike", "ask": 1200, "min": 850},
"💻 Buy a gaming laptop": {"item": "gaming laptop", "ask": 3000, "min": 2300},
"🎟️ Buy season tickets": {"item": "season ticket", "ask": 600, "min": 420},
} 

SENSORY = {
"👁️ Sight": ["big", "huge", "bright", "dark", "green", "golden", "tiny", "sharp", "shiny", "colorful",
"colourful", "sparkling", "wide", "muddy", "blue"],
"👂 Sound": ["loud", "quiet", "noisy", "splash", "splashing", "buzz", "chirp", "chirping", "roar",
"whisper", "hiss", "silent", "sound", "hear", "heard"],
"✋ Touch": ["rough", "smooth", "soft", "hot", "cold", "warm", "scaly", "slippery", "sticky", "wet",
"dry", "hard"],
"👃 Smell": ["smell", "smells", "fresh", "stinky", "sweet", "scent", "fragrant", "aroma"],
"👅 Taste": ["taste", "tastes", "sweet", "salty", "sour", "bitter", "delicious", "spicy"],
}
ADJECTIVES = ["beautiful", "amazing", "powerful", "dangerous", "friendly", "clever", "brave", "gentle",
"enormous", "fearless", "peaceful", "wonderful", "helpful", "useful", "tiny", "huge", "bright",
"shiny", "colorful", "strong", "small", "big", "lovely", "important", "huge"]
TRANSITIONS = ["firstly", "first", "also", "besides", "moreover", "however", "in addition", "for example",
"for instance", "finally", "in conclusion", "as a result", "because", "therefore", "although",
"on the other hand"] 

W_TOPICS = ["The crocodile and the plover", "My best friend (two is better than one)",
"My favourite place", "A famous landmark in Saudi Arabia"]
W_STEPS = [
("1️⃣ Topic sentence", "Introduce what you will describe and why it is special."),
("2️⃣ Sensory details", "Describe what you see, hear, touch, smell or taste."),
("3️⃣ Connect ideas", "Use other / others / another / the other(s), an emphatic do, and linking words."),
("4️⃣ Conclusion", "Finish with your feeling or lesson. Start with 'In conclusion'."),
]


=====================================================================
4) TAB 1 - GRAMMAR (FMF)
=====================================================================
def tab_grammar():
st.markdown("### 🎯 Grammar Arena: Other · Others · Another · Emphatic Do")
with st.expander("📘 FMF cheat sheet (Form · Meaning · Function)"):
st.markdown(
"- another + singular noun → one more (another game)\n"
"- other + plural / uncountable noun → additional or different (other games)\n"
"- others = other + plural noun, without the noun (Some are fun; others are boring.)\n"
"- the other → the second one of two\n"
"- the others → all the rest of a known group\n"
"- Emphatic do (do / does / did + base verb) → to stress or correct (I do like it!)"
) 

choice = st.selectbox("اختر اهتمامك / Choose your interest", list(INTERESTS))
d = INTERESTS[choice]
if st.button("🎤 Start live debate", key="start_debate"):
st.session_state.debate = build_debate(d) 

for side, who, line, note in st.session_state.debate:
cls = "team-a" if side == "A" else "team-b"
st.markdown('<div class="say ' + cls + '"><b>' + who + '</b><br>' + hl(line) + '</div>',
unsafe_allow_html=True)
st.caption("📌 " + note) 

show_live(d["topic"], "🌐 Live content about my interest") 

st.markdown("#### 🥊 Your rebuttal")
st.caption("اكتب رداً من جملتين أو أكثر واستخدم 3 تراكيب على الأقل: another / other / others / the other / the others / emphatic do")
with st.form("rebuttal_form"):
text = st.text_area("Write your rebuttal", height=110, placeholder="I do like " + d["obj"] + ", but ...")
go = st.form_submit_button("🚀 Analyze my grammar")
if go:
found = detect_structures(text)
new = [s for s in found if s not in st.session_state.gram_awarded]
st.session_state.gram_awarded.extend(new)
st.session_state.points += 5 * len(new)
st.session_state.gram_last = {"found": sorted(found), "new": new}
st.rerun()
last = st.session_state.gram_last
if last:
all_s = ["another", "other", "others", "the other", "the others", "emphatic do"]
chips = "".join('<span class="chip ' + ("chip-on" if s in last["found"] else "") + '">' + s + '</span>'
for s in all_s)
st.markdown(chips, unsafe_allow_html=True)
if last["new"]:
st.success("+" + str(5 * len(last["new"])) + " points for: " + ", ".join(last["new"]))
if len(last["found"]) >= 3:
st.success("🏆 Excellent! You used " + str(len(last["found"])) + " target structures.")
else:
st.info("Try to use at least 3 different structures. Found: " + (", ".join(last["found"]) or "none")) 

st.markdown("#### ✅ Quick check")
with st.form("gq_form"):
answers = []
for i, q in enumerate(GQ):
answers.append(st.radio(str(i + 1) + ". " + q["q"], q["o"], index=None, key="gq_" + str(i)))
sub = st.form_submit_button("Check answers")
if sub:
score = sum(1 for a, q in zip(answers, GQ) if a == q["a"])
st.session_state.gq_result = {"score": score, "answers": answers}
if not st.session_state.gq_awarded:
st.session_state.gq_awarded = True
st.session_state.points += score * 10
st.rerun()
res = st.session_state.gq_result
if res:
st.markdown("Score: " + str(res["score"]) + " / " + str(len(GQ)) + " ")
for i, (a, q) in enumerate(zip(res["answers"], GQ)):
if a == q["a"]:
st.write("✅ " + str(i + 1) + ". " + q["a"])
else:
st.write("❌ " + str(i + 1) + ". Correct answer: " + q["a"] + " ")


=====================================================================
5) TAB 2 - READING (ENVIRONMENTAL DETECTIVE)
=====================================================================
def reset_reading():
st.session_state.rd_idx = 0
st.session_state.rd_result = {}
st.session_state.rd_hints = []
st.session_state.rd_over = False
st.session_state.energy = 100


def tab_reading():
st.markdown("### 🕵️ The Environmental Detective")
st.caption("Nile crocodile = تمساح النيل | plover (zic-zac) = الزقزاق | mutualism = تبادل المنفعة")
st.markdown('<div class="card">' + PASSAGE + '</div>', unsafe_allow_html=True)
show_live("crocodile plover mutualism", "🌐 Open live case file") 

idx = st.session_state.rd_idx
total = len(RQ) 

if st.session_state.rd_over:
if idx in st.session_state.rd_result:
ok, why = st.session_state.rd_result[idx]
st.info(("✅ " if ok else "❌ ") + why)
st.error("⚡ Your energy is empty. Mission failed - but every detective learns from mistakes!")
if st.button("🔄 Restart mission", key="rd_restart_over"):
reset_reading()
st.rerun()
return 

if idx >= total:
pts = st.session_state.points
rank = "🥇 Master Detective" if pts >= 100 else "🥈 Senior Detective" if pts >= 50 else "🥉 Junior Detective"
st.success("🎉 Case closed! Rank: " + rank + " | Energy left: " + str(st.session_state.energy))
if st.button("🔄 New mission", key="rd_restart_done"):
reset_reading()
st.rerun()
return 

q = RQ[idx]
st.progress(idx / total)
st.markdown("Clue " + str(idx + 1) + " / " + str(total) + " ") 

if idx in st.session_state.rd_result:
ok, why = st.session_state.rd_result[idx]
(st.success if ok else st.error)(("✅ Correct! +20 points. " if ok else "❌ Not quite (-20 energy). ") + why)
label = "Finish ✅" if idx + 1 >= total else "Next clue ➡️"
if st.button(label, key="rd_next_" + str(idx)):
st.session_state.rd_idx += 1
st.rerun()
return 

choice = st.radio(q["q"], q["o"], index=None, key="rd_choice_" + str(idx))
if idx in st.session_state.rd_hints:
st.info("💡 " + q["hint"])
c1, c2 = st.columns(2)
if c1.button("💡 Hint (-10 ⚡)", key="rd_hint_" + str(idx)):
if idx not in st.session_state.rd_hints:
st.session_state.rd_hints.append(idx)
st.session_state.energy = max(0, st.session_state.energy - 10)
if st.session_state.energy <= 0:
st.session_state.rd_over = True
st.rerun()
if c2.button("🔎 Check", key="rd_check_" + str(idx)):
if choice is None:
st.warning("Choose an answer first.")
else:
ok = choice == q["a"]
if ok:
st.session_state.points += 20
st.session_state.energy = min(100, st.session_state.energy + 5)
else:
st.session_state.energy = max(0, st.session_state.energy - 20)
st.session_state.rd_result[idx] = (ok, q["why"])
if st.session_state.energy <= 0:
st.session_state.rd_over = True
st.rerun()


=====================================================================
6) TAB 3 - SPEAKING (THE LIVE DEAL MAKER)
=====================================================================
def reset_deal(name):
s = SCENARIOS[name]
st.session_state.deal_scn = name
st.session_state.deal_msgs = [
("seller", "Good morning! This " + s["item"] + " costs " + str(s["ask"]) + " SAR. It's in excellent condition.")
]
st.session_state.deal_meter = 25
st.session_state.deal_round = 0
st.session_state.deal_used = []
st.session_state.deal_state = "playing"
st.session_state.deal_offer = None


def deal_turn(msg):
s = SCENARIOS[st.session_state.deal_scn]
ask, floor = s["ask"], s["min"]
txt = msg.replace("’", "'")
low = txt.lower()
st.session_state.deal_msgs.append(("you", msg))
st.session_state.deal_round += 1 

found = [p for p in NEGOTIATING if p.lower().replace("’", "'") in low]
new = [p for p in found if p not in st.session_state.deal_used]
st.session_state.deal_used.extend(new) 

delta = min(len(new), 3) * 8
if found and not new:
delta -= 3
if not found:
delta -= 5
rude = re.search(r"\b(stupid|idiot|shut up|rubbish|useless)\b", low)
if rude:
delta -= 15 

nums = re.findall(r"\d{1,3}(?:,\d{3})+|\d+", txt)
offer = int(nums[-1].replace(",", "")) if nums else None
if offer is not None:
st.session_state.deal_offer = offer
if offer >= floor:
delta += 15
elif offer >= 0.7 * ask:
delta += 5
else:
delta -= 5 

meter = max(0, min(100, st.session_state.deal_meter + delta))
st.session_state.deal_meter = meter
counter = max(floor, int(ask - (ask - floor) * meter / 100)) 

if rude:
reply = "Hmm, that's not very polite. I can only do business with respect."
elif not found:
reply = "I'd love to help, but please use negotiating language, like 'How about...' or 'I can offer you...'."
elif offer is None:
reply = "Interesting. What price do you have in mind?"
elif meter >= 70 and offer >= floor:
pts = 30 + max(0, 8 - st.session_state.deal_round) * 5
st.session_state.points += pts
st.session_state.deal_state = "won"
reply = "You have a deal at " + str(offer) + " SAR! Pleasure doing business with you. (+" + str(pts) + " points)"
elif offer >= floor:
reply = "Your price is fair, but I need you to be more persuasive. Use more negotiating phrases!"
else:
reply = "I'm afraid that's too low for me. How about " + str(counter) + " SAR?" 

st.session_state.deal_msgs.append(("seller", reply))
if st.session_state.deal_state != "won" and st.session_state.deal_round >= 8:
st.session_state.deal_state = "lost"
st.session_state.deal_msgs.append(("seller", "I'm sorry, we've run out of time. Maybe next time!"))


def tab_deal():
st.markdown("### 🤝 The Live Deal Maker")
st.caption("استخدم عبارات جدول Negotiating لرفع نسبة نجاح الصفقة. أنت المشتري والذكاء الاصطناعي هو البائع.")
pick = st.selectbox("Choose a deal", list(SCENARIOS), key="deal_pick")
if st.session_state.deal_scn != pick:
reset_deal(pick) 

s = SCENARIOS[st.session_state.deal_scn]
with st.expander("🌐 Live market intel (Perplexity)"):
res = live_pipeline("fair price of a used " + s["item"] + " market")
st.write(res["answer"]) 

meter = st.session_state.deal_meter
st.progress(meter / 100)
st.markdown("Deal success: " + str(meter) + "% | Round " + str(st.session_state.deal_round) + " / 8")
chips = "".join(
'<span class="chip ' + ("chip-on" if p in st.session_state.deal_used else "") + '">' + p + '</span>'
for p in NEGOTIATING
)
st.markdown(chips, unsafe_allow_html=True) 

for role, text in st.session_state.deal_msgs:
with st.chat_message("assistant" if role == "seller" else "user"):
st.write(text) 

if st.session_state.deal_state == "playing":
with st.form("deal_form", clear_on_submit=True):
msg = st.text_input("Your offer", placeholder="How about 900 SAR? I'm willing to pay cash.")
send = st.form_submit_button("Send ✉️")
if send and msg.strip():
deal_turn(msg.strip())
st.rerun()
elif st.session_state.deal_state == "won":
st.success("🏆 Deal closed! Great negotiating.")
else:
st.error("⏰ Deal failed. Try again with more negotiating phrases.")
if st.button("🔄 Restart deal", key="deal_restart"):
reset_deal(st.session_state.deal_scn)
st.rerun()


=====================================================================
7) TAB 4 - WRITING ASSISTANT
=====================================================================
def count_words(t):
return len(re.findall(r"[A-Za-z']+", t))


def sensory_hits(text):
low = text.lower()
return [k for k, ws in SENSORY.items() if any(re.search(r"\b" + w + r"\b", low) for w in ws)]


def analyze_essay(parts):
text = " ".join(parts)
low = text.lower()
words = count_words(text)
cats = sensory_hits(text)
adjs = {a for a in ADJECTIVES if re.search(r"\b" + a + r"\b", low)}
trans = {t for t in TRANSITIONS if re.search(r"\b" + t + r"\b", low)}
gram = detect_structures(text)
has_topic = count_words(parts[0]) >= 8
has_concl = count_words(parts[3]) >= 8
sentences = [x for x in re.split(r"[.!?]+", text) if x.strip()]
avg = words / len(sentences) if sentences else 0 

score = (
min(words / 100, 1) * 20
+ min(len(cats) / 3, 1) * 20
+ min(len(adjs) / 6, 1) * 15
+ min(len(trans) / 3, 1) * 15
+ min(len(gram) / 3, 1) * 15
+ (7.5 if has_topic else 0)
+ (7.5 if has_concl else 0)
)
return {"score": int(round(score)), "words": words, "cats": cats, "adjs": adjs, "trans": trans,
"gram": gram, "topic": has_topic, "concl": has_concl, "avg": avg}


def live_hint(step, text, topic):
n = count_words(text)
low = text.lower()
if step == 0:
if n == 0:
return "💡 ابدأ بجملة رئيسية مثل: " + topic + " shows that two is better than one."
if n < 8:
return "✍️ الجملة قصيرة؛ أضف سبب تميّز الموضوع (8 كلمات على الأقل)."
return "✅ جملة موضوع ممتازة! انتقل إلى التفاصيل الحسية."
if step == 1:
cats = sensory_hits(text)
missing = [k for k in SENSORY if k not in cats]
if n == 0:
return "💡 صف ما تراه وما تسمعه: The huge, scaly crocodile lies in the warm sun..."
if len(cats) < 3:
return "🎯 أضف حاسة جديدة: " + ", ".join(missing[:2]) + " (تحتاج 3 حواس على الأقل)."
return "✅ رائع! استخدمت " + str(len(cats)) + " حواس."
if step == 2:
gram = detect_structures(text)
tr = [t for t in TRANSITIONS if re.search(r"\b" + t + r"\b", low)]
tips = []
if len(gram) < 2:
tips.append("استخدم another / others / the other أو emphatic do")
if len(tr) < 2:
tips.append("أضف كلمات ربط: also, however, for example")
return "🔗 " + ("؛ ".join(tips) if tips else "✅ ربط ممتاز للأفكار!")
if n == 0:
return "💡 ابدأ بـ: In conclusion, ..."
if "conclusion" not in low:
return "🏁 جرّب أن تبدأ الخاتمة بـ In conclusion أو To sum up."
return "✅ خاتمة جيدة!"


def tab_writing():
st.markdown("### ✍️ Smart Writing Coach: Descriptive Essay")
topic = st.selectbox("Choose your topic", W_TOPICS, key="w_topic")
show_live(topic, "🌐 Live ideas for my topic") 

step = st.session_state.w_step
data = st.session_state.w_data
title, task = W_STEPS[step]
st.progress((step + 1) / len(W_STEPS))
st.markdown("" + title + " - Step " + str(step + 1) + " / " + str(len(W_STEPS)))
st.caption(task) 

val = st.text_area("Write here", value=data[step], height=140, key="w_text_" + str(step))
data[step] = val
st.session_state.w_data = data
st.info(live_hint(step, val, topic)) 

c1, c2 = st.columns(2)
if c1.button("⬅️ Back", key="w_back") and step > 0:
st.session_state.w_step -= 1
st.rerun()
if c2.button("Next ➡️", key="w_next") and step < len(W_STEPS) - 1:
st.session_state.w_step += 1
st.rerun() 

a = analyze_essay(data)
st.markdown("#### 📊 Essay quality meter")
st.progress(a["score"] / 100)
band = ("🔴 Needs work" if a["score"] < 40 else "🟡 Good start" if a["score"] < 70
else "🟢 Great" if a["score"] < 85 else "🌟 Excellent")
st.markdown("" + str(a["score"]) + " / 100 - " + band)
st.write("📝 Words: " + str(a["words"]) + " (target 80-150) | 👁️ Senses: " + str(len(a["cats"]))
+ " | 🎨 Adjectives: " + str(len(a["adjs"])) + " | 🔗 Linkers: " + str(len(a["trans"]))
+ " | 🎯 Unit grammar: " + str(len(a["gram"])) + "")
st.write(("✅" if a["topic"] else "⬜") + " Topic sentence " + ("✅" if a["concl"] else "⬜") + " Conclusion") 

if a["score"] >= 70 and not st.session_state.w_awarded:
st.session_state.w_awarded = True
st.session_state.points += 40
st.session_state.celebrate = True
st.rerun() 

if any(x.strip() for x in data):
st.markdown("#### 📄 Your essay")
essay = " ".join(x.strip() for x in data if x.strip())
st.code(essay, language=None)


=====================================================================
8) MAIN
=====================================================================
init_state()
if st.session_state.deal_scn is None:
reset_deal(list(SCENARIOS)[0]) 

st.markdown(
'<div class="hero"><h1>🌍 The Live-World Simulator</h1>'
'<p>Mega Goal 3 • Unit 1 • Two Is Better Than One</p></div>',
unsafe_allow_html=True,
)
if st.session_state.celebrate:
st.session_state.celebrate = False
st.balloons()
st.text_input("👤 اسم الطالب / Student name", key="name", placeholder="اكتب اسمك هنا...")
if st.session_state.name.strip():
st.write("Welcome, " + st.session_state.name.strip() + " ! 👋") 

m1, m2 = st.columns(2)
m1.metric("⭐ Points", st.session_state.points)
m2.metric("⚡ Detective energy", str(st.session_state.energy) + "%")
st.progress(st.session_state.energy / 100) 

t1, t2, t3, t4 = st.tabs(["🎯 Grammar", "🕵️ Reading", "🤝 Speaking", "✍️ Writing"])
with t1:
tab_grammar()
with t2:
tab_reading()
with t3:
tab_deal()
with t4:
tab_writing() 

st.markdown(
'<div class="footer">جميع الحقوق محفوظة © المعلم مبارك آل مطلقة - عام 2026م'
'<br>Developed by Tr. Mubarak Almutlakah</div>',
unsafe_allow_html=True,
)
st.markdown("<!-- Tr. Mubarak Almutlakah -->", unsafe_allow_html=True)
End of file - Tr. Mubarak Almutlakah

