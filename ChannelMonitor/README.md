#Channel Monitor

![](https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTrT1Dl7QTXqqDn4CzCj1Wn9YBuRFl8K498Xw&usqp=CAU)

Channel Monitor reacts to channel_archive, channel_crated, and channel_deleted slack events and logs the events. 

This log will be maintained inside of errbot (using the default storage backend) and can also be echoed into a slack 
channel as events happen. 

# Configuration
Reads config from env vars:

* CHANMON_CHANNEL: str, slack channel to post logs to. If not configured, no slack logs will be posted
* CHANMON_LOG_DAYS: int, number of days worth of logs to keep. Default is 90.
* CHANMON_LOG_JANITOR_INTERVAL: int, number of seconds between janitor runs. Longer is better to prevent unneccesary 
locks. Default is 600

# Requirements
Requires your errbot to be running [andrewthetechie/err-slackextendedbackend](https://github.com/andrewthetechie/err-slackextendedbackend) 
as its backend. The plugin uses extra callbacks that the SlackExtended backend triggers to function.
