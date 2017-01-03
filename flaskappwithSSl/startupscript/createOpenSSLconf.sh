#!/bin/bash
# Create File openssl.cnf Used in Creating Certificates
tee /app/ca/openssl.cnf <<-'EOF'
HOME = .
RANDFILE = .rnd
[ ca ]
Default_ca = CA_default
[ CA_Default ]
Default_days = 3650
Default_md = sha256
Preserve = no
Email_in_dn = no
Nameopt = default_ca
Certopt = default_ca
Policy = policy_match
[ policy_match ]
countryName = match
stateOrProvinceName = match
organizationName = match
organizationalUnitName = optional
commonName = supplied
emailAddress = optional
[ req ]
Default_bits = 4096
Default_keyfile = key.pem
Default_md = sha256
String_mask = nombstr
distinguished_name = req_distinguished_name
Req_extensions = v3_req
[ req_distinguished_name ]
0.organizationName = Organization Name (company)
organizationalUnitName = Organizational Unit Name (department, division)
emailAddress = Email Address
emailAddress_max = 40
localityName = Locality Name (city, district)
stateOrProvinceName = State or Province Name (full name)
countryName = Country Name (2 letter code)
countryName_min = 2
countryName_max = 2
commonName = Common Name (hostname, IP, or your name)
commonName_max = 64
0.organizationName_default = Northgate Public Services
organizationalUnitName_default = NDS
emailAddress_default = nds@northgate-is.com
localityName_default = Milton Keynes
stateOrProvinceName_default = Buckinghamshire
countryName_default = UK
commonName_default = $ENV::CN
[ v3_ca ]
basicConstraints = CA:TRUE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer:always
[ v3_req ]
basicConstraints = CA:FALSE
subjectKeyIdentifier = hash
EOF