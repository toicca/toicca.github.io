---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

<style>
  .cv-collapsible > summary {
    cursor: pointer;
    list-style: none;
    display: flex;
    align-items: baseline;
    gap: 0.5em;
  }
  .cv-collapsible > summary::-webkit-details-marker {
    display: none;
  }
  .cv-collapsible > summary::before {
    content: "▶";
    display: inline-block;
    font-size: 0.6em;
    transition: transform 0.15s ease;
  }
  .cv-collapsible[open] > summary::before {
    transform: rotate(90deg);
  }
  .cv-collapsible > summary h1 {
    display: inline;
    margin: 0;
  }
</style>

Education
======
* PhD, Doctoral Programme in Science, University of Helsinki, 2024 -- present
* M.Sc. in Theoretical and Computation Methods, University of Helsinki, 2021 -- 2023
  * Thesis: "Relative response measurement between light quark and gluon jets at the CMS experiment"
* B.Sc. in Physical Sciences, University of Helsinki, 2019 -- 2021, with distinction
  * Thesis: "Mapping the electrostatic potential of a molecule from its electron density using parallel computing"
* Finnish Matriculation Exam, Kotkan lyseon lukio, 2015 -- 2018

Employment history
======
* 2024 -- present: PhD student, Helsinki Institute of Physics CMS group
  * Projects: Calibration of light quark and gluon jet taggers, Prompt Jet Energy Corrections, All-hadronic Vector Boson Scattering, and Underlying Event studies
* 2022 -- 2023: Research assistant, Helsinki Institute of Physics CMS group
  * Project: The relative Jet Energy Scale of light quark and gluon jets
* 2020 -- 2023: Teaching assistant, guide, and tutor, University of Helsinki, Department of Physics
* 2021: Research assistant, Aalto University, Surfaces and Interfaces at the Nanoscale group
  * Project: CUDA based Poisson equation solver for electrostatic potentials of molecules
* Co-author, Eira High School for Adults / Finnish Ministry of Education
  * Project: Exercises for "Fysiikkaa omaan tahtiin" high school electromagnetics course

<details class="cv-collapsible">
<summary><h1>Publications (including with CMS Collaboration)</h1></summary>
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
</details>

<details class="cv-collapsible">
<summary><h1>Talks</h1></summary>
  {% assign talks_dated = site.talks | where_exp: "item", "item.date" | sort: "date" | reverse %}
  {% assign talks_undated = site.talks | where_exp: "item", "item.date == nil" %}
  <ul>{% for post in talks_dated %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}{% for post in talks_undated %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}</ul>
</details>

<details class="cv-collapsible">
<summary><h1>Teaching</h1></summary>
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
</details>

Awards and achievements
======
* 2026: Best experimental speaker, Conference on Diffraction and low-x
* 2023: Grant for success in studies, Mathematics and Natural Sciences fund of the University of Helsinki
* 2022: Grant for success in studies, Mathematics and Natural Sciences fund of the University of Helsinki
* 2019: Diploma for excellent performance, Finnish Air Force Reserve Officer School
* 2018: Stipend for studies in music and school choir, Kotkan lyseon lukio

Certification and training
======
* 2026: CERN Guide
* 2018 -- 2019: Finnish Reserve Officer School, Finnish Air Force

Service and leadership
======
* 2026 -- present: CMS, Jet and MET algorithms and reconstruction, convener
* 2026 -- present: ECFA Early-Career Researchers Panel, panel member
* 2024 -- 2025: Helsingin yliopiston Filosofisen tiedekunnan promootio, treasurer and organizer
* 2023 -- 2024: Master's Programme in Materials Research, steering group student representative
* 2023 -- 2024: Master's Programme in Theoretical and Computation Methods, steering group student representative
* 2022 -- present: Helsinki Institute of Physics PR contact
  * Organized high-school visits to the University of Helsinki and Helsinki Institute of Physics
* 2023 -- 2025: CMS Physics Masterclasses, organizer for Helsinki Institute of Physics
* 2021: Student organization Meridiaani ry, treasurer and board member

Languages
======
* Finnish, mother tongue
* English, C2 (self-assessed)
* Swedish, A2 (self-assessed)
* French, A1 (self-assessed)
