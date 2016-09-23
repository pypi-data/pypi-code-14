import boto3
from botocore.exceptions import ClientError
import click


# TODO: for 'self' published AMIs, standardize the 'name' so you can search for OS flavor as well
image_metadata = {
    'amazon': {
        'amazon_minimal': {'name': '*amzn-ami-minimal-*-VERSION.x86_64*', 'owner': 'amazon'},
        'amazon': {'name': '*amzn-ami-*-VERSION.x86_64*', 'owner': 'amazon'},
    },
    'canonical': {
        'ubuntu': {'name': '*ubuntu-*-RELEASE-*-VERSION', 'owner': '099720109477'}
    },
    'self': {}
}

instance_to_arch = {
    "t1.micro": "paravirtual",
    "t2.nano": "hvm",
    "t2.micro": "hvm",
    "t2.small": "hvm",
    "t2.medium": "hvm",
    "t2.large": "hvm",
    "m1.small": "paravirtual",
    "m1.medium": "paravirtual",
    "m1.large": "paravirtual",
    "m1.xlarge": "paravirtual",
    "m2.xlarge": "paravirtual",
    "m2.2xlarge": "paravirtual",
    "m2.4xlarge": "paravirtual",
    "m3.medium": "hvm",
    "m3.large": "hvm",
    "m3.xlarge": "hvm",
    "m3.2xlarge": "hvm",
    "m4.large": "hvm",
    "m4.xlarge": "hvm",
    "m4.2xlarge": "hvm",
    "m4.4xlarge": "hvm",
    "m4.10xlarge": "hvm",
    "c1.medium": "paravirtual",
    "c1.xlarge": "paravirtual",
    "c3.large": "hvm",
    "c3.xlarge": "hvm",
    "c3.2xlarge": "hvm",
    "c3.4xlarge": "hvm",
    "c3.8xlarge": "hvm",
    "c4.large": "hvm",
    "c4.xlarge": "hvm",
    "c4.2xlarge": "hvm",
    "c4.4xlarge": "hvm",
    "c4.8xlarge": "hvm",
    "r3.large": "hvm",
    "r3.xlarge": "hvm",
    "r3.2xlarge": "hvm",
    "r3.4xlarge": "hvm",
    "r3.8xlarge": "hvm",
    "i2.xlarge": "hvm",
    "i2.2xlarge": "hvm",
    "i2.4xlarge": "hvm",
    "i2.8xlarge": "hvm",
    "d2.xlarge": "hvm",
    "d2.2xlarge": "hvm",
    "d2.4xlarge": "hvm",
    "d2.8xlarge": "hvm",
    "hi1.4xlarge": "hvm",
    "hs1.8xlarge": "hvm",
    "cr1.8xlarge": "hvm",
    "cc2.8xlarge": "hvm"
}


def sort_image_list(thelist):
    return sorted(thelist, key=lambda k: k['CreationDate'])


def find_virt_type(instance_size):
    try:
        return instance_to_arch.get(instance_size)
    except KeyError:
        return ""


def find_image(owner, os, version, release, pattern, virt_type, region):
    if owner == 'self':
        image_metadata[owner][os] = {
            'name': pattern,
            'owner': 'self'
        }
    version_to_find = image_metadata[owner][os]['name'].replace('OS', os).replace('VERSION', version).replace('RELEASE', release)
    ec2_client = boto3.client('ec2', region_name=region)
    try:
        images = sort_image_list(ec2_client.describe_images(
            Owners=[image_metadata[owner][os]['owner']],
            Filters=[
                {'Name': 'state', 'Values': ['available']},
                {'Name': 'architecture', 'Values': ['x86_64']},
                {'Name': 'virtualization-type', 'Values': [virt_type]},
                {'Name': 'root-device-type', 'Values': ['ebs']},
                {'Name': 'name', 'Values': [version_to_find]}
            ]
        )['Images'])
        return images[-1]['ImageId']
    except ClientError as e:
        print("Error: {}".format(e.message))
    except IndexError:
        return ""


@click.command()
@click.argument('instance_size')
@click.option('--owner', default='amazon', help='owner of this AMI.  defaults to "amazon"')
@click.option('--os', default='amazon', help='OS to search for')
@click.option('--version', default='*', help='AMI version to search for')
@click.option('--release', default='*', help='Release of OS to search for')
@click.option('--pattern', default='OS.VERSION.RELEASE', help='pattern to use for Name.  See README.md for details')
@click.option('--region', default='us-west-2', help='region to query')
def main(instance_size, owner, os, version, release, pattern, region):
    virt_type = find_virt_type(instance_size)
    print(find_image(owner, os, version, release, pattern, virt_type, region))


if __name__ == "__main__":
    main()
