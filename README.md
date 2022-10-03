
# CurrencyConverter

This repository contains the source code of currency converter application.  

The main features are:
- currency rates come from the official NBP API,
- local cache for obtained data,
- unique requests are logged into AWS S3 service.


# How to use it:

1. Save your AWS credentials into file `aws_credentials`

2. Build container:
```
docker build -t converter .
```

3. Run container:
```
docker run -it converter bash
```

4. Run converter:
```
converter -a 2 -f USD -t THB -d 2022-10-03
```

5. For help run:
```
converter -h
```
