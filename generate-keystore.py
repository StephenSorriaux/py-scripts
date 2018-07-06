#! /usr/bin/python
import os
import sys
import hashlib
import subprocess
import datetime

MYDIR = os.path.abspath(os.path.dirname(__file__))
OPENSSL = '/usr/bin/openssl'
KEYTOOL = '/usr/bin/keytool'
CA_CERT = 'ca.cert'
CA_KEY = 'ca.key'
KEYSIZE='4096'
DAYS='365'
PASSWORD='testpass'
# Extra X509 args. Consider using e.g. ('-passin', 'pass:blah') if your
# CA password is 'blah'. For more information, see:
#
# http://www.openssl.org/docs/apps/openssl.html#PASS_PHRASE_ARGUMENTS
X509_EXTRA_ARGS = ()

def openssl(*args):
    cmdline = [OPENSSL] + list(args)
    subprocess.check_call(cmdline)

def keytool(*args):
    cmdline = [KEYTOOL] + list(args)
    subprocess.check_call(cmdline)

def gencert(domain, rootdir=MYDIR, keysize=KEYSIZE, days=DAYS,ca_cert=CA_CERT,
            ca_key=CA_KEY, password=PASSWORD):
    def dfile(ext):
        return os.path.join('domains', '%s.%s' % (domain, ext))

    os.chdir(rootdir)

    if not os.path.exists('domains'):
        os.mkdir('domains')

    keytool('-genkey', '-alias', 'localhost', '-keyalg', 'RSA', '-keystore',
        dfile('keystore.jks'), '-keysize', keysize,'-storepass', password,
        '-keypass', password,'-dname',
        'C=FR,ST=RA,L=Lyon,O=Kazoo,CN=%s' % domain, '-noprompt')

    keytool('-certreq', '-alias', 'localhost', '-keystore',
        dfile('keystore.jks'),'-storepass', password, '-keypass',
        password, '-file', dfile('request'), '-noprompt')

    openssl('x509', '-req', '-days', str(days), '-in', dfile('request'),
            '-CA', ca_cert, '-CAkey', ca_key,
            '-set_serial',
            '0x%s' % hashlib.md5(domain +
                                 str(datetime.datetime.now())).hexdigest(),
            '-out', dfile('cert'),
            '-extensions', 'v3_req',
            *X509_EXTRA_ARGS)

    keytool('-import','-trustcacerts','-alias', 'root', '-file', 'ca.cert',
        '-keystore', dfile('keystore.jks'), '-noprompt','-storepass',
        password, '-keypass', password)

    keytool('-import','-alias', 'localhost', '-file', dfile('cert'),
        '-keystore', dfile('keystore.jks'), '-noprompt','-storepass',
        password,'-keypass', password)

    keytool('-import','-alias', 'root', '-file', 'ca.cert',
        '-keystore', dfile('truststore.jks'), '-noprompt','-storepass',
        password)

    print "Done. The keystore is at %s, the cert is at %s, and the " \
          "CA cert is at %s." % (dfile('keystore.jks'), dfile('cert'), ca_cert)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: %s <domain or ip>" % sys.argv[0]
        sys.exit(1)
    gencert(sys.argv[1])
