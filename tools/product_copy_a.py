# Product copy, part 1 of 2.
#
# Rules this copy is written under:
#   • Every claim is a SUPPLY claim — what the material is, what class of
#     molecule, what the assay measured, how to store and reconstitute it.
#     Nothing about what a compound does to a person. That's the line the
#     business runs on and the line that keeps the ad account approvable.
#   • Compounds are named by their catalog display name. Three of them ship
#     under house codes on purpose; whether the chemical names go on-site is a
#     decision the owner hasn't made yet, so this copy doesn't make it for them.
#   • No invented numbers. No molecular weights, CAS numbers, sequences or
#     stability half-lives — a wrong figure on a page selling reference material
#     is worse than no figure. Reconstitution examples are plain arithmetic from
#     the vial mass, which is checkable.
#   • Every entry is written from scratch rather than templated. The whole point
#     is that these pages stop being 94–99% identical to each other.

CONTENT_A = {

"reta-10mg": dict(
  tagline="Triple incretin receptor agonist, supplied as lyophilized reference material.",
  overview=(
    "GL-3RT is a synthetic peptide studied as an agonist at three incretin and "
    "glucagon-family receptors at once — GLP-1, GIP and the glucagon receptor. "
    "That triple profile is what distinguishes it in the literature from single- "
    "and dual-agonist compounds, and it is the reason receptor-selectivity and "
    "binding-affinity work on this class is run across all three targets rather "
    "than one. Supplied here as a lyophilized powder in a sealed 10mg vial, as "
    "consistent reference material for in-vitro receptor and analytical studies. "
    "For research use only — not for human or veterinary use."
  ),
  analytical=(
    "HPLC establishes the purity figure on the certificate: the proportion of "
    "total peak area attributable to the target peptide. Mass spectrometry is "
    "the separate question of identity — confirming the observed mass matches "
    "the intended sequence, so a pure sample of the wrong compound can't pass "
    "as a clean result. Both run on every lot."
  ),
  handling=(
    "Keep the sealed vial cold and out of light until use. Reconstitute with "
    "bacteriostatic water down the vial wall rather than directly onto the "
    "powder cake, and swirl rather than shake. At 10mg, 2mL of diluent gives "
    "5 mg/mL and 1mL gives 10 mg/mL — run your own figures through the "
    "reconstitution calculator. Refrigerate once in solution."
  ),
  benefits=[
    "Triple-agonist profile: GLP-1, GIP and glucagon receptors",
    "10mg lyophilized powder, sealed vial",
    "99.4% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Batch Certificate of Analysis on file",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What makes a triple agonist different from a dual agonist?",
     "The number of receptor targets it acts on. Dual agonists engage two of the "
     "incretin-family receptors; GL-3RT is characterised across three — GLP-1, "
     "GIP and glucagon. In research terms that means selectivity work has to be "
     "run against all three rather than assumed from one."),
    ("What purity figure does this lot carry?",
     "99.4% by HPLC, with identity confirmed by mass spectrometry. The Certificate "
     "of Analysis for the batch you receive is available on request and ships with "
     "the order."),
    ("How should it be stored before reconstitution?",
     "Sealed, cold and out of light. Lyophilized peptide is far more stable dry "
     "than in solution, so leave it in powder form until the day you need it."),
  ],
),

"tirz-10mg": dict(
  tagline="Dual GIP and GLP-1 receptor agonist, lyophilized.",
  overview=(
    "NV-2TZ is a synthetic peptide characterised in the literature as a dual "
    "agonist — engaging both the GIP and GLP-1 receptors from a single sequence. "
    "It sits between the single-receptor agonists and the triple-agonist "
    "compounds, and comparative receptor work in this class usually uses all "
    "three tiers to separate what each additional target contributes. Supplied "
    "as a lyophilized powder in a sealed 10mg vial, as consistent reference "
    "material for in-vitro binding and analytical studies. For research use only "
    "— not for human or veterinary use."
  ),
  analytical=(
    "Two tests answering two different questions. HPLC reports how much of the "
    "sample is the target peptide, expressed as percent of total peak area. Mass "
    "spectrometry confirms the molecule is the one intended by matching observed "
    "mass against the expected sequence. A certificate carrying only one of them "
    "leaves the other question open."
  ),
  handling=(
    "Store the sealed vial cold and dark. Reconstitute slowly with bacteriostatic "
    "water aimed at the vial wall — a stream directed onto the cake can shear "
    "peptide. At 10mg, 2mL of diluent yields 5 mg/mL. Once in solution, keep it "
    "refrigerated and stop agitating it; peptides degrade faster wet than dry."
  ),
  benefits=[
    "Dual-agonist profile: GIP and GLP-1 receptors",
    "10mg lyophilized powder, sealed vial",
    "99.3% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Batch Certificate of Analysis on file",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("How does this differ from a single-receptor agonist?",
     "It engages two receptors — GIP and GLP-1 — from one sequence, where a "
     "single agonist engages one. That difference is exactly what comparative "
     "receptor-binding studies in this class are designed to characterise."),
    ("Is the Certificate of Analysis specific to my vial's batch?",
     "Yes. The COA references the production lot the vial came from, not a "
     "generic sample tested once. Every batch is analysed independently."),
    ("What diluent should be used?",
     "Bacteriostatic water is the standard choice for multi-draw work. We stock "
     "it in 3ml and 10ml vials as a laboratory supply."),
  ],
),

"cagri-10mg": dict(
  tagline="Long-acting amylin analog, supplied lyophilized.",
  overview=(
    "Cagrilintide is a synthetic analog of amylin, the pancreatic peptide "
    "co-secreted with insulin, studied at the amylin and calcitonin receptor "
    "family. Its research interest lies in a modified structure intended to "
    "extend stability relative to native amylin, which makes it a common "
    "reference point in work comparing analog design against the endogenous "
    "sequence. Supplied as a lyophilized powder in a sealed 10mg vial, as "
    "consistent, high-purity material for in-vitro receptor and analytical "
    "studies. For research use only — not for human or veterinary use."
  ),
  analytical=(
    "Purity by HPLC and identity by mass spectrometry, on every lot. Amylin "
    "analogs are prone to aggregation, which makes the chromatographic profile "
    "worth reading in full rather than glancing at the headline percentage — the "
    "shape of the trace around the main peak tells you as much as the number."
  ),
  handling=(
    "Sealed, cold and out of light before use. Reconstitute gently down the vial "
    "wall; this class is sensitive to mechanical agitation, so swirl and never "
    "shake. At 10mg, 2mL gives 5 mg/mL. Refrigerate in solution and inspect for "
    "cloudiness before each draw."
  ),
  benefits=[
    "Synthetic amylin analog",
    "10mg lyophilized powder, sealed vial",
    "99.2% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Batch Certificate of Analysis on file",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What is amylin?",
     "A pancreatic peptide hormone co-secreted with insulin. Cagrilintide is a "
     "synthetic analog of it, studied at the amylin and calcitonin receptor "
     "family in laboratory research."),
    ("Why does aggregation matter for this compound?",
     "Peptides in this family can self-associate in solution, which shows up in "
     "the chromatogram as shoulders or extra peaks. It's a reason to read the "
     "full HPLC trace on the COA rather than only the purity figure."),
    ("How is purity verified?",
     "Independent third-party HPLC for purity and mass spectrometry for identity, "
     "run on each production lot."),
  ],
),

"tesa-10mg": dict(
  tagline="GHRH analog studied at the growth-hormone-releasing hormone receptor.",
  overview=(
    "Tesamorelin is a synthetic analog of growth-hormone-releasing hormone, "
    "studied for its interaction with the GHRH receptor. Structurally it is a "
    "stabilised version of the native 44-amino-acid releasing factor, and that "
    "modification is the usual subject of comparison work against the "
    "endogenous sequence. It appears frequently as a reference compound in "
    "receptor-binding and analytical method development. Supplied as a "
    "lyophilized powder in a sealed 10mg vial, as consistent, high-purity "
    "material for in-vitro laboratory studies. For research use only — not for "
    "human or veterinary use."
  ),
  analytical=(
    "This lot assayed at 99.5% by HPLC — the highest figure in the current "
    "catalog — with identity confirmed by mass spectrometry. HPLC answers how "
    "much of the sample is the target compound; mass spec answers whether the "
    "target compound is what the label says. Both appear on the batch "
    "certificate."
  ),
  handling=(
    "Keep sealed, cold and out of light. Reconstitute with bacteriostatic water "
    "run down the inside of the vial, swirling until the cake clears rather than "
    "shaking. At 10mg, 2mL of diluent gives 5 mg/mL and 5mL gives 2 mg/mL. Once "
    "reconstituted, refrigerate and protect from light."
  ),
  benefits=[
    "Synthetic GHRH analog",
    "10mg lyophilized powder, sealed vial",
    "99.5% verified purity — highest in the catalog",
    "Identity confirmed by mass spectrometry",
    "Batch Certificate of Analysis on file",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What receptor is Tesamorelin studied at?",
     "The growth-hormone-releasing hormone (GHRH) receptor. It is a synthetic "
     "analog of the native releasing factor, used as reference material in "
     "in-vitro receptor work."),
    ("Why is this lot's purity higher than most?",
     "Purity is a property of the production lot, not the compound. This batch "
     "assayed at 99.5% by HPLC. Every lot is tested independently and the figure "
     "on your certificate is the figure for your vial."),
    ("What concentration will 2mL give me?",
     "5 mg/mL from a 10mg vial. The reconstitution calculator will work out any "
     "other target concentration and the aliquot volume for a given mass."),
  ],
),

"motsc-10mg": dict(
  tagline="Mitochondrial-derived peptide encoded in mitochondrial DNA.",
  overview=(
    "MOTS-C belongs to an unusual class: peptides encoded not in the nuclear "
    "genome but within mitochondrial DNA itself. That origin is most of why it "
    "draws research attention — it sits at the interface between mitochondrial "
    "and nuclear signalling, and is studied in work on metabolic regulation at "
    "the cellular level. As a short peptide it is also a convenient subject for "
    "analytical method development. Supplied as a lyophilized powder in a sealed "
    "10mg vial, as consistent reference material for in-vitro laboratory "
    "studies. For research use only — not for human or veterinary use."
  ),
  analytical=(
    "Short peptides give clean chromatography, which makes the HPLC purity "
    "figure straightforward to read on this one. Mass spectrometry confirms "
    "identity against the expected sequence. Both are run per lot by an "
    "independent laboratory and reported on the batch certificate."
  ),
  handling=(
    "Store the sealed vial cold and dark. Reconstitute with bacteriostatic water "
    "against the vial wall and swirl to dissolve. At 10mg, 1mL gives 10 mg/mL "
    "and 2mL gives 5 mg/mL. Keep refrigerated once in solution and avoid "
    "repeated warming and cooling."
  ),
  benefits=[
    "Mitochondrial-derived peptide (encoded in mtDNA)",
    "10mg lyophilized powder, sealed vial",
    "99.1% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Batch Certificate of Analysis on file",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What does 'mitochondrial-derived' mean?",
     "The peptide is encoded within mitochondrial DNA rather than the nuclear "
     "genome. Only a small number of peptides are known to originate this way, "
     "which is a large part of the research interest in this class."),
    ("Is it third-party tested?",
     "Yes — independent HPLC for purity and mass spectrometry for identity, on "
     "every production lot, with the certificate on file."),
    ("How long does reconstituted material last?",
     "That depends on your diluent, storage temperature and protocol, so we "
     "don't publish a figure we haven't measured under your conditions. Peptides "
     "are markedly more stable lyophilized than in solution — reconstitute what "
     "you need, when you need it."),
  ],
),

"igf1lr3-1mg": dict(
  tagline="Long-arginine IGF-1 analog, supplied in a 1mg vial.",
  overview=(
    "IGF-1 LR3 is a modified analog of insulin-like growth factor 1, carrying an "
    "extended N-terminal sequence and a substitution that reduces its affinity "
    "for IGF-binding proteins relative to native IGF-1. That reduced binding is "
    "the whole point of the analog in research terms, and it is what makes it a "
    "standard comparator in work on IGF signalling and binding-protein "
    "interactions. Supplied as a lyophilized powder in a sealed 1mg vial — a "
    "smaller unit than the rest of the catalog, matching how it is typically "
    "used. For research use only — not for human or veterinary use."
  ),
  analytical=(
    "A 1mg fill leaves less material for destructive testing, so the analytical "
    "pass matters more, not less. HPLC gives the purity figure and mass "
    "spectrometry confirms identity against the expected modified sequence — "
    "which for an analog is the test that distinguishes it from the native "
    "protein."
  ),
  handling=(
    "Sealed, cold and out of light. This is a 1mg vial, so diluent volumes are "
    "correspondingly small: 1mL gives 1 mg/mL, 2mL gives 0.5 mg/mL. Add the "
    "diluent slowly against the wall and swirl. Small fills are easy to lose to "
    "over-dilution — work the numbers through the calculator before you draw."
  ),
  benefits=[
    "Modified IGF-1 analog with reduced binding-protein affinity",
    "1mg lyophilized powder, sealed vial",
    "99.0% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Batch Certificate of Analysis on file",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What does LR3 refer to?",
     "The structural modifications that distinguish this analog from native "
     "IGF-1 — an extended N-terminal sequence and an amino acid substitution "
     "that together reduce affinity for IGF-binding proteins."),
    ("Why is this a 1mg vial when most of the catalog is 5 or 10mg?",
     "It matches how the compound is typically used in laboratory work. Filling "
     "it larger would mean most of the vial degrading in solution before it was "
     "consumed."),
    ("What concentration does 1mL give?",
     "1 mg/mL from a 1mg vial. Use the reconstitution calculator for any other "
     "target — small fills are the easiest ones to get wrong."),
  ],
),

"bpc157-5mg": dict(
  tagline="Pentadecapeptide sequence, supplied lyophilized.",
  overview=(
    "BP+ is a synthetic pentadecapeptide — a fifteen-amino-acid sequence "
    "originally identified from a fragment of a protein found in gastric juice. "
    "It is one of the more widely cited short peptides in in-vitro tissue and "
    "cell-culture literature, which also makes it a common subject for "
    "analytical method development and a frequent component of multi-peptide "
    "research blends. Supplied as a lyophilized powder in a sealed 5mg vial, as "
    "consistent, high-purity reference material. For research use only — not for "
    "human or veterinary use."
  ),
  analytical=(
    "Fifteen residues is short enough to give a clean, well-resolved "
    "chromatogram, so the HPLC figure on this one is easy to read with "
    "confidence. Mass spectrometry confirms the observed mass matches the "
    "intended sequence. Independent, per lot, reported on the certificate."
  ),
  handling=(
    "Keep sealed, cold and out of light. Reconstitute with bacteriostatic water "
    "down the vial wall and swirl to clear. At 5mg, 1mL gives 5 mg/mL and 2mL "
    "gives 2.5 mg/mL. Refrigerate once in solution and keep it out of the light."
  ),
  benefits=[
    "Synthetic pentadecapeptide (15 amino acids)",
    "5mg lyophilized powder, sealed vial",
    "99.3% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Also supplied in the Wolverine and Klow research blends",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What does pentadecapeptide mean?",
     "A peptide fifteen amino acids long. The prefix simply describes chain "
     "length — it says nothing about function."),
    ("Is this the same material used in the blends?",
     "Yes. The Wolverine and Klow blends are built from the same lots, tested "
     "the same way, with certificates on file."),
    ("What purity did this lot assay at?",
     "99.3% by HPLC, with identity confirmed by mass spectrometry. Your COA "
     "references your specific production lot."),
  ],
),

"tb500-5mg": dict(
  tagline="Synthetic fragment of the thymosin beta-4 sequence.",
  overview=(
    "TB-500 is a synthetic peptide corresponding to an active region of thymosin "
    "beta-4, a naturally occurring protein involved in actin regulation. Working "
    "with the fragment rather than the full protein is deliberate in research "
    "settings: it is far easier to synthesise reproducibly and to characterise "
    "analytically, which makes it a practical reference material for in-vitro "
    "cytoskeletal and cell-culture work. Supplied as a lyophilized powder in a "
    "sealed 5mg vial. For research use only — not for human or veterinary use."
  ),
  analytical=(
    "Fragment peptides have to be confirmed as the fragment, not the parent "
    "protein and not a truncation of it — which is precisely the question mass "
    "spectrometry answers by matching observed mass to the intended sequence. "
    "HPLC supplies the purity figure alongside it. Both run on every lot."
  ),
  handling=(
    "Sealed, cold and dark until use. Reconstitute with bacteriostatic water "
    "against the wall of the vial, swirling rather than shaking. At 5mg, 1mL "
    "gives 5 mg/mL and 2.5mL gives 2 mg/mL. Refrigerate in solution."
  ),
  benefits=[
    "Synthetic fragment of the thymosin beta-4 sequence",
    "5mg lyophilized powder, sealed vial",
    "99.1% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Also supplied in the Wolverine, Glow and Klow research blends",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("Is TB-500 the same as thymosin beta-4?",
     "No. It is a synthetic peptide corresponding to an active region of that "
     "protein, not the full-length protein itself."),
    ("Why supply a fragment rather than the whole protein?",
     "Reproducibility. A short synthetic sequence can be made to a consistent "
     "specification and characterised cleanly by HPLC and mass spec, which a "
     "full-length protein preparation makes considerably harder."),
    ("Which blends contain it?",
     "Wolverine Stack, Glow Blend and Klow Blend all include TB-500 alongside "
     "other compounds from this catalog."),
  ],
),

"kpv-10mg": dict(
  tagline="C-terminal tripeptide fragment of alpha-MSH.",
  overview=(
    "KPV is a tripeptide — lysine, proline, valine — corresponding to the "
    "C-terminal end of alpha-melanocyte-stimulating hormone. It is studied "
    "specifically as the minimal fragment of that sequence, which is what makes "
    "it useful: it lets structure-activity work isolate the contribution of the "
    "terminal residues from the rest of the parent molecule. At three residues "
    "it is the shortest peptide in this catalog. Supplied as a lyophilized "
    "powder in a sealed 10mg vial. For research use only — not for human or "
    "veterinary use."
  ),
  analytical=(
    "Three residues is about as simple as peptide chromatography gets, so the "
    "HPLC trace on this one is unusually clean and the purity figure "
    "correspondingly unambiguous. Mass spectrometry confirms identity. Both are "
    "independent and per lot."
  ),
  handling=(
    "Store sealed, cold and out of light. Reconstitute with bacteriostatic water "
    "down the vial wall. At 10mg, 2mL gives 5 mg/mL and 1mL gives 10 mg/mL. "
    "Short peptides dissolve readily — if the cake resists, warm the vial in the "
    "hand rather than agitating it. Refrigerate in solution."
  ),
  benefits=[
    "Tripeptide: lysine–proline–valine",
    "C-terminal fragment of the alpha-MSH sequence",
    "10mg lyophilized powder, sealed vial",
    "99.0% verified purity by HPLC",
    "Batch Certificate of Analysis on file",
    "Also supplied in the Klow research blend",
  ],
  faqs=[
    ("What does KPV stand for?",
     "The three amino acids in the sequence — lysine (K), proline (P) and valine "
     "(V), in that order."),
    ("How does it relate to alpha-MSH?",
     "It corresponds to the C-terminal end of the alpha-MSH sequence. Studying "
     "the fragment separately is how structure-activity work isolates what those "
     "terminal residues contribute."),
    ("Is it included in any blends?",
     "Yes — Klow Blend combines KPV with GHK-Cu, BP+ and TB-500."),
  ],
),

"ghkcu-100mg": dict(
  tagline="Copper-binding tripeptide complex, 100mg vial.",
  overview=(
    "GHK-Cu is a tripeptide — glycine, histidine, lysine — complexed with "
    "copper(II). The copper is not an additive but part of what is being "
    "studied: the peptide's defining property is its affinity for copper ions, "
    "and the complex behaves differently from the free peptide in both assay and "
    "solution. It appears widely in in-vitro matrix and cell-culture literature "
    "and in analytical work on metal-peptide complexes. This is the 100mg fill, "
    "for work that consumes material at volume. For research use only — not for "
    "human or veterinary use."
  ),
  analytical=(
    "Metal-complexed peptides need care in interpretation: the chromatographic "
    "behaviour of the complex is not that of the bare peptide, and a method "
    "developed for one won't read the other correctly. HPLC gives the purity "
    "figure, mass spectrometry confirms identity, both per lot and both "
    "independent."
  ),
  handling=(
    "Sealed, cold and out of light — the complex is light-sensitive and the "
    "characteristic blue colour is worth checking before use. Reconstitute down "
    "the vial wall. At 100mg, 10mL gives 10 mg/mL and 5mL gives 20 mg/mL. "
    "Refrigerate in solution and keep it dark."
  ),
  benefits=[
    "Tripeptide (glycine–histidine–lysine) complexed with copper(II)",
    "100mg lyophilized powder — the volume fill",
    "99.2% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Also supplied in the Glow and Klow research blends",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What is the difference between the 50mg and 100mg vials?",
     "Fill quantity only — same compound, same specification, same testing. The "
     "100mg vial is the better value per milligram for work that consumes "
     "material at volume."),
    ("Why is the copper part of the name?",
     "Because it is part of the molecule being supplied. GHK-Cu is the tripeptide "
     "complexed with copper(II), and the complex is what is characterised — not "
     "the peptide with copper added separately."),
    ("Why does it need to be kept dark?",
     "Copper-peptide complexes are light-sensitive. Store the sealed vial out of "
     "light and keep reconstituted material dark and refrigerated."),
  ],
),

"ghkcu-50mg": dict(
  tagline="Copper-binding tripeptide complex, 50mg vial.",
  overview=(
    "GHK-Cu is a tripeptide — glycine, histidine, lysine — complexed with "
    "copper(II). Its defining characteristic is affinity for copper ions, and it "
    "is the complex rather than the free peptide that is normally the subject of "
    "study; the two behave differently in solution and on an analytical column. "
    "This is the 50mg fill, sized for smaller protocols and for method "
    "development where a 100mg vial would degrade in solution before it was "
    "consumed. For research use only — not for human or veterinary use."
  ),
  analytical=(
    "The same two questions as every lot: HPLC for how much of the sample is the "
    "target complex, mass spectrometry for whether the target complex is what it "
    "should be. Metal-peptide complexes make the second question less trivial "
    "than usual, which is why it isn't skipped."
  ),
  handling=(
    "Store sealed, cold and out of light; the complex is light-sensitive. "
    "Reconstitute against the vial wall and swirl. At 50mg, 5mL gives 10 mg/mL "
    "and 2.5mL gives 20 mg/mL. Keep reconstituted material refrigerated and "
    "dark."
  ),
  benefits=[
    "Tripeptide (glycine–histidine–lysine) complexed with copper(II)",
    "50mg lyophilized powder — the smaller fill",
    "99.2% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Also available as a 100mg vial",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("Should I take the 50mg or the 100mg vial?",
     "The compound and specification are identical. Take the 50mg if your "
     "protocol won't consume 100mg while it is still in good condition — "
     "lyophilized material keeps far better than reconstituted material."),
    ("What gives it the blue colour?",
     "The copper(II) in the complex. It's a useful visual check: a sealed vial "
     "that has lost its characteristic colour is worth questioning before use."),
    ("Is it third-party tested?",
     "Yes — independent HPLC and mass spectrometry on every production lot, with "
     "the certificate on file."),
  ],
),

"mt1-10mg": dict(
  tagline="Alpha-MSH analog selective for the melanocortin-1 receptor.",
  overview=(
    "MT-1 is a synthetic analog of alpha-melanocyte-stimulating hormone, "
    "characterised in the literature by its selectivity for the melanocortin-1 "
    "receptor subtype. That selectivity is the point of the compound in research "
    "terms: the melanocortin family has five known receptor subtypes with "
    "overlapping ligands, and a selective analog is what lets binding work "
    "attribute an effect to one subtype rather than the family. Supplied as a "
    "lyophilized powder in a sealed 10mg vial. For research use only — not for "
    "human or veterinary use."
  ),
  analytical=(
    "For a selective analog, identity confirmation is the test that matters "
    "most — the melanocortin analogs are structurally close to one another, and "
    "a purity figure alone would not distinguish them. Mass spectrometry matches "
    "observed mass to the intended sequence; HPLC supplies the purity number "
    "alongside it."
  ),
  handling=(
    "Sealed, cold and out of light. Reconstitute with bacteriostatic water down "
    "the vial wall, swirling until clear. At 10mg, 2mL gives 5 mg/mL and 1mL "
    "gives 10 mg/mL. Refrigerate once in solution and keep protected from "
    "light."
  ),
  benefits=[
    "Synthetic alpha-MSH analog",
    "Selective for the melanocortin-1 receptor subtype",
    "10mg lyophilized powder, sealed vial",
    "99.0% verified purity by HPLC",
    "Identity confirmed by mass spectrometry",
    "Ships from the USA in 2–5 business days",
  ],
  faqs=[
    ("What does MC1R selectivity mean?",
     "The melanocortin family has five known receptor subtypes. A selective "
     "analog binds preferentially to one — here MC1R — which is what allows "
     "in-vitro work to attribute a binding result to that subtype rather than to "
     "the receptor family as a whole."),
    ("How is it distinguished from other melanocortin analogs?",
     "By mass spectrometry. Compounds in this family are structurally similar "
     "enough that a purity figure alone would not tell them apart, which is why "
     "identity confirmation is run on every lot."),
    ("What is the parent molecule?",
     "Alpha-melanocyte-stimulating hormone (alpha-MSH), the endogenous peptide "
     "that signals through the melanocortin receptor family."),
  ],
),

}
