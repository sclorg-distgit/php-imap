This repository contains sources for RPMs that are used
to build Software Collections for CentOS by SCLo SIG.

This branch is for sclo-php73 packages (for rh-php73 SCL)


PHP 7.3 / EL 7

    build -bs *spec --define "scl rh-php73" --define "dist .el7"
    cbs add-pkg    sclo7-sclo-php73-sclo-candidate --owner=sclo  sclo-php73-php-imap
    cbs add-pkg    sclo7-sclo-php73-sclo-testing   --owner=sclo  sclo-php73-php-imap
    cbs add-pkg    sclo7-sclo-php73-sclo-release   --owner=sclo  sclo-php73-php-imap
    cbs build      sclo7-sclo-php73-sclo-el7       <above>.src.rpm
    cbs tag-build  sclo7-sclo-php73-sclo-testing   <previous>

