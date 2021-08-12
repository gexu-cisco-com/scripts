export VAULT_ADDR="https://east.keeper.cisco.com"
export VAULT_NAMESPACE="meetpaas/mccgovrd"
export VAULT_PREFIX="secret/data/mccgovrd"
export CLUSTER_DOMAIN="govrd.wbx3.com"
export CLOUD="govrdv"
export CNC="mccgovrd"
export INFRA_REPO="https://github.com/mpegovrd/govrd-infra.git"
export INFRA_APP_CONFIGS_REPO="https://github.com/mpegovrd/infra-app-configs.git"

echo "Paste your Vault Token and press Enter:"
read -sr VAULT_TOKEN_INPUT
export VAULT_TOKEN=$VAULT_TOKEN_INPUT
echo "Vault Token exported.\n"

# WBX3 AWS Account Route53 Credentials
echo "Pulling AWS_SECRET_ACCESS_KEY from Vault..."
export AWS_SECRET_ACCESS_KEY=$(curl -s -X GET -H "X-Vault-Token: $VAULT_TOKEN_INPUT" -H "X-Vault-Namespace: $VAULT_NAMESPACE" $VAULT_ADDR/v1/secret/data/$CNC/infra/mccgovrd/aws/credentials | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['data']['AWS_SECRET_ACCESS_KEY'])")
echo "AWS_SECRET_ACCESS_KEY Pulled.\n"

echo "Pulling AWS_ACCESS_KEY_ID from Vault..."
export AWS_ACCESS_KEY_ID=$(curl -s -X GET -H "X-Vault-Token: $VAULT_TOKEN_INPUT" -H "X-Vault-Namespace: $VAULT_NAMESPACE" $VAULT_ADDR/v1/secret/data/$CNC/infra/mccgovrd/aws/credentials | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['data']['AWS_ACCESS_KEY_ID'])")
echo "AWS_ACCESS_KEY_ID Pulled.\n"

echo "Pulling AWS_DEFAULT_REGION from Vault..."
export AWS_DEFAULT_REGION=$(curl -s -X GET -H "X-Vault-Token: $VAULT_TOKEN_INPUT" -H "X-Vault-Namespace: $VAULT_NAMESPACE" $VAULT_ADDR/v1/secret/data/$CNC/infra/mccgovrd/aws/credentials | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['data']['AWS_DEFAULT_REGION'])")
echo "AWS_DEFAULT_REGION Pulled.\n"

export AWS_DEFAULT_REGION=us-east-1
echo "AWS_DEFAULT_REGION is ${AWS_DEFAULT_REGION}."

echo "Type the target cluster name and press Enter:"
read -r TARGET_CLUSTER
export CLUSTER=$TARGET_CLUSTER
echo "Exported cluster name is ${CLUSTER}."
