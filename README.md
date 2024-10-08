Simpyl PGP login/register. Allows users to select display name from their PGP manager of choice. If colisions are found, a random digit is added until it is a valid display name (username).

Login Proccess:

* User enters public PGP key to the server
* Server encrypts a confirmation code with the User's public PGP key
* User enters Decrypted code and is logged in by the fingerprint and the code

GnuPG Required: 

Linux: https://gnupg.org/download/index.html
Windows: https://gnupg.org/ftp/gcrypt/binary/ 