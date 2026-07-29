# Product copy, part 2 of 2. Same rules as content_a.py.
#
# The blends are the hardest entries to keep distinct, because Glow, Klow and
# the two Wolverine fills overlap in composition — Glow and Klow were 94%
# identical before this rewrite. Each is written around what its particular
# combination is, and around the fill size, rather than around a shared
# "research blend" paragraph.

CONTENT_B = {

"semax-5mg": dict(
  tagline="Synthetic analog of an ACTH fragment.",
  overview=(
    "Semax is a short synthetic peptide derived from a fragment of "
    "adrenocorticotropic hormone, modified with an added terminal sequence "
    "intended to improve stability over the unmodified fragment. It is studied "
    "in in-vitro neurochemical work and is a frequent subject in analytical "
    "literature, where its small size and defined structure make it a "
    "convenient standard. Supplied as a lyophilized powder in a sealed 5mg vial, "
    "as consistent, high-purity reference material. For research use only — not "
    "for human or veterinary use."
  ),
  analytical=(
    "Short, well-defined sequences produce sharp chromatographic peaks, so the "
    "HPLC purity figure here is straightforward to interpret. Mass spectrometry "
    "confirms the modification is present — for a stabilised fragment, that is "
    "the difference between the analog and the plain fragment it derives from."
  ),
  handling=(
    "Store the sealed vial cold and out of light. Reconstitute with "
    "bacteriostatic water against the vial wall and swirl gently. At 5mg, 1mL "
    "gives 5 mg/mL and 2.5mL gives 2 mg/mL. Refrigerate once in solution."
  ),
  benefits=[
    "Synthetic analog of an ACTH-derived fragment",
    "5mg lyophilized powder, sealed vial",
    "99.1% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Batch Certificate of Analysis on file",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What is Semax derived from?",
     "A fragment of adrenocorticotropic hormone (ACTH), with an added terminal "
     "sequence. The modification is what distinguishes the analog from the "
     "unmodified fragment."),
    ("How is the modification verified?",
     "Mass spectrometry. The observed mass differs between the analog and the "
     "plain fragment, so identity testing distinguishes them where a purity "
     "figure would not."),
    ("What purity did this batch assay at?",
     "99.1% by HPLC. Your Certificate of Analysis references the specific "
     "production lot your vial came from."),
  ],
),

"selank-10mg": dict(
  tagline="Synthetic analog of the immunopeptide tuftsin.",
  overview=(
    "Selank is a short synthetic peptide based on tuftsin, a naturally occurring "
    "tetrapeptide fragment of an immunoglobulin heavy chain, extended with an "
    "additional sequence for stability. It is studied in in-vitro neurochemical "
    "and immunological research, and its structural relationship to a native "
    "immune fragment is the usual reason it appears in comparison work. Supplied "
    "as a lyophilized powder in a sealed 10mg vial. For research use only — not "
    "for human or veterinary use."
  ),
  analytical=(
    "HPLC establishes purity as a percentage of total peak area; mass "
    "spectrometry confirms the sequence, including the stabilising extension "
    "that distinguishes Selank from tuftsin itself. Both are run by an "
    "independent laboratory on each production lot."
  ),
  handling=(
    "Sealed, cold and out of light before use. Reconstitute down the vial wall "
    "with bacteriostatic water and swirl to clear. At 10mg, 2mL gives 5 mg/mL "
    "and 1mL gives 10 mg/mL. Keep refrigerated in solution."
  ),
  benefits=[
    "Synthetic analog of tuftsin",
    "10mg lyophilized powder, sealed vial",
    "99.0% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Batch Certificate of Analysis on file",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What is tuftsin?",
     "A naturally occurring tetrapeptide derived from an immunoglobulin heavy "
     "chain. Selank is a synthetic analog of it with an added stabilising "
     "sequence."),
    ("How does Selank differ from tuftsin?",
     "By the additional terminal residues. That difference shows up in the mass "
     "spectrum, which is how identity is confirmed on each lot."),
    ("Is a Certificate of Analysis included?",
     "Yes. Every batch is independently tested and the COA for your lot ships "
     "with the order."),
  ],
),

"kisspeptin10-5mg": dict(
  tagline="Ten-residue KISS1R ligand fragment.",
  overview=(
    "Kisspeptin-10 is the ten-amino-acid C-terminal fragment of kisspeptin, the "
    "peptide product of the KISS1 gene, and retains the region responsible for "
    "binding at the KISS1 receptor. Working with the decapeptide rather than the "
    "full-length peptide is standard in receptor studies: it is easier to "
    "synthesise reproducibly and isolates the binding region from the rest of "
    "the parent sequence. Supplied as a lyophilized powder in a sealed 5mg vial. "
    "For research use only — not for human or veterinary use."
  ),
  analytical=(
    "Fragment identity is the critical test here — several kisspeptin fragments "
    "of different lengths are in circulation, and they are not "
    "interchangeable. Mass spectrometry confirms this is the ten-residue form; "
    "HPLC reports the purity of that form on the lot you receive."
  ),
  handling=(
    "Store sealed, cold and dark. Reconstitute with bacteriostatic water run "
    "down the wall of the vial. At 5mg, 1mL gives 5 mg/mL and 2.5mL gives "
    "2 mg/mL. Refrigerate in solution and avoid repeated freeze-thaw cycles."
  ),
  benefits=[
    "Ten-residue C-terminal fragment of kisspeptin",
    "Retains the KISS1R binding region",
    "5mg lyophilized powder, sealed vial",
    "99.0% verified purity by HPLC",
    "Fragment length confirmed by mass spectrometry",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("Why the '-10' in the name?",
     "It specifies chain length. Kisspeptin-10 is the ten-amino-acid C-terminal "
     "fragment; other fragment lengths exist and are distinct compounds."),
    ("Does the fragment bind the same receptor as the full peptide?",
     "The ten-residue fragment retains the C-terminal region responsible for "
     "binding at the KISS1 receptor, which is why it is the form normally used "
     "in receptor work."),
    ("How do I know I received the ten-residue form?",
     "Mass spectrometry on the production lot confirms it, and the result is on "
     "the batch Certificate of Analysis."),
  ],
),

"nad-500mg": dict(
  tagline="Nicotinamide adenine dinucleotide — cofactor, not a peptide.",
  overview=(
    "NAD+ is a coenzyme present in every living cell, central to redox reactions "
    "and a substrate for several enzyme families. It is the one item in this "
    "part of the catalog that is not a peptide, and it behaves differently for "
    "it — different solubility, different stability profile, different "
    "analytical method. It is supplied at 500mg, by far the largest fill here, "
    "because cofactor work consumes material at a completely different scale "
    "from receptor studies. For research use only — not for human or veterinary "
    "use."
  ),
  analytical=(
    "A small molecule, not a peptide, so the analytical approach differs from "
    "the rest of the catalog: purity is still established chromatographically "
    "and identity by mass, but the methods are those appropriate to a "
    "nucleotide cofactor rather than to a synthesised peptide sequence."
  ),
  handling=(
    "Store the sealed vial cold and out of light. NAD+ is hygroscopic — keep it "
    "sealed until use and don't leave it open to room air. At 500mg, 5mL of "
    "diluent gives 100 mg/mL and 10mL gives 50 mg/mL. Prepare fresh where your "
    "protocol allows; this one is less forgiving in solution than the peptides."
  ),
  benefits=[
    "Coenzyme (nucleotide cofactor), not a peptide",
    "500mg — the largest fill in the catalog",
    "99.1% verified purity",
    "Identity confirmed by mass spectrometry",
    "Batch Certificate of Analysis on file",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("Is NAD+ a peptide?",
     "No. It is a nucleotide cofactor — a small molecule rather than an amino "
     "acid sequence. That affects how it dissolves, how it stores and which "
     "analytical methods apply."),
    ("Why is the vial so much larger than the others?",
     "Cofactor work consumes material at a different scale from receptor "
     "studies. A 10mg fill would be impractical for most protocols that call "
     "for it."),
    ("What does hygroscopic mean in practice?",
     "It draws moisture from the air. Keep the vial sealed until you are ready "
     "to reconstitute, and don't leave it standing open."),
  ],
),

"ss31-10mg": dict(
  tagline="Mitochondria-targeting tetrapeptide with affinity for cardiolipin.",
  overview=(
    "SS-31 is a synthetic tetrapeptide studied for its affinity for cardiolipin, "
    "a phospholipid found almost exclusively in the inner mitochondrial "
    "membrane. That localisation is the compound's defining research property: "
    "it is one of the small number of peptides characterised as concentrating at "
    "a specific subcellular membrane rather than acting at a cell-surface "
    "receptor, which makes it a reference point in mitochondrial and "
    "membrane-interaction studies. Supplied as a lyophilized powder in a sealed "
    "10mg vial. For research use only — not for human or veterinary use."
  ),
  analytical=(
    "Four residues, with an alternating structural motif that is easy to "
    "confirm by mass and well behaved on a column. HPLC supplies the purity "
    "figure and mass spectrometry the identity confirmation, both from an "
    "independent laboratory on every lot."
  ),
  handling=(
    "Sealed, cold and out of light. Reconstitute against the vial wall with "
    "bacteriostatic water. At 10mg, 2mL gives 5 mg/mL and 1mL gives 10 mg/mL. "
    "Refrigerate once in solution. If your work involves membrane preparations, "
    "prepare the peptide solution fresh."
  ),
  benefits=[
    "Synthetic tetrapeptide (4 amino acids)",
    "Studied for affinity to cardiolipin",
    "10mg lyophilized powder, sealed vial",
    "99.2% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What is cardiolipin?",
     "A phospholipid found almost exclusively in the inner mitochondrial "
     "membrane. SS-31's affinity for it is why the compound is studied in "
     "mitochondrial research rather than in receptor work."),
    ("How is this different from a receptor-binding peptide?",
     "Most peptides in this catalog are characterised by what cell-surface "
     "receptor they bind. SS-31 is characterised by where it localises — a "
     "specific intracellular membrane — which is a different kind of property "
     "and needs different assays."),
    ("What is the purity on this lot?",
     "99.2% by HPLC, with identity confirmed by mass spectrometry and the "
     "certificate on file for your batch."),
  ],
),

"pt141-5mg": dict(
  tagline="Melanocortin receptor ligand, cyclic heptapeptide.",
  overview=(
    "PT-141 is a synthetic cyclic peptide studied at the melanocortin receptor "
    "family, with characterised activity at the MC3 and MC4 subtypes. Its cyclic "
    "structure is the notable feature analytically — cyclisation changes both "
    "stability and chromatographic behaviour relative to a linear sequence of "
    "the same composition, and it is the reason this compound is often used as a "
    "reference in method development for constrained peptides. Supplied as a "
    "lyophilized powder in a sealed vial. For research use only — not for human "
    "or veterinary use."
  ),
  analytical=(
    "Cyclic peptides can co-elute with their linear counterparts under a poorly "
    "chosen method, which makes identity confirmation more than a formality "
    "here. Mass spectrometry distinguishes the cyclised form; HPLC supplies the "
    "purity figure for it. Independent, per lot."
  ),
  handling=(
    "Store the sealed vial cold and out of light. Reconstitute with "
    "bacteriostatic water down the vial wall and swirl to dissolve. Work your "
    "target concentration and aliquot volume through the reconstitution "
    "calculator against the vial's labelled mass. Refrigerate in solution."
  ),
  benefits=[
    "Synthetic cyclic peptide",
    "Studied at MC3 and MC4 melanocortin receptor subtypes",
    "Lyophilized powder, sealed vial",
    "99.0% verified purity by HPLC",
    "Cyclised form confirmed by mass spectrometry",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What does cyclic mean for a peptide?",
     "The chain is closed into a ring rather than left as a linear sequence. "
     "That changes stability and how the molecule behaves on an analytical "
     "column, which is why identity testing matters on this one."),
    ("Which receptors is it studied at?",
     "The melanocortin family, with characterised activity at the MC3 and MC4 "
     "subtypes."),
    ("Is the linear form distinguishable from the cyclic form?",
     "By mass spectrometry, yes. Under some chromatographic methods the two can "
     "co-elute, which is precisely why we don't rely on HPLC alone."),
  ],
),

"glow-70mg": dict(
  tagline="Three-compound blend: GHK-Cu, BP+ and TB-500 in one 70mg vial.",
  overview=(
    "Glow Blend combines three compounds from this catalog in a single "
    "lyophilized vial: GHK-Cu, the copper-complexed tripeptide; BP+, the "
    "fifteen-residue synthetic peptide; and TB-500, the thymosin beta-4 "
    "fragment. Blends exist to remove a reconstitution step for protocols that "
    "would otherwise prepare three vials separately — the trade-off being that "
    "the ratio is fixed at manufacture and cannot be varied. Each component is "
    "drawn from the same lots supplied individually, with the same testing. For "
    "research use only — not for human or veterinary use."
  ),
  analytical=(
    "A blend is analytically harder than a single compound: the method has to "
    "resolve three peptides in one sample, including a metal-complexed one that "
    "does not behave like the other two. HPLC and mass spectrometry are run on "
    "the blended lot rather than inferred from the component certificates."
  ),
  handling=(
    "Sealed, cold and out of light — the GHK-Cu component makes this blend "
    "light-sensitive, so treat the whole vial accordingly. Reconstitute against "
    "the vial wall. At 70mg total, 3.5mL gives 20 mg/mL of combined peptide. "
    "Note that this is total mass across three compounds, not 70mg of any one of "
    "them. Refrigerate and keep dark in solution."
  ),
  benefits=[
    "Three compounds in one vial: GHK-Cu, BP+, TB-500",
    "70mg total peptide mass, lyophilized",
    "99.2% verified purity by HPLC",
    "Tested as a blend, not inferred from components",
    "Fixed ratio — set at manufacture",
    "Light-sensitive: contains the copper complex",
  ],
  faqs=[
    ("What is the difference between Glow and Klow?",
     "Klow adds a fourth compound, KPV, to the same three and is filled at 80mg "
     "rather than 70mg. If you don't need the KPV component, Glow is the "
     "narrower blend."),
    ("Does 70mg mean 70mg of each compound?",
     "No — 70mg is the total peptide mass in the vial, divided across the three "
     "components. That matters when you calculate concentration, so use total "
     "mass unless you're working to a component figure from the certificate."),
    ("Is the blend tested, or just its ingredients?",
     "The blended lot is tested. Component certificates wouldn't tell you "
     "whether the blend was combined correctly."),
  ],
),

"klow-80mg": dict(
  tagline="Four-compound blend: KPV, GHK-Cu, BP+ and TB-500 in one 80mg vial.",
  overview=(
    "Klow Blend is the four-component formulation: it takes the same GHK-Cu, BP+ "
    "and TB-500 combination as Glow Blend and adds KPV, the alpha-MSH C-terminal "
    "tripeptide, at a total fill of 80mg. It is the broadest blend in the "
    "catalog and the one to take when a protocol calls for the tripeptide "
    "fragment alongside the other three. As with all blends the ratio is fixed "
    "at manufacture, which is the cost of not preparing four vials separately. "
    "For research use only — not for human or veterinary use."
  ),
  analytical=(
    "Four peptides in one sample, one of them metal-complexed and one only three "
    "residues long — a wide spread of chromatographic behaviour to resolve in a "
    "single method. HPLC and mass spectrometry are run on the blended lot, not "
    "carried over from the component certificates."
  ),
  handling=(
    "Store sealed, cold and dark; the GHK-Cu component makes the vial "
    "light-sensitive. Reconstitute down the vial wall and swirl. At 80mg total, "
    "4mL gives 20 mg/mL of combined peptide — again, total across four "
    "compounds rather than 80mg of any single one. Refrigerate in solution."
  ),
  benefits=[
    "Four compounds in one vial: KPV, GHK-Cu, BP+, TB-500",
    "80mg total peptide mass, lyophilized",
    "The broadest blend in the catalog",
    "99.2% verified purity by HPLC",
    "Tested as a blend, not inferred from components",
    "Light-sensitive: contains the copper complex",
  ],
  faqs=[
    ("Should I take Klow or Glow?",
     "Klow if your protocol wants KPV alongside the other three; Glow if it "
     "doesn't. The three shared components are the same material either way."),
    ("What does the KPV component add?",
     "KPV is a tripeptide corresponding to the C-terminal end of the alpha-MSH "
     "sequence. It is the only component of Klow not also present in Glow."),
    ("Is 80mg the mass of each compound?",
     "No — it is the total peptide mass across all four, which is the figure to "
     "use when calculating concentration from the vial."),
  ],
),

"wolverine-10mg": dict(
  tagline="Two-compound blend: BP+ and TB-500, 10mg fill.",
  overview=(
    "Wolverine Stack pairs two compounds from this catalog in a single vial: "
    "BP+, the fifteen-residue synthetic peptide, and TB-500, the thymosin "
    "beta-4 fragment. It is the simplest blend here — two components rather than "
    "three or four — which makes it the easiest to reason about analytically and "
    "the one most often used where a protocol wants the pair without the copper "
    "complex that the Glow and Klow blends carry. This is the 10mg fill. For "
    "research use only — not for human or veterinary use."
  ),
  analytical=(
    "Two peptides of similar character in one sample, and no metal complex to "
    "complicate the method — which makes this the most straightforward blend in "
    "the catalog to resolve chromatographically. HPLC and mass spectrometry are "
    "run on the blended lot."
  ),
  handling=(
    "Sealed, cold and out of light. With no copper component this blend is less "
    "light-sensitive than Glow or Klow, but the same handling costs nothing. "
    "Reconstitute down the vial wall. At 10mg total, 1mL gives 10 mg/mL of "
    "combined peptide. Refrigerate in solution."
  ),
  benefits=[
    "Two compounds in one vial: BP+ and TB-500",
    "10mg total peptide mass, lyophilized",
    "No copper complex — simpler handling than Glow or Klow",
    "99.1% verified purity by HPLC",
    "Tested as a blend, not inferred from components",
    "Also available as a 20mg fill",
  ],
  faqs=[
    ("What is the difference between the 10mg and 20mg vials?",
     "Fill quantity only — same two compounds, same ratio, same testing. The "
     "20mg vial suits protocols that will consume it before it degrades in "
     "solution."),
    ("How does this differ from Glow Blend?",
     "Glow adds GHK-Cu to the same two compounds. Wolverine is the pair on its "
     "own, which also means it isn't light-sensitive in the way the "
     "copper-containing blends are."),
    ("Is 10mg the mass of each peptide?",
     "No — it is the combined mass of both. Use the total when calculating "
     "concentration."),
  ],
),

"wolverine-20mg": dict(
  tagline="Two-compound blend: BP+ and TB-500, 20mg fill.",
  overview=(
    "The 20mg fill of Wolverine Stack — the same BP+ and TB-500 pairing as the "
    "10mg vial, at double the total peptide mass. The larger fill is the better "
    "value per milligram, and suits protocols that will work through it while "
    "the material is still in good condition; lyophilized peptide keeps far "
    "better than reconstituted peptide, so the right fill size is the one your "
    "work actually consumes. No copper complex, which keeps handling simpler "
    "than the Glow and Klow blends. For research use only — not for human or "
    "veterinary use."
  ),
  analytical=(
    "Same two-peptide method as the 10mg fill, run independently on this lot — "
    "a larger fill does not inherit the smaller one's certificate. HPLC for "
    "purity, mass spectrometry for identity of both components."
  ),
  handling=(
    "Store sealed, cold and out of light. Reconstitute against the vial wall and "
    "swirl. At 20mg total, 2mL gives 10 mg/mL and 1mL gives 20 mg/mL of combined "
    "peptide. Refrigerate in solution — and with the larger fill, plan draw "
    "volumes so the vial is consumed rather than stored half-used."
  ),
  benefits=[
    "Two compounds in one vial: BP+ and TB-500",
    "20mg total peptide mass — the larger fill",
    "Better value per milligram than the 10mg vial",
    "99.1% verified purity by HPLC",
    "No copper complex — simpler handling than Glow or Klow",
    "Tested as a blend, not inferred from components",
  ],
  faqs=[
    ("Should I take the 10mg or 20mg vial?",
     "Take the fill your protocol will consume. Lyophilized material keeps far "
     "better than material sitting reconstituted in a fridge, so the larger vial "
     "is only better value if it gets used."),
    ("Is the ratio the same as the 10mg vial?",
     "Yes — same two compounds in the same proportion, just twice the total "
     "mass."),
    ("Does this lot share a certificate with the 10mg fill?",
     "No. Each production lot is tested independently and carries its own "
     "Certificate of Analysis."),
  ],
),

"cjc1295-ipa-5-5": dict(
  tagline="Two-peptide fusion vial: CJC-1295 and Ipamorelin, 5mg each.",
  overview=(
    "This vial contains two distinct peptides at 5mg each: CJC-1295, a modified "
    "GHRH analog, and Ipamorelin, a selective growth-hormone secretagogue "
    "peptide. They are studied together because they act at different targets — "
    "one at the GHRH receptor, the other as a ghrelin-receptor agonist — which "
    "makes the pair a standard subject in work separating the contributions of "
    "two distinct signalling routes. Unlike the blends, this is a stated 5mg of "
    "each rather than a fixed proportion of a combined mass. For research use "
    "only — not for human or veterinary use."
  ),
  analytical=(
    "Two peptides at a known 1:1 fill, which makes the chromatography easier to "
    "read than a proportional blend — both components should resolve as "
    "comparable peaks. HPLC gives purity and mass spectrometry confirms both "
    "identities, on the combined lot."
  ),
  handling=(
    "Sealed, cold and out of light. Reconstitute down the vial wall and swirl "
    "until clear. With 5mg of each compound (10mg total), 2mL of diluent gives "
    "2.5 mg/mL of each and 5 mg/mL combined — be explicit in your notes about "
    "which of those two figures you are working to. Refrigerate in solution."
  ),
  benefits=[
    "Two peptides, 5mg each: CJC-1295 and Ipamorelin",
    "Stated per-compound fill, not a proportional blend",
    "Distinct targets: GHRH receptor and ghrelin receptor",
    "99.2% verified purity by HPLC",
    "Both identities confirmed by mass spectrometry",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("How is this different from the blends?",
     "The fill is stated per compound — 5mg of each — rather than as a total "
     "mass split in a fixed ratio. That makes concentration calculations "
     "unambiguous for either component."),
    ("Why are these two studied together?",
     "They act at different targets: CJC-1295 at the GHRH receptor and "
     "Ipamorelin as a ghrelin-receptor agonist. Pairing them is how research "
     "separates the two signalling routes."),
    ("What concentration does 2mL give?",
     "2.5 mg/mL of each compound, or 5 mg/mL of combined peptide. Record which "
     "convention you are using — it is the most common source of confusion with "
     "a two-compound vial."),
  ],
),

"solvent-3ml": dict(
  tagline="Bacteriostatic water, 3ml — laboratory diluent.",
  overview=(
    "Bacteriostatic water is sterile water containing a small proportion of "
    "benzyl alcohol as a bacteriostatic agent, which is what makes it suitable "
    "for multiple withdrawals from the same vial rather than single use. It is "
    "the standard diluent for reconstituting lyophilized peptides in laboratory "
    "work. This is the 3ml vial — the right size for reconstituting one or two "
    "small-fill compounds without leaving diluent standing unused. Supplied as a "
    "laboratory consumable. For research use only — not for human or veterinary "
    "use."
  ),
  analytical=(
    "This is a supply item, not a synthesised compound, so it carries batch "
    "documentation rather than an HPLC purity assay — the relevant records are "
    "sterility and fill, not peak area. Every lot is documented and the "
    "paperwork is available on request."
  ),
  handling=(
    "Store at room temperature, out of direct light, with the stopper intact. "
    "Swab the stopper before each withdrawal — the bacteriostatic agent is what "
    "permits multiple draws, but it does not compensate for a contaminated "
    "septum. A 3ml vial will reconstitute, for example, three 10mg vials at "
    "1mL each."
  ),
  benefits=[
    "Sterile water with benzyl alcohol as bacteriostatic agent",
    "3ml vial — sized for one or two small reconstitutions",
    "Supports multiple withdrawals from the same vial",
    "Batch documented",
    "Also available as a 10ml vial",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What makes it bacteriostatic?",
     "A small proportion of benzyl alcohol, which inhibits bacterial growth. "
     "That is what allows a vial to be drawn from more than once."),
    ("Should I take the 3ml or 10ml?",
     "The 3ml suits one or two reconstitutions. If you are preparing several "
     "vials at once, the 10ml wastes less."),
    ("Why is there no purity percentage on this item?",
     "It is a laboratory supply rather than a synthesised compound. The relevant "
     "records are sterility and fill documentation, not an HPLC assay."),
  ],
),

"solvent-10ml": dict(
  tagline="Bacteriostatic water, 10ml — laboratory diluent.",
  overview=(
    "The 10ml fill of bacteriostatic water: sterile water with benzyl alcohol as "
    "a bacteriostatic agent, permitting repeated withdrawals from a single vial. "
    "This is the size to take when reconstituting several compounds in a "
    "session, or when working with the larger fills in this catalog — a single "
    "500mg NAD+ vial can take 10ml on its own at 50 mg/mL. Supplied as a "
    "laboratory consumable. For research use only — not for human or veterinary "
    "use."
  ),
  analytical=(
    "A supply item rather than a synthesised compound, so it carries batch "
    "documentation rather than a chromatographic purity figure. Sterility and "
    "fill records are the relevant paperwork and are available on request."
  ),
  handling=(
    "Room temperature, out of direct light, stopper intact. Swab before every "
    "withdrawal; the bacteriostatic agent slows growth, it does not sterilise a "
    "contaminated septum. At 10ml this vial will carry a full session of "
    "reconstitutions — plan draws so it is used within a sensible window rather "
    "than kept half-full indefinitely."
  ),
  benefits=[
    "Sterile water with benzyl alcohol as bacteriostatic agent",
    "10ml vial — the volume fill",
    "Supports multiple withdrawals from the same vial",
    "Suits larger reconstitutions such as the 500mg NAD+ fill",
    "Batch documented",
    "Also available as a 3ml vial",
  ],
  faqs=[
    ("How many vials will 10ml reconstitute?",
     "It depends on your target concentrations. As a reference point, ten 10mg "
     "vials at 1mL each, or a single 500mg NAD+ vial at 50 mg/mL."),
    ("Can it be drawn from repeatedly?",
     "Yes — that is what the bacteriostatic agent is for. Swab the stopper "
     "before each withdrawal regardless."),
    ("Is it the same water as the 3ml vial?",
     "Yes, same specification. Only the fill volume differs."),
  ],
),

}
