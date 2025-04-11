# Geração de certificados

```sh
#!/bin/bash

set -e

DOMAIN="private.nbdev.com.br"
CERT_DIR="./certs"
mkdir -p "$CERT_DIR"

echo "🔧 Criando Autoridade Certificadora (CA)..."
openssl req -x509 -new -nodes -days 3650 -newkey rsa:2048 \
  -keyout "$CERT_DIR/ca.key" -out "$CERT_DIR/ca.crt" \
  -subj "/C=BR/ST=RJ/L=Quatis/O=NBDev/OU=Infra/CN=Local CA"

echo "🔧 Criando chave e CSR para o servidor..."
openssl req -new -nodes -newkey rsa:2048 \
  -keyout "$CERT_DIR/server.key" -out "$CERT_DIR/server.csr" \
  -subj "/C=BR/ST=RJ/L=Quatis/O=NBDev/OU=Backend/CN=$DOMAIN"

echo "📄 Gerando arquivo server.ext..."
cat > "$CERT_DIR/server.ext" <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
EOF

echo "🔐 Assinando certificado do servidor com a CA..."
openssl x509 -req -in "$CERT_DIR/server.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" \
  -CAcreateserial -out "$CERT_DIR/server.crt" -days 3650 -extfile "$CERT_DIR/server.ext"

echo "👤 Criando chave e CSR do cliente..."
openssl req -new -nodes -newkey rsa:2048 \
  -keyout "$CERT_DIR/client.key" -out "$CERT_DIR/client.csr" \
  -subj "/C=BR/ST=RJ/L=Quatis/O=NBDev/OU=Client/CN=cliente1"

echo "🔐 Assinando certificado do cliente com a CA..."
openssl x509 -req -in "$CERT_DIR/client.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" \
  -CAcreateserial -out "$CERT_DIR/client.crt" -days 3650

echo "✅ Certificados gerados com sucesso em '$CERT_DIR':"
ls -1 "$CERT_DIR"
```

# Configuração no Nginx

```sh
ssl_certificate     /etc/nginx/certs/server.crt;
ssl_certificate_key /etc/nginx/certs/server.key;
ssl_client_certificate /etc/nginx/certs/ca.crt;
ssl_verify_client on;
```
