#!/bin/bash
set -e

cd /app/ca
rm *.pem *.csr -rf

#Temp, remove after
if [ -z "$EXTERNAL_HOST" ]; then	
	export CN=`hostname`	
	echo '### CN taken as container hostname: ' $CN	
else
	export CN=$EXTERNAL_HOST
	echo '### CN taken as external host: ' $CN	
fi
OPENSSL_CONF=/app/ca/openssl.cnf
HN=`hostname`
IP=$(hostname -I | awk '{print $1}')

echo "\n\n"

if [ ! -f /app/ca/ca-cert.pem ]; then
	#Create CA Root key #ca-key.pem
	echo '###Creating CA private key'
	openssl genrsa -out ca-key.pem 4096
	#Create CA Root certificate #ca-cert.pem
	echo '###Creating CA certificate'
	openssl req -new -x509 -days 3650 -batch -key ca-key.pem -sha256 -out ca-cert.pem -extensions v3_ca
else
	echo '### CA certifcate already exists'
fi

#Generate Server Certificate Key # server-key.pem
echo '###Creating Server private key'
openssl genrsa -out server-key.pem 4096

#Create server certificate CSR #server.csr
echo '###Creating server CSR'
openssl req -sha256 -subj "/CN=${CN}" -batch -new -key server-key.pem -out server.csr -config $OPENSSL_CONF

#Create extFile for additional certificate
#subjectAltName=DNS:example.com,DNS:www.example.com"
# Checking, if variable are present
subaltname="IP:$IP,IP:127.0.0.1,DNS:$HN"
echo '### Creating extfile.cnf'
if [ ! -z "$EXTERNAL_HOST" ]; then
	echo '### Env EXTERNAL_HOST present: ' $EXTERNAL_HOST
	echo '### Adding to external host to additional subject'
	subaltname=$subaltname",DNS:'$EXTERNAL_HOST'"
else
	echo '### Env EXTERNAL_HOST missing, no addition to additional subject'
fi
if [ ! -z "$HOST_HOSTNAME" ]; then
	echo '### Env HOST_HOSTNAME present: ' $HOST_HOSTNAME
	echo '### Adding to host to additional subject'	
	subaltname=$subaltname",DNS:$HOST_HOSTNAME"	
else
	echo '### Env HOST_HOSTNAME missing, no addition to additional subject'
fi
echo subjectAltName = $subaltname > extfile.cnf

#Create server certifcate server-cert.pem
echo '### Creating server certificate'
openssl x509 -req -days 3650 -sha256 -in server.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -extfile extfile.cnf

echo '###Changing Certificate Permission'
chmod -v 0400 ca-key.pem server-key.pem
chmod -v 0444 ca-cert.pem server-cert.pem

exit
#openssl genrsa -out client-key.pem 4096
#openssl req -subj '/CN=client' -new -key client-key.pem -out client.csr
#echo extendedKeyUsage = clientAuth > extfile.cnf
#openssl x509 -req -days 3650 -sha256 -in client.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem -extfile extfile.cnf
#chmod -v 0400 ca-key.pem client-key.pem server-key.pem
#chmod -v 0444 ca-cert.pem server-cert.pem client-cert.pem
