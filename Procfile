vitrine: bash -c 'if [ "$TSURU_APPNAME" = "vitrine" ]; then vitrine-manage assets build; vitrine -c "/home/application/current/vitrine.conf" -p 8888; else tail -f /dev/null; fi'
vitrine_commits_worker: bash -c 'if [ "$TSURU_APPNAME" = "vitrine-commits-worker" ]; then vitrine-commits-worker -s 1 -w 1; else tail -f /dev/null; fi'
vitrine_langstats_worker: bash -c 'if [ "$TSURU_APPNAME" = "vitrine-langstats-worker" ]; then vitrine-langstats-worker -s 1 -w 1; else tail -f /dev/null; fi'
