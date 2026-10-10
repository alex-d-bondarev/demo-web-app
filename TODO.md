[x] Fix existing tests
[x] Add swagger UI
[ ] Make FrontEnd work
    [x] Make sure items-service can create items
    [x] Make sure reviews-service can create reviews
    [ ] Make sure FrontEnd can use updated code
[ ] Add DB versioning
[ ] Fix DB gaps
[ ] Install [Kiwi TCMS](https://kiwitcms.readthedocs.io/en/latest/installing_docker.html#example-with-docker-compose)
[ ] Write down tests in Kiwi
[ ] Install Grafana and Prometheus
[ ] Make services report metrics to Grafana (tps, feature, response time, etc)
[ ] Push existing test metrics to Prometheus
[ ] Create test dashboard
[ ] Try to deploy to other laptop with basic k8s
[ ] Add k6
[ ] Add ArgoCD
[ ] Choose cloud k8s
[ ] Add a tool to looks for security vulnerabilities
[ ] Bump up dependency versions
[ ] Improve test coverage
[ ] Add contract tests
[ ] Add wiremock logic:
    [ ] Providers have lists of items for items-service
    [ ] Items' prices can change within a range to be used in /purchase-from-provider
[ ] Items should not be deleted, but archived instead to avoid DB gaps
[ ] Move logic from `app.py` to a new "service" layer
[ ] Review existing functionality
[ ] Add linters or SonarCube and report
