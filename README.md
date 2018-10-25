# Team Stats

This pulls team stats from Jira and github

## Setup

```shell
pip3 install jira
pip3 install PyGithub
pip3 install PyMySQL
cp sample-settings.json settings.json
echo "fill out settings.json"
```

`./run-report.py > reports/some-report-name.csv`

Alternatively you can just run `./build-deploy.sh`

### Docker Setup

* build: `docker build -t py-rt .`
* run with volume to get latest w/o build: `docker run --rm -v ${pwd}:/program py-rt:latest ./python/<script>`
* example: `docker run --rm -v ${pwd}:/program py-rt:latest ./python/jira_test_time_in_status.py`

## References

* https://jira.readthedocs.io/en/latest/
* https://pygithub.readthedocs.io/en/latest/reference.html
