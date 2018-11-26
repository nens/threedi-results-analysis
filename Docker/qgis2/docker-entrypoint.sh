#!/bin/sh

USERNAME=$(cut -d: -f1 /etc/passwd | tail -1)
USER_ID=$(id -u ${USERNAME})

if [ "$1" = 'bash' ]; then
    exec bash
fi

exec gosu $USERNAME:$USER_ID "${@}"
