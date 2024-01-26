#!/usr/bin/env python

import requests

prom_sql = '100 - rate(container_cpu_usage_seconds_total{job="kubelet", container!="POD", container!="", pod!="", namespace!="", instance="10.0.1.100:10250"}[5m]) * 100'

response = requests.get('https://prom-stg.mediass.it/api/v1/query',
    params={'query': prom_sql})
print(response.json()["data"]['result'])