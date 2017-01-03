#!/bin/bash
# Create Folder to Run Certificate Creation Scripts


PRESENTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d /app/ca ]; then
  echo '### Creating ca folder'
  mkdir -p /app/ca
fi

if [ ! -f /app/server.crt ]; then
	echo '### Certificate do not exist, creating one...'
	if [ ! -f /app/ca/openssl.cnf ]; then
		echo '### OpenSSL config do not exist, creating one...'
		sh $PRESENTDIR/createOpenSSLconf.sh
	fi
	sh $PRESENTDIR/createcert.sh
	echo '### Copying Certificate to app directory'
	cp /app/ca/server-key.pem /app/server.key
	cp /app/ca/server-cert.pem /app/server.crt
else
	echo '### Certificates are present'
fi

echo '### Starting Flask app'
cd /app
python main.py