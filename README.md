# Websphere Docker Sample Config and App Deployment

** Build Image ***
`docker build -t was-app:v1 .`

** Get admin password from running image **
`docker exec was-server cat /tmp/PASSWORD`

** Run Image **
`docker run --name was-server -p 9043:9043 -p 9443:9443 -d was-app:v1`

## URLS
** Websphere admin console **
https://localhost:9043/ibm/console/login.do?action=secure

** Deployed app that shows DNS caching behaviour **
https://localhost:9443/InetAddr/InetAddressInfoTest.jsp