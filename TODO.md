[x] Fix existing tests
[x] Add swagger UI
[x] Make FrontEnd work
    [x] Make sure items-service can create items
    [x] Make sure reviews-service can create reviews
    [x] Make sure FrontEnd can use updated code
[x] Add DB versioning
[ ] Cleanup
    [ ] Remove review_item till it is used again
    [x] Remove purchase_order till it is used again
    [x] Remove purchase_order_item till it is used again
    [ ] Check for other unused
[ ] Try to deploy to other laptop with basic k8s
[ ] Review existing functionality
[ ] Add wiremock logic:
    [ ] Providers have lists of items for items-service
    [ ] Items' prices can change within a range to be used in /purchase-from-provider
[ ] Items should not be deleted, but archived instead to avoid DB gaps
[ ] Move logic from `app.py` to a new "service" layer
[ ] Install [Kiwi TCMS](https://kiwitcms.readthedocs.io/en/latest/installing_docker.html#example-with-docker-compose)
[ ] Write down tests in Kiwi
[ ] Install Grafana and Prometheus
[ ] Make services report metrics to Grafana (tps, feature, response time, etc)
[ ] Push existing test metrics to Prometheus
[ ] Create test dashboard
[ ] Add k6
[ ] Add ArgoCD
[ ] Add SonarCloud/Qube
[ ] Choose cloud (managed k8s vs k3s)
[ ] Add a tool to looks for security vulnerabilities
[ ] Bump up dependency versions
[ ] Improve test coverage
[ ] Add contract tests
[ ] Add linters or SonarCube and report
