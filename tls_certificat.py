# example of checking TLS certificate using OpenSSL
# Použití: python tls_certificat.py <hostname> <port>
import sys
import ssl
import socket


def check_tls_certificate(hostname, port):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        # try to establish TLS connection, which will automatically verify the certificate
        try:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(f"TLS certifikát pro {hostname}:{port} je platný.")
                print("Informace o certifikátu:")
                # vypíše informace o certifikátu, např. subjekt, vydavatele, platnost atd.
                certificate_dict = ssock.getpeercert()
                print(f"Certifikát subjekt: {certificate_dict.get('subject')}")
                print(f"Certifikát vydavatel: {certificate_dict.get('issuer')}")
                print(f"Platnost od: {certificate_dict.get('notBefore')}")
        except ssl.SSLError as e:
            print(f"Chyba při ověřování TLS certifikátu pro {hostname}:{port}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python tls_certificat.py <hostname> <port>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    check_tls_certificate(hostname, port)
