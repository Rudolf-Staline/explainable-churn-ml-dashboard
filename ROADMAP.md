# Roadmap

## Completed in v0.1

- Reproducible tabular churn training pipeline.
- FastAPI scoring service with health, prediction, batch prediction, and model metadata endpoints.
- React/TypeScript decision dashboard.
- Local explanation layer for top prediction drivers.
- Synthetic sample dataset for smoke testing.
- Minimal pytest API coverage.

## Next improvements

1. Add a dedicated `make train` / `make test` workflow.
2. Add model calibration and threshold optimization for retention budgets.
3. Add CSV batch upload and downloadable scoring results.
4. Add SHAP plots or permutation importance visualizations in the dashboard.
5. Add data quality checks before training.
6. Add experiment tracking with MLflow or a lightweight local registry.
7. Add Dockerfiles for production-style image builds.
