@Grab(group='io.github.http-builder-ng', module='http-builder-ng-okhttp', version='1.0.3' )
@Grab(group='ch.qos.logback', module='logback-classic', version='1.2.3')
@Grab(group='com.fasterxml.jackson.core', module="jackson-databind", version='2.9.7')

import groovy.transform.Field
import groovy.transform.ToString
import groovyx.net.http.HttpBuilder
import org.slf4j.LoggerFactory
import ch.qos.logback.classic.Level
import ch.qos.logback.classic.Logger

Logger root = (Logger)LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME)
root.setLevel(Level.INFO)
def log = LoggerFactory.getLogger(this.class)

@Field def settings = new groovy.json.JsonSlurper().parse(new File(args[0]))
@Field def github = HttpBuilder.configure {
  request.uri = 'https://api.github.com/'
  def credentials = settings.github_username + ":" + settings.github_password
  // can't use basic auth like this, since github replies with 422 instead of 401
  //request.auth.basic settings.github_username, settings.github_password
  // so, preemptive auth instead
  request.headers['Authorization'] = "Basic ${credentials.bytes.encodeBase64().toString()}"
}

def data = [:]

settings.planningPeriods.each { period ->
  data[period.key] = []
  settings.repositories.each { repo ->
    def counts = new RepoCounts()
    counts.repoName = repo
    counts.commitCount = commitCount(repo, period.value)
    data[period.key].add(counts)
    // search API is rate limited to 30 requests per minute
    sleep(2000L)
  }
  log.debug "commit data for ${period.key} complete"
}

println("Period,${settings.repositories.join(',')}")
data.each { key, values ->
  println("$key,${values.commitCount.join(',')}")
}

def commitCount(String repoName, String dateRange) {
  return github.get {
    request.uri.path = '/search/commits'
    request.uri.query = [ q: "committer-date:$dateRange+repo:$repoName" ]
    request.accept = 'application/vnd.github.cloak-preview'
  }?.total_count
}

@ToString(includeNames=true)
class RepoCounts {
  String repoName
  int commitCount
}

