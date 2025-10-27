This repository contains the solution to TerraQuantum's (TQ) assignment.

## Installation

First, download the repository:

```git clone https://github.com/ganesh7shahane/TQ_test.git```

Second, create the environment:

```conda env create -f environment.yaml

conda activate TQ_test
```

## Getting started

- A high level summary is contained in [High_Level_Summary.pdf](https://github.com/ganesh7shahane/TQ_test/blob/main/High_Level_Summary.pdf) as requested.

- The solution is distributed in 5 different jupyter notebooks, each with the preferred order of prefixes: '1_', '2_', '3_'...

- 5 notebooks were made and not just one for ease of organisation and presenting it to interviewers.

- Open each in VS code (or directly through the terminal), and simply press "▶️Run All" for each of the notebooks: first notebook to run should be `1_Purchasable_compounds.ipynb`, next one should be `2_PrepareProtein.ipynb` and so on.

## Summary table
The following is the summary of top molecules prioritised for synthesis:

|     |   ID | SMILES                                                      | CatalogID                    |   best_affinity_kcal_per_mol |    LE |    LOGP |   HB_donors |    MW |
|----:|-----:|:------------------------------------------------------------|:-----------------------------|-----------------------------:|------:|--------:|------------:|------:|
|   4 | 1027 | c1ccc(Nc2nc(NCc3ccncc3OCC3CCOC3)nc3[nH]cnc23)cc1            | s_27____10228314____10803818 |                       -9.322 | 0.301 | 2.21485 |           3 | 417.5 |
|  34 | 1182 | CC1COCC(CCNc2nc(Nc3ccccc3)c3[nH]cnc3n2)O1                   | s_27____25523224____10803818 |                       -9.188 | 0.353 | 2.11777 |           3 | 354.4 |
|  45 | 1217 | COC(C)(CNc1nc(Nc2ccccc2)c2[nH]cnc2n1)C1CCOCC1               | s_27____20762476____10803818 |                       -9.091 | 0.325 | 2.5621  |           3 | 382.5 |
|  51 | 1261 | c1ccc(Nc2nc(N[C@H]3CC[C@H](Oc4cnccn4)CC3)nc3[nH]cnc23)cc1   | s_27____12806124____10803818 |                       -9.205 | 0.307 | 2.75276 |           3 | 402.5 |
|  68 | 1400 | Clc1cncc(OCCCNc2nc(Nc3ccccc3)c3[nH]cnc3n2)n1                | s_27____25541468____10803818 |                       -9.094 | 0.325 | 2.53429 |           3 | 396.8 |
|  81 |  226 | COc1cc(OC)c(CCNc2nc(Nc3ccccc3)c3[nH]cnc3n2)cn1              | s_27____16908938____10803818 |                       -9.056 | 0.312 | 2.92152 |           3 | 391.4 |
|  95 |  286 | c1ccc(Nc2nc(NCC3CCOC34CCOCC4)nc3[nH]cnc23)cc1               | s_27____25521308____10803818 |                       -9.437 | 0.337 | 1.75067 |           3 | 380.5 |
| 108 |  323 | c1ccc(Nc2nc(NC[C@H]3C[C@H]4COC[C@@H](C3)C4)nc3[nH]cnc23)cc1 | m_27____25523998____10803818 |                       -9.396 | 0.348 | 2.97952 |           3 | 364.5 |
| 129 |  393 | CCC12CCC(Nc3nc(Nc4ccccc4)c4[nH]cnc4n3)(CO1)C2               | m_27____19140552____10803818 |                       -9.244 | 0.356 | 2.9406  |           3 | 350.4 |
| 147 |  452 | CC12CCC(Nc3nc(Nc4ccccc4)c4[nH]cnc4n3)(CC1)CO2               | m_27____25557544____10803818 |                       -9.539 | 0.367 | 2.93545 |           3 | 350.4 |
| 172 |  530 | c1ccc(Nc2nc(NCC3CCCC4(CCOC4)O3)nc3[nH]cnc23)cc1             | s_27____14051036____10803818 |                       -9.198 | 0.329 | 2.5351  |           3 | 380.5 |
| 188 |  605 | CO[C@H]1[C@H](Nc2nc(Nc3ccccc3)c3[nH]cnc3n2)COC12CCC2        | s_27____20349660____10803818 |                       -9.558 | 0.354 | 2.53491 |           3 | 366.4 |
| 215 |  678 | c1ccc(Nc2nc(NC3COC4(CCOCC4)C3)nc3[nH]cnc23)cc1              | s_27____25521160____10803818 |                       -9.702 | 0.359 | 1.63313 |           3 | 366.4 |
| 221 |  693 | COC(CNc1nc(Nc2ccccc2)c2[nH]cnc2n1)C1CCCOC1                  | s_27____13903878____10803818 |                       -9.075 | 0.336 | 2.32308 |           3 | 368.4 |
| 236 |  733 | CCOC(CNc1nc(Nc2ccccc2)c2[nH]cnc2n1)C1CCOC1                  | s_27____17757172____10803818 |                       -9.017 | 0.334 | 2.23532 |           3 | 368.4 |
| 280 |   87 | CO[C@H]1[C@H](Nc2nc(Nc3ccccc3)c3[nH]cnc3n2)COC1(C)C         | m_27____18799958____10803818 |                       -9.104 | 0.35  | 2.39816 |           3 | 354.4 |


## Managing scaling, logging and results tracking for large-scale CADD workflows

For managing large-scale CADD (Computer-Aided Drug Design) workflow, integrating proven tools and best practices from data engineering, informatics, and workflow automation is critical. Here’s how it’s typically accomplished:

- Cloud infrastructure (AWS Batch, Google Cloud Life Sciences, or on-prem clusters with SLURM) is often leveraged for horizontal scaling. These allow you to scale compute resources according to demand and process hundreds or thousands of docking, simulation, or scoring jobs in parallel.

- Use workflow management systems such as Apache Airflow for orchestrating and scheduling large numbers of jobs. These tools can distribute tasks over multiple nodes and handle dependencies, failures, and retries automatically.

- Implement structured logging throughout all workflow components—for example, using Python’s `logging` library with JSON output to enable easier parsing and aggregation of logs from multiple processes.

- Use database-backed result tracking for CADD output (e.g., compound activities, free energy results, docking scores). Relational databases (PostgreSQL, MySQL), NoSQL stores (MongoDB), or specialized workflow metadata tools (MLflow, Weights & Biases) can capture run configurations, job statuses, and results for later analysis, comparison, and provenance.


## List of AI tools used for the assignment
... and how I worked with them:

- ChatGPT 5.0 was used extensively to write the code. It helped me write majority of the helper functions contained in the notebooks. Perplexity and Gemini were used to a minor extent.
  
- Github co-pilot was used for automatic completions of scripts for visualisation and analysing molecules.
