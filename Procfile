vitrine: bash -c 'if [ $VITRINE ]; then vitrine -c "/home/application/current/vitrine.conf" -p 8888; else tail -f /dev/null; fi'
vitrine-lagstats-worker: bash -c 'if [ -z $VITRINE_LAGSTATS_WORKER ]; then vitrine-lagstats-worker -s 1 -w 1 -vvv; else tail -f /dev/null; fi'
vitrine-worker: bash -c 'if [ -z $VITRINE_WORKER ]; then vitrine-worker -s 1 -w 1 -vvv; else tail -f /dev/null; fi'
