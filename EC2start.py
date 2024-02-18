import boto3

region = 'us-east-1'

ec2 = boto3.client('ec2', region_name=region)

def get_instance_ids(environment):
    filters = [
        {'Name': 'tag:Environment', 'Values': [environment]},
    ]
    response = ec2.describe_instances(Filters=filters)
    instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]
    return instance_ids

def get_instance_states(instance_ids):
    response = ec2.describe_instances(InstanceIds=instance_ids)
    instance_states = {instance['InstanceId']: instance['State']['Name'] for reservation in response['Reservations'] for instance in reservation['Instances']}
    return instance_states

def main():
    environment = 'prod'
    action = 'Toggle' 

    instance_ids = get_instance_ids(environment)

    if not instance_ids:
        print(f"No instances found with tag Environment={environment}")
        return

    instance_states = get_instance_states(instance_ids)
    print(f"Current instance states: {instance_states}")

    for instance_id, state in instance_states.items():
        if action == 'Toggle':
            if state == 'running':
                ec2.stop_instances(InstanceIds=[instance_id])
                print(f"Stopping instance: {instance_id}")
            elif state == 'stopped':
                ec2.start_instances(InstanceIds=[instance_id])
                print(f"Starting instance: {instance_id}")
        else:
            print(f"Invalid action: {action}")
            return

    print("Action completed successfully")

if __name__ == "__main__":
    main()

