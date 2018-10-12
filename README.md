# Team Stats

This pulls team stats from Jira and github

## Setup

```shell
pip3 install jira
pip3 install PyGithub
cp sample-settings.json settings.json
echo "fill out settings.json"
```

`./run-report.py > reports/some-report-name.csv`

Alternatively you can just run `./build-deploy.sh`

## References

* https://jira.readthedocs.io/en/latest/
* https://pygithub.readthedocs.io/en/latest/reference.html