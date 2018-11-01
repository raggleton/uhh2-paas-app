#!/usr/bin/env bash

# Setup ssh first
# Should setup env var first with GIT_USERNAME and GIT_EMAIL
eval $(ssh-agent -s)
ssh-add /secrets/ssh-privatekey
git config user.name "${GIT_USERNAME}"
git config user.email "${GIT_EMAIL}"

# The following bit is as per the run script
# https://github.com/sclorg/s2i-python-container/blob/master/3.6/s2i/bin/run

# Guess the number of workers according to the number of cores
function get_default_web_concurrency() {
  limit_vars=$(cgroup-limits)
  local $limit_vars
  if [ -z "${NUMBER_OF_CORES:-}" ]; then
    echo 1
    return
  fi

  local max=$((NUMBER_OF_CORES*2))
  # Require at least 43 MiB and additional 40 MiB for every worker
  local default=$(((${MEMORY_LIMIT_IN_BYTES:-MAX_MEMORY_LIMIT_IN_BYTES}/1024/1024 - 43) / 40))
  default=$((default > max ? max : default))
  default=$((default < 1 ? 1 : default))
  # According to http://docs.gunicorn.org/en/stable/design.html#how-many-workers,
  # 12 workers should be enough to handle hundreds or thousands requests per second
  default=$((default > 12 ? 12 : default))
  echo $default
}

# Run the server
export WEB_CONCURRENCY=${WEB_CONCURRENCY:-$(get_default_web_concurrency)}
echo ${WEB_CONCURRENCY}
exec gunicorn wsgi --bind=0.0.0.0:8080 --access-logfile=- --config "$APP_CONFIG"
