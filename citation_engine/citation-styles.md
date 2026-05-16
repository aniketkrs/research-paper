# Citation Styles Reference

This file is the canonical guide for in-text citations and reference entries
in every style this skill supports. The bibliography formatter
(`scripts/format_bibliography.py`) implements these rules exactly.

> **Rule of thumb:** when in doubt, copy the example for the entry type that
> matches your source most closely. Punctuation, italics, and capitalization
> are part of the rule — not stylistic choices.

---

## Common metadata fields

Every reference entry should be modeled internally as:

```yaml
- id: smith2023llm                     # cite key (lowercase, no spaces)
  type: article-journal                # article-journal | article-conference | book | chapter | report | webpage | dataset | thesis | preprint
  authors:
    - {family: Smith, given: Jane A.}
    - {family: Doe,   given: Alice}
    - {family: Lee,   given: Kim B.}
  year: 2023
  month: 03                            # optional
  title: "Large language models in software engineering: A systematic survey"
  container: "ACM Computing Surveys"   # journal, book, or proceedings
  volume: 55
  issue: 4
  pages: "1-37"
  publisher: "ACM"
  address: "New York, NY, USA"         # for books / proceedings
  doi: "10.1145/3589334"
  url: "https://doi.org/10.1145/3589334"
  arxiv_id: "2301.12345"               # optional
  isbn: "978-0-12-345678-9"            # books
  edition: 3                            # books, optional
  editors:                              # for chapters and edited books
    - {family: Brown, given: Q.}
  accessed: "2024-05-12"               # webpages
  notes: ""                             # free text
```

The skill's outputs always use these fields under the hood. Each style below
is a deterministic projection of these fields into formatted text.

---

## 1. Harvard (author–year)

**In-text:**

| Pattern                          | Example                                 |
| -------------------------------- | --------------------------------------- |
| One author                       | (Smith, 2023)                           |
| Two authors                      | (Smith and Doe, 2023)                   |
| Three+ authors                   | (Smith et al., 2023)                    |
| Page-specific                    | (Smith, 2023, p. 45) / (..., pp. 45–58) |
| Multiple sources                 | (Smith, 2023; Doe, 2022)                |
| Author as part of sentence       | "Smith (2023) argued that …"            |
| Same author, multiple works      | (Smith, 2023a, 2023b)                   |
| Organization author              | (World Health Organization, 2024)       |
| No date                          | (Smith, n.d.)                           |
| Secondary citation               | (Jones, 1990, cited in Smith, 2023)     |

**Reference list (alphabetical by family name):**

- **Journal article:**
  Smith, J. A., Doe, A. and Lee, K. B. (2023) 'Large language models in
  software engineering: A systematic survey', *ACM Computing Surveys*,
  55(4), pp. 1–37. doi:10.1145/3589334.

- **Conference paper:**
  Doe, A. and Lee, K. (2022) 'Title of paper', in *Proceedings of the
  35th Conference on Foo (CONF '22)*. New York: ACM, pp. 12–24.
  doi:10.1145/xxxxxxx.

- **Book:**
  Smith, J. A. (2021) *Title of the Book*. 3rd edn. Cambridge:
  Cambridge University Press.

- **Book chapter:**
  Lee, K. (2020) 'Chapter title', in Brown, Q. (ed.) *Title of Book*.
  Oxford: Oxford University Press, pp. 101–125.

- **Report:**
  World Health Organization (2024) *Title of report*. Report No. WHO/123.
  Geneva: WHO. Available at: https://who.int/... (Accessed: 12 May 2024).

- **Webpage:**
  Smith, J. (2023) *Title of page*. Available at: https://example.com/x
  (Accessed: 12 May 2024).

- **Preprint (arXiv):**
  Smith, J. and Doe, A. (2024) 'Title of preprint', arXiv:2403.01234.
  Available at: https://arxiv.org/abs/2403.01234 (Accessed: 12 May 2024).

- **Dataset:**
  Smith, J. (2023) *Title of dataset* [Dataset]. Zenodo.
  doi:10.5281/zenodo.xxxxxxx.

- **Thesis:**
  Doe, A. (2022) *Title of thesis*. PhD thesis, University of Oxford.

---

## 2. APA 7th edition

**In-text:** parenthetical (Author, Year) or narrative Author (Year). 3+
authors collapse to "et al." from the first citation.

| Pattern        | Example                                       |
| -------------- | --------------------------------------------- |
| Parenthetical  | (Smith, 2023)                                 |
| Two authors    | (Smith & Doe, 2023)                           |
| 3+ authors     | (Smith et al., 2023)                          |
| Direct quote   | (Smith, 2023, p. 45)                          |
| Multiple works | (Doe, 2022; Smith, 2023)                      |

**Reference list (alphabetical, hanging indent):**

- **Journal article (with DOI):**
  Smith, J. A., Doe, A., & Lee, K. B. (2023). Large language models in
  software engineering: A systematic survey. *ACM Computing Surveys, 55*(4),
  1–37. https://doi.org/10.1145/3589334

- **Book:**
  Smith, J. A. (2021). *Title of the book* (3rd ed.). Cambridge University
  Press.

- **Edited chapter:**
  Lee, K. (2020). Chapter title. In Q. Brown (Ed.), *Title of book* (pp.
  101–125). Oxford University Press.

- **Conference paper:**
  Doe, A., & Lee, K. (2022, October 10–14). *Title of paper* [Paper
  presentation]. CONF '22, City, Country. https://doi.org/10.1145/xxxxxxx

- **Preprint:**
  Smith, J., & Doe, A. (2024). *Title of preprint*. arXiv.
  https://doi.org/10.48550/arXiv.2403.01234

- **Webpage:**
  Smith, J. (2023, March 5). *Title of page*. Site Name.
  https://example.com/x

- **Report:**
  World Health Organization. (2024). *Title of report* (Report No. WHO/123).
  https://who.int/...

- **Dataset:**
  Smith, J. (2023). *Title of dataset* [Dataset]. Zenodo.
  https://doi.org/10.5281/zenodo.xxxxxxx

---

## 3. IEEE (numeric)

**In-text:** square-bracket numbers in **order of first appearance**. Multiple
in one bracket: `[1], [2]` or `[1]–[3]`.

> "As demonstrated in [3], the proposed method achieves …"
> "Several studies [1], [2], [5] have shown …"

**Reference list (numeric, in order of appearance):**

- **Journal article:**
  [1] J. A. Smith, A. Doe, and K. B. Lee, "Large language models in
  software engineering: A systematic survey," *ACM Comput. Surv.*, vol. 55,
  no. 4, pp. 1–37, Mar. 2023, doi: 10.1145/3589334.

- **Conference paper:**
  [2] A. Doe and K. Lee, "Title of paper," in *Proc. 35th Conf. on Foo
  (CONF '22)*, New York, NY, USA, Oct. 2022, pp. 12–24, doi: 10.1145/xxxxxxx.

- **Book:**
  [3] J. A. Smith, *Title of the Book*, 3rd ed. Cambridge, U.K.: Cambridge
  Univ. Press, 2021.

- **Book chapter:**
  [4] K. Lee, "Chapter title," in *Title of Book*, Q. Brown, Ed. Oxford,
  U.K.: Oxford Univ. Press, 2020, pp. 101–125.

- **Preprint (arXiv):**
  [5] J. Smith and A. Doe, "Title of preprint," 2024, *arXiv:2403.01234*.

- **Standard:**
  [6] *IEEE Standard for Floating-Point Arithmetic*, IEEE Standard 754-2019,
  Jul. 2019.

- **Webpage:**
  [7] J. Smith, "Title of page," *Site Name*, Mar. 5, 2023. [Online].
  Available: https://example.com/x. [Accessed: May 12, 2024].

- **Dataset:**
  [8] J. Smith, "Title of dataset," Zenodo, 2023, doi: 10.5281/zenodo.xxxxxxx.

---

## 4. MLA 9th edition

**In-text:** (Author Page) — no comma, no year in parenthetical.

> "Smith argues this point clearly (45)."
> "(Smith and Doe 102)"
> "(Smith et al. 17–19)"

**Works Cited (alphabetical, hanging indent):**

- **Journal article:**
  Smith, Jane A., et al. "Large Language Models in Software Engineering: A
  Systematic Survey." *ACM Computing Surveys*, vol. 55, no. 4, 2023, pp. 1–37.
  *ACM Digital Library*, https://doi.org/10.1145/3589334.

- **Book:**
  Smith, Jane A. *Title of the Book*. 3rd ed., Cambridge UP, 2021.

- **Webpage:**
  Smith, Jane. "Title of Page." *Site Name*, 5 Mar. 2023,
  example.com/x. Accessed 12 May 2024.

---

## 5. Chicago (author–date and notes-bibliography)

### 5a. Author–date (sciences, social sciences)

**In-text:** (Smith 2023, 45) — note the **space**, no comma between year and
page.

**Reference list:**
- Smith, Jane A., Alice Doe, and Kim B. Lee. 2023. "Large Language Models in
  Software Engineering: A Systematic Survey." *ACM Computing Surveys* 55 (4):
  1–37. https://doi.org/10.1145/3589334.

### 5b. Notes–bibliography (humanities)

**Footnote (first time):**
1. Jane A. Smith, Alice Doe, and Kim B. Lee, "Large Language Models in
   Software Engineering: A Systematic Survey," *ACM Computing Surveys* 55,
   no. 4 (2023): 12, https://doi.org/10.1145/3589334.

**Subsequent shortened note:**
2. Smith, Doe, and Lee, "Large Language Models," 14.

**Bibliography entry:** same as 5a but with the names inverted only on the
first author.

---

## 6. Nature (numeric superscript)

**In-text:** superscript numerals, ordered by appearance, multiple separated
by commas without spaces:

> "Earlier work has challenged this view^3,7,12."

**Reference list (numbered, in order of appearance):**

1. Smith, J. A., Doe, A. & Lee, K. B. Large language models in software
   engineering: a systematic survey. *ACM Comput. Surv.* **55**, 1–37 (2023).
2. Doe, A. & Lee, K. Title of paper. In *Proc. 35th Conf. on Foo* 12–24
   (ACM, 2022).
3. Smith, J. A. *Title of the Book* 3rd edn (Cambridge Univ. Press, 2021).
4. World Health Organization. *Title of report*. Report No. WHO/123 (WHO,
   2024).

Note Nature's specific conventions:
- Initials before family name in references.
- `&` (not "and") for the last author.
- Volume in **bold**.
- Year at the end in parentheses.

---

## 7. arXiv-style numeric

Most arXiv submissions use **author-year** via natbib (so use APA / Harvard
above), but ML / vision papers often use **numeric IEEE-like brackets**.
The CVPR / ICCV / NeurIPS / ICLR community prefers `[1]`. Use the IEEE rules
above and remove journal abbreviations (CVPR papers use full names).

Common ML preprint pattern:
> [1] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L.,
> Gomez, A., Kaiser, Ł., and Polosukhin, I. Attention is all you need.
> *NeurIPS*, 2017.

---

## 8. Style-conversion rules

`scripts/format_bibliography.py` accepts `--from auto --to <style>` and
applies the projections above. Internal canonical form is the YAML-style
metadata in §"Common metadata fields".

| From → To  | Notes                                                        |
| ---------- | ------------------------------------------------------------ |
| Anything → IEEE  | Number entries in order of first in-text citation.       |
| Anything → Harvard / APA | Sort alphabetically by family name + year.       |
| APA → Harvard    | Replace `&` with `and`; `(2023)` becomes `(2023)`.       |
| Harvard → IEEE   | Replace `(Smith, 2023)` with `[N]` per citation order.   |
| Author–year → numeric | Build an appearance-order index first, then number. |

Always **rebuild** the reference list when switching styles — never patch
in place.

---

## 9. DOI / URL hygiene

- Always store the canonical DOI URL: `https://doi.org/<doi>`.
- For arXiv: `https://arxiv.org/abs/<id>` (preferred over PDF URL).
- For URLs without DOIs, store the **archived** version when available
  (Wayback Machine) and use the access date in styles that require it.
- Strip tracking parameters (`utm_*`, `ref=`, `?source=`).
- Verify each DOI with a `doi.org` HEAD request when web tools are available.

---

## 10. De-duplication and disambiguation

- Two entries are duplicates if they share **(DOI)** *or*
  **(first-author family + year + first 5 normalized title words)**.
- For two works by the same author in the same year, append a/b/c: e.g.,
  Smith (2023a), Smith (2023b). The skill assigns letters in order of first
  in-text citation.
- For shared cite keys, the canonical form is
  `<lower(family)>_<year>_<first-content-word>`, e.g., `smith_2023_llm`.

---

## 11. In-text citation density (sanity defaults)

- **Introduction:** 6–15 citations per page, mostly to anchor the field.
- **Related Work / Literature Review:** 15–40 per section.
- **Methodology:** 0–5 per page (cite when adopting a known method).
- **Results / Findings:** 0–2 per page (mostly your own results).
- **Discussion:** 5–10 per page (compare to prior work).
- **Conclusion:** 0–2.

If a section is far below these floors, the validation pipeline will flag it
("Insufficient citations").

---

## 12. Quick reference — minimum required fields

A citation cannot ship without these:

| Source type        | Minimum required                                           |
| ------------------ | ---------------------------------------------------------- |
| Journal article    | authors, year, title, container, volume, pages, doi/url    |
| Conference paper   | authors, year, title, container, pages, doi/url            |
| Book               | authors, year, title, publisher                            |
| Book chapter       | authors, year, chapter title, editors, book title, pages, publisher |
| Report             | author/org, year, title, report no., publisher, url        |
| Webpage            | author/org, year, title, url, accessed                     |
| Preprint           | authors, year, title, arxiv_id or url                      |
| Dataset            | author/org, year, title, doi/url                           |
| Thesis             | author, year, title, degree, institution                   |

Any reference missing a required field is marked `[INCOMPLETE]` and surfaced
in the review pipeline.
