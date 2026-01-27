# Azure CLI Query Patterns

## Identity / Subscription
- Current account: `az account show`
- List subscriptions: `az account list -o table`
- Set subscription: `az account set --subscription <SUBSCRIPTION_ID_OR_NAME>`

## Compute (VM)
- List VMs: `az vm list -d -o table`
- VM details: `az vm show -g <rg> -n <vm>`

## Storage
- List accounts: `az storage account list -o table`
- Check public access: `az storage account show -g <rg> -n <acct> --query "allowBlobPublicAccess"`

## RBAC / IAM
- List role assignments: `az role assignment list --assignee <principal> -o table`
- List role definitions: `az role definition list -o table`

## Azure Functions
- List function apps: `az functionapp list -o table`

## AKS
- List clusters: `az aks list -o table`

## App Service
- List web apps: `az webapp list -o table`

## Key Vault
- List vaults: `az keyvault list -o table`

## Network
- NSGs: `az network nsg list -o table`
- Public IPs: `az network public-ip list -o table`

## Azure Monitor (metrics)
- Example metrics query:
  `az monitor metrics list --resource <resourceId> --metric "Percentage CPU" --interval PT1H`

## Costs
- Use Cost Management (read-only) via `az costmanagement` if enabled.

## Common write actions (confirm before running)
- Start/stop VM: `az vm start|stop -g <rg> -n <vm>`
- Scale AKS: `az aks scale -g <rg> -n <cluster> --node-count N`
- Delete resource: `az resource delete --ids <resourceId>`
