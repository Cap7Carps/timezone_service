## Timezone Service - Nicholas Carpenter

#### Run Locally:

1. `export FLASK_APP=timezone_service/app.py`
2. `flask run`


#### Sample Requests:

```
curl -X POST \
  http://127.0.0.1:5000/ \
  -H 'Content-Type: application/json' \
  -H 'Host: 127.0.0.1:5000' \
  -d '{"timezone": "GMT+7"}'
```

#### Testing:
```python
python -m pytest
```

#### General Information:

This Application accepts an application/json PUT Request in the Form: 
`{'timezone':  'GMT±Hours'}`

It returns a greeting based on the time of day at that timezone.

****

### Changes were the service Business Critical:

Should the service become business critical with 50k daily requests the following could be implemented:

1. The application could be deployed on a scaling infrastructure and put behind a web service gateway interface. This would spread the load over many different machines.
2. An in-memory database, such as redis, could be installed and used as a cache. A proxy could be setup to first direct requests directly towards the redis cache and only afterwards to the main app.
3. The app could be converted to a system that updates a redis database with key, value pair of form: 'GMT+/-HH': 'Greeting'. 
The user request would instead directly query the redis database.

