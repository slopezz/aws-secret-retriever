import base64
import json
import argparse
import sys
import boto3
from botocore.exceptions import ClientError

def set_client(region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    return client

def set_secret(args):
    client = set_client(args["region"])
    secret_string = {args["secret_key"]: args["secret_value"]}
    secret_string = json.dumps(secret_string)

    try:
        create_secret_response = client.create_secret(
            Name=args["secret_name"], SecretString=secret_string
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceExistsException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            print("SECRET_ALREADY_EXISTS")
            sys.exit(-1)
            raise e

def get_secret(secret_name, region_name):
    client = set_client(region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            print("SECRET_NOT_FOUND")
            sys.exit(-1)
            # raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = json.loads(get_secret_value_response["SecretString"])
        else:
            secret = json.loads(
                base64.b64decode(get_secret_value_response["SecretBinary"])
            )

    return secret

def get_secret_key(args):
    secret = get_secret(args["SECRET_NAME"], args["region"])
    secretUser = list(secret)[0]
    return secret, secretUser

def print_secret_value(args):
    secret, secretUser = get_secret_key(args)
    print(secret[secretUser])

def print_secret_key(args):
    _, secretUser = get_secret_key(args)
    print(secretUser)

def _print_decider(args):
    if args["operation"] == "key":
        print_secret_key(args)
    elif args["operation"] == "value":
        print_secret_value(args)

def setup_cli():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [positional arguments] --region (Default: us-east-1)"
    )
    subparsers = parser.add_subparsers()

    parser_secret_get = subparsers.add_parser(
        "get", add_help=False, help="%(prog)s get (key|value) SECRET_NAME"
    )
    parser_secret_get.add_argument("operation", type=str, choices=["key", "value"])
    parser_secret_get.add_argument(
        "SECRET_NAME", type=str, help="The name of the secret stored in AWS"
    )
    parser_secret_get.add_argument(
        "--region",
        required=False,
        type=str,
        default="us-east-1",
        help="(Default=us-east-1)",
    )
    parser_secret_get.set_defaults(func=_print_decider)

    parser_set = subparsers.add_parser("set", help="%(prog)s set value SECRET_NAME")
    parser_set.add_argument(
        "--secret-name", required=True, type=str, help="The Name of The New AWS Secret"
    )
    parser_set.add_argument(
        "--secret-key", required=True, type=str, help="The Name of the Secret Key"
    )
    parser_set.add_argument(
        "--secret-value", required=True, type=str, help="The value of the Secret Key"
    )
    parser_set.add_argument(
        "--region",
        required=False,
        type=str,
        default="us-east-1",
        help="(Default=us-east-1)",
    )
    parser_set.set_defaults(func=set_secret)
    args = parser.parse_args()

    if vars(args):
        args.func(vars(args))
    else:
        parser.print_help()

if __name__ == "__main__":
    setup_cli()
