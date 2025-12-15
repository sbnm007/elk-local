# elk-local
Entire ELK setup for local linux machine


# Data
Logs are produced by python file which mimics java logs

application.log   # INFO/WARN/ERROR (business)
error.log         # ERROR only + stacktrace
access.log        # HTTP access logs
audit.log         # security / audit events



# After creating filebeat config file
docker-compose up filebeat to check if its working


# Logstash is configured with inputs and outputs and in outputs it just stdouts


# logstash has grok layer which processes log files and outputs necessary values