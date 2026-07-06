# Dominio

```mermaid
flowchart LR
    Military["military"] --> Shared["shared.kernel"]
    Organization["organization"] --> Shared
    ServiceScale["service_scale"] --> Military
    ServiceScale --> Shared
    ServiceExchange["service_exchange"] --> ServiceScale
    ServiceExchange --> Military
```
