# Faculdade Rio Branco API

A crawler made using Scrapy that access restricted area from my college and return grade data.

## Usage

Make a JSON POST request to ```frb-api.herokuapp.com/crawl.json``` with these data:

```
{
"start_requests": "false",
"spider_name": "RioBranco",
"user" : "USER",
"password":"PASSWORD"
}
```

Replace USER and PASSWORD values for your correspondent data for access Rio Branco restricted area.
