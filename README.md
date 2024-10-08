Simpyl PGP login/register. Allows users to select display name from their PGP manager of choice. 

If display name collisions are found, a random digit is added until a unique one is found.

Login Proccess:

* User enters public PGP key to the server
* Server encrypts a confirmation code with the user's public PGP key
* User enters decrypted code and is logged in by the fingerprint and the code

GnuPG Required: 

Linux: https://gnupg.org/download/index.html

Windows: https://gnupg.org/ftp/gcrypt/binary/ 
