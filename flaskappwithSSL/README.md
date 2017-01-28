### flaskappwithSSL
Same as flaskappwithWerkzeug, but configure to run on SSL. It useful in scenarios, where you need to configure containers behind load balancer. This will test load balancer for SSL traffic.

Certificates are created in createcert.sh and use OPENSSL to create self sign certificates

By default, it will generate certificate with Common Name (CN) = container hostname. If you need to name of external DNS or load balancer name, etc. You can pass environmental variable name "$EXTERNAL_HOST" when starting the container

If you have your CA, and want to use your CA certificates to issue server certificates, you can map volume to app/ca to mount the ca certificate in container

CA Certificate Name - ca-cert.pem
CA Key without Passphase Name - ca-key.pem

If you have doubt, just go through bash script createcert.sh and you will be able to get most of the stuff.

dockerCommand to run docker container would be 

docker run -p 443:5000 --name stressorSSL -e EXTERNAL_HOST=abc.com -v ~\mycerts\ca:\app\ca sbrakl\stressor:ssl