# Raw Run Bundle

This directory preserves a minimal raw bundle for the AutoResearch campaign.
It is meant for traceability from processed accounting files back to individual
live runs.

## Imported Raw Files

For each available `worker_confirmation` run, the bundle keeps:

- `config_resolved.yaml`
- `run_manifest.json`
- `baseline_verification.json`
- `interactive_initial_prompt.txt`
- `interactive_session.json`
- `evaluations.jsonl`
- `run_summary.json`

These files are enough to inspect the run seed, workload, worker/model, prompt
snapshot, step-by-step evaluator records, final loss/success values, wall time,
and accounting cost fields.

## Coverage

The inspected remote workspace contained 250 `worker_confirmation` run
directories. All 250 were imported with the seven files listed above.

The balanced `n=30` manifest has 270 rows. Of those rows:

- 180 have raw files present in this bundle.
- 90 reference `worker_pilot` sources that were not present in the inspected
  remote workspace.

See:

- `manifests/raw_import_summary.json`
- `manifests/raw_run_inventory.csv`
- `manifests/balanced_n30_raw_coverage.csv`
- `manifests/raw_file_manifest_sha256.csv`

## Not Included

The import intentionally excludes intermediate workspace trees, verifier raw
workspace directories, proposed solution files, Slurm output, and cluster logs.
Those files are much larger and more environment-bound. If needed later, they
should be exported as an external artifact with checksums rather than committed
directly to the product repository.
