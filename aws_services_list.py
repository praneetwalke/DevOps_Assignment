import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def list_aws_services(region):
    """
    This function lists EC2 and RDS services in the specified AWS region.
    It connects to EC2 and RDS using boto3 clients and fetches running instances.
    """
    session = boto3.Session(region_name=region)
    ec2 = session.client('ec2')
    rds = session.client('rds')

    try:
        print(f"---- AWS Services in Region: {region} ----")

        # List EC2 instances
        ec2_instances = ec2.describe_instances()
        if ec2_instances['Reservations']:
            print(f"\nEC2 Instances in {region}:")
            for reservation in ec2_instances['Reservations']:
                for instance in reservation['Instances']:
                    print(f"  - Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}, Type: {instance['InstanceType']}")
        else:
            print(f"No EC2 instances found in {region}.")

        # List RDS instances
        rds_instances = rds.describe_db_instances()
        if rds_instances['DBInstances']:
            print(f"\nRDS Instances in {region}:")
            for db_instance in rds_instances['DBInstances']:
                print(f"  - DB Instance ID: {db_instance['DBInstanceIdentifier']}, Status: {db_instance['DBInstanceStatus']}, Engine: {db_instance['Engine']}")
        else:
            print(f"No RDS instances found in {region}.")

    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure them properly.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials. Please check your configuration.")
    except Exception as e:
        print(f"An error occurred in region {region}: {str(e)}")


def main():
    """
    This function retrieves all available AWS regions and calls the list_aws_services
    function for each region.
    """
    ec2_client = boto3.client('ec2')

    try:
        regions = ec2_client.describe_regions()['Regions']
        region_names = [region['RegionName'] for region in regions]

        # Iterate over each region to list services
        for region in region_names:
            list_aws_services(region)

    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure them properly.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials. Please check your configuration.")
    except Exception as e:
        print(f"An error occurred while listing regions: {str(e)}")


if __name__ == "__main__":
    main()
