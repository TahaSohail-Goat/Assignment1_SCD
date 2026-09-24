# DevOps Engineering Contract

Required:
- backend multi-stage image
- frontend multi-stage image
- pinned bases
- non-root
- exec-form CMD
- healthcheck
- cache-friendly Dockerfile order
- `.dockerignore`
- build context measurement
- Compose healthchecks
- healthy `depends_on`
- two networks
- three named volumes
- development bind mount only where appropriate
- production file uses images, not build
- no published DB/cache production ports
