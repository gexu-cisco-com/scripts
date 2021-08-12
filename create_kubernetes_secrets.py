"""
Create kubeadm and kubeadmin secrets in vault

Usage:
  create_kubernetes_secrets.py <cnc> <cluster>

Arguments:
  cnc           Name of command and control (eg mccgovrd)
  cluster       Cluster name (eg mccgovrd01)

Required environment variables:
  VAULT_ADDR      Address of vault
  VAULT_NAMESPACE Enterprise namespace of vault
  VAULT_TOKEN     A vault token with CRUD permission to {cnc}/kubernetes/{cluster}/kubeadm*
"""
from os import environ
from random import choice
from sys import exit

from hvac import Client

bootstrap_token_chars = "0123456789abcdefghijklmnopqrstuvwxyz"


# to_vault - creates kubeadm and kubeadmin secrets in vault given user/env inputs.
# vault_namespace defaults to None value if non-enterprise vault instance is used.
def to_vault(cnc, cluster, vault_addr, vault_token, secret_name, vault_namespace=None):

    # create client instance using given vault values.
    client = Client(url=vault_addr, token=vault_token, namespace=vault_namespace)

    # set path for kubeadmin secret.
    vault_path = f"{cnc}/kubernetes/{cluster}/{secret_name}"

    # create empty dict for creds.
    creds = {}

    if secret_name == 'kubeadm':

        token_pre = "".join(choice(bootstrap_token_chars) for x in range(6))
        token_post = "".join(choice(bootstrap_token_chars) for x in range(16))

        token = token_pre + "." + token_post

        creds["join_token"] = token

    elif secret_name == 'kubeadmin':

        token = "".join(choice(bootstrap_token_chars[:16]) for x in range(64))

        creds["kubeadm_certificate_key"] = token

    # try the following,
    try:

        # set response as create secret
        response = client.secrets.kv.v2.create_or_update_secret(
            path=vault_path, secret=creds
        )

        # if the creation failed,
        if not response:

            # log the failure.
            print(f"Failed to write credentials to vault at: {vault_path}")

        # else, the creation succeeded,
        else:

            # log the success.
            print(f"Wrote credentials to vault at: {vault_path}")

    # catch any Exception,
    except Exception as exc:

        # log the exception.
        print(f"Got exception writing to vault: {exc}")

        # raise the exception.
        raise


# main method.
if __name__ == "__main__":

    # if envvar contains Vault ADDR and TOKEN,
    if "VAULT_ADDR" in environ and "VAULT_TOKEN" in environ:

        # try the following,
        try:

            # create kubeadmin in vault
            to_vault(
                environ["CNC"],
                environ["CLUSTER"],
                environ["VAULT_ADDR"],
                environ["VAULT_TOKEN"],
                "kubeadmin",
                environ.get("VAULT_NAMESPACE"),
            )

            # create kubeadm in vault
            to_vault(
                environ["CNC"],
                environ["CLUSTER"],
                environ["VAULT_ADDR"],
                environ["VAULT_TOKEN"],
                "kubeadm",
                environ.get("VAULT_NAMESPACE"),
            )

        # catch any Exception,
        except Exception as exc:

            # Report exception.
            print(f"Got exception {exc}")

            # exit with code 1.
            exit(1)

        # otherwise, no error,
        else:

            # exit with code 0.
            exit(0)

    # otherwise, no exports,
    else:

        # notify the needed exports.
        print("Export VAULT_ADDR, VAULT_NAMESPACE, and VAULT_TOKEN.")

        # exit with code 1.
        exit(1)
