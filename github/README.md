# Github metrics

This directory contains Groovy scripts capable of interacting with the [github v3 API](https://developer.github.com/v3/).

## Requirements

* JDK 8+
* Groovy 2.4+

The scripts will use the Groovy [@Grab](http://docs.groovy-lang.org/latest/html/documentation/grape.html) annotation
to fetch dependencies. The first time you run these script you may observe a delay as the dependencies
are being cached locally.

## activity_by_planning_period.groovy

This script walks through the repositories and planning periods and uses the 
[Github Search API](https://developer.github.com/v3/search/) to collect the activity within. 

Expected fragments in `settings.json`:

```
{
  "github_username": "yourusername",
  "github_password": "yourgithubaccesstoken",
  "repositories": [
    "sonatype/foo-repo1", "sonatype/foo-repo2", "sonatype/foo-repo3", ...
  ],
  "planningPeriods": {
    "periodName1": "2017-10-26..2017-12-21",
    "periodName2": "2017-12-22..2018-02-15",
    ...
  }
}
```

Running:

> groovy activity_by_planning_period.groovy ../path/to/settings.json
