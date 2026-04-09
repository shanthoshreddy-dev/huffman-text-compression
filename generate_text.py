"""
Generates realistic English text using real word frequency distribution (Zipf law).
Simulates content from stories/papers — lowercase only, no punctuation.
"""
import random, re

# ~5000 real English words (mix of common + academic + narrative vocabulary)
# Grouped roughly by frequency for realistic Zipf distribution
FREQ_TIERS = {
    0: ["the","of","and","a","to","in","is","it","you","that","he","was","for","on","are",
        "as","with","his","they","at","be","this","from","or","one","had","by","but","not",
        "what","all","were","when","we","there","can","an","your","which","their","said",
        "if","do","into","has","more","her","two","like","him","see","time","could","no",
        "make","than","been","its","now","my","made","over","did","down","only","way"],

    1: ["find","use","may","water","long","little","very","after","words","called","just",
        "where","most","know","get","through","back","much","before","go","good","new",
        "write","our","used","me","man","too","any","day","same","right","look","think",
        "also","around","another","came","come","work","three","word","must","because",
        "does","part","even","place","well","such","here","take","why","help","put","great",
        "still","own","while","should","never","each","those","people","how","let","large",
        "big","give","hand","turn","small","set","off","again","old","between","need","last"],

    2: ["school","follow","move","try","kind","spell","add","land","below","often","together",
        "city","run","once","open","seem","light","example","begin","life","always","next",
        "hard","both","near","real","face","already","tell","since","side","keep","children",
        "feet","eyes","start","stop","mile","night","walk","white","sea","began","grow","took",
        "river","four","carry","state","book","hear","without","second","later","miss","idea",
        "enough","eat","watch","far","almost","above","girl","sometimes","mountain","cut",
        "young","talk","soon","list","song","being","leave","family","body","music","color"],

    3: ["stand","sun","fish","area","mark","dog","horse","birds","problem","room","knew",
        "ever","piece","told","usually","friend","ready","country","father","tree","earth",
        "thought","head","under","story","saw","left","few","north","air","away","animal",
        "house","page","letter","mother","answer","found","study","plant","cover","food",
        "group","hold","ground","interest","reach","fast","five","sing","listen","six",
        "table","travel","less","morning","ten","simple","several","toward","war","lay",
        "against","pattern","slow","center","love","person","money","serve","appear","road",
        "map","rain","rule","govern","pull","cold","notice","voice","fall","power","town",
        "fine","drive","short","red","fly","gave","unit","figure","certain","field","deep"],

    4: ["across","today","during","though","heart","class","space","happened","point","game",
        "system","bring","watch","shell","dry","within","floor","ice","ship","across","stay",
        "green","known","island","week","less","machine","base","ago","stood","plane","wonder",
        "laugh","thousand","ago","ran","check","game","shape","equate","hot","miss","brought",
        "heat","snow","tire","bring","yes","distant","fill","east","paint","language","among",
        "grand","ball","yet","wave","drop","heart","present","heavy","dance","engine","position",
        "arm","wide","sail","material","fraction","science","clean","energy","hunt","probable",
        "perhaps","rest","rather","final","written","star","party","force","hat","gold","age"],

    5: ["win","decide","decimal","gentle","woman","captain","practice","separate","difficult",
        "doctor","please","protect","noon","whose","locate","ring","character","insect","caught",
        "period","indicate","radio","spoke","atom","human","history","effect","electric","expect",
        "crop","modern","element","hit","student","corner","party","supply","bone","rail","imagine",
        "provide","agree","thus","capital","chair","danger","fruit","rich","thick","soldier","process",
        "operate","guess","necessary","sharp","wing","create","neighbor","wash","bat","rather","crowd",
        "corn","compare","poem","string","bell","depend","meat","rub","tube","famous","dollar","stream",
        "fear","sight","thin","triangle","planet","hurry","chief","colony","clock","mine","tie","enter",
        "major","fresh","search","send","yellow","gun","allow","print","dead","spot","desert","suit"],

    6: ["current","lift","rose","continue","block","chart","hat","sell","success","company",
        "subtract","event","particular","deal","swim","term","opposite","wife","shoe","shoulder",
        "spread","arrange","camp","invent","cotton","born","determine","quart","nine","truck",
        "noise","level","chance","gather","shop","stretch","throw","shine","property","column",
        "molecule","select","wrong","gray","repeat","require","broad","prepare","salt","nose",
        "plural","anger","claim","continent","hollow","yet","lead","constitute","glass","vowel",
        "toward","power","town","fine","drive","short","red","fly","gave","unit","figure",
        "master","protect","noon","whose","locate","ring","character","insect","caught","period",
        "indicate","radio","spoke","atom","human","history","effect","electric","expect","crop"],
}

# Additional words to make dictionary larger than text vocabulary
EXTRA_WORDS = [
    "abolish","abrupt","absent","absorb","abstract","abundant","academic","accept","access",
    "accurate","achieve","acquire","active","actual","adapt","address","adequate","adjust",
    "advance","adverse","affect","affirm","afford","agenda","aggregate","agile","alert",
    "allocate","alter","ambiguous","ample","analyze","anchor","ancient","annual","apparent",
    "apply","approve","argue","arise","aspect","assess","assign","assist","assume","attach",
    "attempt","attribute","audit","authorize","balance","barrier","benefit","broad","budget",
    "capable","capture","category","caution","challenge","channel","clarity","classify",
    "collaborate","commit","complex","component","concept","conclude","conduct","confirm",
    "conflict","connect","consequence","consider","consistent","construct","context","contrast",
    "contribute","control","convert","coordinate","correct","criteria","critical","crucial",
    "culture","cycle","database","debate","decline","define","deliver","demonstrate","depend",
    "describe","design","detect","develop","digital","dimension","direct","discuss","distribute",
    "diverse","document","domain","dominant","dynamic","economic","effective","efficient",
    "eliminate","emerge","emphasis","enhance","ensure","establish","evaluate","evidence",
    "examine","exceed","execute","expand","explicit","explore","expose","extend","external",
    "facilitate","factor","feature","focus","format","formula","foundation","framework",
    "function","generate","global","guideline","handle","identify","impact","implement",
    "improve","include","indicate","individual","influence","inform","initial","integrate",
    "interpret","introduce","invest","involve","isolate","justify","knowledge","layer","limit",
    "maintain","manage","measure","method","minimize","monitor","multiple","network","objective",
    "obtain","optimize","organize","output","overall","parameter","perform","precise","predict",
    "primary","principle","priority","process","produce","project","promote","propose","protect",
    "publish","qualify","quantity","question","recognize","recommend","reduce","reflect","region",
    "relate","release","relevant","reliable","represent","require","resolve","resource","respond",
    "result","retain","reveal","review","revise","scale","secure","select","sequence","significant",
    "similar","solution","source","specific","standard","strategy","structure","submit","support",
    "survey","sustain","target","technique","theory","transfer","transform","translate","trigger",
    "understand","update","utilize","validate","variable","verify","version","volume","withdraw",
]

ALL_WORDS = []
seen = set()
for tier_words in FREQ_TIERS.values():
    for w in tier_words:
        if w not in seen: seen.add(w); ALL_WORDS.append(w)
for w in EXTRA_WORDS:
    if w not in seen: seen.add(w); ALL_WORDS.append(w)

# Weights: tier 0 = very frequent, tiers decrease, extra words = rare
def word_weights():
    weights = []
    tier_base = {0:100, 1:40, 2:15, 3:6, 4:2.5, 5:1.0, 6:0.4}
    for tier, words in FREQ_TIERS.items():
        base = tier_base[tier]
        for i, w in enumerate(words):
            weights.append((w, base / (i+1)))
    for w in EXTRA_WORDS:
        weights.append((w, 0.1))
    return weights

WEIGHTED = word_weights()
WORDS_LIST  = [w for w,_ in WEIGHTED]
WEIGHT_LIST = [v for _,v in WEIGHTED]

def generate(n_words):
    return ' '.join(random.choices(WORDS_LIST, weights=WEIGHT_LIST, k=n_words))

print(f"Vocabulary size: {len(ALL_WORDS)} words  ({len(FREQ_TIERS[0])} tier0, extras: {len(EXTRA_WORDS)})")

if __name__ == '__main__':
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 250
    print(generate(n))
