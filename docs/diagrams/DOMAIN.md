# Domain Diagram

```mermaid
flowchart LR
    Identity["Identity"] --> Audit["Audit"]
    Organization["Organization"] --> Military["Military"]
    Military --> ServiceScale["ServiceScale"]
    Leave["Leave"] --> ServiceScale
    Settings["Settings"] --> ServiceScale
    ServiceScale --> ServiceExchange["ServiceExchange"]
    ServiceExchange --> Audit
    ServiceScale --> Reports["Reports"]
    Audit --> Reports
    Notification["Notification"] --> Identity
    Notification --> ServiceScale
```
