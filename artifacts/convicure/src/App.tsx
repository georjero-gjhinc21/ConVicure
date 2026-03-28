import { useEffect, useRef, useState, Component, type ReactNode } from "react";

function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const scrollTo = (id: string) => {
    const el = document.querySelector(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    setMenuOpen(false);
  };

  return (
    <nav id="navbar" className={scrolled ? "scrolled" : ""}>
      <div className="nav-inner">
        <a href="#hero" className="nav-logo" onClick={(e) => { e.preventDefault(); scrollTo("#hero"); }}>
          <span className="logo-con">Con</span><span className="logo-vi">Vi</span><span className="logo-cure">Cure</span>
        </a>
        <button className="nav-toggle" aria-label="Toggle menu" onClick={() => setMenuOpen(!menuOpen)}>
          <span></span><span></span><span></span>
        </button>
        <div className={`nav-links${menuOpen ? " open" : ""}`}>
          {[["#problem", "The Problem"], ["#approach", "Our Approach"], ["#pipeline", "Pipeline"], ["#science", "Science"], ["#tbi", "TBI Program"], ["#team", "Leadership"]].map(([href, label]) => (
            <a key={href} href={href} onClick={(e) => { e.preventDefault(); scrollTo(href); }}>{label}</a>
          ))}
          <a href="#contact" className="nav-cta" onClick={(e) => { e.preventDefault(); scrollTo("#contact"); }}>Contact Us</a>
        </div>
      </div>
    </nav>
  );
}

function Hero() {
  const scrollTo = (id: string) => {
    const el = document.querySelector(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };
  return (
    <section id="hero">
      <div className="hero-bg"></div>
      <div className="hero-content">
        <p className="hero-label">Preclinical-Stage Biopharmaceutical Company</p>
        <h1>Developing the First-in-Class Treatment for <em>Persistent Tick-Borne Illness</em></h1>
        <p className="hero-sub">A four-drug combination therapy based on peer-reviewed research by our founding scientist, targeting the pathogens that current antibiotics leave behind.</p>
        <div className="hero-actions">
          <a href="#approach" className="btn btn-primary" onClick={(e) => { e.preventDefault(); scrollTo("#approach"); }}>Our Science</a>
          <a href="#contact" className="btn btn-outline" onClick={(e) => { e.preventDefault(); scrollTo("#contact"); }}>Partner With Us</a>
        </div>
        <div className="hero-stats">
          <div className="stat">
            <span className="stat-num">476K+</span>
            <span className="stat-label">New U.S. Lyme cases annually</span>
          </div>
          <div className="stat">
            <span className="stat-num">20%</span>
            <span className="stat-label">Develop persistent symptoms</span>
          </div>
          <div className="stat">
            <span className="stat-num">Zero</span>
            <span className="stat-label">FDA-approved treatments for persistent Lyme</span>
          </div>
        </div>
      </div>
    </section>
  );
}

function useIntersection(ref: React.RefObject<Element | null>) {
  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add("visible");
      });
    }, { threshold: 0.1 });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [ref]);
}

function Problem() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  return (
    <section id="problem" ref={ref}>
      <div className="container">
        <p className="section-label">The Unmet Need</p>
        <h2>Millions Suffer. No FDA-Approved Treatment Exists.</h2>
        <div className="problem-grid">
          <div className="problem-card">
            <div className="problem-icon">🦠</div>
            <h3>Lyme Disease (Borreliosis)</h3>
            <span className="pathogen-species">Borrelia burgdorferi s.l.</span>
            <p>The spirochete bacterium that causes Lyme disease. Standard antibiotics kill active bacteria but fail against semi-dormant <strong>"persister"</strong> forms that evade treatment and drive chronic symptoms.</p>
          </div>
          <div className="problem-card">
            <div className="problem-icon">🧬</div>
            <h3>Bartonellosis</h3>
            <span className="pathogen-species">Bartonella henselae &amp; related species</span>
            <p>An intracellular bacterium found in 30–50% of Lyme patients as a coinfection. Causes neuropsychiatric and vascular symptoms. Requires extended, targeted antibiotic combinations that standard Lyme protocols ignore.</p>
          </div>
          <div className="problem-card">
            <div className="problem-icon">🩸</div>
            <h3>Babesiosis</h3>
            <span className="pathogen-species">Babesia microti, B. duncani &amp; related species</span>
            <p>A malaria-like parasite that infects red blood cells. Standard Lyme antibiotics have zero effect. Requires antiparasitic therapy — yet is frequently overlooked, misdiagnosed, or dismissed entirely.</p>
          </div>
        </div>
        <div className="problem-callout">
          <p>These three pathogens — the <strong>"Trio Coinfection"</strong> — attack patients simultaneously. Yet no existing treatment addresses all three. Current protocols fail because they treat one pathogen while leaving the others unchecked.</p>
        </div>
      </div>
    </section>
  );
}

function Approach() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  return (
    <section id="approach" ref={ref}>
      <div className="container">
        <p className="section-label">Our Approach</p>
        <h2>Four Drugs. Three Pathogens. One Combination Therapy.</h2>
        <p className="section-intro">ConViCure is developing a rationally designed four-drug combination that simultaneously targets all three pathogens in persistent tick-borne illness — a first-of-its-kind approach pursuing FDA approval.</p>
        <div className="drug-grid">
          <div className="drug-card">
            <div className="drug-number">1</div>
            <h3>CvC-1</h3>
            <p className="drug-target">Targets: Borrelia burgdorferi s.l. (active + persister forms)</p>
            <p>The lead compound — identified through high-throughput screening of nearly 8,000 compounds by our founding scientist's research team. Uniquely kills both actively replicating spiral forms <em>and</em> semi-dormant round-body persister forms of Borrelia. FDA-approved compound being reformulated as a novel oral liposomal delivery system.</p>
          </div>
          <div className="drug-card">
            <div className="drug-number">2</div>
            <h3>CvC-2</h3>
            <p className="drug-target">Targets: Borrelia, Bartonella</p>
            <p>Broad-spectrum macrolide antibiotic with intracellular penetration. Effective against both extracellular Borrelia and intracellular Bartonella. Well-established safety profile with decades of clinical use.</p>
          </div>
          <div className="drug-card">
            <div className="drug-number">3</div>
            <h3>CvC-3</h3>
            <p className="drug-target">Targets: Borrelia persisters, biofilms</p>
            <p>FDA-approved compound with demonstrated activity against Borrelia persister cells and biofilm formations. Disrupts the protective barriers that allow bacteria to survive standard antibiotic treatment.</p>
          </div>
          <div className="drug-card">
            <div className="drug-number">4</div>
            <h3>CvC-4</h3>
            <p className="drug-target">Targets: Babesia spp., inflammation</p>
            <p>Natural compound with potent antiparasitic activity against Babesia species and demonstrated anti-inflammatory and neuroprotective properties. Addresses the parasitic coinfection component that antibiotics cannot reach.</p>
          </div>
        </div>
        <div className="delivery-callout">
          <h3>Liposomal Oral Delivery Innovation</h3>
          <p>CvC-1 was historically IV-only and discontinued from commercial markets. ConViCure is developing a proprietary oral liposomal formulation that solves the bioavailability challenge — making this breakthrough compound accessible to patients as an oral medication for the first time.</p>
        </div>
      </div>
    </section>
  );
}

function Pipeline() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  return (
    <section id="pipeline" ref={ref}>
      <div className="container">
        <p className="section-label">Development Pipeline</p>
        <h2>Structured Path to FDA Approval</h2>
        <div className="pipeline-visual">
          <div className="pipeline-header-row">
            <div className="pipeline-name-col">Program</div>
            <div className="pipeline-stage">Discovery</div>
            <div className="pipeline-stage">Preclinical</div>
            <div className="pipeline-stage">IND Filing</div>
            <div className="pipeline-stage">Phase 1/2</div>
          </div>
          <div className="pipeline-row">
            <div className="pipeline-name-col">
              <strong>Persistent Tick-Borne Illness</strong>
              <span className="pipeline-detail">4-drug combination therapy</span>
            </div>
            <div className="pipeline-stage"><div className="pipeline-bar bar-done"></div></div>
            <div className="pipeline-stage"><div className="pipeline-bar bar-active"></div></div>
            <div className="pipeline-stage"><div className="pipeline-bar bar-future"></div></div>
            <div className="pipeline-stage"><div className="pipeline-bar bar-future"></div></div>
          </div>
        </div>
        <div className="pathway-grid">
          <div className="pathway-card">
            <h3>505(b)(2) Pathway</h3>
            <p>ConViCure's lead compounds are FDA-approved drugs, enabling us to reference existing safety data rather than conducting full de novo safety studies. This significantly reduces the time, cost, and risk compared to a traditional new drug application.</p>
          </div>
          <div className="pathway-card">
            <h3>LPAD Pathway</h3>
            <p>The Limited Population Pathway for Antibacterial Drugs allows FDA approval based on smaller, more focused clinical trials for serious infections with unmet needs — directly applicable to persistent Lyme disease where no approved treatment exists.</p>
          </div>
          <div className="pathway-card">
            <h3>Orphan Drug Designation</h3>
            <p>ConViCure is pursuing Orphan Drug Designation for Babesiosis and Bartonellosis indications, which provides regulatory incentives including 7 years of market exclusivity, tax credits, and reduced FDA filing fees.</p>
          </div>
        </div>
      </div>
    </section>
  );
}

function Science() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  return (
    <section id="science" ref={ref}>
      <div className="container">
        <p className="section-label">The Science</p>
        <h2>Peer-Reviewed Research. Published Results. Proven Mechanism.</h2>
        <div className="science-content">
          <div className="science-text">
            <h3>High-Throughput Discovery</h3>
            <p>ConViCure's research originated with our founding scientist's laboratory, where the team systematically screened nearly <strong>8,000 chemical compounds</strong> and tested 50 molecules in culture before identifying the most effective and safest candidates for in vivo testing.</p>
            <h3>Dual-Kill Capability</h3>
            <p>The pivotal 2020 study published in <em>Scientific Reports</em> demonstrated that our combination therapy's lead compound completely eliminates both actively replicating spiral forms and semi-dormant round-body "persister" forms of <em>Borrelia burgdorferi</em>. This dual-kill capability is what distinguishes our proprietary combination from standard antibiotics like doxycycline, which kill active bacteria but fail against the persisters believed to drive lingering symptoms.</p>
            <h3>In Vivo Validation</h3>
            <p>In mouse models evaluated at 7, 14, and 21-day intervals, the lead compound eliminated Borrelia infection. The study further demonstrated that combining it with a complementary antibiotic was even more effective at killing doxycycline-tolerant persisters — supporting the rationale for our combination therapy approach.</p>
            <div className="validation-callout">
              <p>Our founding scientist's discoveries have been independently validated by researchers at Tulane University, Northeastern University, and Columbia University, and adopted into clinical practice by leading tick-borne disease physicians.</p>
            </div>
          </div>
          <div className="science-sidebar">
            <div className="science-stat-card">
              <span className="science-big">~8,000</span>
              <span>Compounds screened</span>
            </div>
            <div className="science-stat-card">
              <span className="science-big">14,600+</span>
              <span>Citations (Lead Scientist)</span>
            </div>
            <div className="science-stat-card">
              <span className="science-big">100%</span>
              <span>Persister elimination in vitro</span>
            </div>
            <div className="pub-card">
              <h4>Key Publication</h4>
              <p><em>Pothineni et al.</em> "Identification of new drug candidates against Borrelia burgdorferi using high-throughput screening." <strong>Scientific Reports</strong>, 2020.</p>
              <p className="pub-affiliation">Peer-Reviewed · Scientific Reports · 2020</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function FeaturedVideo() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  return (
    <section id="featured-video" ref={ref}>
      <div className="container">
        <p className="section-label">From Our Founding Scientist</p>
        <h2>See the Discovery Explained Firsthand</h2>
        <p className="section-intro video-intro">
          Dr. Jayakumar Rajadas speaks directly about the peer-reviewed research behind ConViCure's
          combination therapy — the science, the mechanism, and why this approach works where
          standard antibiotics fail.
        </p>
        <div className="video-container">
          <div className="video-wrapper">
            <iframe
              src="https://www.youtube.com/embed/aUlKTnrGPgc?rel=0&modestbranding=1&color=white"
              title="ConViCure – Founding Scientist on Tick-Borne Illness Research"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
          <div className="video-caption-row">
            <div className="video-caption-item">
              <span className="video-caption-icon">🔬</span>
              <span>High-throughput compound screening explained</span>
            </div>
            <div className="video-caption-item">
              <span className="video-caption-icon">🧫</span>
              <span>Persister cell mechanism demonstrated</span>
            </div>
            <div className="video-caption-item">
              <span className="video-caption-icon">📋</span>
              <span>Published in Nature's Scientific Reports</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Publications() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  const pubs = [
    {
      journal: "Scientific Reports (Nature Publishing Group)",
      year: "2020",
      summary: "Lead compound eliminated Lyme bacteria in preclinical models, outperforming 7,450 compounds screened.",
      link: "https://www.nature.com/articles/s41598-020-59600-4",
    },
    {
      journal: "Antibiotics (MDPI)",
      year: "2020",
      summary: "FDA-approved metabolic agent showed borreliacidal and anti-inflammatory activity in vivo.",
      link: "https://pubmed.ncbi.nlm.nih.gov/32971817/",
    },
    {
      journal: "Drug Design, Development & Therapy",
      year: "2016",
      summary: "High-throughput screening identified 20 FDA-approved compounds effective against persistent Borrelia.",
      link: "https://pubmed.ncbi.nlm.nih.gov/27103785/",
    },
    {
      journal: "ILADS Scientific Conference",
      year: "2022",
      summary: "Dual-action mechanism demonstrated: anti-inflammatory and anti-persister properties in lead compound.",
      link: "https://www.ilads.org/ilads-conference/orlando-2022/",
    },
  ];
  return (
    <section id="publications" ref={ref}>
      <div className="container">
        <p className="section-label">The Evidence</p>
        <h2>Peer-Reviewed Research</h2>
        <p className="section-intro">ConViCure's science is grounded in published, independently peer-reviewed research. Click any entry to access the original paper.</p>
        <div className="pub-grid">
          {pubs.map((p) => (
            <div className="pub-research-card" key={p.journal}>
              <div className="pub-research-top">
                <span className="pub-research-journal">{p.journal}</span>
                <span className="pub-research-year">{p.year}</span>
              </div>
              <p className="pub-research-summary">{p.summary}</p>
              <a href={p.link} target="_blank" rel="noopener noreferrer" className="btn btn-sm">Read Paper →</a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Press() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  const outlets = [
    { name: "Medical News Today", link: "https://www.medicalnewstoday.com/articles/lyme-disease-treatment" },
    { name: "Neuroscience News", link: "https://neurosciencenews.com/lyme-disease-antibiotics-15914/" },
    { name: "Bay Area Lyme Foundation", link: "https://www.bayarealyme.org/our-research/our-scientists/jayakumar-rajadas/" },
    { name: "Tick Boot Camp Podcast", link: "https://tickbootcamp.com/episode-557-the-stanford-scientist-rewriting-the-future-of-lyme-disease-treatment-dr-jayakumar-rajadas-tick-boot-camp/" },
    { name: "Google Scholar (14,600+ citations)", link: "https://scholar.google.com/citations?user=UtBbZSoAAAAJ&hl=en" },
  ];
  return (
    <section id="press" ref={ref}>
      <div className="container">
        <p className="section-label">Media Coverage</p>
        <h2>Featured In</h2>
        <div className="press-strip">
          {outlets.map((o) => (
            <a key={o.name} href={o.link} target="_blank" rel="noopener noreferrer" className="press-item">
              {o.name}
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

function useCountUp(target: number, duration = 1800, active = false) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!active) return;
    let start = 0;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= target) { setCount(target); clearInterval(timer); }
      else setCount(Math.floor(start));
    }, 16);
    return () => clearInterval(timer);
  }, [active, target, duration]);
  return count;
}

function CountStat({ value, suffix, label }: { value: number; suffix: string; label: string }) {
  const [active, setActive] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const observer = new IntersectionObserver(([e]) => { if (e.isIntersecting) setActive(true); }, { threshold: 0.4 });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  const count = useCountUp(value, 1800, active);
  return (
    <div className="research-stat" ref={ref}>
      <span className="research-stat-num">{count.toLocaleString()}{suffix}</span>
      <span className="research-stat-label">{label}</span>
    </div>
  );
}

function ResearchStats() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  return (
    <section id="research-stats" ref={ref}>
      <div className="container">
        <p className="section-label">By The Numbers</p>
        <h2>A Research Program Built on Decades of Science</h2>
        <div className="research-stats-grid">
          <CountStat value={7450} suffix="+" label="Compounds Screened" />
          <CountStat value={238} suffix="+" label="Peer-Reviewed Publications" />
          <CountStat value={82} suffix="+" label="Patents Filed" />
          <CountStat value={14600} suffix="+" label="Academic Citations" />
          <CountStat value={30} suffix="+" label="Years of Research" />
        </div>
      </div>
    </section>
  );
}

function Timeline() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  const milestones = [
    { year: "2011", text: "Research program launched" },
    { year: "2016", text: "4,000+ drugs screened — 20 FDA-approved hits identified" },
    { year: "2020", text: "Lead compound published in Nature Scientific Reports" },
    { year: "2020", text: "Second compound validated in vivo (Antibiotics journal)" },
    { year: "2022", text: "Dual-action mechanism presented at ILADS conference" },
    { year: "2025", text: "Oral formulation development underway" },
    { year: "2026", text: "Advancing toward FDA IND clearance" },
  ];
  return (
    <section id="timeline" ref={ref}>
      <div className="container">
        <p className="section-label">Research History</p>
        <h2>Milestones Toward the Clinic</h2>
        <div className="timeline">
          {milestones.map((m, i) => (
            <div className={`timeline-item ${i % 2 === 0 ? "left" : "right"}`} key={`${m.year}-${i}`}>
              <div className="timeline-dot"></div>
              <div className="timeline-card">
                <span className="timeline-year">{m.year}</span>
                <p>{m.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function LymeResources() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  const orgs = [
    { name: "Bay Area Lyme Foundation", link: "https://www.bayarealyme.org/" },
    { name: "Global Lyme Alliance", link: "https://www.globallymealliance.org/" },
    { name: "LymeDisease.org", link: "https://www.lymedisease.org/" },
    { name: "ILADS", link: "https://www.ilads.org/" },
    { name: "Project Lyme", link: "https://projectlyme.org/" },
    { name: "LymeX Innovation", link: "https://www.hhs.gov/cto/initiatives/innovation-and-partnerships/lyme-innovation/index.html" },
    { name: "CDC Lyme Disease", link: "https://www.cdc.gov/lyme/" },
  ];
  return (
    <section id="resources" ref={ref}>
      <div className="container">
        <p className="section-label">The Ecosystem</p>
        <h2>Lyme Disease Resources</h2>
        <p className="section-intro">ConViCure operates within a well-funded, growing patient and research ecosystem. These organizations are advancing awareness, research, and advocacy for tick-borne illness worldwide.</p>
        <div className="resources-grid">
          {orgs.map((o) => (
            <a key={o.name} href={o.link} target="_blank" rel="noopener noreferrer" className="resource-tile">
              {o.name}
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

function InvestorThesis() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  const scrollTo = (id: string) => {
    const el = document.querySelector(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };
  const pillars = [
    {
      icon: "🎯",
      heading: "Zero Competition",
      body: "No FDA-approved treatment exists for persistent tick-borne illness. ConViCure is the first company pursuing a four-drug combination approach to address all three co-infecting pathogens simultaneously.",
    },
    {
      icon: "📊",
      heading: "Massive Addressable Market",
      body: "476,000+ new U.S. Lyme cases annually. ~95,000 patients per year develop persistent symptoms. A condition with no approved treatment, growing patient advocacy, and increasing insurer pressure to find solutions.",
    },
    {
      icon: "⚡",
      heading: "De-Risked via 505(b)(2)",
      body: "All four lead compounds are existing FDA-approved drugs. ConViCure leverages prior safety data, dramatically reducing time, cost, and risk versus traditional new drug applications — a structurally faster path to market.",
    },
    {
      icon: "🏆",
      heading: "World-Class Science",
      body: "238+ peer-reviewed publications, 14,600+ citations, and independent validation at Tulane, Northeastern, and Columbia. The lead compound was selected from 7,450 screened candidates and published in Nature's Scientific Reports.",
    },
    {
      icon: "🧬",
      heading: "Platform Optionality",
      body: "The same neuroprotective and anti-inflammatory mechanisms being studied for tick-borne illness also apply to traumatic brain injury — a $17B+ DOD-relevant market providing meaningful pipeline expansion potential.",
    },
    {
      icon: "📅",
      heading: "Near-Term Catalysts",
      body: "Oral liposomal formulation development underway. Orphan Drug Designation filings planned for Babesiosis and Bartonellosis. IND clearance targeted for next funding milestone — clear, measurable progress ahead.",
    },
  ];
  return (
    <section id="investor-thesis" ref={ref}>
      <div className="container">
        <p className="section-label">Investment Opportunity</p>
        <h2>Why ConViCure, Why Now</h2>
        <p className="section-intro thesis-intro">
          ConViCure sits at the intersection of a massive unmet medical need, de-risked science,
          and a first-mover regulatory advantage. Six reasons investors are taking a close look.
        </p>
        <div className="thesis-grid">
          {pillars.map((p) => (
            <div className="thesis-card" key={p.heading}>
              <div className="thesis-icon">{p.icon}</div>
              <h3>{p.heading}</h3>
              <p>{p.body}</p>
            </div>
          ))}
        </div>
        <div className="raise-banner">
          <p className="raise-label">Active Seed Round</p>
          <h3>Currently Raising <em>$6.5M</em></h3>
          <p className="raise-desc">
            Funding will advance ConViCure from preclinical through IND clearance and into Phase 1/2
            clinical trials — the pivotal milestone that de-risks the asset and unlocks partnership
            and licensing opportunities.
          </p>
          <div className="raise-milestones">
            <div className="raise-milestone">
              <span className="raise-milestone-num">1</span>
              <span>Complete oral liposomal formulation</span>
            </div>
            <div className="raise-milestone">
              <span className="raise-milestone-num">2</span>
              <span>File Orphan Drug Designation</span>
            </div>
            <div className="raise-milestone">
              <span className="raise-milestone-num">3</span>
              <span>Submit FDA IND application</span>
            </div>
            <div className="raise-milestone">
              <span className="raise-milestone-num">4</span>
              <span>Enter Phase 1/2 clinical trials</span>
            </div>
          </div>
          <a
            href="#contact"
            className="btn btn-raise"
            onClick={(e) => { e.preventDefault(); scrollTo("#contact"); }}
          >
            Request Investor Materials →
          </a>
        </div>
      </div>
    </section>
  );
}

function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<{ role: "user" | "ai"; text: string }[]>([
    { role: "ai", text: "Welcome to ConViCure. I can answer questions about our science, pipeline, and mission. How can I help?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [retryMsg, setRetryMsg] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (open) bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  const send = async () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text }]);
    setLoading(true);
    setRetryMsg("");

    let attempt = 0;
    const maxAttempts = 3;
    const delays = [1000, 2000, 4000];

    while (attempt < maxAttempts) {
      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json() as { reply: string };
        setMessages((prev) => [...prev, { role: "ai", text: data.reply }]);
        setLoading(false);
        setRetryMsg("");
        return;
      } catch (err) {
        console.error(`Chat request error (attempt ${attempt + 1}):`, err);
        attempt++;
        if (attempt < maxAttempts) {
          setRetryMsg(`Retrying... (${attempt}/${maxAttempts - 1})`);
          await new Promise((r) => setTimeout(r, delays[attempt - 1]));
        }
      }
    }

    setLoading(false);
    setRetryMsg("");
    setMessages((prev) => [...prev, { role: "ai", text: "Sorry, I'm having trouble connecting right now. Please try again shortly or email info@convicure.com." }]);
  };

  return (
    <>
      <button className="chat-fab" onClick={() => setOpen((o) => !o)} aria-label="Open chat">
        {open ? "✕" : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        )}
      </button>
      {open && (
        <div className="chat-panel">
          <div className="chat-header">
            <span><span className="logo-con">Con</span><span className="logo-vi">Vi</span><span className="logo-cure">Cure</span> AI Assistant</span>
            <button onClick={() => setOpen(false)} aria-label="Close chat">✕</button>
          </div>
          <div className="chat-messages">
            {messages.map((m, i) => (
              <div key={i} className={`chat-msg chat-msg--${m.role}`}>
                <p>{m.text}</p>
              </div>
            ))}
            {loading && (
              <div className="chat-msg chat-msg--ai">
                <p>{retryMsg || "Thinking…"}</p>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
          <div className="chat-input-row">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Ask about our science or pipeline…"
              disabled={loading}
            />
            <button onClick={send} disabled={loading || !input.trim()}>Send</button>
          </div>
          <p className="chat-disclaimer">AI assistant — for informational purposes only</p>
        </div>
      )}
    </>
  );
}

function TBI() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  return (
    <section id="tbi" ref={ref}>
      <div className="container">
        <p className="section-label">Secondary Program</p>
        <h2>Traumatic Brain Injury Research</h2>
        <div className="tbi-content">
          <div className="tbi-text">
            <p>Building on the neuroprotective and anti-inflammatory properties observed in our combination therapy platform, ConViCure is exploring therapeutic applications for traumatic brain injury (TBI).</p>
            <p>TBI affects an estimated 2.8 million Americans annually, with particular relevance to military service members exposed to blast overpressure and combat-related injuries. The earlier brain injury can be addressed, the better the expected patient outcome — yet objective diagnosis and acute treatment remain the two greatest unmet gaps.</p>
            <p>Several components of ConViCure's combination platform have demonstrated relevant mechanisms: anti-inflammatory activity that may reduce secondary injury cascade, neuroprotective properties that could stabilize acute injury, and biofilm-disrupting activity relevant to infection prevention in complex traumatic wounds.</p>
            <p>This program is in early-stage research and represents pipeline optionality for ConViCure's drug repurposing platform.</p>
          </div>
          <div className="tbi-facts">
            <div className="tbi-fact">
              <span className="tbi-num">2.8M</span>
              <span>Americans affected by TBI annually</span>
            </div>
            <div className="tbi-fact">
              <span className="tbi-num">DOD</span>
              <span>Alignment with military research priorities</span>
            </div>
            <div className="tbi-fact">
              <span className="tbi-num">Platform</span>
              <span>Leverages existing combination therapy research</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Team() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  const members = [
    {
      photo: "/team/jayakumar-rajadas.png",
      photoPosition: "center center",
      initials: "JR",
      name: "Jayakumar Rajadas, PhD",
      title: "Founder & Chief Scientist",
      bio: "Dr. Jayakumar Rajadas, PhD, brings over 30 years of research leadership in drug delivery, biomaterials, and infectious disease therapeutics. He has authored 238+ peer-reviewed publications (14,600+ citations), developed 82+ patents, and co-founded five biotechnology companies. His research program screened over 7,450 compounds to identify novel therapeutic candidates for persistent tick-borne infections — work featured in major media outlets and adopted by clinicians worldwide.",
    },
    {
      photo: "/team/george-vincent.png",
      initials: "GV",
      name: "George Vincent",
      title: "CEO",
      bio: "Brings operational leadership, financial management, and fundraising expertise to professionalize ConViCure's business infrastructure and lead the company's capital raise and investor readiness efforts.",
    },
    {
      photo: "/team/catherine-shachaf.jpg",
      initials: "CS",
      name: "Catherine Shachaf, PhD",
      title: "Chief Operating Officer",
      bio: "Experienced operational leader in life sciences with expertise in coordinating cross-functional scientific and business teams. Drives strategic partnerships, opportunity sourcing, and operational execution across ConViCure's programs.",
    },
    {
      photo: "/team/mohammed-inayathullah.jpg",
      photoPosition: "center center",
      initials: "MI",
      name: "Mohammed Inayathullah, PhD",
      title: "Chief Scientist",
      bio: "Co-author on the pivotal study published in Scientific Reports. Deep expertise in drug delivery systems, biomaterials, and preclinical development. Provides scientific leadership alongside Dr. Rajadas on formulation and efficacy studies.",
    },
    {
      photo: "/team/adrian-salmeron.jpg",
      initials: "AS",
      name: "Adrian Salmeron",
      title: "Vice President",
      bio: "Supports ConViCure's operational growth and strategic initiatives. Contributes to business development, stakeholder engagement, and the coordination of cross-functional efforts as the company advances toward clinical development.",
    },
  ];
  return (
    <section id="team" ref={ref}>
      <div className="container">
        <p className="section-label">Leadership</p>
        <h2>Experienced Team. World-Class Science.</h2>
        <div className="team-grid">
          {members.map((m) => (
            <div className="team-card" key={m.name}>
              <div className="team-photo-wrap">
                <img
                  src={m.photo}
                  alt={m.name}
                  className="team-photo"
                  style={m.photoPosition ? { objectPosition: m.photoPosition } : undefined}
                  onError={(e) => {
                    (e.currentTarget as HTMLImageElement).style.display = "none";
                    const fallback = e.currentTarget.nextElementSibling as HTMLElement | null;
                    if (fallback) fallback.style.display = "flex";
                  }}
                />
                <div className="team-avatar team-avatar-fallback" style={{ display: "none" }}>{m.initials}</div>
              </div>
              <div className="team-card-body">
                <h3>{m.name}</h3>
                <p className="team-title">{m.title}</p>
                <p>{m.bio}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Contact() {
  const ref = useRef<HTMLElement>(null);
  useIntersection(ref);
  return (
    <section id="contact" ref={ref}>
      <div className="container">
        <p className="section-label">Get In Touch</p>
        <h2>Partnering &amp; Investment Inquiries</h2>
        <p className="section-intro">ConViCure welcomes conversations with investors, research collaborators, and strategic partners committed to advancing treatments for tick-borne illness.</p>
        <div className="contact-grid">
          <div className="contact-info">
            <div className="contact-item">
              <h3>General Inquiries</h3>
              <p><a href="mailto:info@convicure.com">info@convicure.com</a></p>
            </div>
            <div className="contact-item">
              <h3>Location</h3>
              <p>San Francisco Bay Area, California</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  const scrollTo = (id: string) => {
    const el = document.querySelector(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };
  return (
    <footer>
      <div className="container">
        <div className="footer-inner">
          <div className="footer-brand">
            <span className="nav-logo">
              <span className="logo-con">Con</span><span className="logo-vi">Vi</span><span className="logo-cure">Cure</span>
            </span>
            <p className="footer-tagline">Treatments for persistent tick-borne illness.</p>
          </div>
          <div className="footer-links">
            {[["#approach", "Our Approach"], ["#pipeline", "Pipeline"], ["#science", "Science"], ["#team", "Team"], ["#contact", "Contact"]].map(([href, label]) => (
              <a key={href} href={href} onClick={(e) => { e.preventDefault(); scrollTo(href); }}>{label}</a>
            ))}
          </div>
        </div>
        <div className="footer-legal">
          <p>&copy; 2026 ConViCure, Inc. All rights reserved. ConViCure is a preclinical-stage company. No products have been approved by the FDA. Information on this website is for informational purposes only and does not constitute medical advice.</p>
        </div>
      </div>
    </footer>
  );
}

class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean }> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error: unknown, info: unknown) {
    console.error("[ConViCure] Rendering error:", error, info);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", gap: 16, padding: 40, textAlign: "center" }}>
          <h2 style={{ color: "#0d2d4e" }}>Something went wrong.</h2>
          <p style={{ color: "#555" }}>Please refresh the page. If the issue persists, contact <a href="mailto:info@convicure.com">info@convicure.com</a>.</p>
          <button onClick={() => window.location.reload()} style={{ padding: "10px 24px", background: "#1a7a6e", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontWeight: 600 }}>Refresh Page</button>
        </div>
      );
    }
    return this.props.children;
  }
}

export default function App() {
  useEffect(() => {
    const check = async () => {
      try {
        const res = await fetch("/api/health");
        if (!res.ok) console.warn("[ConViCure] Health check failed:", res.status);
      } catch (err) {
        console.warn("[ConViCure] Health check unreachable:", err);
      }
    };
    check();
    const interval = setInterval(check, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <ErrorBoundary>
      <Navbar />
      <Hero />
      <Problem />
      <Approach />
      <Pipeline />
      <Science />
      <FeaturedVideo />
      <Publications />
      <Press />
      <ResearchStats />
      <Timeline />
      <TBI />
      <LymeResources />
      <Team />
      <InvestorThesis />
      <Contact />
      <Footer />
      <ChatWidget />
    </ErrorBoundary>
  );
}
